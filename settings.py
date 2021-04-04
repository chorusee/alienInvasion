class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 初始三条命
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 5

        # 外星人设置
        self.fleet_drop_speed = 100

        # 加快游戏速度的节奏
        self.speedup_scale = 1.5
        # 分数提高速度
        self.score_scale = 1.8

        # 动态设置
        # 飞船速度
        self.ship_speed = 1.5
        # 子弹速度
        self.bullet_speed = 1
        # 外星人速度
        self.alien_speed = 0.5
        # 外星人移动方向，fleet_direction为1表示右移，-1表示左移
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50


    def init_dynamic_settings(self):
        """初始化动态设置"""
        # 动态设置
        # 飞船速度
        self.ship_speed = 1.5
        # 子弹速度
        self.bullet_speed = 1
        # 外星人速度
        self.alien_speed = 0.5
        # 外星人移动方向，fleet_direction为1表示右移，-1表示左移
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points *= self.score_scale
