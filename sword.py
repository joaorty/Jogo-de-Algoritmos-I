import pygame


class Sword(pygame.sprite.Sprite):
    def __init__(self, jogador, groups):
        super().__init__(groups)
        direction = jogador.status.split('_')[0]
        # print(direction)

        full_path = 'assets/espada/tile000_' + direction + '.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'direita':
            self.rect = self.image.get_rect(midleft=jogador.rect.midright + pygame.math.Vector2(-35, 0))
        elif direction == 'esquerda':
            self.rect = self.image.get_rect(midright=jogador.rect.midleft + pygame.math.Vector2(35, 0))
        elif direction == 'cima':
            self.rect = self.image.get_rect(midbottom=jogador.rect.midtop + pygame.math.Vector2(0, 10))
        elif direction == 'baixo':
            self.rect = self.image.get_rect(midtop=jogador.rect.midbottom + pygame.math.Vector2(0, -10))
