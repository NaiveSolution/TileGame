import tiles
import settings
import pygame.key as key
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SEMICOLON

class Character(tiles.TileBlock):
    def __init__(self, x, y, file_name):
        super().__init__()
        self.is_interactable = True
        self.action_tick = 0
        self.collision = True
        self.is_npc = True
        self.iwindow_on = False
        self.grid_position_x = x
        self.grid_position_y = y
        self.load_image(file_name, -1)
        self.create_at_position(x, y)
        
        # The following members contain the block types of all surrounding blocks
        # in the 4 principal directions
        self.block_above = None
        self.block_below = None
        self.block_left = None
        self.block_right = None

    def move(self, x, y, surrounding_sprite_list):
        if self.is_npc and not self.check_valid_position(x, y):
            print('NPC exited grid, deleting')
            self.destroy()
            return
        
        if not self.check_valid_position(x, y):
            print('Trying to go out of grid!')
            return

        for sprite in surrounding_sprite_list:
            if surrounding_sprite_list is not None:
                if sprite.collision or sprite.is_npc:
                    # Do stuff only if the character is the player
                    if isinstance(self, Player):
                        if sprite.is_npc:
                            print('open window')
                            self.iwindow_on = True
                            return
                        if sprite.collision:
                            print('blocked')
                            return
                    else:
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

class Player(Character):
    # Sprite for the player
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)
        self.is_npc = False

    def update(self):
        # Count down a move ticker so that the sprite can only move as a fraction of
        # the game FPS, which is every 1.5 seconds, or, settings.FPS + settings.FPS / 2
        # print(f'\t\t\t{self.block_above.__class__}\n{self.block_left.__class__}\t\t{self.block_right.__class__}\n\t\t\t{self.block_below.__class__}')

        if self.action_tick > 0:
            self.action_tick -= 1
        keystate = key.get_pressed()
        if self.action_tick == 0:
            self.action_tick += settings.TICKER_TIME
            if keystate[K_UP]:
                # The pixel number increases DOWNWARD from the top of the screen
                self.move(self.grid_position_x, self.grid_position_y - 1, self.block_above)
            if keystate[K_DOWN]:
                self.move(self.grid_position_x, self.grid_position_y + 1, self.block_below)
            if keystate[K_LEFT]:
                self.move(self.grid_position_x - 1, self.grid_position_y, self.block_left)
            if keystate[K_RIGHT]:
                self.move(self.grid_position_x + 1, self.grid_position_y, self.block_right)
            if keystate[K_SEMICOLON]:
                self.move(0, 0, None)
        # x, y = self.get_grid_coords()

class NonPlayableCharacter(Character):
    # Sprite 
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)
        self.is_enemy = False
        