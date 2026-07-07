import datetime
from app.database import SessionLocal
from data.pipeline.types_and_matchups import ingest_types
from data.pipeline.meta_stats import fetch_usage_data, ingest_usage_data
from data.pipeline.pokemon import ingest_pokemon

# 1760 rating cutoff reflects high-level play specifically.
# Lower cutoffs include less intentional team-building
# which would distort meta-relevance weighting.
DATE_TO_GET = datetime.date(2026, 6, 1)
FORMAT_NAME = "gen9championsvgc2026regmb-1760"

with SessionLocal() as session:
    ingest_types(session=session)
    usage_data = fetch_usage_data(date=DATE_TO_GET, format_name=FORMAT_NAME)
    pokemons = ingest_pokemon(session=session, usage_data=usage_data)
    ingest_usage_data(session=session, pokemons=pokemons, usage_data=usage_data)

    session.commit()