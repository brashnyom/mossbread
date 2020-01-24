import pyglet
import yaml

from typing import Dict

from game_map import GameMap


class Rendering:
    TILE_SIZE = 32
    TILESET_PATH = "sample_tileset.png"

    def __init__(self, game_map: GameMap = None):
        self.window = pyglet.window.Window(800, 600)

        tileset_image = pyglet.resource.image(self.TILESET_PATH)
        assert tileset_image.width % self.TILE_SIZE == 0
        assert tileset_image.height % self.TILE_SIZE == 0

        self.tileset_grid = pyglet.image.ImageGrid(
            tileset_image,
            int(tileset_image.height / self.TILE_SIZE),
            int(tileset_image.width / self.TILE_SIZE),
        )
        self.tileset = pyglet.image.TextureGrid(self.tileset_grid)

        self.tile_data = Rendering.load_tile_data()
        self.game_map = game_map

        self.window_width_tiles = int(self.window.width / self.TILE_SIZE)
        self.window_height_tiles = int(self.window.height / self.TILE_SIZE)
        self.camera_center_offset_x = int(self.window_width_tiles / 2)
        self.camera_center_offset_y = int(self.window_height_tiles / 2)
        self.camera_x = 0
        self.camera_y = 0

    @staticmethod
    def load_tile_data() -> Dict[int, Dict[str, int]]:
        tile_data_file = pyglet.resource.file("tiles.yml")
        tile_data = yaml.safe_load(tile_data_file)
        tile_data_file.close()
        return tile_data

    def center_camera(self, x: int, y: int):
        self.camera_x = x - self.camera_center_offset_x
        self.camera_y = y - self.camera_center_offset_y

    def draw_tile(self, x: int, y: int, tile: int):
        sheet_x = self.tile_data[tile]["sheet_x"]
        sheet_y = self.tile_data[tile]["sheet_y"]

        self.tileset[sheet_y, sheet_x].blit(x * self.TILE_SIZE, y * self.TILE_SIZE)

    def draw_tile_relative(self, x: int, y: int, tile: int):
        self.draw_tile(x - self.camera_x, y - self.camera_y, tile)

    def draw_map(self):
        # Read the level map from the bottom-left,
        # since (0,0) in pyglet is bottom-left
        for row_idx in range(0, self.game_map.height):
            y_pos = self.game_map.height - (row_idx + 1)
            for col_idx in range(0, self.game_map.width):
                x_pos = col_idx
                self.draw_tile_relative(
                    x_pos, y_pos, self.game_map.get(col_idx, row_idx)
                )
