from typing import Dict

from game_map import GameMap


class EntityHandler:
    def __init__(self, game_map: GameMap):
        self.entities: Dict[int, Entity] = dict()
        self.entity_id_tracker = 0
        self.game_map = game_map

    def spawn_entity(self, x: int, y: int, tile_id: int):
        # TODO Implement re-use of free entity IDs left behind
        # after an entity is deleted
        self.entities[self.entity_id_tracker] = Entity(
            self.entity_id_tracker, x, y, tile_id
        )
        self.entity_id_tracker += 1
        return self.entities[self.entity_id_tracker - 1]

    def move_entity(self, target_entity_id: int, x: int, y: int):
        # TODO Should this method work by incrementing the target entity's
        # coordinates or directly setting them to the requested position?
        # TODO Add other ways of resolving collisions instead of preventing
        # movement (for example, by damaging one of the entities)
        target_entity = self.entities[target_entity_id]

        if not self.game_map.traversable(target_entity.x + x, target_entity.y + y):
            return

        for entity_id, entity in self.entities.items():
            if entity_id == target_entity_id:
                continue
            if (target_entity.x + x) == entity.x and (target_entity.y + y) == entity.y:
                return

        target_entity.x += x
        target_entity.y += y


class Entity:
    def __init__(self, id: int, x: int, y: int, tile_id: int):
        self.id = id
        self.x = x
        self.y = y
        self.tile_id = tile_id
