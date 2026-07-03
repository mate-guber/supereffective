from sqlalchemy.orm import Session
from app.models import Pokemon
from data.pipeline.fetch_json import fetch_json

pokemons: list[Pokemon] = []

def ingest_pokemon(session: Session, pokemon_names: list[str]) -> list[Pokemon]:
    # Take a list of pokemon names, query PokeAPI, return Pokemon model objects list
    # Also add them to the session
    return pokemons