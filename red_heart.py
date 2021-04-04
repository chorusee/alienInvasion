import pygame
from pygame.sprite import Sprite


class RedHeart(Sprite):
    """生命值"""

    def __init__(self):
        """初始化"""
        super().__init__()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/red_heart.bmp')
        self.rect = self.image.get_rect()
