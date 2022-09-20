import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, asset, pos, groups, sprite_type):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = pygame.image.load(asset).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
