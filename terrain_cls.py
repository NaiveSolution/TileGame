from os import truncate
import tile_cls
    
class NormalTerrain(tile_cls.TileBlock):
    def __init__(self, x, y, file_name):
        super().__init__()
        self.collision = False
        self.is_interactable = True
        self.load_image(file_name)
        self.create_at_position(x, y)
        

class ImpassableTerrain(tile_cls.TileBlock):
    def __init__(self, x, y, file_name):
        super().__init__()
        self.collision = True
        self.load_image(file_name)
        self.create_at_position(x, y)
        
