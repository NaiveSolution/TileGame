import pygame as pg 
import settings
import os

class TileBlock(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.is_interactable = False
        self.collision = False
        self.is_npc = False
        self.image = None
        self.rect = None
        self.grid_position_x = None
        self.grid_position_y = None

    def load_image(self, file_name, colorkey=None):
        self.image = pg.image.load(os.path.join(settings.img_folder, file_name)).convert()
        self.image = pg.transform.scale(self.image, (settings.TILE_SIZE, settings.TILE_SIZE))
        if colorkey is not None:
            if colorkey == -1:
                colorkey = self.image.get_at((0, 0))
            self.image.set_colorkey(colorkey, pg.RLEACCEL)
        self.rect = self.image.get_rect()
        return self.image, self.rect

    def check_valid_position(self, x, y):
        # Checks if the tile is within the bounds of the map grid
        if x > settings.NUMBER_OF_TILES - 1 or x < 0:
            return False
        if y > settings.NUMBER_OF_TILES - 1 or y < 0:
            return False
        return True
        
    def create_at_position(self, x, y):
        if not self.check_valid_position(x, y):
            raise Exception(f'Cannot make a Tileblock sprite at: [{x}][{y}]')
        self.grid_position_x = x
        self.grid_position_y = y
        self.rect.center = (settings.GRID_LAYOUT[self.grid_position_x][self.grid_position_y])
        
    def get_grid_coords(self):
        # Debugging purposes
        # print(f'Position ({self.__class__.__name__}): [{self.grid_position_x}][{self.grid_position_y}]')
        # print(f'Pixel : [{self.rect.centerx}][{self.rect.centery}]')
        return self.grid_position_x, self.grid_position_y

    def load_sound(self, file_name):
        pass

    def update(self):
        pass

    def destroy(self):
        pass