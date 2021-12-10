import pygame as pg
import settings
from character_cls import Player
from gameworld_cls import GameWorld


def main():

    # Setup the window
    pg.display.set_caption("Tile Game")
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pg.time.Clock()

    running = True

    # Create the controller for displaying maps n shit
    game_world = GameWorld()

    # Main game loop
    while running:
        clock.tick(settings.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        # Update game state
        game_world.all_sprites.update()
        
        # Draw / render on screen
        screen.fill(settings.WHITE)
        game_world.all_sprites.draw(screen)

        # After drawing everything flip the display
        pg.display.flip()
        # x, y = game_world.player.get_grid_coords()
        game_world.update_surrounds()
        
    pg.quit()

if __name__ == "__main__":
    main()