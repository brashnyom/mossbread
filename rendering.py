import pyglet


class Rendering:
    TILE_SIZE = 32
    TILESET_PATH = 'sample_tileset.png'
    TILESET_WIDTH = 2
    TILESET_HEIGHT = 2

    def __init__(self, game_map=None):
        self.window = pyglet.window.Window()

        # Window size be a multiplier of TILE_SIZE
        # to avoid half-drawn tiles
        assert self.window.width % self.TILE_SIZE == 0
        assert self.window.height % self.TILE_SIZE == 0

        tileset_image = pyglet.resource.image(self.TILESET_PATH)
        tileset_grid = pyglet.image.ImageGrid(
            tileset_image, self.TILESET_HEIGHT, self.TILESET_WIDTH)
        self.tileset = pyglet.image.TextureGrid(tileset_grid)

        self.game_map = game_map

        self.camera_x = 0
        self.camera_y = 0

    def draw_tile(self, x, y, tile):
        self.tileset[tile].blit(x, y)

    def draw_map(self):
        # iterate rows in reverse (0-based)
        for row_idx in range(self.game_map.map_height-1, -1, -1):
            # columns are iterated normally
            # this reads the level map from the bottom-left,
            # as is the rendering done in pyglet (0,0 is bottom left)
            for col_idx in range(0, self.game_map.map_width):
                tile = self.game_map[self.game_map.map_height
                                     * row_idx + col_idx] - 1
                x_pos = col_idx * self.TILE_SIZE
                y_pos = (self.game_map.map_height - (row_idx + 1)) \
                    * self.TILE_SIZE

                self.tileset[tile].blit(x_pos - self.camera_x,
                                        y_pos - self.camera_y)
