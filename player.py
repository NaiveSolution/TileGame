import pygame as pg 
import settings
import os

class Enemy(pg.sprite.Sprite):
    # Sprite 
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
    
class Player(pg.sprite.Sprite):
    # Sprite for the player
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # Get an image from file and scale it to match the tilesize
        self.image = pg.image.load(os.path.join(settings.img_folder, "p1_jump.png")).convert()
        self.image = pg.transform.scale(self.image, (settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.set_colorkey(settings.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (settings.WIDTH / 2, settings.HEIGHT / 2)
        self.move_ticker = 0
        
    def update(self):
        # Count down a move ticker so that the sprite can only move as a fraction of
        # the game FPS, which is every 1.5 seconds, or, settings.FPS + settings.FPS / 2
        if self.move_ticker > 0:
            self.move_ticker -= 1
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            if self.move_ticker == 0:
                self.move_ticker += settings.TICKER_TIME
                self.rect.center = (self.rect.centerx, self.rect.centery - settings.TILE_SIZE)
        if keystate[pg.K_DOWN]:
            if self.move_ticker == 0:
                self.move_ticker += settings.TICKER_TIME
                self.rect.center = (self.rect.centerx, self.rect.centery + settings.TILE_SIZE)
        if keystate[pg.K_LEFT]:
            if self.move_ticker == 0:
                self.move_ticker += settings.TICKER_TIME
                self.rect.center = (self.rect.centerx - settings.TILE_SIZE, self.rect.centery)
        if keystate[pg.K_RIGHT]:
            if self.move_ticker == 0:
                self.move_ticker += settings.TICKER_TIME
                self.rect.center = (self.rect.centerx + settings.TILE_SIZE, self.rect.centery)
        # Add statement to stop from moving off screen
    
    def get_xy(self):
        return self.rect.y, self.rect.x
