import pytest
import yaml


from io import StringIO
from contextlib import redirect_stderr
from pprint import pformat

from items import (
    ItemGeneral,
    ItemWeapon,
    ItemArmor,
    ItemFood,
    item_type_to_class,
    load_items,
)
from tests.conftest import get_relative_path


sample_general_item = ItemGeneral(
    id=1, name="test", description="test description", type="general"
)

sample_weapon_item = ItemWeapon(
    id=2,
    name="test weapon",
    description="test weapon description",
    type="weapon",
    damage=5,
)

sample_armor_item = ItemArmor(
    id=3,
    name="test armor",
    description="test armor description",
    type="armor",
    defense=10,
)

sample_food_item = ItemFood(
    id=4,
    name="test food",
    description="test food description",
    type="food",
    hp_restored=15,
)


def test_item_type_to_class():
    assert len(item_type_to_class) == 4
    assert item_type_to_class["general"] == ItemGeneral
    assert item_type_to_class["weapon"] == ItemWeapon
    assert item_type_to_class["armor"] == ItemArmor
    assert item_type_to_class["food"] == ItemFood


def test_load_items():
    with open(get_relative_path("fixtures/items.yml"), "r") as infile:
        items = load_items(infile.read())
    assert len(items) == 4
    assert set(items) == set(
        (sample_general_item, sample_weapon_item, sample_armor_item, sample_food_item,)
    )


def test_load_items_unknown_item_type():
    item = [
        {
            "id": 123,
            "name": "test unknown",
            "description": "invalid item with unknown type",
            "type": "strange nonexistent",
        }
    ]
    with pytest.raises(KeyError):
        stderr = StringIO()
        with redirect_stderr(stderr):
            load_items(yaml.dump(item))
        assert (
            stderr.getvalue()
            == "Unknown item type 'strange nonexistent' for item with id=123!"
        )


@pytest.mark.parametrize(
    "invalid_item,expected_err",
    [
        (
            [
                {
                    "id": 1,
                    "name": "test invalid",
                    "description": "invalid item with too much attributes",
                    "type": "general",
                    "broken": "additional, unknown attribute",
                }
            ],
            "__new__() got an unexpected keyword argument 'broken'",
        ),
        (
            [
                {
                    "id": 1,
                    "name": "test invalid",
                    "description": "invalid item with missing required attributes",
                    "type": "armor",
                }
            ],
            "__new__() missing 1 required positional argument: 'defense'",
        ),
    ],
)
def test_load_items_invalid_items(invalid_item, expected_err):
    with pytest.raises(TypeError) as excinfo:
        stderr = StringIO()
        with redirect_stderr(stderr):
            load_items(yaml.dump(invalid_item))

        assert (
            stderr.getvalue()
            == f"Error! Could not load the following item:\n{pformat(invalid_item)}"
        ), stderr.getvalue()

    exception_message = str(excinfo.value)
    assert expected_err in exception_message, exception_message
