class GameStats:
    """跟踪游戏统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings

        # 剩下几条命
        self.ship_left = self.settings.ship_limit
        # 游戏分数
        self.score = 0
        # 等级
        self.level = 1

        # 游戏刚启动时处于活动状态
        self.game_active = True

    def reset_stats(self):
        """重置统计信息"""
        self.ship_left = self.settings.ship_limit
        self.game_active = True
        self.score = 0
        self.level = 1
