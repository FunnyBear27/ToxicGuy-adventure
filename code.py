import os
import pygame
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


FPS = 15
WIDTH = 800
HEIGHT = 800


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Border(x, y)
                Killer_Tile('wall', x, y)
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


class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('beginning screen.ui', self)
        self.initUI()

    def initUI(self):
        self.play_button.clicked.connect(self.begin)
        self.history_button.clicked.connect(self.story)

    def begin(self):
        self.close()

    def story(self):
        print('h')
        pass


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(vertical_borders)
        self.image = pygame.Surface([1, 50])
        self.rect = pygame.Rect(x, y, 1, 50)

        self.add(vertical_borders)
        self.image = pygame.Surface([1, 50])
        self.rect = pygame.Rect(x + 50, y, 1, 50)

        self.add(horizontal_borders)
        self.image = pygame.Surface([50, 1])
        self.rect = pygame.Rect(x, y + 50, 50, 1)


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


class Killer_Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(killer_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.flag = True
        self.count = 0
        self.clock = pygame.time.Clock()
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)

    def update(self, *args):
        print(self.flag)
        self.count += 1
        if self.count % 2 == 0:
            self.image = go_image

        if self.count % 2 == 1:
            self.image = player_image

        if 273 in args and 'K_RIGHT' in args:
            if args[2] < 16:
                self.rect.y -= 8
                self.rect.x += 6

            if args[2] > 16 and not self.flag:
                self.rect.y += 8
                self.rect.x += 6

            if args[2] == 31 and self.flag:
                self.rect.y -= 8

        if 273 in args and 'K_LEFT' in args:
            if args[2] < 16:
                print(args)
                self.rect.y -= 8
                self.rect.x -= 6

            if args[2] > 16 and not self.flag:
                print(args)
                self.rect.y += 8
                self.rect.x += 6

            if args[2] == 31 and self.flag:
                self.rect.y -= 8

        elif 273 in args:
            if args[2] < 16:
                self.rect.y -= 8

            if args[2] > 16 and not self.flag:
                self.rect.y += 8

            if args[2] == 31 and self.flag:
                self.rect.y -= 8

        if 'K_RIGHT' in args and self.flag:
            self.rect.x += 10

        if 'K_LEFT' in args and self.flag:
            self.rect.x -= 10
        elif not self.flag:
            self.rect.y += 10

        if pygame.sprite.spritecollideany(self, killer_tiles_group):
            if not pygame.sprite.spritecollideany(self, vertical_borders):
                if not pygame.sprite.spritecollideany(self, horizontal_borders):
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
flaggy = False

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = StartScreen()
#     ex.show()
#     sys.exit(app.exec())

clock = pygame.time.Clock()
camera = Camera()

screen = pygame.display.set_mode((800, 550))
screen.fill(pygame.Color('blue'))

tile_images = {'wall': load_image('grass 2.png'),
               'empty': load_image('transparent.png'),
               'soil': load_image('soil.png'),
               'cloud': load_image('cloud.png')}
player_image = load_image('hero.png')
go_image = load_image('hero_go.png')
fon = pygame.transform.scale(load_image('anim.gif'), (WIDTH, HEIGHT))

tile_width = tile_height = 64

player, level_x, level_y = generate_level(load_level('map.txt'))
screen.blit(fon, (0, 0))

running = True
run = True
a = 'v'
pygame.display.flip()
pygame.init()

while running:
    while a:
        player_group.draw(screen)
        a = player_group.update()
        clock.tick(FPS)

    keys = pygame.key.get_pressed()  # checking pressed keys

    if keys[pygame.K_LEFT]:
        touch = player.update('K_LEFT')
        a = 'K_LEFT'
        player_group.update()
        player_group.draw(screen)

    if keys[pygame.K_RIGHT]:
        a = 'K_RIGHT'
        touch = player.update('K_RIGHT')
        player_group.update()
        player_group.draw(screen)

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    tiles_group.update()
    all_sprites.update()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 273:
                for i in range(32):
                    screen.blit(fon, (0, 0))
                    touch = player.update(273, a, i)
                    all_sprites.draw(screen)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    tiles_group.update()
                    pygame.display.flip()
            else:
                a = player.update(event.key)

    screen.blit(fon, (0, 0))
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
