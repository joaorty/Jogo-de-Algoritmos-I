import pygame
from config import *
from enemy import Enemy
from tile import Tile
from player import Player
from sword import Sword
from ui import UI
import random


class Level:
    def __init__(self):
        self.inimigo = None
        self.player = None
        self.display_surface = pygame.display.get_surface()
        self.count_map = 0

        self.visible_sprites = VisibleGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.map = MAP_ENTITIES
        self.create_map(FIRST_MAP)
        self.randomize_position_enemies()
        self.create_map_entities()

        self.attack = None
        self.tela = None

        self.ui = UI()

    def randomize_position_enemies(self):
        interval = random.randint(MIN_INIMIGOS, MAX_INIMIGOS)
        # self.has_enemies = True
        for count in range(interval):
            i = random.randint(2, 9)  # números escolhidos por conta da parede
            j = random.randint(2, 18)
            if self.map[i][j] == 'J':
                count -= 1
            else:
                self.map[i][j] = 'I'

    def create_map(self, MAP):
        for row_index, row in enumerate(MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'X':
                    Tile('assets/parede.jpg', (x, y), [self.visible_sprites, self.obstacles_sprites], 'parede')
                if col == ' ':
                    Tile('assets/piso.jpg', (x, y), [self.visible_sprites], 'piso')
                if col == 'D':
                    Tile('assets/porta.png', (x, y), [self.visible_sprites], 'porta')

    def create_attack(self):
        self.attack = Sword(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_sword(self):
        if self.attack:
            self.attack.kill()
        self.attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player)

    def create_map_entities(self):
        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'J' and self.count_map == 0:
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites, self.create_attack,
                                         self.destroy_sword)
                elif col == 'I':
                    self.inimigo = Enemy((x, y), [self.visible_sprites, self.attackable_sprites],
                                         self.obstacles_sprites, self.damage_player)

    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def change_level(self):
        print(self.check_has_enemies())
        print(self.collision_with_door())
        if not self.check_has_enemies() and self.collision_with_door():
            self.count_map += 1
            for sprite in self.visible_sprites:
                sprite.kill()
            self.create_map(SECOND_MAP_ONWARDS)
            self.randomize_position_enemies()
            self.create_map_entities()
            tmp_health = self.player.health
            self.player.kill()
            self.player = Player((TILESIZE * 1, TILESIZE * 5), [self.visible_sprites], self.obstacles_sprites,
                                 self.create_attack,
                                 self.destroy_sword)
            self.player.health = tmp_health

    def check_has_enemies(self):
        enemy_sprites = [sprite for sprite in self.visible_sprites.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        if not enemy_sprites:
            return False
        else:
            return True

    def collision_with_door(self):
        doors = pygame.sprite.Group()
        for sprite in self.visible_sprites:
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'porta':
                doors.add(sprite)
        if pygame.sprite.spritecollide(self.player, doors, False):
            return True
        else:
            return False

    def restart_game(self):
        for sprite in self.visible_sprites.sprites():
            sprite.kill()
        for sprite in self.obstacles_sprites.sprites():
            sprite.kill()
        for sprite in self.attackable_sprites.sprites():
            sprite.kill()
        for sprite in self.attack_sprites.sprites():
            sprite.kill()
        self.count_map = 0
        self.create_map(FIRST_MAP)
        self.create_map_entities()

    def game_over(self):
        if self.player.health <= 0:
            self.tela = pygame.display.set_mode((WIDTH, HEIGHT))
            FONT = pygame.font.Font(UI_FONT, 72)
            text = FONT.render("GAME OVER", True, (200, 200, 200))
            text_restart = FONT.render("PRESS R TO RESTART", True, (200, 200, 200))
            self.tela.fill((0, 0, 0))
            self.tela.blit(text, (WIDTH // 2 - text.get_width() / 2, HEIGHT // 2 - text.get_height() / 2))
            self.tela.blit(text_restart, (WIDTH // 2 - text.get_width() / 2, HEIGHT // 2 - text.get_height() * 1.5))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.restart_game()

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        self.visible_sprites.update_enemies(self.player)
        self.obstacles_sprites.update()
        self.change_level()
        self.game_over()
        self.player_attack_logic()
        self.ui.display(self.player)


class VisibleGroup(pygame.sprite.Group):
    def __init__(self):
        super(VisibleGroup, self).__init__()

    def update_enemies(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
