#scoreboard.py

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """Вывод СТАТЫ"""

    def __init__(self, ai_game):
        """Атрибуты подсчет статы"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Параметры шрифта
        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 48)
        #Исходное изображение
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Перевод счета в картиночку"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #Вывод на правый верхний угол
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение"""
        high_score_str = "High Score " + str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #Рекорд в центре сверху
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx 
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Вывод уровня дабдабдаб"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        #Вывод урвоня под счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def check_high_score(self):
        """Рекорд"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """ВЫВОД СТАТЫ и уровня и оставшегося резерва)"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


    def show_high_score(self):
        """Вывод рекорды(центр)"""
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def prep_ships(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)