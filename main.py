import pyglet
from pyglet.window import key
from rendering import Rendering
from game_map import GameMap
from entities import PlayerEntity


game_map = GameMap()
game_map.load_mapfile("sample_map.txt")
rendering = Rendering(game_map)
entities = list()
player = PlayerEntity()
player.x = 1
player.y = 1
entities.append(player)
rendering.center_camera(player.x, player.y)


@rendering.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        player.y += 1
    elif symbol == key.S:
        player.y -= 1
    elif symbol == key.D:
        player.x += 1
    elif symbol == key.A:
        player.x -= 1
    rendering.center_camera(player.x, player.y)


@rendering.window.event
def on_draw():
    rendering.window.clear()
    rendering.draw_map()
    for entity in entities:
        rendering.draw_tile_relative(entity.x, entity.y, entity.tile_num)


pyglet.app.run()
