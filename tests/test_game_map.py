import os
import pytest

from array import array
from game_map import GameMap


sample_map_data = (
    array("I", (1, 2, 1)),
    array("I", (1, 0, 1)),
    array("I", (1, 1, 1)),
)
sample_game_map = GameMap(sample_map_data, 3, 3)


def get_relative_path(filepath: str):
    return os.path.join(os.path.dirname(__file__), filepath)


def test_game_map_init():
    assert sample_game_map.map_data == sample_map_data
    assert sample_game_map.width == 3
    assert sample_game_map.height == 3


def test_game_map_get():
    for x in range(0, 3):
        for y in range(0, 3):
            assert sample_game_map.get(x, y) == sample_map_data[y][x]


def test_game_map_get_out_of_bounds():
    with pytest.raises(AssertionError):
        sample_game_map.get(-1, 0)
        sample_game_map.get(0, -1)
        sample_game_map.get(-1, -1)
        sample_game_map.get(3, 0)
        sample_game_map.get(0, 3)
        sample_game_map.get(3, 3)


def test_game_map_load_mapfile():
    map_data, width, height = GameMap.load_mapfile(
        get_relative_path("fixtures/sample_map.txt")
    )
    assert map_data == sample_map_data
    assert width == 3
    assert height == 3

    # Assert map is read right-up (since (0,0) is bottom-left)
    assert map_data[0][1] == 2
    assert map_data[1][1] == 0
    assert map_data[2][1] == 1


def test_game_map_load_mapfile_different_delim():
    map_data, width, height = GameMap.load_mapfile(
        get_relative_path("fixtures/sample_map_different_delim.txt"), delimiter=" "
    )
    assert map_data == sample_map_data
    assert width == 3
    assert height == 3


def test_game_map_load_mapfile_nonrectangular():
    with pytest.raises(AssertionError):
        GameMap.load_mapfile(
            get_relative_path("fixtures/sample_map_nonrectangular.txt")
        )


def test_game_map_from_file():
    game_map = GameMap.from_file(get_relative_path("fixtures/sample_map.txt"))
    assert game_map.map_data == sample_map_data
    assert game_map.width == 3
    assert game_map.height == 3

    # Assert map is read right-up
    assert game_map.get(1, 0) == 2
    assert game_map.get(1, 1) == 0
    assert game_map.get(1, 2) == 1
