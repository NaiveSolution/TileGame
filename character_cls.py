import tile_cls
import settings
import pygame.key as key
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SEMICOLON

class Character(tile_cls.TileBlock):
    def __init__(self):
        super().__init__()
        self.is_interactable = True
        self.action_tick = 0
        self.is_npc = False
        self.collision = True

    def move(self, x, y):
        if self.is_npc and not self.check_valid_position(x, y):
            print('NPC exited grid, deleting')
            self.destroy()
            return
        
        if not self.check_valid_position(x, y):
            print('Trying to go out of grid!')
            return

        self.grid_position_x = x
        self.grid_position_y = y
        self.rect.center = (settings.GRID_LAYOUT[self.grid_position_x][self.grid_position_y])

class Player(Character):
    # Sprite for the player
    def __init__(self, x, y):
        super().__init__()
        # Get an image from file and scale it to match the tilesize
        self.image, self.rect = self.load_image("character_player.png", -1)
        self.is_npc = False
        self.grid_position_x = x
        self.grid_position_y = y
        if not self.check_valid_position:
            raise Exception(f'Tried to create a tile outside of the grid at: [{self.grid_position_x}][{self.grid_position_y}]')

    def update(self):
        # Count down a move ticker so that the sprite can only move as a fraction of
        # the game FPS, which is every 1.5 seconds, or, settings.FPS + settings.FPS / 2
        if self.action_tick > 0:
            self.action_tick -= 1
        keystate = key.get_pressed()
        if keystate[K_UP]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                # The pixel number increases __downward__ from the top of the screen
                self.move(self.grid_position_x, self.grid_position_y - 1)
        if keystate[K_DOWN]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(self.grid_position_x, self.grid_position_y + 1)
        if keystate[K_LEFT]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(self.grid_position_x - 1, self.grid_position_y)
        if keystate[K_RIGHT]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(self.grid_position_x + 1, self.grid_position_y)
        if keystate[K_SEMICOLON]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(0, 0)
        
        # Add statement to stop from moving off screen
    


class Enemy(Character):
    # Sprite 
    def __init__(self, x, y):
        super().__init__(self)
        self.is_npc = True
        self.grid_position_x = x
        self.grid_position_y = y
        if not self.check_valid_position:
            raise Exception(f'Tried to create a tile outside of the grid at: [{self.grid_position_x}][{self.grid_position_y}]')
