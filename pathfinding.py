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
