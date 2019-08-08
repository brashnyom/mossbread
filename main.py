import pyglet
from pyglet.window import key
from rendering import Rendering
from game_map import GameMap


game_map = GameMap()
game_map.load_mapfile('sample_map.txt')
rendering = Rendering(game_map)


@rendering.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        rendering.camera_y += rendering.TILE_SIZE
    elif symbol == key.S:
        rendering.camera_y -= rendering.TILE_SIZE
    elif symbol == key.D:
        rendering.camera_x += rendering.TILE_SIZE
    elif symbol == key.A:
        rendering.camera_x -= rendering.TILE_SIZE


@rendering.window.event
def on_draw():
    rendering.window.clear()
    rendering.draw_map()


pyglet.app.run()
