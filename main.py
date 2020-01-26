import pyglet
import yaml

from typing import Dict

from pyglet.window import key

from rendering import Rendering
from game_map import GameMap
from entities import EntityHandler


def load_tile_data(filepath: str) -> Dict[int, Dict[str, int]]:
    tile_data_file = pyglet.resource.file(filepath)
    tile_data = yaml.safe_load(tile_data_file)
    tile_data_file.close()
    return tile_data


tile_data = load_tile_data("assets/tiles.yml")


game_map = GameMap.from_file("assets/sample_map.txt")
rendering = Rendering(game_map, tile_data)
entity_handler = EntityHandler(game_map, rendering, tile_data)

entity_handler.spawn_entity(1, 1, 5)
entity_handler.spawn_entity(15, 15, 5)

player = entity_handler.entities[0]

rendering.center_camera(player.x, player.y)


@rendering.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        entity_handler.move_entity(0, 0, 1)
    elif symbol == key.S:
        entity_handler.move_entity(0, 0, -1)
    elif symbol == key.D:
        entity_handler.move_entity(0, 1, 0)
    elif symbol == key.A:
        entity_handler.move_entity(0, -1, 0)
    rendering.center_camera(player.x, player.y)


@rendering.window.event
def on_draw():
    rendering.window.clear()
    rendering.draw_map()
    entity_handler.update_entities()


pyglet.app.run()
