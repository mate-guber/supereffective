import httpx
from sqlalchemy.orm import Session
from app.models import Type, TypeMatchup
from data.pipeline.fetch_json import fetch_json


def iter_damage_pairs(response_cache, relation_multipliers):
    """Yield (attacker_name, defender_name, multiplier) for every type matchup."""
    for attacker, relations in response_cache.items():
        for relation_key, multiplier in relation_multipliers:
            for defender in relations[relation_key]:
                yield attacker, defender['name'], multiplier

def ingest_types(session: Session) -> None:
    """Fetch all Pokemon types and their damage relations from PokeAPI, then stage
    Type and TypeMatchup objects in the given session.

    Excludes legacy/non-VGC types: unknown, shadow, stellar. Type rows missing
    from TypeMatchup are assumed neutral (1x multiplier) by convention.

    Args:
        session: SQLAlchemy session to stage the new objects in. This function
            does not call session.commit() as that's the caller's responsibility.

    Raises:
        httpx.HTTPStatusError: If any PokeAPI request returns a 4xx or 5xx response.
    """

    response_cache: dict[str, dict] = {}
    types: dict[str, Type] = {}
    matchups: list[TypeMatchup] = []

    relation_multipliers = [
        ('double_damage_to', 2.0),
        ('half_damage_to', 0.5),
        ('no_damage_to', 0.0),
        ]

    with httpx.Client() as client:
        type_collection = fetch_json(client, 'https://pokeapi.co/api/v2/type/', params={'limit': 100})
        
        # excluding legacy/non-VGC types: unknown, shadow, stellar
        excluded = {'stellar', 'unknown', 'shadow'}
        urls = [entry['url'] for entry in type_collection['results'] if entry['name'] not in excluded]

        for url in urls:
            r = fetch_json(client, url)
            response_cache[r['name']] = r['damage_relations']

            obj = Type(name=r['name'])
            types[r['name']] = obj

    for attacker, defender_name, multiplier in iter_damage_pairs(response_cache, relation_multipliers):
        matchups.append(TypeMatchup(
            attacker_type=types[attacker],
            defender_type=types[defender_name],
            multiplier=multiplier
        ))

    # Due to SQLAlchemy cascade behaviour Type objects get added transitively
    session.add_all(matchups)
