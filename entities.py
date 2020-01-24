from rendering import Rendering


class BaseEntity:
    """
    Serves as a template for entities in the world.
    """

    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def update_sprite_pos(self, x: int, y: int):
        self.sprite.x = x * Rendering.TILE_SIZE
        self.sprite.y = y * Rendering.TILE_SIZE
