import httpx
import datetime
from sqlalchemy.orm import Session
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
    """Fetches usage data from Smogon stats for a specific date 
    and format. Converts the Smogon stats Pokemon naming convention
    to PokeAPI slug format.

    Args:
        date: A date object describing which year-month the data will be
            pullef from. The day attribute does not matter.
        format_name: Smogon stats' internal name representing different 
            competitive formats or regulations.
            eg.: gen9championsvgc2026regmb with -0/-1500/-1630/-1760 
            attached to the end representing elo cutoff.
    
    Returns:
        A dict of pokemon names and their usage frequency. 
        Names are normalized to match PokeAPI slug format.
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
    
    pass