import settings
from terrain_cls import NormalTerrain, ImpassableTerrain
from tile_cls import TileBlock
import json
import os
from character_cls import Player
from pygame.sprite import LayeredUpdates

class GameWorld:
    ''' This class keeps track of the state of the game world which includes the current
    map to display and the game world size, while also storing the pygame sprites 
    of the current map.

    The game world is defined by a n x m grid called world_size which is all the valid
    positions a player can move to. When the player moves out of bounds of the current 
    map that the player is on, a new map is loaded
    '''

    def __init__(self):
        # Initialise the starting position of the player at (1, 1)
        self.current_world_row = 2
        self.current_world_column = 2

        self.player = Player(5,5)

        # Maintain a list of sprites for characters and background
        # These lists are meant to change with every world map the player is in
        self.list_of_characters = [self.player]
        self.list_of_map_blocks = list() # map blocks for the current map only

        # Maintain a sprite group that the game loop interacts with
        self.all_sprites = LayeredUpdates()
        self.read_map_file_and_make_map(self.current_world_row, self.current_world_column)
        self.all_sprites.add(self.list_of_characters, self.list_of_map_blocks)
        self.all_sprites.move_to_front(self.player)


    def check_valid_world_position(self, x, y):
        # Checks if the tile is within the bounds of the map grid
        if x > settings.NUMBER_OF_MAPS - 1 or x < 0:
            return False
        if y > settings.NUMBER_OF_MAPS - 1 or y < 0:
            return False
        return True
    
    def make_map_tile_at_location(self, row, col, file_name, terrain_type):
        if terrain_type == 0:
            terrain_block = NormalTerrain(row, col, file_name)
        elif terrain_type == 1:
            terrain_block = ImpassableTerrain(row, col, file_name)
        else:
            print('Not a terrain_type')
            return
        return terrain_block

    def read_map_file_and_make_map(self, world_map_row, world_map_column):
        # create a map by iterating through the GRID_LAYOUT using make_map_tile_at_location()
        # save it as a list in the self.world_map position given by map_row, map_col
        file_path = os.path.join(settings.map_folder, f'map_{world_map_row}_{world_map_column}.json')
        with open(file_path) as f:
            map_data = json.load(f)
            for map_tile in map_data['data']:
                self.list_of_map_blocks.append(
                    self.make_map_tile_at_location(
                        row=map_tile['map_row'],
                        col=map_tile['map_col'],
                        file_name=map_tile['filename'],
                        terrain_type=map_tile['terrain_type']
                    )
                )

    def update_current_world_position(self, current_wm_row, current_wm_column, new_wm_row, new_wm_column):
        #TODO
        pass
    
    def update_surrounds(self):
        # loads the surrounding blocks into all characters on the map
        for character in self.list_of_characters:
            x, y = character.get_grid_coords()
            above = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x][y-1])[0]
            below = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x][y+1])[0]
            left = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x-1][y])[0]
            right = self.all_sprites.get_sprites_at(settings.GRID_LAYOUT[x+1][y])[0]

            character.get_surrounds(above, below, left, right)

    def add_character(self, character):
        self.list_of_characters.append(character)
        
    def return_map_dict(self):
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
        return a