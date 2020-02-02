import pytest

from collections import deque

from entities import get_traversable_neighbours, breadth_first_search, EntityHandler


def test_get_traversable_neighbours_simple(sample_game_map):
    neighbours = get_traversable_neighbours(sample_game_map, 8, 2, tuple())
    assert set(neighbours) == {(7, 2), (9, 2), (8, 1), (8, 3)}


def test_get_traversable_neighbours_blocked(sample_game_map):
    neighbours = get_traversable_neighbours(sample_game_map, 9, 3, tuple())
    assert set(neighbours) == {(8, 3), (9, 2)}


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0, 0, {(0, 1), (1, 0)}),
        (0, 20, {(0, 19), (1, 20)}),
        (20, 0, {(20, 1), (19, 0)}),
        (20, 20, {(20, 19), (19, 20)}),
    ],
)
def test_get_traversable_neighbours_out_of_bounds(sample_game_map, x, y, expected):
    neighbours = get_traversable_neighbours(sample_game_map, x, y, tuple())
    assert set(neighbours) == expected


def test_get_traversable_neighbours_seen(sample_game_map):
    neighbours = get_traversable_neighbours(sample_game_map, 8, 2, ((7, 2), (8, 3)))
    assert set(neighbours) == {(9, 2), (8, 1)}


def test_breadth_first_search_no_possible_path(sample_game_map):
    path = breadth_first_search(sample_game_map, (2, 8), (8, 2))
    assert path == deque()


def test_breadth_first_search_possible_path(sample_game_map):
    expected_path = deque(
        (
            (2, 12),
            (3, 12),
            (4, 12),
            (5, 12),
            (6, 12),
            (6, 13),
            (6, 14),
            (6, 15),
            (5, 15),
            (4, 15),
            (3, 15),
            (3, 16),
            (3, 17),
            (3, 18),
            (3, 19),
            (4, 19),
            (5, 19),
            (5, 18),
            (6, 18),
            (7, 18),
            (8, 18),
        )
    )
    path = breadth_first_search(sample_game_map, (2, 12), (8, 18))
    assert path == expected_path


def test_entity_handler_spawn_entity(sample_game_map):
    handler = EntityHandler(sample_game_map)
    entity_one = handler.spawn_entity(0, 0, 1)
    entity_two = handler.spawn_entity(1, 1, 1)
    assert tuple(handler.entities.keys()) == (0, 1)
    assert tuple(handler.entities.values()) == (entity_one, entity_two)


def test_entity_handler_move_entity(sample_game_map):
    handler = EntityHandler(sample_game_map)
    entity_one = handler.spawn_entity(2, 2, 1)
    handler.move_entity(entity_one.id, 1, 1)
    assert entity_one.x == 3
    assert entity_one.y == 3


def test_entity_handler_move_entity_blocked_by_terrain(sample_game_map):
    handler = EntityHandler(sample_game_map)
    entity_one = handler.spawn_entity(4, 3, 1)
    handler.move_entity(entity_one.id, 1, 0)
    assert entity_one.x == 4
    assert entity_one.y == 3


def test_entity_handler_move_entity_blocked_by_entity(sample_game_map):
    handler = EntityHandler(sample_game_map)
    entity_one = handler.spawn_entity(2, 2, 1)
    entity_two = handler.spawn_entity(3, 2, 1)
    handler.move_entity(entity_one.id, 1, 0)
    handler.move_entity(entity_two.id, -1, 0)
    assert entity_one.x == 2
    assert entity_one.y == 2
    assert entity_two.x == 3
    assert entity_two.y == 2
