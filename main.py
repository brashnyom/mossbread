import pyglet
import yaml

from pyglet.window import key

from rendering import Tileset, Rendering
from game_map import GameMap
from entities import Character, NPC, EntityHandler

tile_data_file = pyglet.resource.file("assets/tiles.yml")
tile_data = yaml.safe_load(tile_data_file)
tile_data_file.close()

tileset = Tileset("assets/sample_tileset.png", tile_data)
game_map = GameMap.from_file("assets/courtyard.csv", tile_data)
rendering = Rendering(tileset)
entity_handler = EntityHandler(game_map)

player = entity_handler.spawn_entity(Character, 1, 1, 6)
npc = entity_handler.spawn_entity(NPC, 47, 2, 6)

rendering.add_entity(player)
rendering.add_entity(npc)

npc.set_path(game_map, 9, 3)


@rendering.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        entity_handler.move_entity(player.id, 0, 1)
    elif symbol == key.S:
        entity_handler.move_entity(player.id, 0, -1)
    elif symbol == key.D:
        entity_handler.move_entity(player.id, 1, 0)
    elif symbol == key.A:
        entity_handler.move_entity(player.id, -1, 0)
    rendering.center_camera(player.x, player.y)


@rendering.window.event
def on_draw():
    rendering.window.clear()
    rendering.draw_map(game_map)
    rendering.draw_entities(entity_handler.entities)


rendering.center_camera(player.x, player.y)

pyglet.clock.schedule_interval(entity_handler.update_npc_pos, 0.1)

pyglet.app.run()
