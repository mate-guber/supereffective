import httpx
from sqlalchemy.orm import Session
from app.models import Pokemon, MetaUsageData
from data.pipeline.fetch_json import fetch_json

usage_data_cache = {}
pokemon_names = []

def fetch_legal_pokemon_list() -> list[str]:
    #Ffetch usage data from smogon stats.
    # Return a list of normalized pokemon names available in the format.
    return pokemon_names

def ingest_usage_data(session: Session, pokemon: list[Pokemon]) -> None:
    # Build MetaUsageData model objects then add them to the session
    pass