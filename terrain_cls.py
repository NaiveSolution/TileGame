import tile_cls
    
class NormalTerrain(tile_cls.TileBlock):
    def __init__(self, x, y, file_name):
        super().__init__()
        self.collision = False
        self.create_at_position(x, y)
        self.load_image(file_name)

class ImpassableTerrain(tile_cls.TileBlock):
    def __init__(self, x, y, file_name):
        super().__init__()
        self.collision = True
        self.create_at_position(x, y)
        self.load_image(file_name)
