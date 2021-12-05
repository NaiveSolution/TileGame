import pygame as pg
import settings
from character_cls import Player
from terrain_cls import NormalTerrain, ImpassableTerrain


def set_map_block(row, col, file_name, terrain_type):
    ''' Create a terrain block for a position on the map grid.
        Use terrain_type = 0 for Terrain() or terrain_type = 1 for ImpassableTerrain().
    '''
    if terrain_type == 0:
        terrain_block = NormalTerrain(row, col, file_name)
    elif terrain_type == 1:
        terrain_block = ImpassableTerrain(row, col, file_name)
    else:
        print('Not a terrain_type')
        return
    return terrain_block

def main():
    flag = True

    # Setup the window
    pg.display.set_caption("Tile Game")
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pg.time.Clock()

    running = True

    # Create the sprites
    player = Player(5, 5) # Create a player at some coords
    all_sprites = pg.sprite.LayeredUpdates()
    all_sprites.add(player)
                

    # Main game loop
    while running:
        clock.tick(settings.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        # For testing of set_map_block
        if flag:
            if player.get_grid_coords()[0] == 6 and player.get_grid_coords()[1] == 6:
                terrain_block_list = set_map_block(0, 0, 'terrain_zigzag.png')
                all_sprites.add(terrain_block_list)

                all_sprites.move_to_front(player)
                flag = False
        # Update game state
        all_sprites.update()
        
        # Draw / render on screen
        screen.fill(settings.BLUE)
        all_sprites.draw(screen)

        # After drawing everything flip the display
        pg.display.flip()
        x, y = player.get_grid_coords()
        

    pg.quit()
# Game loop
if __name__ == "__main__":
    main()