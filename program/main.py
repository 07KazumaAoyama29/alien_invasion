import sys
import pygame

from settings import Settings
from ship import Ship
from enemy import Enemy

class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("エイリアン侵略")

        self.ship = Ship(self)
        self.enemy = Enemy(self)
    
    def run_game(self):
        """ゲームのメインループ"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.clock.tick(60)#1秒間に60回ループが実行されるように"務める"
    
    def _check_events(self):
        """キーボードとマウスのイベントに対応する"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:#右が押されたら
                    self.ship.is_moving_right = True
                elif event.key == pygame.K_LEFT:#左が押されたら
                    self.ship.is_moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:#右が離されたら
                    self.ship.is_moving_right = False
                elif event.key == pygame.K_LEFT:#左が離されたら
                    self.ship.is_moving_left = False
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blit()
        self.enemy.blit()
            
        #最新の画面を表示
        pygame.display.flip()


if __name__ == "__main__":
    AlienInvasion().run_game()