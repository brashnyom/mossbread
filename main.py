import pyglet
from pyglet.window import key
from rendering import Rendering
from game_map import GameMap
from entities import PlayerEntity


game_map = GameMap()
game_map.load_mapfile('sample_map.txt')
rendering = Rendering(game_map)
entities = list()
player = PlayerEntity()
player.x = 1
player.y = 1
entities.append(player)


@rendering.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        rendering.camera_y += 1
    elif symbol == key.S:
        rendering.camera_y -= 1
    elif symbol == key.D:
        rendering.camera_x += 1
    elif symbol == key.A:
        rendering.camera_x -= 1


@rendering.window.event
def on_draw():
    rendering.window.clear()
    rendering.draw_map()
    for entity in entities:
        rendering.draw_relative(entity.x, entity.y, entity.tile_num)


pyglet.app.run()
