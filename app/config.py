import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from solana.rpc.api import Client
from app.models.main import create_all_tables

load_dotenv()

app = Flask(__name__)

DEBUG_MODE = os.getenv("DEBUG", "false") == "true"

# 初始化数据库连接
PSQL_DB_URL = os.getenv("PSQL_DB_URL")
if not PSQL_DB_URL:
    raise RuntimeError("PSQL_DB_URL not found in env")
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_DB_URL
db = SQLAlchemy(app)
with app.app_context():
    create_all_tables(db)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db.engine)

# RPC客户端
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "http://127.0.0.1:8899")
rpc_client = Client(endpoint=SOLANA_RPC_URL)

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()