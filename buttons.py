import pygame as pg
import settings

# ---- BUTTON CLASS ONLY CONSTANTS ---- #
LARGE_BUTTON = (100, 50)
SMALL_BUTTON = (75, 30)
# ------------------------------------- #

class Button():
    '''copy-pasted from https://github.com/furas/python-examples/blob/master/pygame/button-hover/example-1.py
    '''

    def __init__(self, text, x=0, y=0, width=100, height=50, command=None):

        self.text = text
        self.command = command
        
        self.image_normal = pg.Surface((width, height))
        self.image_normal.fill(settings.GREEN)

        self.image_hovered = pg.Surface((width, height))
        self.image_hovered.fill(settings.RED)

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pg.font.Font('freesansbold.ttf', 15)
        
        text_image = font.render(text, True, settings.WHITE)
        text_rect = text_image.get_rect(center = self.rect.center)
        
        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)

        self.hovered = False

    def update(self):

        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal
        
    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if event.type == pg.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.hovered:
                print('Clicked:', self.text)
                if self.command:
                    self.command()
                