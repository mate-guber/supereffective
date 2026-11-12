import pytest
from engine.weights import MetaEntry, compute_type_weights
from engine.errors import TypeDataError

def test_single_type_gets_full_usage():
    types = ["grass", "fire", "water"]
    entry = MetaEntry(
        pokemon_name="grass-pokemon",
        types=("grass",),
        usage=0.3
    )
    result = compute_type_weights(types, [entry])

    assert result == pytest.approx({
        "grass": 0.3,
        "fire": 0.0,
        "water": 0.0
    })

def test_dual_type_gets_usage_for_both():
    types = ["grass", "fire", "water"]
    entry = MetaEntry(
        pokemon_name="grass-pokemon",
        types=("grass", "fire"),
        usage=0.5
    )
    result = compute_type_weights(types, [entry])

    assert result == pytest.approx({
        "grass": 0.5,
        "fire": 0.5,
        "water": 0.0
    })

def test_weight_accumulation():
    types = ["grass", "fire", "water"]
    entry1 = MetaEntry(
        pokemon_name="grass-pokemon",
        types=("grass",),
        usage=0.2
    )
    entry2 = MetaEntry(
        pokemon_name="grass-water-pokemon",
        types=("grass", "water"),
        usage=0.3
    )
    result = compute_type_weights(types, [entry1, entry2])

    assert result == pytest.approx({
        "grass": 0.5,
        "fire": 0.0,
        "water": 0.3
    })

def test_unknown_type_raises_error():
    types = ["grass", "fire", "water"]
    entry = MetaEntry(
        pokemon_name="mystery-pokemon",
        types=("dragon",),
        usage=0.3
    )
    with pytest.raises(TypeDataError, match="mystery-pokemon.*dragon"):
        compute_type_weights(types, [entry])

def test_empty_meta_entries_list():
    types = ["grass", "fire", "water"]
    result = compute_type_weights(types, [])

    assert result == pytest.approx({
        "grass": 0.0,
        "fire": 0.0,
        "water": 0.0
    })