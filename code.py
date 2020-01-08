import os
import pygame
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


FPS = 50
WIDTH = 800
HEIGHT = 800


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                KillerTile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '/':
                Tile('soil', x, y)
            elif level[y][x] == '*':
                Tile('cloud', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in list(mapFile)]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(vertical_borders)
        self.image = pygame.Surface([1, 50])
        self.rect = pygame.Rect(x, y, x, y + 50)

        self.add(vertical_borders)
        self.image = pygame.Surface([1, 50])
        self.rect = pygame.Rect(x + 50, y, x + 50, y + 50)

        self.add(horizontal_borders)
        self.image = pygame.Surface([50, 1])
        self.rect = pygame.Rect(x, y + 50, x + 50, y + 50)


class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('beginning screen.ui', self)
        self.initUI()

    def initUI(self):
        self.play_button.clicked.connect(self.begin)
        self.history_button.clicked.connect(self.story)

    def begin(self):
        print('d')

    def story(self):
        print('h')
        pass


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.width = 800
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.width // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class KillerTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(killer_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.flag = True
        self.clock = pygame.time.Clock()
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)

    def update(self, *args):
        if 273 in args and self.flag and self.rect.x < 3840:
            self.rect.y -= 4
            self.rect.x += 4
            return False

        if pygame.K_RIGHT in args and self.flag and self.rect.x < 3904:
            self.rect.x += tile_width

        if pygame.K_LEFT in args and self.flag and self.rect.x > 0:
            self.rect.x -= tile_width

        if not self.flag:
            self.rect.y += 5

        if pygame.sprite.spritecollideany(self, vertical_borders, horizontal_borders):
            self.flag = True
            return False
        else:
            self.flag = False
            return True


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
killer_tiles_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartScreen()
    ex.show()
    sys.exit(app.exec())

clock = pygame.time.Clock()
camera = Camera()

screen = pygame.display.set_mode((800, 550))
screen.fill(pygame.Color('blue'))

tile_images = {'wall': load_image('grass 2.png'),
               'empty': load_image('sky.png'),
               'soil': load_image('soil.png'),
               'cloud': load_image('cloud.png')}
player_image = load_image('hero.png')

tile_width = tile_height = 64

player, level_x, level_y = generate_level(load_level('map.txt'))

running = True
pygame.display.flip()
pygame.init()

screen.fill(pygame.Color('white'))
all_sprites.draw(screen)
tiles_group.draw(screen)
player_group.draw(screen)
player_group.update()
tiles_group.update()
all_sprites.update()
pygame.display.flip()

a = True

while running:
    while a:
        player_group.draw(screen)
        a = player_group.update()
        clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 273:
                for i in range(32):
                    touch = player.update(273)
                    screen.fill(pygame.Color('white'))
                    player_group.draw(screen)
                    player_group.update()
                    pygame.display.flip()
            else:
                a = player.update(event.key)

    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    tiles_group.update()
    all_sprites.update()
    pygame.display.flip()

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    clock.tick(FPS)
