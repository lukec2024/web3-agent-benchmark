from sqlalchemy import Column, String, DateTime, Text, JSON, Integer
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, UTC
from app.models.base import Base
from sqlalchemy.orm import mapped_column

class Round(Base):
    __tablename__ = "rounds"

    id = mapped_column(String(32), primary_key=True)
    agent_name = mapped_column(String(64), nullable=False)
    prompt = mapped_column(JSON, nullable=False)
    validation = mapped_column(JSONB, nullable=False)
    agent_kp = mapped_column(String(256), nullable=False)
    agent_pubkey = mapped_column(String(64), nullable=False)
    reward = mapped_column(Integer, default=0)
    created_at = mapped_column(DateTime, default=datetime.now(UTC))