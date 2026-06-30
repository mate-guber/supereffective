from app.database import SessionLocal
from data.pipeline.types_and_matchups import ingest_types


with SessionLocal() as session:
    ingest_types(session)

    session.commit()