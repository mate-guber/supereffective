import httpx
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Pokemon, Type
from data.pipeline.fetch_json import fetch_json


def ingest_pokemon(session: Session, usage_data: dict[str, float]) -> dict[str, Pokemon]:
    """Ensure a Pokemon row exists for each name in usage_data, 
    fetching missing ones from PokeAPI.

    Existing Pokemon are looked up by name and reused as-is. 
    Names not yet present in the database are fetched and constructed 
    with their speed stat and types. 
    New Pokemon are staged on the session but not committed.

    Args:
        session: Active SQLAlchemy session used for existing-row lookups 
            and staging new rows.
        usage_data: Mapping of normalized Pokemon names 
            (PokeAPI slug format) to their usage percentage.

    Returns:
        A dict mapping each original name from usage_data to its 
        corresponding Pokemon object
        (either the existing DB row or a newly constructed one).

    Raises:
        httpx.HTTPStatusError: If a PokeAPI request for a new 
            Pokemon fails.
    """

    pokemons: dict[str, Pokemon] = {}

    type_stmt = select(Type)
    types_by_name = {t.name: t for t in session.scalars(type_stmt).all()}

    pokemon_stmt = select(Pokemon).where(Pokemon.name.in_(usage_data.keys()))
    existing = session.scalars(pokemon_stmt)
    existing_by_name = {p.name: p for p in existing}

    with httpx.Client() as client:
        for name in usage_data.keys():
            if name in existing_by_name:
                pokemons[name] = existing_by_name[name]
                continue

            data = fetch_json(client, f"https://pokeapi.co/api/v2/pokemon/{name}/")
            speed = next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == "speed")
            pokemon_types = [types_by_name[t['type']['name']]for t in data['types']]
            pokemons[name] = Pokemon(name=name, speed=speed, species_type=pokemon_types)
    
    session.add_all(pokemons.values())
    
    return pokemons