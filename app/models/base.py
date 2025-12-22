from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase, SerializerMixin):
    pass