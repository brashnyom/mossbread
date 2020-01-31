import pytest
import os
import yaml

from game_map import GameMap


def get_relative_path(filepath: str):
    return os.path.join(os.path.dirname(__file__), filepath)


@pytest.fixture(scope="module")
def test_game_map():
    return GameMap.from_file(get_relative_path("fixtures/map.csv"))


@pytest.fixture(scope="module")
def test_tiles():
    with open(get_relative_path("fixtures/map.csv")) as infile:
        tiles = yaml.safe_load(infile)
    return tiles
