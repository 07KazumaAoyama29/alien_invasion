class Settings:
    def __init__(self):
        """ゲームの初期設定"""
        #画面に関する設定
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #playerの設定
        self.ship_speed = 2.5
        self.ship_limit = 3

        #弾の設定
        self.bullet_speed = 20.0
        self.bullet_width = 30
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 300

        #敵の設定
        self.enemy_speed = 1.0
        self.fleet_drop_speed = 90
        self.fleet_direction = 1#右:1, 左:-1