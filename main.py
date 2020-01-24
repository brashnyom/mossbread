import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite
from rendering import Rendering
from game_map import GameMap

from entities import Entity


game_map = GameMap.from_file("sample_map.txt")
rendering = Rendering(game_map)

player_image = rendering.get_tile_as_image(5)

player = Entity(1, 1, Sprite(player_image, 0, 0))
npc = Entity(15, 10, Sprite(player_image, 0, 0))

entities = list()
entities.append(player)
entities.append(npc)

rendering.center_camera(player.x, player.y)


def move_entity(entity_idx: int, x: int, y: int):
    target_entity = entities[entity_idx]
    potential_map_tile = game_map.get(
        target_entity.x + x, game_map.height - (target_entity.y + y + 1)
    )
    if potential_map_tile != 1:
        return

    for idx, entity in enumerate(entities):
        if idx == entity_idx:
            continue
        if (target_entity.x + x) == entity.x and (target_entity.y + y) == entity.y:
            return

    target_entity.x += x
    target_entity.y += y


@rendering.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        move_entity(0, 0, 1)
    elif symbol == key.S:
        move_entity(0, 0, -1)
    elif symbol == key.D:
        move_entity(0, 1, 0)
    elif symbol == key.A:
        move_entity(0, -1, 0)
    rendering.center_camera(player.x, player.y)


@rendering.window.event
def on_draw():
    rendering.window.clear()
    rendering.draw_map()
    for entity in entities:
        entity.update_sprite_pos(*rendering.relative_to_camera(entity.x, entity.y))
        entity.sprite.draw()


pyglet.app.run()
