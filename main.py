import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite
from rendering import Rendering
from game_map import GameMap

from entities import BaseEntity


game_map = GameMap.from_file("sample_map.txt")
rendering = Rendering(game_map)

player_image = rendering.get_tile_as_image(5)
player_sprite = Sprite(player_image, 0, 0)

player = BaseEntity(1, 1, player_sprite)
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
    player.update_sprite_pos(*rendering.relative_to_camera(player.x, player.y))
    player.sprite.draw()


pyglet.app.run()
