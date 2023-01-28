#game_stats.py
from settings import Settings

class GameStats():
    """Статистика для Alien Invasion"""
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()

        #Запуск в неактивном состоянии
        self.game_active = False

        #Рекорд
        filename = 'score.txt'
        with open(filename) as file_object:
            score = file_object.read()
            self.high_score = int(score)

    def reset_stats(self):
        """Статистика по ходу раунда"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
