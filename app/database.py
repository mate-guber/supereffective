from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///supereffective.db")
SessionLocal = sessionmaker(bind=engine)