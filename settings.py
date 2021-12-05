import os

# Setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# Some game constants
TILE_SIZE = 32 # Must be an integer
NUMBER_OF_TILES = 17 # TODO: set the starting tile center according to an odd or even number
HEIGHT = TILE_SIZE * NUMBER_OF_TILES
WIDTH = TILE_SIZE * NUMBER_OF_TILES

# Tile Map Constants
# Create a square grid of size n x n containing tuples of (x, y) coordinates
GRID_LAYOUT = [[0 for x in range(0, NUMBER_OF_TILES)] for y in range(0, NUMBER_OF_TILES)]
for j in range(0, NUMBER_OF_TILES):
    for i in range(0, NUMBER_OF_TILES):
        GRID_LAYOUT[i][j] = ( (TILE_SIZE / 2) + i * TILE_SIZE, (TILE_SIZE / 2) + j * TILE_SIZE )
if NUMBER_OF_TILES % 2 == 0:
    CENTER = (int(NUMBER_OF_TILES/2), int(NUMBER_OF_TILES/2))
else:
    CENTER = (int(NUMBER_OF_TILES/2) + 1, int(NUMBER_OF_TILES/2) + 1)
print(CENTER)
# Do I need TOP_RIGHT/LEFT and BOTTOM_RIGHT/LEFT ?

# Other game settings
FPS = 20
TICKER_TIME = int(FPS * 0.135) # Used for setting the action_tick as a fraction of the FPS

# Useful colours
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)