import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

        # 移动方向，-1向左，1向右
        self.direction = 1

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.settings.alien_speed * self.direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘，就改变移动方向，否则随即决定是否改变方向"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            self._change_direction()

    def check_break_through(self):
        """外星人到达了底部返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True
        return False

    def _change_direction(self):
        """改变外星人的方向"""
        self.rect.y += 2 * self.rect.height
        self.direction *= -1
