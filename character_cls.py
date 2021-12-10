import tile_cls
import settings
import pygame.key as key
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SEMICOLON

class Character(tile_cls.TileBlock):
    def __init__(self):
        super().__init__()
        self.is_interactable = True
        self.action_tick = 0
        self.collision = True

        # The following members contain the block types of all surrounding blocks
        # in the 4 principal directions
        self.block_above = None
        self.block_below = None
        self.block_left = None
        self.block_right = None

    def move(self, x, y, surrounding_block):
        if self.is_npc and not self.check_valid_position(x, y):
            print('NPC exited grid, deleting')
            self.destroy()
            return
        
        if not self.check_valid_position(x, y):
            print('Trying to go out of grid!')
            return

        if surrounding_block is not None:
            if surrounding_block.collision or surrounding_block.is_npc:
                print('blocked')
                return

        self.grid_position_x = x
        self.grid_position_y = y
        self.rect.center = (settings.GRID_LAYOUT[self.grid_position_x][self.grid_position_y])

    def get_surrounds(self, sprite_above, sprite_below, sprite_left, sprite_right):
        self.block_above = sprite_above
        self.block_below = sprite_below
        self.block_left = sprite_left
        self.block_right = sprite_right

        print(f'\t\t\t{self.block_above.__class__}\n{self.block_left.__class__}\t\t{self.block_right.__class__}\n\t\t\t{self.block_below.__class__}')

class Player(Character):
    # Sprite for the player
    def __init__(self, x, y):
        super().__init__()
        # Get an image from file and scale it to match the tilesize
        self.image, self.rect = self.load_image("character_player.png", -1)
        self.grid_position_x = x
        self.grid_position_y = y
        if not self.check_valid_position:
            raise Exception(f'Tried to create the player outside of the grid at: [{self.grid_position_x}][{self.grid_position_y}]')
        self.move(self.grid_position_x, self.grid_position_y, None)

    def update(self):
        # Count down a move ticker so that the sprite can only move as a fraction of
        # the game FPS, which is every 1.5 seconds, or, settings.FPS + settings.FPS / 2
        if self.action_tick > 0:
            self.action_tick -= 1
        keystate = key.get_pressed()
        if keystate[K_UP]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                # The pixel number increases DOWNWARD from the top of the screen
                self.move(self.grid_position_x, self.grid_position_y - 1, self.block_above)
        if keystate[K_DOWN]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(self.grid_position_x, self.grid_position_y + 1, self.block_below)
        if keystate[K_LEFT]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(self.grid_position_x - 1, self.grid_position_y, self.block_left)
        if keystate[K_RIGHT]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(self.grid_position_x + 1, self.grid_position_y, self.block_right)
        if keystate[K_SEMICOLON]:
            if self.action_tick == 0:
                self.action_tick += settings.TICKER_TIME
                self.move(0, 0, None)
        
class Enemy(Character):
    # Sprite 
    def __init__(self, x, y):
        super().__init__(self)
        self.is_npc = True
        self.grid_position_x = x
        self.grid_position_y = y
        if not self.check_valid_position:
            raise Exception(f'Tried to create a tile outside of the grid at: [{self.grid_position_x}][{self.grid_position_y}]')
