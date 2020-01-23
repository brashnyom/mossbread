class BaseEntity:
    """
    Serves as a template for entities in the world.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.tile_num = None


class PlayerEntity(BaseEntity):
    def __init__(self):
        super(PlayerEntity, self).__init__()
        self.tile_num = 5
