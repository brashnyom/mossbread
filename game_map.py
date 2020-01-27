from array import array
from typing import Tuple


class GameMap:
    def __init__(self, map_data: tuple, width: int, height: int):
        self.map_data = map_data
        self.width = width
        self.height = height

    def get(self, x: int, y: int) -> int:
        assert x >= 0 and x <= self.width, x
        assert y >= 0 and y <= self.height, y
        return self.map_data[y][x]

    @staticmethod
    def load_mapfile(path: str, delimiter: str = ",") -> Tuple[tuple, int, int]:
        # Works only with rectangular maps
        map_width, map_height = 0, 0
        map_data = list()

        with open(path, "r") as mapfile:
            # Read the level map from the bottom-left to the top-right
            for line in reversed(list(mapfile)):
                split_line = line.strip().split(delimiter)

                if map_width == 0:
                    map_width = len(split_line)
                else:
                    assert len(split_line) == map_width

                map_height += 1

                map_row = array("I")
                map_row.extend(map(int, split_line))
                map_data.append(map_row)

        return tuple(map_data), map_width, map_height

    @staticmethod
    def from_file(path: str, delimiter: str = ",") -> "GameMap":
        return GameMap(*GameMap.load_mapfile(path, delimiter))
