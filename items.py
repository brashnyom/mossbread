import pyglet
import yaml
from typing import List, Dict, Tuple, NamedTuple, Any


class ItemGeneral(NamedTuple):
    id: int
    name: str
    description: str
    type: str


class ItemWeapon(ItemGeneral):
    damage: int


class ItemArmor(ItemGeneral):
    damage: int


class ItemFood(ItemGeneral):
    damage: int


item_type_to_class = {
    "general": ItemGeneral,
    "weapon": ItemWeapon,
    "armor": ItemArmor,
    "food": ItemFood,
}


def get_item_attribute_values(
    item_attrs: Dict[str, Any], attributes: Tuple[str, ...]
) -> Tuple[Any, ...]:
    assert all(
        (attr in item_attrs for attr in attributes)
    ), f"Attributes from {attributes} not found in {item_attrs}!"
    return tuple(item_attrs[attr] for attr in attributes)


def load_items(filepath: str) -> List[tuple]:
    items: List[tuple] = list()
    items_data_file = pyglet.resource.file(filepath)
    items_data: dict = yaml.safe_load(items_data_file)
    for item_data in items_data:
        if item_data["type"] in item_type_to_class:
            item_type = item_type_to_class[item_data["type"]]
            items.append(
                item_type(*get_item_attribute_values(item_data, item_type._fields))
            )
        else:
            print(f"Unknown item type {item_data['type']} for item {item_data['id']}!")
    return items


class Inventory:
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.inventory = list()

    def equip(self):
        pass

    def unequip(self, slot: str):
        pass

    def add_item(self, item: dict):
        pass

    def remove_item(self, item: dict):
        pass
