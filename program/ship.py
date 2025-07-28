import pygame

class Ship:
    """宇宙船(player)を管理するクラス"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #宇宙船の画像を読み込み、サイズを取得
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        #宇宙船を画面下部の中央に配置
        self.rect.midbottom = self.screen_rect.midbottom

        #playerの水平位置の浮動小数点数を格納する
        self.x = float(self.rect.x)
        
        #左右の移動のフラグ
        self.is_moving_right = False
        self.is_moving_left = False

    def update(self):
        """移動フラグによって宇宙船の位置を更新する"""
        if self.is_moving_right:
            if self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
        if self.is_moving_left:
            if self.rect.left > 0:
                self.x -= self.settings.ship_speed

        #self.xからrectオブジェクトの位置を更新する(rectに保存されるのは整数部分だけだから。)
        self.rect.x = self.x
    
    def blit(self):
        """宇宙船を現在位置に描画する"""
        self.screen.blit(self.image, self.rect)