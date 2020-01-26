import time

from collections import deque
from typing import Dict, Tuple, List, Any

from pyglet.sprite import Sprite

from rendering import Rendering
from game_map import GameMap


def get_traversable_neighbours(
    game_map: GameMap, tile_data: Dict[int, Dict[str, Any]], x_pos, y_pos, seen
) -> List[Tuple[int, int]]:
    neighbours: List[Tuple[int, int]] = list()

    for (x, y) in (
        (x_pos, y_pos - 1),
        (x_pos, y_pos + 1),
        (x_pos - 1, y_pos),
        (x_pos + 1, y_pos),
    ):
        if x < 0 or x > game_map.width:
            continue
        if y < 0 or y > game_map.height:
            continue
        if not tile_data[game_map.get(x, y)]["solid"] and (x, y) not in seen:
            neighbours.append((x, y))

    return neighbours


def breadth_first_search(
    game_map,
    tile_data: Dict[int, Dict[str, Any]],
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> List[Tuple[int, int]]:
    start_time = time.time()

    frontier: deque = deque()
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = dict()

    frontier.append(start)
    came_from[start] = start

    while frontier:
        node = frontier.popleft()

        if node == end:
            path: List[Tuple[int, int]] = list()
            while node in came_from:
                new_node = came_from[node]
                path.append(node)
                del came_from[node]
                node = new_node

            end_time = time.time()
            print(f"Found path in {(end_time - start_time) * 1000} miliseconds!")
            return path

        neighbours = get_traversable_neighbours(
            game_map, tile_data, node[0], node[1], came_from.keys()
        )
        frontier.extend(neighbours)
        for neighbour in neighbours:
            came_from[neighbour] = node

    end_time = time.time()
    print(f"Could not find a path in {(end_time - start_time) * 1000} miliseconds.")
    return list()


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
        potential_map_tile = self.game_map.get(target_entity.x + x, target_entity.y + y)
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
