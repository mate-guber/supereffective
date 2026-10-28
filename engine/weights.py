from typing import NamedTuple

class MetaEntry(NamedTuple):
    pokemon_name: str
    types: tuple[str, ...]
    usage: float