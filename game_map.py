class GameMap(list):

    def __init__(self):
        self.map_width = 0
        self.map_height = 0
        self.map_data = []

    def __getitem__(self, index):
        return self.map_data[index]

    def load_mapfile(self, path):
        self.map_width = 0
        self.map_height = 0
        self.map_data = []

        # Automatically determines map width and height,
        # but works only with rectangular maps
        with open(path, 'r') as mapfile:
            for line in mapfile:
                self.map_height += 1

                split_line = line.strip().split(',')
                for sym in split_line:
                    self.map_data.append(int(sym))

                if self.map_width == 0:
                    self.map_width = len(split_line)
                else:
                    assert len(split_line) == self.map_width
