import settings
import json
import pygame as pg
import os
import sys
import json
from terrain_cls import NormalTerrain, ImpassableTerrain
# from consolemenu import *
# from consolemenu.items import *

current_world_map_row = 0
current_world_map_column = 0
terrain_block_file = None
current_terrain_type = 0
block_list = list()
'''
    This script creates an empty world json file.
    It can be filled with your own data to make your own map. 
    It can also be used to view your creation in pygame
    The text file will be read by a GameWorld object in main.

    For example, given world size n = 3 and map size m = 2, the script will write this:
    (where n = settings.NUMBER_OF_MAPS and m = settings.NUMBER_OF_TILES)
    {
        'map_data': [
            {
                'world_row' : 0,
                'world_col' : 0,
                'data' :[
                    {
                        'map_row' : 0,
                        'map_col' : 0,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 0,
                        'map_col' : 1,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 1,
                        'map_col' : 0,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 1,
                        'map_col' : 1,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                ]
            },
            {
                'world_row' : 0,
                'world_col' : 1,
                'data' :[
                    {
                        'map_row' : 0,
                        'map_col' : 0,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 0,
                        'map_col' : 1,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 1,
                        'map_col' : 0,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 1,
                        'map_col' : 1,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                ]
            },
            .
            .
            .
            {
                'world_row' : n,
                'world_col' : n,
                'data' :[
                    {
                        'map_row' : 0,
                        'map_col' : 0,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 0,
                        'map_col' : 1,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 1,
                        'map_col' : 0,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                    {
                        'map_row' : 1,
                        'map_col' : 1,
                        'filename': 'blank.png'
                        'terrain_type' : 0
                    },
                ]
            }
    }
'''

def check_valid_position(x, y, grid_size):
    # Checks if the tile is within the bounds of the map grid
    if x > grid_size - 1 or x < 0:
        return False
    if y > grid_size - 1 or y < 0:
        return False
    return True

def set_row_col(grid_size):
    row = input("Enter Row: ")
    col = input("Enter Column: ")
    while row.isalpha() or int(row) < 0 or int(row) > grid_size - 1:
        row = input('Invalid row. Please enter a valid row number:')
    while col.isalpha() or int(col) < 0 or int(col) > grid_size - 1:
        col = input('Invalid column. Please enter a valid column number:')
    return int(row), int(col)

def make_map_tile_at_location(row, col, file_name, terrain_type):
    if terrain_type == 0:
        terrain_block = NormalTerrain(row, col, file_name)
    elif terrain_type == 1:
        terrain_block = ImpassableTerrain(row, col, file_name)
    else:
        print('Not a terrain_type')
        return
    return terrain_block

def display_current_map(data):
    global block_list
    global terrain_block_file
    global current_terrain_type
    x, y = None, None
    pg.display.set_caption(f"Map position: [{current_world_map_row}][{current_world_map_column}]")
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))

    for d in data:
        terrain_block = make_map_tile_at_location(d['map_row'], d['map_col'], d['filename'], d['terrain_type'])
        block_list.append(terrain_block)
    background = pg.sprite.Group()
    background.add(block_list)
    

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for sprite in background:
                    if sprite.rect.collidepoint(pos):
                        x, y = sprite.get_grid_coords()
                        running = False
        background.update()
        screen.fill(settings.WHITE)
        background.draw(screen)
        pg.display.flip()
    pg.quit()
    return x, y

def choose_terrain_block_file():
    global terrain_block_file
    print('\nCurrent terrain block file: ', terrain_block_file)
    file_dict = {}
    n = 0
    # Create a dict of all the files in terrain/ to use in the main loop
    for file in sorted(os.listdir(settings.img_folder)):
        file_dict.update({n : file})
        n += 1
    for k,v in file_dict.items():
        print(f'[{k}] {v}')
    selection = input("Make your selection, or 'x' to go back: ")
    # Dont mess up your selection, I cbf validating input atm
    if selection == 'x' or selection == 'X':
        return
    terrain_block_file = file_dict[int(selection)]

def get_selection(map_row, map_col):
    print('---- Move Commands ----')
    print('[w] Move up\t\t[W] Move up and set block')
    print('[s] Move down\t\t[S] Move down and set block')
    print('[a] Move left\t\t[A] Move left and set block')
    print('[d] Move right\t\t[D] Move right and set block')
    print('[5] Move to position')
    print('\n---- Set block attributes ----')
    print('[6] Set terrain .png file')
    print('[7] Set as normal terrain')
    print('[8] Set as impassable terrain')
    print('[9] Write current block values')
    print('\n---- General commands ----')
    print('[I/i] Inspect current map block')
    print('[C/c] Display current world map in pygame')
    print('[P/p] Save')
    print('[B/b] Save and exit')
    print('[X/x] Quit')

    print(f'Current map position: [{map_row}][{map_col}]\n')
    selection = input('Command: ')
    return selection

# This function writes the chosen map grid and fills them with blank.png's 
def create_empty_map(world_row, world_col):
    d = {}
    d['world_row'] = world_row
    d['world_col'] = world_col
    d['data'] = []
    for i in range(0, settings.NUMBER_OF_TILES):
        for j in range(0, settings.NUMBER_OF_TILES):
            map_data = {
                'map_row' : i,
                'map_col' : j,
                'filename' : 'blank.png',
                'terrain_type' : 0
            }
            d['data'].append(map_data)
    return d

