import sys
import pygame
from random import choices
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # 统计信息，创建计分板
        self.game_stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self, 'Play')
        # 隐藏光标
        pygame.mouse.set_visible(False)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件
            self._check_events()

            # 游戏处于活动状态，就继续游戏
            if self.game_stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            else:
                # 游戏结束
                pass

            # 每次循环时都重绘屏幕
            self._update_screen()

    def _check_events(self):
        """相应按键和鼠标事件"""
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
            elif even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif even.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif even.key == pygame.K_q:
                    sys.exit()
                elif even.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif even.type == pygame.KEYUP:
                if even.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif even.key == pygame.K_LEFT:
                    self.ship.moving_left = False
            elif even.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()

        # 如果游戏处于非活动状态，绘制play按钮
        if not self.game_stats.game_active:
            self.play_button.draw_button()
            # 显示鼠标
            pygame.mouse.set_visible(True)

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入到bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少外星人
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)
        available_space_y = self.settings.screen_height - 5 * alien_height - self.ship.rect.height
        number_aliens_y = available_space_y // (2 * alien_height)

        # 创建外星人
        for row_number in range(number_aliens_y):
            # 隔一行创建一队外星人
            if row_number % 2 == 0:
                selected_number = choices(range(number_aliens_x), k=3)
                for alien_number in selected_number:
                    self._create_alien(row_number, alien_number)

    def _create_alien(self, row_number, alien_number):
        """创建单个外星人，加入到aliens中"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien_x = alien_width + 2 * alien_number * alien_width
        alien_y = alien_height + 2 * row_number * alien_height
        alien.x = alien_x
        alien.rect.x = alien_x
        alien.rect.y = alien_y
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测飞船和外星人的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 外星人突破了防线
        self._check_fleet_break_through()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            alien.check_edges()

    def _check_fleet_break_through(self):
        """检测外星人是否突破防线"""
        for alien in self.aliens.copy():
            if alien.check_break_through():
                self._ship_hit()
                # 消去这个外星人
                self.aliens.remove(alien)

    def _check_bullet_alien_collisions(self):
        """检查子弹和外星人碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.game_stats.score += int(round(self.settings.alien_points * len(aliens)))
            self.scoreboard.prep_score()
        if not self.aliens:
            # 删除现有的所有子弹，并创建新的外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 等级提高
            self.game_stats.level += 1
            self.scoreboard.prep_level()

    def _ship_hit(self):
        """相应飞船被外星人撞到"""

        # 将ship_left减一
        self.game_stats.ship_left -= 1
        self.scoreboard.prep_red_heart()

        if self.game_stats.ship_left <= 0:
            self.game_stats.game_active = False
            # 检查是否诞生了最高分
            self.scoreboard.check_high_score()

        # 暂停
        sleep(0.5)

    def _check_play_button(self, mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_stats.game_active:
            # 重置难度
            self.settings.init_dynamic_settings()
            # 重置统计信息
            self.game_stats.reset_stats()
            self.game_stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_red_heart()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)
