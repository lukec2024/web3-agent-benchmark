from flask import Blueprint, request, abort
from bson.objectid import ObjectId
from app.models.round import Round
from app.config import db, rpc_client
from sqlalchemy.orm import defer
from sqlalchemy import desc
from voyager.utils.question import QuestController
from voyager.utils.prepare_token import _mint_spl_token
from solders.keypair import Keypair
from base58 import b58encode

round_bp = Blueprint('round', __name__)

@round_bp.get('/new')
def create_new_round():
    agent_name = request.args.get('agent_name', default="Unknown", type=str)
    
    agent_kp = Keypair()
    agent_pubkey = str(agent_kp.pubkey())
    prompt, validation = generate_questions(agent_kp, agent_pubkey)

    round_id = str(ObjectId())
    round = Round(
        id = round_id,
        agent_name=agent_name,
        prompt=prompt,
        validation=validation,
        agent_kp=b58encode(bytes(agent_kp)).decode('utf-8'),
        agent_pubkey=agent_pubkey,
        reward=0,
    )
    db.session.add(round)
    db.session.commit()
    return round.to_dict(rules=("-validation",))

@round_bp.get('/get/<round_id>')
def get_round(round_id: str):
    full = request.args.get('full', default=False, type=bool)
    rules = ("-validation",) if not full else ()
    round = db.session.query(Round).options(
        defer(Round.validation)
    ).filter(Round.id==round_id).one_or_none()
    if round:
        return round.to_dict(rules=rules)
    abort(404)

@round_bp.get('/list/<int:page>/<int:size>')
def list_round(page: int, size: int):
    page_size = size = min(100, size)
    offset = (page - 1) * page_size
    rounds = db.session.query(Round).options(
        defer(Round.validation)
    ).order_by(desc(Round.id)).limit(page_size).offset(offset).all()
    result = [round.to_dict(rules=("-validation",)) for round in rounds]
    return result

def generate_questions(agent_kp: Keypair, agent_pubkey: str):
    prompt = {}
    validation = {}
    question_path = "voyager/question_bank/automic_problems"
    question_controller = QuestController(question_path, question_path)
    token_mints = _mint_spl_token(agent_kp, rpc_client)
    quest_names = sorted(list(question_controller.question_benches.keys()))
    # Natural language prompt with random values
    for question_key in quest_names:
        question = question_controller._load_question(question_key, token_mints, token_mints)
        natural_language_prompt = question_controller._generate_natural_language_prompt(question, agent_pubkey, token_mints, [])
        # Remove useless data
        for post_conds in question["validation"]["post_conditions"]:
            if "description" in post_conds:
                del post_conds["description"]
        question_id = str(ObjectId())
        prompt[question_id] = {"prompt": natural_language_prompt}
        validation[question_id] = {
            "id": question["id"],
            "reward": 0,
            "category": question["id"],
            "subcategory": question["subcategory"],
            "validation": {"post_conditions": question["validation"]["post_conditions"]}
        }
    return prompt, validation