#background.py

import pygame
import math
from settings import Settings

class Background():
    """Анимированный бэкграунд ШО?"""
    def __init__(self, ai_game):
        super().__init__
        #self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.bg = pygame.image.load('D:/Works/alien_invasion/images/bg1_.png').convert()
        self.bg_width = self.bg.get_width()


    def _anim_bg(self):

        self.scroll = 0
        self.tiles = math.ceil(self.settings.screen_width / self.bg_width) + 1

        for i in range(0, self.tiles):
            self.screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))
 
        self.scroll -=5

        if abs(self.scroll) > self.bg_width:
            self.scroll = 0




