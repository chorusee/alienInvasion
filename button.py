import pygame.font


class Button:

    def __init__(self, ai_game, label):
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (128, 255, 255)
        self.text_color = (255, 255, 255)

        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮标签
        self._prep_label(label)

    def _prep_label(self, label):
        """将label渲染成图像，并使其在按钮上居中"""
        self.label_image = self.font.render(label, True, self.text_color, self.button_color)
        self.label_image_rect = self.label_image.get_rect()
        self.label_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.label_image, self.label_image_rect)
