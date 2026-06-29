from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Table, Column
from datetime import datetime, date

import database as db


pokemon_to_type_association = Table(
    "pokemon_to_type_association",
    db.Base.metadata,
    Column("species_id", ForeignKey("pokemon_species.id"), primary_key=True),
    Column("pokemon_type_id", ForeignKey("pokemon_type.id"), primary_key=True),
)

class Type(db.Base):
    __tablename__ = "pokemon_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

class Pokemon(db.Base):
    __tablename__ = "pokemon_species"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True)
    speed: Mapped[int] 

    species_type: Mapped[List["Type"]] = relationship(secondary=pokemon_to_type_association)

class TypeMatchup(db.Base):
    __tablename__ = "type_matchup"

    attacker: Mapped[int] = mapped_column(ForeignKey("pokemon_type.id"), primary_key=True)
    defender: Mapped[int] = mapped_column(ForeignKey("pokemon_type.id"), primary_key=True)
    attacker_type: Mapped["Type"] = relationship(foreign_keys=[attacker])
    defender_type: Mapped["Type"] = relationship(foreign_keys=[defender])
    multiplier: Mapped[float]

class MetaUsageData(db.Base):
    __tablename__ = "meta_usage_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon_species.id"))
    usage_percentage: Mapped[float] 
    from_month: Mapped[date]
    format_name: Mapped[str]

class Concept(db.Base):
    __tablename__ = "concept"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    description: Mapped[str]
    difficulty: Mapped[int]

class Question(db.Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    answer: Mapped[str]
    concept_id: Mapped[int] = mapped_column(ForeignKey("concept.id"))

class UserData(db.Base):
    __tablename__ = "user_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

class AnswerRecord(db.Base):
    __tablename__ = "answer_record"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    correct: Mapped[bool]
    timestamp: Mapped[datetime]