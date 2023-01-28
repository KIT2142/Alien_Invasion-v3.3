#settings
import pygame
import math

class Settings():
    """Класс для хранения настроек игори алияне инвазион"""
    def __init__(self):
        """Инициализирует настройки игры"""
        #Параметры экрана
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        #Бэкграунд
        self.bg = pygame.image.load('D:/Works/alien_invasion/images/bg1_.png').convert()
        self.bg_width = self.bg.get_width()

        #Значения для бэкграунда
        self.scroll = 0
        self.tiles = math.ceil(self.screen_width/ self.bg_width) + 1

        #Настройки противников 
        self.alien_speed = 1.0
        self.fleet_drop_speed = 8
        #Fleet_directions = 1 обозначает движение вправо, а -1 - влево
        self.fleet_directions = 1

        #Настройки корабля
        self.ship_speed = 2
        self.ship_limit = 3

        #Вражеская плазма
        self.op_plasma_speed = 6
        self.op_plasma_width = 4
        self.op_plasma_height = 18
        self.op_plasma_color = 0, 255, 80
        self.op_plasma_allowed = 10

        #Параметры снаряда
        self.bullet_speed = 4
        self.bullet_width = 2
        self.bullet_height = 11
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 5

        #Темп ускорения
        self.speedup_scale = 1.3
        self.initialize_dynamic_settings()

        #Модифаер увеличения кол-ва очков за сбитие по ходу увеличения сложности игры
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """Настройки меняюещиеся в игре"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 5.0
        self.alien_speed_factor = 2.0
        self.op_plasma_speed_factor = 10

        #Но не очко обычно губит 
        self.alien_points = 5

        #Движение флота влево(-1) и в право (1)
        self.fleet_directions = 1

    def increase_speed(self):
        """Увеличение настроек скорости и стоимости в зависимости от уровня"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.op_plasma_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)

    
        