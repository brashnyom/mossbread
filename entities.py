import time

from collections import deque
from typing import Dict, Tuple, List, Deque

from game_map import GameMap


def get_traversable_neighbours(
    game_map: GameMap, x_pos, y_pos, seen
) -> List[Tuple[int, int]]:
    neighbours: List[Tuple[int, int]] = list()

    for (x, y) in (
        (x_pos, y_pos - 1),
        (x_pos, y_pos + 1),
        (x_pos - 1, y_pos),
        (x_pos + 1, y_pos),
    ):
        if x < 0 or x >= game_map.width:
            continue
        if y < 0 or y >= game_map.height:
            continue
        if game_map.traversable(x, y) and (x, y) not in seen:
            neighbours.append((x, y))

    return neighbours


def breadth_first_search(
    game_map, start: Tuple[int, int], end: Tuple[int, int],
) -> Deque[Tuple[int, int]]:
    start_time = time.time()

    frontier: deque = deque()
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = dict()

    frontier.append(start)
    came_from[start] = start

    while frontier:
        node = frontier.popleft()

        if node == end:
            path: Deque[Tuple[int, int]] = deque()
            while node in came_from:
                new_node = came_from[node]
                path.appendleft(node)
                del came_from[node]
                node = new_node

            end_time = time.time()
            print(f"Found path in {(end_time - start_time) * 1000} miliseconds!")
            return path

        neighbours = get_traversable_neighbours(
            game_map, node[0], node[1], came_from.keys()
        )
        frontier.extend(neighbours)
        for neighbour in neighbours:
            came_from[neighbour] = node

    end_time = time.time()
    print(f"Could not find a path in {(end_time - start_time) * 1000} miliseconds.")
    return deque()


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
