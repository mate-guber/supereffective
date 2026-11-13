import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.database import Base
import app.models as models
import engine.loaders as loaders
import engine.weights as weights
import engine.errors as errors

@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()

def test_get_every_type_name(session):
    grass = models.Type(name="grass")
    fire = models.Type(name="fire")
    session.add_all([grass, fire])
    result = loaders.get_every_type_name(session)
    assert set(result) == {"grass", "fire"}

def test_get_every_type_name_empty_table(session):
    with pytest.raises(errors.TypeDataError, match="No type names"):
        loaders.get_every_type_name(session)

def test_loader_returns_entry_with_name_types_and_usage(session):
    grass = models.Type(name="grass")
    fire = models.Type(name="fire")
    pokemon = models.Pokemon(species_type=[grass, fire],
                             name="grassyfireguy",
                             speed=96)
    usage = models.MetaUsageData(pokemon=pokemon,
                                 usage_percentage=0.8)
    session.add_all([grass, fire, pokemon, usage])
    result = loaders.get_meta_entries(session)
    assert len(result) == 1
    entry = result[0]
    assert entry.pokemon_name == "grassyfireguy"
    assert set(entry.types) == {"grass", "fire"}
    assert entry.usage == pytest.approx(0.8)

def test_empty_meta_usage_data_table(session):
    with pytest.raises(errors.MetaDataError, match="No meta usage"):
        loaders.get_meta_entries(session)

def test_no_type_pokemon_in_meta_entries(session):
    pokemon = models.Pokemon(species_type=[],
                             name="missingtype",
                             speed=10)
    usage = models.MetaUsageData(pokemon=pokemon,
                                 usage_percentage=0.1)
    session.add_all([pokemon, usage])
    with pytest.raises(errors.MetaDataError, match="missingtype"):
        loaders.get_meta_entries(session)