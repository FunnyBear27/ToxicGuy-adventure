import pygame
import os


WIDTH, HEIGHT = 800, 550


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class StartScreen:
    def __init__(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

                    return
            pygame.display.flip()