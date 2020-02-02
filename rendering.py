import pyglet

from typing import Dict, Tuple, Final, Any
from math import ceil

from game_map import GameMap
from entities import Entity


class Tileset:
    TILE_SIZE: Final[int] = 32

    def __init__(self, tileset_path: str, tile_data: Dict[int, Dict[str, Any]]):
        self.tile_data = tile_data

        tileset_image = pyglet.resource.image(tileset_path)
        assert tileset_image.width % self.TILE_SIZE == 0
        assert tileset_image.height % self.TILE_SIZE == 0

        self.tileset_grid = pyglet.image.ImageGrid(
            tileset_image,
            int(tileset_image.height / self.TILE_SIZE),
            int(tileset_image.width / self.TILE_SIZE),
        )
        self.tileset = pyglet.image.TextureGrid(self.tileset_grid)

    def __getitem__(self, tile_id: int) -> pyglet.image.TextureRegion:
        sheet_x = self.tile_data[tile_id]["sheet_x"]
        sheet_y = self.tile_data[tile_id]["sheet_y"]
        return self.tileset[sheet_y, sheet_x]


class Rendering:
    def __init__(self, tileset: Tileset):
        self.tileset = tileset

        self.window = pyglet.window.Window(800, 600)
        self.window_width_tiles = int(ceil(self.window.width / self.tileset.TILE_SIZE))
        self.window_height_tiles = int(
            ceil(self.window.height / self.tileset.TILE_SIZE)
        )

        self.camera_center_offset_x = int(self.window_width_tiles / 2)
        self.camera_center_offset_y = int(self.window_height_tiles / 2)
        self.camera_x = 0
        self.camera_y = 0

        self.entities: Dict[int, pyglet.sprite.Sprite] = dict()

    def center_camera(self, x: int, y: int):
        self.camera_x = x - self.camera_center_offset_x
        self.camera_y = y - self.camera_center_offset_y

    def relative_to_camera(self, x: int, y: int) -> Tuple[int, int]:
        return x - self.camera_x, y - self.camera_y

    def draw_tile(self, x: int, y: int, tile_id: int):
        self.tileset[tile_id].blit(
            x * self.tileset.TILE_SIZE, y * self.tileset.TILE_SIZE
        )

    def draw_tile_relative(self, x: int, y: int, tile_id: int):
        self.draw_tile(*self.relative_to_camera(x, y), tile_id)

    def draw_map(self, game_map: GameMap):
        start_x, start_y = max(self.camera_x, 0), max(self.camera_y, 0)
        rel_x, rel_y = self.relative_to_camera(start_x, start_y)
        end_x = self.window_width_tiles - rel_x
        end_y = self.window_height_tiles - rel_y

        for y_pos in range(start_y, min(start_y + end_y, game_map.height)):
            for x_pos in range(start_x, min(start_x + end_x, game_map.width)):
                self.draw_tile_relative(x_pos, y_pos, game_map.get(x_pos, y_pos))

    def add_entity(self, entity: Entity):
        self.entities[entity.id] = pyglet.sprite.Sprite(
            self.tileset[entity.tile_id], entity.x, entity.y
        )

    def draw_entities(self, entities: Dict[int, Entity]):
        for entity in entities.values():
            if entity.id in self.entities:
                x, y = self.relative_to_camera(entity.x, entity.y)
                self.entities[entity.id].x = x * self.tileset.TILE_SIZE
                self.entities[entity.id].y = y * self.tileset.TILE_SIZE
                self.entities[entity.id].draw()
