from typing import Dict

from game_map import GameMap


class Entity:
    def __init__(self, id: int, x: int, y: int, tile_id: int):
        self.id = id
        self.x = x
        self.y = y
        self.tile_id = tile_id


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
        target_entity = self.entities[target_entity_id]

        target_entity.x += x
        target_entity.y += y

        if self.handle_collision_terrain(target_entity):
            target_entity.x -= x
            target_entity.y -= y

        for entity_id, entity in self.entities.items():
            if entity_id == target_entity_id:
                continue
            elif self.check_collision(target_entity, entity):
                if self.handle_collision_entity(target_entity, entity):
                    target_entity.x -= x
                    target_entity.y -= y
                    break

    def check_collision(self, l_entity: Entity, r_entity: Entity) -> bool:
        return l_entity.x == r_entity.x and l_entity.y == r_entity.y

    def handle_collision_terrain(self, entity: Entity) -> bool:
        # It is assumed that the entity is colliding with the terrain on
        # the tile it is currently standing on
        return not self.game_map.traversable(entity.x, entity.y)

    def handle_collision_entity(self, l_entity: Entity, r_entity: Entity) -> bool:
        # l_entity is the entity which initiated the collision
        return True
