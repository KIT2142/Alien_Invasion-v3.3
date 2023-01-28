import sys
import pygame
import math
import shelve
import random
from settings import Settings
from ship import Ship
from bullet import Bullet
from plasmabolt import Plasmabolt
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from os import path

clock = pygame.time.Clock()
FPS = 165

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Экземпляр хранения игровой статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.plasma = pygame.sprite.Group()

        self._create_fleet()

        #Создание кнопки Play
        self.play_button = Button(self, "Play")

        #Stars
        self.stars = pygame.sprite.Group()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            clock.tick(FPS)
            self._check_events() 
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self.update_opposition_fire()
                self._update_aliens()

            self._update_screen()
            #Отслеживание событий инпута
    
    def _check_events(self):
        """Обрабатывает нажатия клавищ и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)             
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Сброс прогресса
            self.settings.initialize_dynamic_settings()
            #Сброс игры
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            #Зачистка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            self.plasma.empty()
            #Окончание резета игры
            self._create_fleet()
            self.ship.center_ship()
            #БАН мышке
            pygame.mouse.set_visible(False)

           
    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            filename = 'score.txt'
            with open(filename, 'w') as file_object:
                file_object.write(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self.plasma.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)


    def _check_keyup_events(self, event):
        """Реагирует на опускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets)< self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def alien_fire(self):
        """Враг тоже стрелять умеет"""
        if len(self.plasma)< self.settings.op_plasma_allowed:
            new_plasma = Plasmabolt(self)
            self.plasma.add(new_plasma)

    def _create_fleet(self):
        """Создание флота противника"""
        #Создание 1 противника
        #Интервал через одного
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (4 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (8 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)   

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_height * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение флота края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает флот и направление движения"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_directions *= - 1

    def _update_bullets(self):
        """Обновлеяет позиции болтов и удаляет старые"""
        # Обновление позиции снарядов
        self.bullets.update()

        #Удаление болтов вышедших за пределы экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)  

        self._check_bullet_allien_collisions()

    def update_opposition_fire(self):
        """То же самое что и _update_bullets тока для алиенов"""
        self.plasma.update()

        for bolt in self.plasma.copy():
            if bolt.rect.top >= self.settings.screen_height:
                self.plasma.remove(bolt)

    def _check_bullet_allien_collisions(self):
        """Обработка попаданий"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        #Добавление очков за сбитие
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score() 
            
        #Создание нового флота
        if not self.aliens:
            self.bullets.empty()
            self.plasma.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте""" 
        self._check_fleet_edges()
        self.aliens.update()
        
        #Проверка колллизий "Противник-Игрок"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Проверка прохода к нижнему краю
        self._check_aliens_bottom()

        #Проверка каллизии "Плазма-Игрок"
        if pygame.sprite.spritecollideany(self.ship, self.plasma):
            self._check_direct_hit()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем (или плазмой)"""
        if self.stats.ships_left > 0: 
            #Уменьшение ships_left и обновление панельки резервов
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Очистка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            self.plasma.empty()

            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            #Пауза
            sleep(5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверка прохода вражеского к флота к нижнемукраю экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                """Аналогично столкновению с кораблем"""
                self._ship_hit()
                break

    def _check_direct_hit(self):
        """Обработка попадания плазмой по кораблю"""
        if self.stats.ships_left > 0:
            #Корабль минус
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Зачистка экрана
            self.aliens.empty()
            self.bullets.empty()
            self.plasma.empty()

            #Пересоздание сценария
            self._create_fleet()
            self.ship.center_ship()

            #Пауза
            sleep(5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _anim_bg(self):
        """Анимированный бэкграунд шо?"""
        #run = True
        #while run:
        for i in range(0, self.settings.tiles):
            self.screen.blit(self.settings.bg, (i * self.settings.bg_width + self.settings.scroll, 0))
 
        self.settings.scroll -=2

        if abs(self.settings.scroll) > self.settings.bg_width:
            self.settings.scroll = 0

        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #run = False
            #pygame.display.update()
        #pygame.quit()

			    
    def _update_screen(self):
        #Установка заданного цвета фона и перерисовка экрана при кажом проходе цикла   
        self.screen.fill(self.settings.bg_color)
        self._anim_bg()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        #Вражеская стрельба
        if self.stats.game_active:
            for bolt in self.plasma.sprites():
                bolt.draw_plasmabolt()
            if random.randrange(0, 56) == 1:
                self.alien_fire()

        #Вывод статистики
        self.sb.show_score()
        self.sb.show_high_score()

        #Отображение кнопки "Play" в случае неактивности игры
        if not self.stats.game_active:
            self.play_button.draw_button()

        #Отображение последнего прорисованного экрана.
        pygame.display.flip()

    
if __name__ == '__main__':
    #Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
