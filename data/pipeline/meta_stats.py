import httpx
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.models import Pokemon, MetaUsageData
from data.pipeline.fetch_json import fetch_json

# Unique cases where PokeAPI and Smogon naming conventions mismatch
NAME_OVERRIDES = {
    "basculegion": "basculegion-male",
    "basculegion-f": "basculegion-female",
    "meowstic": "meowstic-male",
    "meowstic-f": "meowstic-female",
    "meowstic-m-mega": "meowstic-male-mega",
    "meowstic-f-mega": "meowstic-female-mega",
    "indeedee": "indeedee-male",
    "indeedee-f": "indeedee-female"
}

# Introduce a single naming convention (PokeAPI) early to avoid confusion
def normalize(name: str) -> str:
    key = name.lower().replace(" ", "-").replace("'","")
    return NAME_OVERRIDES.get(key,key)

def fetch_usage_data(date: datetime.date, format_name: str) -> dict[str, float]:
    """Fetch Pokemon usage percentages from Smogon stats 
    for a given month and format.

    Only the year and month of date are used to construct the request URL.
    Pokemon names are normalized from Smogon's naming convention to 
    PokéAPI slug format.

    Args:
        date: Determines the year and month of the stats to fetch.
        format_name: Smogon's internal format identifier, including the
            rating cutoff suffix (e.g. 'gen9championsvgc2026regmb-1500').

    Returns:
        A dict mapping normalized Pokemon names to their usage percentage
        as a float between 0 and 1.

    Raises:
        httpx.HTTPStatusError: If the Smogon stats request fails.
    """

    with httpx.Client() as client:
        stats = fetch_json(
            client, 
            f"https://www.smogon.com/stats/{date.year}-{date.month}/chaos/{format_name}.json"
            )
    
    usage_data: dict[str, float] = {
        normalize(name): entry['usage'] for name, entry in stats['data'].items()
        }
    return usage_data 

def ingest_usage_data(session: Session, 
                      pokemons: dict[str, Pokemon], 
                      usage_data: dict[str, float]) -> None:
    """Rebuild MetaUsageData rows from the current usage statistics.

    All existing MetaUsageData rows are deleted before inserting fresh ones,
    ensuring stale data from previous ingestion runs never persists.
    New rows are staged on the session but not committed.

    Args:
        session: Active SQLAlchemy session used for deletion and staging.
        pokemons: Mapping of normalized Pokemon names to their corresponding
            Pokemon objects, as returned by ingest_pokemon.
        usage_data: Mapping of normalized Pokemon names to their usage
            percentage, as returned by fetch_usage_data. Keys must match
            those in pokemons.
    """

    session.execute(delete(MetaUsageData))
    stats: list[MetaUsageData] = []

    for name, usage in usage_data.items():
        data = MetaUsageData(pokemon=pokemons[name], 
                             usage_percentage=usage)
        stats.append(data)
    
    session.add_all(stats)