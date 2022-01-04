import pygame as pg
import settings
from characters import Player
from gameworld import GameWorld

def main():

    # Setup the window
    pg.display.set_caption("Tile Game")
    pg.init()
    pg.mixer.init()
    clock = pg.time.Clock()

    running = True

    # Create the controller for displaying maps n shit
    game_world = GameWorld()
    # Main game loop
    while running:
        clock.tick(settings.FPS)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        game_world.update(events)
        pg.display.update()

        
    pg.quit()

if __name__ == "__main__":
    main()