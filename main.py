import pyglet

window = pyglet.window.Window()

tileset_image = pyglet.resource.image('sample_tileset.png')
tileset_grid = pyglet.image.ImageGrid(tileset_image, 2, 2)
tileset = pyglet.image.TextureGrid(tileset_grid)

map_width = 20
map_height = 20
level_map = []
with open('sample_map.txt', 'r') as mapfile:
    for line in mapfile:
        for sym in line.strip().split(','):
            level_map.append(int(sym))

@window.event
def on_draw():
    window.clear()
    for row_idx in range(map_height-1, -1, -1):
        # iterate rows in reverse (0-based)
        for col_idx in range(0, map_width):
            # columns are iterated normally
            # this reads the level map from the bottom-left,
            # as is the rendering done in pyglet (0,0 is bottom left)
            tileset[level_map[map_height * row_idx + col_idx] - 1].blit(col_idx*32, (map_height - (row_idx + 1))*32)

pyglet.app.run()
