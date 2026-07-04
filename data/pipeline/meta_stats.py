import httpx
import datetime
from sqlalchemy.orm import Session
from app.models import Pokemon, MetaUsageData
from data.pipeline.fetch_json import fetch_json


def fetch_usage_data(date: datetime.date, format_name: str) -> dict[str, float]:
    """Fetches usage data from Smogon stats for a specific date and format.

    Args:
        date: A date object describing which year-month the data will be
            pullef from. The day attribute does not matter.
        format_name: Smogon stats' internal name representing different 
            competitive formats or regulations.
            eg.: gen9championsvgc2026regmb with -0/-1500/-1630/-1760 
            attached to the end representing elo cutoff.
    
    Returns:
        usage_data: A dict of pokemon names and their usage frequency.
    """
    # Fetch usage data from smogon stats.
    # Return a list of normalized pokemon names available in the format.

    with httpx.Client() as client:
        stats = fetch_json(
            client, 
            f"https://www.smogon.com/stats/{date.year}-{date.month}/chaos/{format_name}.json"
            )
    
    usage_data: dict[str, float] = {name: entry['usage'] for name, entry in stats['data'].items()}
    return usage_data 

def ingest_usage_data(session: Session, 
                      pokemon: list[Pokemon], 
                      usage_data: dict[str, float], 
                      date: datetime.date) -> None:
    # Build MetaUsageData model objects then add them to the session
    pass