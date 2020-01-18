import os
import sys
import pygame
from Player import Player
from Camera import Camera
from Startscreen import StartScreen
from ui import StartScreen


FPS = 15
WIDTH = 800
HEIGHT = 550


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)

            elif level[y][x] == '#':
                Killer_Tile('trans_vert', x, y)
                FakeKill('wall', x, y)

            elif level[y][x] == '<':
                Tile('empty', x, y)
                LeftBorder(x - 1, y)

            elif level[y][x] == '>':
                Tile('empty', x, y)
                RightBorder(x + 1, y)

            elif level[y][x] == '-':
                Tile('empty', x, y)
                UpperBorder(x, y - 1)

            elif level[y][x] == '/':
                Tile('soil', x, y)

            elif level[y][x] == '*':
                Tile('cloud', x, y)

            elif level[y][x] == '+':
                Tile('empty', x, y)
                Enemy(x, y)

            elif level[y][x] == ']':
                Finish('finish', x, y)

            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y, player_group, all_sprites,
                                    player_image, tile_height,
                                    tile_width, player_shoot,
                                    go_image, killer_tiles_group,
                                    left_border, right_border, upper_border,
                                    shoot_sprite_group,
                                    shoot, enemy_group,
                                    finish_group)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_screen():
    fonn = pygame.transform.scale(load_image('start_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fonn, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                posit = pygame.mouse.get_pos()
                if posit[0] in range(305, 500) and posit[1] in range(140, 200):
                    return

                elif posit[0] in range(320, 485) and posit[1] in range(390, 440):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()


def finish_screen():
    fonn = pygame.transform.scale(load_image('finish_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fonn, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                posit = pygame.mouse.get_pos()
                if posit[0] in range(140, 615) and posit[1] in range(170, 235):
                    return 'next level'

                elif posit[0] in range(85, 660) and posit[1] in range(305, 375):
                    return 'menu'

                elif posit[0] in range(180, 570) and posit[1] in range(435, 510):
                    return 'restart'
        pygame.display.flip()


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


class FakeKill(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Finish(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            ret = finish_screen()
            print(ret)
            return ret


class UpperBorder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(upper_border, all_sprites)
        self.add(upper_border)
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(tile_width * x,
                                               tile_height * y)


class RightBorder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(right_border, all_sprites)
        self.add(right_border)
        self.image = tile_images['trans']
        self.rect = self.image.get_rect().move(tile_width * x,
                                               tile_height * y + 10)


class LeftBorder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(left_border, all_sprites)
        self.add(left_border)
        self.image = tile_images['trans']
        self.rect = self.image.get_rect().move(tile_width * x + 64,
                                               tile_height * y + 10)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(finish_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Killer_Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(killer_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.flag = True
        self.count = 0
        self.dead_flag = False
        self.clock = pygame.time.Clock()
        super().__init__(enemy_group, all_sprites)
        self.image = enemy
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y - 1)

    def update(self, *args):
        if self.flag:
            self.count += 1
            if not self.dead_flag:
                self.rect.x += 3
                if self.count % 20 < 10:
                    self.image = enemy

                else:
                    self.image = enemy_walk

        elif not self.flag:
            self.count += 1
            if not self.dead_flag:
                self.rect.x -= 3
                if self.count % 20 < 10:
                    self.image = pygame.transform.flip(enemy, 180, 0)
                else:
                    self.image = pygame.transform.flip(enemy_walk, 180, 0)

        if pygame.sprite.spritecollideany(self, right_border):
            self.flag = False

        if pygame.sprite.spritecollideany(self, left_border):
            self.flag = True

        if pygame.sprite.spritecollideany(self, shoot_sprite_group):
            self.image = dead_enemy
            self.dead_flag = True


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
killer_tiles_group = pygame.sprite.Group()
left_border = pygame.sprite.Group()
shoot_sprite_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
right_border = pygame.sprite.Group()
upper_border = pygame.sprite.Group()
flaggy = False

clock = pygame.time.Clock()
camera = Camera()

screen = pygame.display.set_mode((800, 550))
screen.fill(pygame.Color('blue'))

tile_images = {'wall': load_image('ground.png'),
               'empty': load_image('transparent.png'),
               'trans': load_image('trans.png'),
               'soil': load_image('soil.png'),
               'cloud': load_image('cloud.png'),
               'finish': load_image('finish.png'),
               'trans_vert': load_image('trans_vert.png')}
button = load_image('button.png')
player_image = load_image('hero.png')
go_image = load_image('hero_go.png')
player_shoot = load_image('hero_shoot.png')
enemy = load_image('enemy.png')
enemy_walk = load_image('enemy_go.png')
dead_enemy = load_image('enemy_dead.png')
shoot = load_image('shoot_sprite.png')
fon = pygame.transform.scale(load_image('cave.png'), (WIDTH, HEIGHT))

tile_width = tile_height = 64

player, level_x, level_y = generate_level(load_level('map.txt'))
screen.blit(fon, (0, 0))
start_screen()

running = True
run = True
a = 'v'
pygame.display.flip()
pygame.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

while running:
    while a:
        player_group.draw(screen)
        a = player_group.update()
        clock.tick(FPS)

    keys = pygame.key.get_pressed()  # checking pressed keys

    if keys[pygame.K_LEFT]:
        touch = player.update('K_LEFT')
        vx = 'K_LEFT'
        player_group.update('K_LEF')
        player_group.draw(screen)

    if keys[pygame.K_RIGHT]:
        vx = 'K_RIGHT'
        touch = player.update('K_RIGHT')
        player_group.update('K_RIGH')
        player_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(32):
                    screen.blit(fon, (0, 0))
                    touch = player.update(273, vx, i)
                    all_sprites.draw(screen)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    tiles_group.update()
                    pygame.display.flip()
                    camera.update(player)
                    if i > 16 and touch == 'fall':
                        break
                    # обновляем положение всех спрайтов
                    for sprite in all_sprites:
                        camera.apply(sprite)
                    clock.tick()

            if event.key == pygame.K_z:
                touch = player.update('shoot', vx)
                for i in range(32):
                    enemy_group.update()
                    shoot_sprite_group.update(vx)
                    screen.blit(fon, (0, 0))
                    player_group.update('image', vx)
                    all_sprites.draw(screen)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    tiles_group.update()
                    pygame.display.flip()
                    camera.update(player)
                    # обновляем положение всех спрайтов
                    for sprite in all_sprites:
                        camera.apply(sprite)
                    clock.tick()

            if event.key == pygame.K_ESCAPE:
                start_screen()

    screen.blit(fon, (0, 0))
    fin = finish_group.update()
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    tiles_group.update()
    all_sprites.update()
    pygame.display.flip()
    if fin == 'menu':
        start_screen()

    elif fin == 'restart':
        player, level_x, level_y = generate_level(load_level('map.txt'))

    elif fin == 'next level':
        player, level_x, level_y = generate_level(load_level('map2.txt'))

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    clock.tick(FPS)
