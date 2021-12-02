import os

# Setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# Some game constants
TILE_SIZE = 32
NUMBER_OF_TILES = 17 # TODO: set the starting tile center according to an odd or even number
HEIGHT = TILE_SIZE * NUMBER_OF_TILES
WIDTH = TILE_SIZE * NUMBER_OF_TILES
FPS = 20
TICKER_TIME = int(FPS * 0.15)

# Useful colours
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)