import pytest

from utils.capped_dict import CappedDict


@pytest.fixture(name='capped_map')
def capped_map_with_3_capacity():
    return CappedDict(3)


def test_add_elements(capped_map):
    capped_map["a"] = 1
    capped_map["b"] = 2
    capped_map["c"] = 3

    assert capped_map.get("a") == 1
    assert capped_map.get("b") == 2
    assert capped_map.get("c") == 3


def test_update_existing_key(capped_map):
    capped_map["b"] = 2

    capped_map["b"] = 7
    assert capped_map.get("b") == 7


def test_capacity_exceeded(capped_map):
    capped_map["a"] = 1
    capped_map["b"] = 2
    capped_map["c"] = 3

    capped_map["d"] = 4
    assert capped_map.get("a") is None
    assert capped_map.get("b") == 2
    assert capped_map.get("c") == 3
    assert capped_map.get("d") == 4


if __name__ == "__main__":
    pytest.main()
