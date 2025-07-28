import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from game_stats import GameStats

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

        #ゲームの統計情報を格納するインスタンスを生成する
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self._create_fleet()

        self.game_active = True
    
    def run_game(self):
        """ゲームのメインループ"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_enemies()
                self._update_screen()
                self.clock.tick(60)#1秒間に60回ループが実行されるように"務める"

    def _ship_hit(self):
        """敵と宇宙船の衝突に関係する"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1#残りの機数を減らす

            #残った敵と弾を破棄する
            self.bullets.empty()
            self.enemies.empty()

            #新しい艦隊を生成し、宇宙船を中央に配置する
            self._create_fleet()
            self.ship.center_ship()

            #一時停止する
            sleep(0.5)
        else:
            self.game_active = False

    def _create_fleet(self):
        """エイリアンの艦隊を作成する"""
        #1匹のエイリアンを生成し、スペースがなくなるまでエイリアンを追加し続ける
        #各エイリアンの間にはエイリアン一匹分のスペースを空ける
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size

        current_x, current_y = enemy_width, enemy_height
        while current_y < (self.settings.screen_height - 3 * enemy_height):
            while current_x < (self.settings.screen_width - 2 * enemy_width):
                self._create_enemy(current_x, current_y)
                current_x += 2 * enemy_width
            
            #列の最後でX座標をリセットし、Y座標を増加する
            current_x = enemy_width
            current_y += 2 * enemy_height
    
    def _create_enemy(self, x_position, y_position):
        """敵を一匹作成し、列の中に配置する"""
        new_enemy = Enemy(self)
        new_enemy.x = x_position
        new_enemy.rect.x = x_position
        new_enemy.rect.y = y_position
        self.enemies.add(new_enemy)
    
    def _update_bullets(self):
        """弾の位置を更新し、古い弾を廃棄する"""
        self.bullets.update()

        #見えなくなった弾を廃棄する
        for bullet in self.bullets.copy():#forループ中にリストを更新すべきではない
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        #弾が敵に当たったかどうかを調べる
        self._check_bullet_enemy_collisions()
    
    def _check_bullet_enemy_collisions(self):
        """弾と敵の衝突に対応する"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.enemies, True, True
        )#3つ目は、bulletを消すかどうか、4つ目はenemyを消すかどうか

        if not self.enemies:#敵をすべて倒したとき
            self.bullets.empty()#弾すべて削除(次のステージに進む)
            self._create_fleet()#艦隊を再配置

    def _update_enemies(self):
        """艦隊にいる全ての敵の位置を更新する"""
        self._check_fleet_edges()
        self.enemies.update()

        #敵と宇宙船の衝突を検知する
        if pygame.sprite.spritecollideany(self.ship, self.enemies):
            self._ship_hit()

        #画面の一番下に到達した敵を探す
        self._check_emnemies_bottom()
    
    def _check_fleet_edges(self):
        """敵が画面の端に達したときの処理"""
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """艦隊を下に移動し、横移動の方向を変更する"""
        for enemy in self.enemies.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
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

    def _check_emnemies_bottom(self):
        """敵が画面の一番下に到達したかどうかを確認する"""
        for enemy in self.enemies.sprites():
            if enemy.rect.bottom >= self.settings.screen_height:
                #宇宙船を破壊したときと同じように扱う
                self._ship_hit()
                break
    
    def _fire_bullet(self):
        """新しい弾を生成し、bulletsグループに追加する"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blit()
        self.enemies.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        #最新の画面を表示
        pygame.display.flip()


if __name__ == "__main__":
    AlienInvasion().run_game()