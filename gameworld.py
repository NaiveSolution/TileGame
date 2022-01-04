import pygame_menu
import settings
import json
import os

from pygame_menu import events 
from pygame import display
from pygame.sprite import LayeredUpdates, Sprite

from terrain import NormalTerrain, ImpassableTerrain
from tiles import TileBlock
from characters import Player, NonPlayableCharacter
from interactive_window import InteractiveWindow

class GameWorld:
    ''' This class keeps track of the state of the game world which includes the current
    map to display and the game world size, while also storing the pygame sprites 
    of the current map.

    The game world is defined by a n x m grid called world_size which is all the valid
    positions a player can move to. When the player moves out of bounds of the current 
    map that the player is on, a new map is loaded
    '''

    def __init__(self):
        self.screen = display.set_mode((settings.WIDTH, settings.HEIGHT))

        # Initialise the starting map of the player
        self.current_world_row = 2
        self.current_world_column = 2

        self.player = Player(1,1, 'player_Player.png')
    
        # Maintain a list of sprites for characters and background
        # These lists are meant to change with every world map the player is in
        self.list_of_characters = [self.player]
        # TODO: Add self.list_of_decorations and its methods
        self.list_of_map_blocks = list() # map blocks for the current map only
        self.all_sprites = LayeredUpdates() # Maintain a sprite group that the game loop interacts with
        self.read_map_file_and_make_map(self.current_world_row, self.current_world_column)

        # The order of .add()'s arguments is important. The first argument should be the terrain
        # which should be the lowest sprite
        self.all_sprites.add(self.list_of_map_blocks, self.list_of_characters)

        # The game can have a menu/interactive window
        self.interactive_window = None

    def check_valid_world_position(self, x, y) -> bool:
        ''' Checks if the tile at location x,y is within the bounds of the map grid
        '''

        if x > settings.NUMBER_OF_MAPS - 1 or x < 0:
            return False
        if y > settings.NUMBER_OF_MAPS - 1 or y < 0:
            return False
        return True
    
    def make_terrain_sprite(self, row, col, file_name, terrain_type) -> Sprite:
        ''' Creates a terrain sprite at location [row, col] in the current map
        '''

        if terrain_type == 0:
            terrain_sprite = NormalTerrain(row, col, file_name)
        elif terrain_type == 1:
            terrain_sprite = ImpassableTerrain(row, col, file_name)
        else:
            print('Not a terrain_type')
            return
        return terrain_sprite

    def make_other_sprite(self, type, row, col, file_name) -> Sprite:
        ''' Creates a non-terrain sprite at location [row, col] such as a character or decoration and returns it
        '''

        if 'character' in type:
            other_sprite = NonPlayableCharacter(row, col, file_name)
            if 'monster' in file_name:
                other_sprite.is_enemy = True
        if 'decoration' in type:
            pass
        return other_sprite

    def read_map_file_and_make_map(self, world_map_row, world_map_column) -> None:
        ''' Create a map by iterating through the GRID_LAYOUT using make_terrain_sprite()
        save it as a list in the self.world_map position given by map_row, map_col
        '''

        file_path = os.path.join(settings.map_folder, f'map_{world_map_row}_{world_map_column}.json')
        with open(file_path) as f:
            map_data = json.load(f)
            for map_tile in map_data['data']:
                self.list_of_map_blocks.append(
                    self.make_terrain_sprite(
                        row=map_tile['map_row'],
                        col=map_tile['map_col'],
                        file_name=map_tile['filename'],
                        terrain_type=map_tile['terrain_type']))
                if map_tile['character']:
                    self.list_of_characters.append(self.make_other_sprite('character', map_tile['map_row'], map_tile['map_col'], map_tile['character']))
                if map_tile['decoration']:
                    self.list_of_characters.append(self.make_other_sprite('decoration', map_tile['map_row'], map_tile['map_col'], map_tile['decoration']))
                
    def update_current_world_position(self, current_wm_row, current_wm_column, new_wm_row, new_wm_column):
        #TODO
        pass
    
    def update(self, events) -> None:
        self.all_sprites.update()
        self.refresh_surrounding_blocks()
        # Draw / render on screen
        self.screen.fill(settings.WHITE)
        self.all_sprites.draw(self.screen)
        # After drawing everything flip the display
        # if self.interactive_window:
        #     pass
        display.flip()

    def refresh_surrounding_blocks(self) -> None:
        ''' Loads the surrounding blocks into all characters on the map. Each character keeps track of
        what is next to it in each primary direction
        '''

        for character in self.list_of_characters:
            x, y = character.get_grid_coords()
            if x in [0, settings.NUMBER_OF_TILES - 1]:
                # if the character is next to the left edge of the screen
                if x == 0:
                    left = None
                    right = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x+1][y])
                # if the character is next to the right edge of the screen
                if x == settings.NUMBER_OF_TILES - 1:
                    right = None
                    left = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x-1][y])
            else:
                left = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x-1][y])
                right = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x+1][y])
            if y in [0, settings.NUMBER_OF_TILES - 1]:
                # if the character is at the top of the screen
                if y == 0:
                    above = None
                    below = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x][y+1])
                # if the character is at the bottom of the screen
                if y == settings.NUMBER_OF_TILES - 1:
                    below = None
                    above = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x][y-1])
            else:
                above = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x][y-1])
                below = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x][y+1])
            character.get_surrounds(above, below, left, right)

        if self.player.iwindow_on:
            self.interactive_window = InteractiveWindow()
            self.player.iwindow_on = False

    # Currently not used but kept in, just in case
    '''def return_map_dict(self):
        if not self.list_of_map_blocks:
            print('Load a map file first!')
            return
        a = list()
        for i in self.list_of_map_blocks:
            b = {}
            x, y = i.get_grid_coords()
            b['row'] = x
            b['col'] = y
            b['collision'] = i.collision
            b['type'] = i
            a.append(b)
        return a'''