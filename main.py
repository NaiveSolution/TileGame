import pygame as pg
import settings
from player import Player

def main():

    # Setup the window
    pg.display.set_caption("Tile Game")
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pg.time.Clock()

    running = True

    # Create the sprites
    player = Player()
    all_sprites = pg.sprite.Group()
    all_sprites.add(player)

    # Main game loop
    while running:
        clock.tick(settings.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    
        # Update game state
        all_sprites.update()
        
        # Draw / render on screen
        screen.fill(settings.BLUE)
        all_sprites.draw(screen)

        # After drawing everything flip the display
        pg.display.flip()
        x, y = player.get_xy()
        print('y = ', y, 'x = ', x)
        

    pg.quit()
# Game loop
if __name__ == "__main__":
    main()