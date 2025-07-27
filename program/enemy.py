import pygame

class Enemy:
    """敵(enemy)を管理するクラス"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #敵の画像を読み込み、サイズを取得
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #宇宙船を画面下部の中央に配置
        self.rect.center = self.screen_rect.center
    
    def blit(self):
        """宇宙船を現在位置に描画する"""
        self.screen.blit(self.image, self.rect)