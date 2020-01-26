import pyglet
import yaml

from typing import Dict

from pyglet.window import key

from rendering import Rendering
from game_map import GameMap
from entities import EntityHandler, breadth_first_search


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
entity_handler.spawn_entity(47, 2, 5)

player = entity_handler.entities[0]
npc = entity_handler.entities[1]

rendering.center_camera(npc.x, npc.y)

npc_path = breadth_first_search(game_map, tile_data, (47, 2), (9, 3))


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


def update_npc_pos(dt):
    if npc_path:
        next_node = npc_path.pop()
        next_x = next_node[0] - npc.x
        next_y = next_node[1] - npc.y

        entity_handler.move_entity(1, next_x, next_y)
        rendering.center_camera(npc.x, npc.y)


pyglet.clock.schedule_interval(update_npc_pos, 0.1)

pyglet.app.run()