# The script keeps track of a dict that contains the map data.
def write_map_block(data):
    global current_terrain_type
    global terrain_block_file

    if terrain_block_file is None:
        print('\nYou must set a .png file first')
        choose_terrain_block_file()
    data['filename'] = terrain_block_file
    data['terrain_type'] = current_terrain_type
    return data

def main():
    print('*************\nThis script is to be run only once to make a single world map!\n*************\n')
    print('Please enter a world map row and column.')
    world_map_row, world_map_column = set_row_col(settings.NUMBER_OF_MAPS)

    # Check if the file already exists. If it does, either open it or save over it
    save_file = f'map_{world_map_row}_{world_map_column}.json'
    if os.path.isfile(os.path.join(settings.map_folder, save_file)):
        overwrite = input(f'{save_file} already exists. Overwrite? [y/n]')
        while overwrite not in ['y', 'Y', 'n', 'N']:
            input(f'Invalid selection. Overwrite? [y/n]')
        if overwrite in ['y', 'Y']:
            world_map_data = create_empty_map(world_map_row, world_map_column)
        else:
            with open(os.path.join(settings.map_folder, save_file)) as f:
                world_map_data = json.load(f)
    else:
        print(f'Generating empty world map data at: [{world_map_row}][{world_map_column}]\n')
        world_map_data = create_empty_map(world_map_row, world_map_column)
    
    map_row, map_col = 0, 0
    index = next((i for i, item in enumerate(world_map_data['data']) if item["map_row"] == map_row and item['map_col'] == map_col), None)

    global current_terrain_type
    selection = None

    while selection != 'X' and selection != 'x':
        selection = get_selection(map_row, map_col)
        # Move commands
        if selection in ['W','w']:
            if check_valid_position(map_row, map_col + 1, settings.NUMBER_OF_TILES):
                map_col += 1
            else:
                print(f'Unable to move up to [{map_row+1}][{map_col}]')
            index = next((i for i, item in enumerate(world_map_data['data']) if item["map_row"] == map_row and item['map_col'] == map_col), None)
            if selection == 'W':
                world_map_data['data'][index] = write_map_block(world_map_data['data'][index])
        if selection in ['S','s']:
            if check_valid_position(map_row, map_col -1, settings.NUMBER_OF_TILES):
                map_col -= 1
            else:
                print(f'Unable to move down to [{map_row-1}][{map_col}]')
            index = next((i for i, item in enumerate(world_map_data['data']) if item["map_row"] == map_row and item['map_col'] == map_col), None)
            if selection == 'S':
                world_map_data['data'][index] = write_map_block(world_map_data['data'][index])
        if selection in ['A','a']:
            if check_valid_position(map_row - 1, map_col, settings.NUMBER_OF_TILES):
                map_row -= 1
            else:
                print(f'Unable to move left to [{map_row}][{map_col - 1}]')
            index = next((i for i, item in enumerate(world_map_data['data']) if item["map_row"] == map_row and item['map_col'] == map_col), None)
            if selection == 'A':
                world_map_data['data'][index] = write_map_block(world_map_data['data'][index])
        if selection in ['D','d']:
            if check_valid_position(map_row + 1, map_col, settings.NUMBER_OF_TILES):
                map_row += 1
            else:
                print(f'Unable to move right to [{map_row}][{map_col + 1}]')
            index = next((i for i, item in enumerate(world_map_data['data']) if item["map_row"] == map_row and item['map_col'] == map_col), None)
            if selection == 'D':
                world_map_data['data'][index] = write_map_block(world_map_data['data'][index])
        if selection == '5':
            map_row, map_col = set_row_col(settings.NUMBER_OF_TILES)

        # Terrain commands
        if selection == '6':
            choose_terrain_block_file()
        if selection == '7':
            current_terrain_type = 0
            print('\nTerrain type is now normal.')
        if selection == '8':
            current_terrain_type = 1
            print('\nTerrain type is now impassable.')
        
        # Write commands
        if selection == '9':
            world_map_data['data'][index] = write_map_block(world_map_data['data'][index])
            
        # Should this exit when the user chooses it? or should it function as a kind of
        # 'save as' function where the file is overwritten with the new data but doesnt
        # exit the editor
        if selection in ['B', 'b']:
            with open(os.path.join(settings.map_folder, f'map_{world_map_row}_{world_map_column}.json'), 'w') as f:
                json_object = json.dumps(world_map_data, indent=4)
                f.write(json_object)
            sys.exit(0)

        # Misc and exit commands
        if selection in ['C', 'c']:
            x, y = display_current_map(world_map_data['data']) 
            if x is not None or y is not None:
                map_row, map_col = x, y
                index = next((i for i, item in enumerate(world_map_data['data']) if item["map_row"] == map_row and item['map_col'] == map_col), None)
        if selection in ['I', 'i']:
            print(world_map_data['data'][index])
        if selection in ['P', 'p']:
            with open(os.path.join(settings.map_folder, save_file), 'w+') as f:
                json.dump(world_map_data, f)
        if selection in ['X', 'x']:
            print('Exiting.')


if __name__ == '__main__':
    main()

'''
    menu = ConsoleMenu()
    set_row_col_menu_item = FunctionItem("Set World Map row and column", set_world_map_row_column)

    build_map_selections = ["Move up", "Move down", "Move left", "Move right"]
    selection_menu = SelectionMenu(build_map_selections)
    build_map_menu_item = SubmenuItem("Build world map", selection_menu, menu)

    menu.append_item(set_row_col_menu_item)
    menu.append_item(build_map_menu_item)

    # menu.append_item(submenu_item)
    menu.show()

'''