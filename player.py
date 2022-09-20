import pygame
from config import *
import os
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_sword):
        super().__init__(groups)
        self.animations = None
        self.image = pygame.image.load('assets/player/baixo_parado/tile000.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.sprite_type = 'player'
        self.animation_speed = 0.40

        self.import_player_assets()
        self.status = 'baixo_parado'

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.sword = SWORD
        self.destroy_sword = destroy_sword

        self.stats = {'health': 100, 'attack': SWORD['damage'], 'speed': 6}
        self.health = self.stats['health']
        self.attack = self.stats['attack']
        self.speed = self.stats['speed']

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        path = 'assets/player/'
        self.animations = {'cima_parado': [], 'cima': [], 'cima_batendo': [],
                           'esquerda_parado': [], 'esquerda': [], 'esquerda_batendo': [],
                           'baixo_parado': [], 'baixo': [], 'baixo_batendo': [],
                           'direita_parado': [], 'direita': [], 'direita_batendo': []
                           }
        for animation in self.animations.keys():
            complete_path = path + animation
            for filename in os.listdir(complete_path):
                if filename.endswith('.png'):
                    self.animations[animation].append(pygame.image.load(complete_path + '/' + filename).convert_alpha())

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_parado' in self.status:
                if '_batendo' in self.status:
                    self.status = self.status.replace('_batendo', '_parado')
                else:
                    self.status = self.status + '_parado'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not '_batendo' in self.status:
                if '_parado' in self.status:
                    self.status = self.status.replace('_parado', '_batendo')
                else:
                    self.status = self.status + '_batendo'
        else:
            if '_batendo' in self.status:
                self.status = self.status.replace('_batendo', '')

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'cima'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'baixo'
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'direita'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'esquerda'
        else:
            self.direction.x = 0

        if keys[pygame.K_z] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_sword()
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def get_player_damage_weapon(self):
        return self.attack

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
