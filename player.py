import pygame as pg 
import settings

class Player(pg.sprite.Sprite):
    # Sprite for the player
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (settings.WIDTH / 2, settings.HEIGHT / 2)
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > settings.HEIGHT - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > settings.WIDTH:
            self.rect.right = 0
    
    def get_xy(self):
        return self.rect.y, self.rect.x
