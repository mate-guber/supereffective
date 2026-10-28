from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select
from engine.weights import MetaEntry
from engine.errors import MetaDataError
from app.models import MetaUsageData, Pokemon

def get_meta_entries(session: Session) -> list[MetaEntry]:
    """Retrieve meta usage information from the db and match it with the
    Pokemon's type.

    Args:
        session: Active SQLAlchemy session used for meta info lookup.
    
    Returns:
        A list of NamedTuples containing a pokemon name, its types, 
        and its usage stat.

    Raises:    
        MetaDataError: If MetaUsageData is empty or a Pokemon has no type.
    """
    usage_stmt = select(MetaUsageData).options(
        joinedload(MetaUsageData.pokemon).selectinload(
            Pokemon.species_type)
        )
    meta_data = session.scalars(usage_stmt)

    meta_entries: list[MetaEntry] = []

    for usage_row in meta_data:
        entry = MetaEntry(
            pokemon_name=usage_row.pokemon.name,
            types=tuple(p_type.name for p_type in usage_row.pokemon.species_type),
            usage=usage_row.usage_percentage
        )

        if not entry.types:
            raise MetaDataError(f"{entry.pokemon_name} has no type")
        meta_entries.append(entry)

    if not meta_entries:
        raise MetaDataError("No meta usage data was found in the database")

    return meta_entries
