from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Type, TypeMatchup, Concept, Question


def seed_type_matchups(session: Session):

    questions: list[Question] = []
    types = session.scalars(select(Type).order_by(Type.name)).all()
    matchup_stmt = select(TypeMatchup)
    matchups = {
        (tm.attacker_id, tm.defender_id) : tm.multiplier 
        for tm in session.scalars(matchup_stmt).all()
        }

    for attacker in types:
        for defender in types:
            multiplier = matchups.get((attacker.id, defender.id), 1.0)
            concept = Concept(
                category="type_matchup", 
                description=f"{attacker.name} attacking {defender.name}"
                )
            question = Question(
                attacker_type=attacker,
                defender_type=defender,
                concept=concept,
                answer=multiplier
            )
            questions.append(question)

    session.add_all(questions)

