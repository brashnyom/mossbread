import pytest
import os
import yaml

from game_map import GameMap
from rendering import Tileset


def get_relative_path(filepath: str):
    return os.path.join(os.path.dirname(__file__), filepath)


@pytest.fixture(scope="module")
def sample_tiles():
    with open(get_relative_path("fixtures/tiles.yml")) as infile:
        tiles = yaml.safe_load(infile)
    return tiles


@pytest.fixture(scope="module")
def sample_game_map(sample_tiles):
    return GameMap.from_file(get_relative_path("fixtures/map.csv"), sample_tiles)


@pytest.fixture(scope="module")
def sample_tileset(sample_tiles):
    return Tileset("fixtures/tileset.png", sample_tiles)
