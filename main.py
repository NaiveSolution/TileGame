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

    current_map = game_world.return_current_map()

    # Create the sprites
    player = Player(0, 0) # Create a player at some coords
    all_sprites = pg.sprite.LayeredUpdates()
    all_sprites.add(player, current_map)
    all_sprites.move_to_front(player)

    # Main game loop
    while running:
        clock.tick(settings.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        # Update game state
        all_sprites.update()
        
        # Draw / render on screen
        screen.fill(settings.WHITE)
        all_sprites.draw(screen)

        # After drawing everything flip the display
        pg.display.flip()
        x, y = player.get_grid_coords()
        

    pg.quit()
# Game loop
if __name__ == "__main__":
    main()