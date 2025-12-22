from app.models.base import Base
from flask_sqlalchemy import SQLAlchemy
# Don't forget to import model, or can't create table automatically
from app.models.round import Round

def create_all_tables(db: SQLAlchemy):
    Base.metadata.create_all(bind=db.engine)