import pyglet
from pyglet.window import key

window = pyglet.window.Window()

TILE_SIZE = 32
tileset_image = pyglet.resource.image('sample_tileset.png')
tileset_grid = pyglet.image.ImageGrid(tileset_image, 2, 2)
tileset = pyglet.image.TextureGrid(tileset_grid)

camera_x = 0
camera_y = 0

map_width = 0
map_height = 0
level_map = []

# Window size should always be a multiplier of TILE_SIZE
# to avoid half-drawn tiles
print(window.width)
assert window.width % TILE_SIZE == 0
print(window.height)
assert window.height % TILE_SIZE == 0

# Automatically determines map width and height
# works only with rectangular maps, however
with open('sample_map.txt', 'r') as mapfile:
    for line in mapfile:
        map_height += 1

        split_line = line.strip().split(',')
        for sym in split_line:
            level_map.append(int(sym))

        if map_width == 0:
            map_width = len(split_line)
        else:
            assert len(split_line) == map_width


@window.event
def on_key_press(symbol, modifiers):
    global camera_x, camera_y
    if symbol == key.W:
        camera_y += TILE_SIZE
    elif symbol == key.S:
        camera_y -= TILE_SIZE
    elif symbol == key.D:
        camera_x += TILE_SIZE
    elif symbol == key.A:
        camera_x -= TILE_SIZE


@window.event
def on_draw():
    window.clear()
    for row_idx in range(map_height-1, -1, -1):
        # iterate rows in reverse (0-based)
        for col_idx in range(0, map_width):
            # columns are iterated normally
            # this reads the level map from the bottom-left,
            # as is the rendering done in pyglet (0,0 is bottom left)

            x_pos = col_idx*TILE_SIZE - camera_x
            y_pos = (map_height - (row_idx + 1))*TILE_SIZE - camera_y

            tileset[level_map[map_height * row_idx + col_idx] - 1].blit(
                x_pos,
                y_pos
            )

pyglet.app.run()
