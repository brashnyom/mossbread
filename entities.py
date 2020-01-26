from typing import Dict, Any

from pyglet.sprite import Sprite

from rendering import Rendering
from game_map import GameMap


class EntityHandler:
    def __init__(
        self,
        game_map: GameMap,
        rendering: Rendering,
        tile_data: Dict[int, Dict[str, Any]],
    ):
        self.entities: Dict[int, Entity] = dict()
        self.entity_id_tracker = 0
        self.game_map = game_map
        self.rendering = rendering
        self.tile_data = tile_data

    def spawn_entity(self, x: int, y: int, tile: int):
        # TODO Implement re-use of free entity IDs left behind
        # after an entity is deleted
        self.entities[self.entity_id_tracker] = Entity(
            x, y, Sprite(self.rendering.get_tile_as_image(tile), 0, 0)
        )
        self.entity_id_tracker += 1

    def move_entity(self, target_entity_id: int, x: int, y: int):
        target_entity = self.entities[target_entity_id]
        potential_map_tile = self.game_map.get(
            target_entity.x + x, self.game_map.height - (target_entity.y + y + 1)
        )
        if self.tile_data[potential_map_tile]["solid"]:
            return

        for entity_id, entity in self.entities.items():
            if entity_id == target_entity_id:
                continue
            if (target_entity.x + x) == entity.x and (target_entity.y + y) == entity.y:
                return

        target_entity.x += x
        target_entity.y += y

    def update_entities(self):
        for entity in self.entities.values():
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
