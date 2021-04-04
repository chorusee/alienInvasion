import pygame.font
from pygame.sprite import Group

from red_heart import RedHeart


def read_high_scores():
    """从文件读取最高分"""
    with open('res/high_scores.txt') as f:
        scores = []
        for line in f:
            scores.append(int(line.strip()))
    return scores


def save_high_scores(scores):
    """保存最高分"""
    with open('res/high_scores.txt', 'w') as f:
        for score in scores:
            f.write(str(score) + '\n')


class Scoreboard:
    """计分板"""

    def __init__(self, ai_game):
        """初始化显示的得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.game_stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图形
        self.prep_score()
        self.prep_level()

        self.prep_red_heart()

        # 前三高的分
        self.high_scores = read_high_scores()

    def prep_score(self):
        """将得分转换成一副渲染的图像"""
        # 舍入得分到10的整数倍
        score_str = '{:,}'.format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 50
        self.score_rect.top = 50

    def prep_level(self):
        """将等级转换成一副渲染的图像"""
        level_str = 'Lv.' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.red_hearts.draw(self.screen)

    def check_high_score(self):
        """检查是否产生了最高分"""
        self.high_scores.append(self.stats.score)
        self.high_scores.sort(reverse=True)
        if len(self.high_scores) > 3:
            save_high_scores(self.high_scores[:3])
        else:
            save_high_scores(self.high_scores)

    def prep_red_heart(self):
        """显示余下还剩多少生命值"""
        self.red_hearts = Group()
        for heart_number in range(self.stats.ship_left):
            red_heart = RedHeart()
            red_heart.rect.x = 50 + heart_number * ( 10 + red_heart.rect.width)
            red_heart.rect.y = 50
            self.red_hearts.add(red_heart)
