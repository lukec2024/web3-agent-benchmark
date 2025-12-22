from flask import Blueprint, request, abort
from app.config import rpc_client, db
from app.models.round import Round
from voyager.utils.validator import calculate_reward
from solders.signature import Signature
from sqlalchemy import func, cast, literal
from sqlalchemy.dialects.postgresql import JSONB

rpc_bp = Blueprint('rpc', __name__)

@rpc_bp.post('/solana')
def rpc():
    is_send_txn = request.json.get("method", "") == "sendTransaction"
    round_id = request.args.get('round', default=None, type=str)
    question_id = request.args.get('question', default=None, type=str)
    if is_send_txn:
        round = db.session.query(Round).filter(Round.id==round_id).first()
        if not round or question_id not in round.validation:
            abort(404) # Abort 404 if no question found
        question = round.validation[question_id]
    resp = rpc_client._provider.session.post(rpc_client._provider.endpoint_uri, json=request.json)
    # Calculate reward
    resp_json = resp.json()
    if is_send_txn and "result" in resp_json:
        get_tx_resp = rpc_client.get_transaction(Signature.from_string(resp_json["result"]), encoding="jsonParsed")
        reward = calculate_reward(get_tx_resp, question, round.agent_pubkey)
        print(f"{question}, {resp_json["result"]}, {reward}")
        db.session.query(Round).filter(
            Round.id == round_id,
        ).update({
            Round.reward: Round.reward + reward,
            Round.validation: func.jsonb_set(
                Round.validation,
                f'{{{question_id},reward}}',
                cast(reward, JSONB),
                True
            )
        }, synchronize_session=False)
        db.session.commit()
        
    return resp.text