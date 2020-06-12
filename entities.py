from typing import Dict, Optional
from collections import deque

from game_map import GameMap
from pathfinding import breadth_first_search


class Entity:
    def __init__(self, id: int, x: int, y: int, tile_id: int):
        self.id = id
        self.x = x
        self.y = y
        self.tile_id = tile_id


class Character(Entity):
    def __init__(self, id: int, x: int, y: int, tile_id: int):
        super(Character, self).__init__(id, x, y, tile_id)
        self.hp = 100
        self.max_hp = 100


class NPC(Character):
    def __init__(self, id: int, x: int, y: int, tile_id: int):
        super(NPC, self).__init__(id, x, y, tile_id)
        self.path: Optional[deque] = None

    def set_path(self, game_map: GameMap, target_x: int, target_y: int):
        self.path = breadth_first_search(
            game_map, (self.x, self.y), (target_x, target_y)
        )


class EntityHandler:
    def __init__(self, game_map: GameMap):
        self.entities: Dict[int, Entity] = dict()
        self.entity_id_tracker = 0
        self.game_map = game_map

    def spawn_entity(self, entity_class, x: int, y: int, tile_id: int):
        # TODO Implement re-use of free entity IDs left behind
        # after an entity is deleted
        self.entities[self.entity_id_tracker] = entity_class(
            self.entity_id_tracker, x, y, tile_id
        )
        self.entity_id_tracker += 1
        return self.entities[self.entity_id_tracker - 1]

    def move_entity(self, target_entity_id: int, x: int, y: int) -> bool:
        # TODO Should this method work by incrementing the target entity's
        # coordinates or directly setting them to the requested position?
        target_entity = self.entities[target_entity_id]

        target_entity.x += x
        target_entity.y += y

        if self.handle_collision_terrain(target_entity):
            target_entity.x -= x
            target_entity.y -= y
            return False

        for entity_id, entity in self.entities.items():
            if entity_id == target_entity_id:
                continue
            elif self.check_collision(target_entity, entity):
                if self.handle_collision_entity(target_entity, entity):
                    target_entity.x -= x
                    target_entity.y -= y
                    return False

        return True

    def check_collision(self, l_entity: Entity, r_entity: Entity) -> bool:
        return l_entity.x == r_entity.x and l_entity.y == r_entity.y

    def handle_collision_terrain(self, entity: Entity) -> bool:
        # It is assumed that the entity is colliding with the terrain on
        # the tile it is currently standing on
        return not self.game_map.traversable(entity.x, entity.y)

    def handle_collision_entity(self, l_entity: Entity, r_entity: Entity) -> bool:
        # l_entity is the entity which initiated the collision
        # if isinstance(l_entity, Character) and isinstance(r_entity, Character):
        #     r_entity.hp -= 20
        #     if r_entity.hp == 0:
        #         del(self.entities[r_entity.id])
        return True

    def update_npc_pos(self, dt):
        for entity_id, entity in self.entities.items():
            if isinstance(entity, NPC) and entity.path:
                next_node = entity.path.popleft()
                next_x = next_node[0] - entity.x
                next_y = next_node[1] - entity.y
                if not self.move_entity(entity_id, next_x, next_y):
                    entity.path.appendleft(next_node)
