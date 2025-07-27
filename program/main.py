import sys
import pygame

from settings import Settings

class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("エイリアン侵略")
    
    def run_game(self):
        """ゲームのメインループ"""
        while True:
            #キーボードとマウスイベントの監視
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            
            self.screen.fill(self.settings.bg_color)
            
            #最新の画面を表示
            pygame.display.flip()
            self.clock.tick(60)#1秒間に60回ループが実行されるように"務める"

if __name__ == "__main__":
    AlienInvasion().run_game()