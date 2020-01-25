from typing import List

from pyglet.sprite import Sprite

from rendering import Rendering
from game_map import GameMap


class EntityHandler:
    def __init__(self, game_map: GameMap, rendering: Rendering):
        self.entities: List[Entity] = list()
        self.game_map = game_map
        self.rendering = rendering

    def spawn_entity(self, x: int, y: int, tile: int):
        self.entities.append(
            Entity(x, y, Sprite(self.rendering.get_tile_as_image(tile), 0, 0))
        )

    def move_entity(self, entity_idx: int, x: int, y: int):
        target_entity = self.entities[entity_idx]
        potential_map_tile = self.game_map.get(
            target_entity.x + x, self.game_map.height - (target_entity.y + y + 1)
        )
        if potential_map_tile != 1:
            return

        for idx, entity in enumerate(self.entities):
            if idx == entity_idx:
                continue
            if (target_entity.x + x) == entity.x and (target_entity.y + y) == entity.y:
                return

        target_entity.x += x
        target_entity.y += y

    def update_entities(self):
        for entity in self.entities:
            entity.update_sprite_pos(
                *self.rendering.relative_to_camera(entity.x, entity.y)
            )
            entity.sprite.draw()


class Entity:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def update_sprite_pos(self, x: int, y: int):
        self.sprite.x = x * Rendering.TILE_SIZE
        self.sprite.y = y * Rendering.TILE_SIZE
