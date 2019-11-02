import pyglet
import yaml


class Rendering:
    TILE_SIZE = 32
    TILESET_PATH = 'sample_tileset.png'

    def __init__(self, game_map=None):
        self.window = pyglet.window.Window()

        # Window size should be a multiplier of
        # TILE_SIZE to avoid half-drawn tiles
        assert self.window.width % self.TILE_SIZE == 0
        assert self.window.height % self.TILE_SIZE == 0

        tileset_image = pyglet.resource.image(self.TILESET_PATH)

        assert tileset_image.width % self.TILE_SIZE == 0
        tileset_width = int(tileset_image.width / self.TILE_SIZE)
        assert tileset_image.height % self.TILE_SIZE == 0
        tileset_height = int(tileset_image.height / self.TILE_SIZE)

        tileset_grid = pyglet.image.ImageGrid(
            tileset_image, tileset_height, tileset_width)
        self.tileset = pyglet.image.TextureGrid(tileset_grid)

        self.tile_data = Rendering.load_tile_data()

        self.game_map = game_map

        self.camera_x = 0
        self.camera_y = 0

    @staticmethod
    def load_tile_data():
        tile_data_file = pyglet.resource.file('tiles.yml')
        tile_data = yaml.safe_load(tile_data_file)
        tile_data_file.close()
        return tile_data

    def draw_tile(self, x, y, tile):
        sheet_x = self.tile_data[tile]['sheet_x']
        sheet_y = self.tile_data[tile]['sheet_y']

        self.tileset[sheet_y, sheet_x].blit(
            x * self.TILE_SIZE,
            y * self.TILE_SIZE
        )

    def draw_relative(self, x, y, tile):
        self.draw_tile(x - self.camera_x, y - self.camera_y, tile)

    def draw_map(self):
        # iterate rows in reverse (0-based)
        for row_idx in range(self.game_map.map_height-1, -1, -1):
            # columns are iterated normally
            # this reads the level map from the bottom-left,
            # as is the rendering done in pyglet (0,0 is bottom left)
            for col_idx in range(0, self.game_map.map_width):
                tile = self.game_map[self.game_map.map_height
                                     * row_idx + col_idx]
                x_pos = col_idx
                y_pos = (self.game_map.map_height - (row_idx + 1))
                self.draw_relative(x_pos, y_pos, tile)
