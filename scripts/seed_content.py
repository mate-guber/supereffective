from app.database import SessionLocal
from data.seed.seed_type_matchups import seed_type_matchups

with SessionLocal() as session:
    seed_type_matchups(session)

    session.commit()