import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from enemy import Enemy

class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        #フルスクリーン表示
        """
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """
        pygame.display.set_caption("エイリアン侵略")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.enemy = Enemy(self)
    
    def run_game(self):
        """ゲームのメインループ"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)#1秒間に60回ループが実行されるように"務める"
    
    def _update_bullets(self):
        """弾の位置を更新し、古い弾を廃棄する"""
        self.bullets.update()

        #見えなくなった弾を廃棄する
        for bullet in self.bullets.copy():#forループ中にリストを更新すべきではない
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
    
    def _check_events(self):
        """キーボードとマウスのイベントに対応する"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """キーを押すイベントに対応する"""
        if event.key == pygame.K_RIGHT:#右が押されたら
            self.ship.is_moving_right = True
        elif event.key == pygame.K_LEFT:#左が押されたら
            self.ship.is_moving_left = True
        elif event.key == pygame.K_q:#Qが押されたらゲーム終了
            sys.exit()
        elif event.key == pygame.K_SPACE:#スペースキーが押されたら弾発射
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """キーを離すイベントに対応する"""
        if event.key == pygame.K_RIGHT:#右が離されたら
            self.ship.is_moving_right = False
        elif event.key == pygame.K_LEFT:#左が離されたら
            self.ship.is_moving_left = False
    
    def _fire_bullet(self):
        """新しい弾を生成し、bulletsグループに追加する"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blit()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.enemy.blit()
            
        #最新の画面を表示
        pygame.display.flip()


if __name__ == "__main__":
    AlienInvasion().run_game()