import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """一匹の敵(enemy)を管理するクラス"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #敵の画像を読み込み、サイズを取得
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #宇宙船を画面下部の中央に配置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #敵の実際の位置を格納する
        self.x = float(self.rect.x)
    
    def blit(self):
        """宇宙船を現在位置に描画する"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """敵が画面の端に達した場合は True を返す"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """敵を移動する"""
        self.x += self.settings.enemy_speed * self.settings.fleet_direction
        self.rect.x = self.x