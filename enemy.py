import os

import pygame
from config import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage_player):
        super().__init__(groups)
        self.diretorio = None
        self.animations = None
        self.status = None
        self.sprite_type = 'enemy'
        self.pos = pos
        self.image = pygame.image.load('assets/inimigo/parado-movendo/parado-movendo.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.health = ENEMY['health']
        self.speed = ENEMY['speed']
        self.attack_radius = ENEMY['attack_radius']
        self.notice_radius = ENEMY['notice_radius']
        self.attack_damage = ENEMY['damage']
        self.resistance = ENEMY['resistance']
        self.obstacle_sprites = obstacle_sprites
        self.import_enemy_assets()
        self.animation_speed = 0.20

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 300
        self.vulnerable = True
        self.hit_time = None
        self.invencibility_duration = 300
        self.damage_player = damage_player

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)

        distance = (player_vector - enemy_vector).magnitude()  # a propria subtração de vetores nao faz com que se
        # ache o novo vetor, é preciso transformar em distancia com magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        return distance, direction

    def import_enemy_assets(self):
        path = 'assets/inimigo/'
        self.animations = {'atacando': [], 'parado-movendo': []}
        for animation in self.animations.keys():
            complete_path = path + animation
            for filename in os.listdir(complete_path):
                if filename.endswith('.png'):
                    self.animations[animation].append(pygame.image.load(complete_path + '/' + filename).convert_alpha())

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invencibility_duration:
                self.vulnerable = True

    def animate(self):  # possivelmente pode ser utilizado mais tarde pra realmente animar
        if self.status == 'attack':
            self.diretorio = 'atacando'
        else:
            self.diretorio = 'parado-movendo'
        animation = self.animations[self.diretorio]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def get_damage(self, player):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= player.get_player_damage_weapon()
        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
