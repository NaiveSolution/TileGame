from generate_map import check_valid_position
import settings
from terrain_cls import NormalTerrain, ImpassableTerrain
from tile_cls import TileBlock
import json
import os

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
        self.current_world_row = 1
        self.current_world_column = 1
        self.current_map_block_list = list()
        self.read_map_file_and_make_map(self.current_world_row, self.current_world_column)

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
                self.current_map_block_list.append(
                    self.make_map_tile_at_location(
                        row=map_tile['map_row'],
                        col=map_tile['map_col'],
                        file_name=map_tile['filename'],
                        terrain_type=map_tile['terrain_type']
                    )
                )

    #TODO
    def update_current_world_position(self, current_wm_row, current_wm_column, new_wm_row, new_wm_column):
        if not check_valid_position(new_wm_row, new_wm_column):
            return
        
    def return_current_map(self):
        if not self.current_map_block_list:
            print('Load a map file first!')
            return
        return self.current_map_block_list