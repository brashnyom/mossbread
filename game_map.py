from array import array
from typing import Tuple, Dict, Any


class GameMap:
    def __init__(
        self,
        map_data: tuple,
        width: int,
        height: int,
        tile_data: Dict[int, Dict[str, Any]],
    ):
        self.map_data = map_data
        self.width = width
        self.height = height
        self.tile_data = tile_data

    @staticmethod
    def load_mapfile(path: str) -> Tuple[tuple, int, int]:
        # Works only with rectangular maps
        map_width, map_height = 0, 0
        map_data = list()

        with open(path, "r") as mapfile:
            # Read the level map from the bottom-left to the top-right
            for line in reversed(list(mapfile)):
                split_line = line.strip().split(",")

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
    def from_file(path: str, tile_data: Dict[int, Dict[str, Any]]) -> "GameMap":
        return GameMap(*GameMap.load_mapfile(path), tile_data)

    def get(self, x: int, y: int) -> int:
        assert x >= 0 and x <= self.width, x
        assert y >= 0 and y <= self.height, y
        return self.map_data[y][x]

    def traversable(self, x: int, y: int) -> bool:
        return not self.tile_data[self.get(x, y)]["solid"]
