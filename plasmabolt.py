#Plasmabolt.py

import pygame
from pygame.sprite import Sprite
import random

class Plasmabolt(Sprite):
    """Вражеская стрельба"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.op_plasma_color
        self.aliens = ai_game.aliens

        #создание вражеского снаряда
        self.rect = pygame.Rect(0,0, self.settings.op_plasma_width, self.settings.op_plasma_height)
        
        #AK-47 FOR EVERYONE
        enemies = []
        for alien in self.aliens:
            enemies.append(alien)
            alien = random.choice(enemies)

        self.rect.midbottom = alien.rect.midbottom

        #{Х}ранение снаряда
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает болт сверху вниз"""
        self.y += self.settings.op_plasma_speed
        self.rect.y = self.y

    def draw_plasmabolt(self):
        """Рисует инопланетный кал шо"""
        pygame.draw.rect(self.screen, self.color, self.rect)



