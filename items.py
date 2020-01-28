import sys
import yaml
from pprint import pprint
from typing import List, NamedTuple


class ItemGeneral(NamedTuple):
    id: int
    name: str
    description: str
    type: str


class ItemWeapon(NamedTuple):
    id: int
    name: str
    description: str
    type: str
    damage: int


class ItemArmor(NamedTuple):
    id: int
    name: str
    description: str
    type: str
    defense: int


class ItemFood(NamedTuple):
    id: int
    name: str
    description: str
    type: str
    hp_restored: int


item_type_to_class = {
    "general": ItemGeneral,
    "weapon": ItemWeapon,
    "armor": ItemArmor,
    "food": ItemFood,
}


def load_items(raw_items_data: str) -> List[tuple]:
    items: List[tuple] = list()
    for item_data in yaml.safe_load(raw_items_data):
        try:
            item_type = item_type_to_class[item_data["type"]]
            items.append(item_type(**item_data))
        except KeyError:
            print(
                (
                    f"Unknown item type '{item_data['type']}' for"
                    "item with id={item_data['id']}!"
                ),
                file=sys.stderr,
            )
            raise
        except TypeError:
            print(
                "Error! Could not load the following item:", file=sys.stderr,
            )
            pprint(item_data, stream=sys.stderr)
            raise
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
