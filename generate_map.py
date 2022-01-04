from pygame import key, K_w, K_a, K_s, K_d
import settings
import json
import pygame as pg
import os

from terrain import NormalTerrain, ImpassableTerrain
from characters import Player, NonPlayableCharacter
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import threading
import time
from functools import partial

'''
    This script creates an empty world map json file.
    It can be filled with your own data to make your own map. 
    It can also be used to view your creation in pygame
    The text file will be read by a GameWorld object in main.

    For example, given world size n = 3 and map size m = 2, the script will write this:
    (where n = settings.NUMBER_OF_MAPS and m = settings.NUMBER_OF_TILES)

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
        }]
'''

class MapMaker:
    def __init__(self) -> None:
        # tkinter options
        self.window_height = 600
        self.window_width = 600
        self.window_margin = 50
        self.refresh = True # used to check if anything has been changed in the map. When false, dont refresh sprites in pygame

        # Setting the initial position of the map cursor
        self.row, self.column = 0, 0
        
        # Setting the current map location in the world
        self.world_row, self.world_column = 0, 0

        # Initialising as an empty map
        self.world_map_data = {}
        self.terrain_sprite_list = list()
        self.other_sprite_list = list()
        self.create_empty_map()

        # Setting the initial block attributes
        self.actionable = False
        self.terrain_file = 'terrain_grass_no-edge.png'
        self.terrain_type = 0
        self.character_file = ''
        self.decoration_file = ''

    def toggle_terrain_type(self):
        if self.terrain_type == 0:
            self.terrain_type = 1
            type = '<Impassable>'
        elif self.terrain_type == 1:
            self.terrain_type = 0
            type = '<Normal>'
        print(f'Set terrain type to {type}')

    def get_index(self, map_row, map_col) -> int:
        ''' The index is the position of the self.row and self.column block in the self.world_map_data['data'] list
            It should be set everytime the map cursor row and column are changed
        '''
        return next((i for i, item in enumerate(self.world_map_data['data']) if item["map_row"] == map_row and item['map_col'] == map_col), None)

    def check_valid_position(self, x, y, grid_size) -> bool:
        '''Checks if the tile is within the bounds of the map grid
        '''
        if x > grid_size - 1 or x < 0:
            return False
        if y > grid_size - 1 or y < 0:
            return False
        return True

    def make_terrain_sprite(self, row, col, file_name, action, terrain_type) -> None:
        if terrain_type == 0:
            terrain_sprite = NormalTerrain(row, col, file_name)
            terrain_sprite.is_interactable = action
        elif terrain_type == 1:
            terrain_sprite = ImpassableTerrain(row, col, file_name)
            terrain_sprite.is_interactable = action
        else:
            print('Not a terrain_type')
            return
        self.terrain_sprite_list.append(terrain_sprite)

    def make_other_sprite(self, type, row, col, file_name) -> None:
        if 'character' in type:
            sprite = NonPlayableCharacter(row, col, file_name)
            if 'monster' in file_name:
                sprite.is_enemy = True
        if 'decoration' in type:
            pass
        self.other_sprite_list.append(sprite)

    def set_sprite_list(self) -> None:
        ''' This function empties the sprite lists, and then takes 'data' from world_map_data 
            and populates the sprite lists for each map row and column
        '''
        self.terrain_sprite_list.clear()
        self.other_sprite_list.clear()

        for d in self.world_map_data['data']:
            self.make_terrain_sprite(d['map_row'], d['map_col'], d['filename'], d['action'], d['terrain_type'])
            if d['character']:
                self.make_other_sprite('character', d['map_row'], d['map_col'], d['character'])
            if d['decoration']:
                self.make_other_sprite('decoration', d['map_row'], d['map_col'], d['decoration'])
        
        self.refresh = False

    def set_current_block(self, type, x, y) -> None:
        n = self.get_index(x, y)
        if type == 1:
            self.world_map_data['data'][n]['filename'] = self.terrain_file
            self.world_map_data['data'][n]['action'] = self.actionable
            self.world_map_data['data'][n]['terrain_type'] = self.terrain_type
            self.world_map_data['data'][n]['character'] = self.character_file
            self.world_map_data['data'][n]['decoration'] = self.decoration_file
        elif type == 0:
            self.world_map_data['data'][n]['filename'] = 'blank.png'
            self.world_map_data['data'][n]['action'] = False
            self.world_map_data['data'][n]['terrain_type'] = 0
            self.world_map_data['data'][n]['character'] = ''
            self.world_map_data['data'][n]['decoration'] = ''
        self.refresh = True

    def choose_sprite_popup_window(self, type) -> None:
        win = tk.Toplevel()
        win.wm_title(f"Choose {type}")
        
        # Create a dict of all the files in img/ to display
        # A valid file starts with either 'terrain_', 'character_' or 'decoration_'
        file_dict = {}
        for count, file in enumerate(sorted([x for x in os.listdir(settings.img_folder) if type in x])):
            file_dict.update({count : os.path.join(settings.img_folder, file)})
        
        button_identities = []

        # callback function to set the sprite file
        def set_terrain(n):
            bname = (button_identities[n])
            if 'terrain' in type:
                self.terrain_file = file_dict[n]
            if 'character' in type:
                self.character_file = file_dict[n]
            if 'decoration' in type:
                self.decoration_file = file_dict[n]
            print(self.terrain_file)
            print(self.character_file)
            print(self.decoration_file)

        n = 0
        # loop through all the images in img_folder and create a list of buttons,
        # calling set_terrain on the enumeration (n)
        for k,v in file_dict.items():
            img = Image.open(v)
            img = img.resize((32, 32), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            b = ttk.Button(win, text=f"{v.split('/')[-1]}", command=partial(set_terrain, n))
            b.grid(sticky='nesw', row=k, column=0)
            panel = tk.Label(win, image = img)
            panel.image = img
            panel.grid(row=k, column=2)
            img = None
            button_identities.append(b)
            n += 1
    
    def create_empty_map(self) -> None:
        ''' This function writes the chosen map grid and fills them with blank.png's 
        '''
        self.world_map_data['world_row'] = self.world_row
        self.world_map_data['world_col'] = self.world_column
        self.world_map_data['data'] = []
        for i in range(0, settings.NUMBER_OF_TILES):
            for j in range(0, settings.NUMBER_OF_TILES):
                map_data = {
                    'map_row' : i,
                    'map_col' : j,
                    'filename' : 'blank.png',
                    'action': False,
                    'terrain_type' : 0,
                    'character' : '',
                    'decoration' : ''}
                self.world_map_data['data'].append(map_data)
        self.refresh = False

    def open_file(self) -> None:
        filename = filedialog.askopenfilename(parent=root)
        if not filename or not filename.endswith('.json'):
            print('Please choose a map file in .json format.')
            return
        with open(filename) as f:
            file_data = json.load(f)
            try:
                self.world_map_data['world_row'] = file_data['world_row']
                self.world_map_data['world_col'] = file_data['world_col']
                # instead of doing self.world_map_data['data'] = file_data['data'], iterate through
                # k,v pairs so in case I add more keys it just changes the existing ones.
                for count, map_cursor in enumerate(file_data['data']):
                    for key, value in map_cursor.items():
                        self.world_map_data['data'][count][key] = value

            except KeyError:
                print('Not a valid map file!')
                return
        
    def save_file(self) -> None:
        f = filedialog.asksaveasfile(mode='w', defaultextension='.json')
        if f is None:
            return
        f.write(json.dumps(self.world_map_data))
        f.close()

    def move_cursor(self, direction) -> None:
        direction = direction.lower()
        if direction == 'up':
            if self.check_valid_position(self.row, self.column + 1, settings.NUMBER_OF_TILES):
                self.column += 1
            else:
                print(f'Unable to move up to [{self.row+1}][{self.column}]')
                return
        if direction == 'down':
            if self.check_valid_position(self.row, self.column -1, settings.NUMBER_OF_TILES):
                self.column -= 1
            else:
                print(f'Unable to move down to [{self.row-1}][{self.column}]')
                return
        if direction == 'left':
            if self.check_valid_position(self.row - 1, self.column, settings.NUMBER_OF_TILES):
                self.row -= 1
            else:
                print(f'Unable to move left to [{self.row}][{self.column - 1}]')
                return
        if direction == 'right':
            if self.check_valid_position(self.row + 1, self.column, settings.NUMBER_OF_TILES):
                self.row += 1
            else:
                print(f'Unable to move right to [{self.row}][{self.column + 1}]')
                return
        self.set_current_block(1, self.row, self.column)
        print(f'Moved to [{self.row}][{self.column}] and set')

    # # Dunno where this is used for anymore
    # def set_row_col(self, grid_size) -> None:
    #     row = input("Enter Row: ")
    #     col = input("Enter Column: ")
    #     while row.isalpha() or int(row) < 0 or int(row) > grid_size - 1:
    #         row = input('Invalid row. Please enter a valid row number:')
    #     while col.isalpha() or int(col) < 0 or int(col) > grid_size - 1:
    #         col = input('Invalid column. Please enter a valid column number:')
    #     return int(row), int(col)

map_maker = MapMaker()

root = tk.Tk()
root.title('Map maker')
root.geometry(f'{map_maker.window_height}x{map_maker.window_width}+{map_maker.window_margin}+{map_maker.window_margin}')

def start_pg():
    t = threading.Thread(target=display_current_map)
    t.start()

def display_current_map():
    pg.display.set_caption(f"Map Maker")
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pg.time.Clock()
    map_maker.set_sprite_list()
    
    background = pg.sprite.LayeredUpdates()
    background.add(map_maker.terrain_sprite_list, map_maker.other_sprite_list)
    
    running = True
    action_tick = 1

    while running:
        clock.tick(settings.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for sprite in background:
                    if sprite.rect.collidepoint(pos):
                        x, y = sprite.get_grid_coords()
                        if event.button == 1:
                            print(f'Setting coordinates: [{x}][{y}] and setting block')
                            map_maker.set_current_block(1, x, y)
                            map_maker.row = x
                            map_maker.column = y
                        if event.button == 3:
                            print(f'Setting coordinates: [{x}][{y}] and removing block')
                            map_maker.set_current_block(0, x, y)
                            map_maker.row = x
                            map_maker.column = y
                        break
            
            # Enable WASD while pygame is running
            keystate = key.get_pressed()
            if action_tick > 0:
                action_tick -= 1
            if action_tick == 0:
                action_tick += settings.TICKER_TIME
                if keystate[K_w]:
                    map_maker.move_cursor('up')
                if keystate[K_a]:
                    map_maker.move_cursor('left')
                if keystate[K_s]:
                    map_maker.move_cursor('down')
                if keystate[K_d]:
                    map_maker.move_cursor('right')

        time.sleep(0.1)

        if map_maker.refresh:
            for i in background.sprites():
                del i
            map_maker.set_sprite_list()
            background.add(map_maker.terrain_sprite_list, map_maker.other_sprite_list)
            background.update()
        screen.fill(settings.WHITE)
        background.draw(screen)
        pg.display.flip()
    pg.quit()

def make_buttons():
    toggle_terrain_button = ttk.Button(root, text="Toggle Terrain Type", command=map_maker.toggle_terrain_type)
    toggle_terrain_button.grid(column=1, row=1, sticky='nesw', padx=5, pady=5)
    
    choose_terrain_button = ttk.Button(root, text="Choose Terrain Sprite", command=lambda: map_maker.choose_sprite_popup_window('terrain'))
    choose_terrain_button.grid(column=1, row=2, sticky='nesw', padx=5, pady=5)

    display_map_button = ttk.Button(root, text="Display map", command=start_pg)
    display_map_button.grid(column=1, row=3, sticky='nesw', padx=5, pady=5)

    choose_character_button = ttk.Button(root, text="Choose Character Sprite", command=lambda: map_maker.choose_sprite_popup_window('character'))
    choose_character_button.grid(column=1, row=4, sticky='nesw', padx=5, pady=5)

    choose_decoration_button = ttk.Button(root, text="Choose Decoration Sprite", command=lambda: map_maker.choose_sprite_popup_window('decoration'))
    choose_decoration_button.grid(column=1, row=5, sticky='nesw', padx=5, pady=5)

    # Testing only
    move_up = ttk.Button(root, text="W", command=lambda: map_maker.move_cursor('up'))
    move_up.grid(column=3, row=1, sticky='nesw', padx=5, pady=5)
    move_down = ttk.Button(root, text="S", command=lambda: map_maker.move_cursor('down'))
    move_down.grid(column=3, row=2, sticky='nesw', padx=5, pady=5)
    move_left = ttk.Button(root, text="A", command=lambda: map_maker.move_cursor('left'))
    move_left.grid(column=2, row=2, sticky='nesw', padx=5, pady=5)
    move_right = ttk.Button(root, text="D", command=lambda: map_maker.move_cursor('right'))
    move_right.grid(column=4, row=2, sticky='nesw', padx=5, pady=5)

def main():
    # run tkinter
    make_buttons()
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=map_maker.open_file)
    filemenu.add_separator()
    filemenu.add_command(label="Save as", command=map_maker.save_file)
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()