import pygame
import sys
from config import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load('assets/musica.wav')
        pygame.mixer.music.play(-1)
        self.tela = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("O Renascimento do Jorge")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.tela.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
