from typing import NamedTuple
from engine.errors import TypeDataError

class MetaEntry(NamedTuple):
    pokemon_name: str
    types: tuple[str, ...]
    usage: float

def compute_type_weights(types: list[str], 
                        meta_entries: list[MetaEntry]
                        ) -> dict[str, float]:
    """Creates weights for every Pokemon type based on meta usage data.
    Dual type pokemon contribute their usage to both of their types' 
    weight. Assigns a weight of 0.0 for types with no usage.

    Args:
        types: A list of every Pokemon type's name.
        meta_entries: A list of MetaEntry that records the meta usage
            data and types for each pokemon species.

    Returns:
        A dictionary that maps types to their weights.
    
    Raises:
        TypeDataError: If a MetaEntry names a type that is not in types.
    """
    weights = {name: 0.0 for name in types}

    for entry in meta_entries:
        for t in entry.types:
            if t not in weights:
                raise TypeDataError(
                    f"{entry.pokemon_name} has unknown type: {t}")
            weights[t] += entry.usage

    return weights