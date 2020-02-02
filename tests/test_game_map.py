import pytest

from array import array
from game_map import GameMap
from tests.conftest import get_relative_path


sample_map_data = tuple(
    reversed(
        (
            array("I", (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0)),
            array("I", (0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)),
            array("I", (1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1)),
            array("I", (1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1)),
            array("I", (1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)),
            array("I", (1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            array("I", (1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1)),
            array("I", (0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)),
            array("I", (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0)),
        )
    )
)


def test_game_map_from_file(sample_game_map, sample_tiles):
    assert sample_game_map.map_data == sample_map_data
    assert sample_game_map.width == 21
    assert sample_game_map.height == 21
    assert sample_game_map.tile_data == sample_tiles

    # Assert map is read right-up
    assert sample_game_map.get(16, 2) == 0
    assert sample_game_map.get(16, 18) == 1


def test_game_map_get_out_of_bounds(sample_game_map):
    with pytest.raises(AssertionError):
        sample_game_map.get(-1, 0)
        sample_game_map.get(0, -1)
        sample_game_map.get(-1, -1)
        sample_game_map.get(21, 0)
        sample_game_map.get(0, 21)
        sample_game_map.get(21, 21)


def test_game_map_load_mapfile_nonrectangular():
    with pytest.raises(AssertionError):
        GameMap.load_mapfile(get_relative_path("fixtures/map_nonrectangular.csv"))


def test_game_map_traversable(sample_game_map):
    assert sample_game_map.traversable(2, 2)
    assert not sample_game_map.traversable(1, 1)
    assert sample_game_map.traversable(16, 2)
    assert not sample_game_map.traversable(16, 18)
