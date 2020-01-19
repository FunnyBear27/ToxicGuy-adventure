import os
import sys
import pygame
from Player import Player
from Camera import Camera

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
                Killer_Tile('wall', x, y)

            elif level[y][x] == '<':
                Tile('empty', x, y)
                LeftBorder(x - 1, y)

            elif level[y][x] == '(':
                LeftKiller(x, y)

            elif level[y][x] == ')':
                RightKiller(x, y)

            elif level[y][x] == '^':
                UpKiller(x, y)

            elif level[y][x] == '>':
                Tile('empty', x, y)
                RightBorder(x + 1, y)

            elif level[y][x] == '-':
                Tile('empty', x, y)
                UpperBorder(x, y - 1)

            elif level[y][x] == '/':
                Tile('soil', x, y)

            elif level[y][x] == '+':
                Tile('empty', x, y)
                Enemy(x, y)

            elif level[y][x] == ']':
                Finish('finish', x, y)

            elif level[y][x] == 'o':
                Rock('rock', x, y)

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
                    return 'again'

                elif posit[0] in range(320, 485) and posit[1] in range(390, 440):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()


def record_check(level, best_score):
    filename = "data/record.txt"
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in list(mapFile)]
        record = (level_map[level].split(';'))[1]
        if best_score < int(record):
            f1 = open("data/record.txt", 'w')
            count = 1
            level += 1
            for elem in level_map:
                if count == level:
                    f1.write(str(level_map[level - 1].split(';')[0]) + ';' + str(best_score))
                    f1.write('\n')
                else:
                    f1.write(elem)
                    f1.write('\n')
                count += 1
    print(best_score, int(record))
    if best_score < int(record):
        return best_score

    else:
        return int(record)


def death_screen():
    fonn = pygame.transform.scale(load_image('death_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fonn, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                posit = pygame.mouse.get_pos()
                if posit[0] in range(85, 660) and posit[1] in range(305, 375):
                    return 'menu'

                elif posit[0] in range(180, 570) and posit[1] in range(435, 510):
                    return 'restart'
        pygame.display.flip()


def finish_screen(record):
    fonn = pygame.transform.scale(load_image('finish_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fonn, (0, 0))
    running = True
    font = pygame.font.Font(None, 56)
    text = font.render(str(record), 1, (255, 255, 255))
    screen.blit(text, (282, 120))

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


class Rock(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites, rock_group)
        self.image = tile_images[tile_type]
        self.dead_flag = False
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + 3)

    def update(self, *args):
        if not pygame.sprite.spritecollideany(self, killer_tiles_group):
            self.rect.y += 5
        if not self.dead_flag:
            self.rect.y += 10

        if pygame.sprite.spritecollideany(self, killer_tiles_group):
            self.image = dust
            self.dead_flag = True

        if self.dead_flag:
            return 'dead'

        if not self.dead_flag:
            return 'alive'


class LeftKiller(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, killer_tiles_group)
        self.image = tile_images['wall']
        self.count = 0
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + 3)

    def update(self, *args):
        self.count += 1
        if self.count % 200 == 1:
            FireballLeft(self.rect.x, self.rect.y)


class FireballLeft(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, fireball_group)
        self.image = pygame.transform.flip(fireball, 180, 0)
        self.rect = self.image.get_rect().move(pos_x,
                                               pos_y + 3)

    def update(self, *args):
        self.rect.x -= 20
        if pygame.sprite.spritecollideany(self, left_border):
            self.kill()


class RightKiller(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, killer_tiles_group)
        self.image = tile_images['wall']
        self.count = 0
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + 3)

    def update(self, *args):
        self.count += 1
        if self.count % 200 == 1:
            FireballRight(self.rect.x, self.rect.y)


class FireballRight(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, fireball_group)
        self.image = fireball
        self.rect = self.image.get_rect().move(pos_x, pos_y + 3)

    def update(self, *args):
        self.rect.x += 10
        if pygame.sprite.spritecollideany(self, right_border):
            self.kill()


class UpKiller(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, killer_tiles_group)
        self.image = tile_images['wall']
        self.count = 0
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + 3)

    def update(self, *args):
        self.count += 1
        if self.count % 200 == 1:
            FireballUp(self.rect.x, self.rect.y)


class FireballUp(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, fireball_group)
        self.image = shoot_vert
        self.rect = self.image.get_rect().move(pos_x, pos_y + 3)

    def update(self, *args):
        self.rect.y -= 10


class Finish(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(finish_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


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
        self.rect = self.image.get_rect().move(tile_width * x - 2,
                                               tile_height * y + 2)


class LeftBorder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(left_border, all_sprites)
        self.add(left_border)
        self.image = tile_images['trans']
        self.rect = self.image.get_rect().move(tile_width * x + 64,
                                               tile_height * y + 2)


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
                                               tile_height * pos_y + 3)


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
        if not pygame.sprite.spritecollideany(self, killer_tiles_group):
            self.rect.y += 5

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

        if pygame.sprite.spritecollideany(self, shoot_sprite_group)\
                or pygame.sprite.spritecollideany(self, rock_group):
            self.image = dead_enemy
            self.dead_flag = True

        if self.dead_flag:
            return 'dead'

        if not self.dead_flag:
            return 'alive'


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
rock_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
flaggy = False

clock = pygame.time.Clock()
camera = Camera()

screen = pygame.display.set_mode((800, 550))
screen.fill(pygame.Color('blue'))

tile_images = {'wall': load_image('ground.png'),
               'empty': load_image('transparent.png'),
               'trans': load_image('trans.png'),
               'soil': load_image('soil.png'),
               'finish': load_image('finish.png'),
               'trans_vert': load_image('trans_vert.png'),
               'rock': load_image('rock.png')}

fireball = load_image('shoot_sprite.png')
dust = load_image('dust.png')
player_image = load_image('hero.png')
go_image = load_image('hero_go.png')
player_shoot = load_image('hero_shoot.png')
enemy = load_image('enemy.png')
enemy_walk = load_image('enemy_go.png')
dead_enemy = load_image('enemy_dead.png')
shoot = load_image('shoot_sprite.png')
shoot_vert = load_image('shoot_sprite_vert.png')
fon = pygame.transform.scale(load_image('cave.png'), (WIDTH, HEIGHT))

tile_width = tile_height = 64

player, level_x, level_y = generate_level(load_level('map.txt'))
screen.blit(fon, (0, 0))
start_screen()

running = True
run = True
fin = 'noth'
touch = 'noth'
level_number = 0
a = 'v'
vx = 'K_RIGHT'

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
                for i in range(80):
                    camera.update(player)
                    # обновляем положение всех спрайтов
                    for sprite in all_sprites:
                        camera.apply(sprite)
                    clock.tick()
                    screen.blit(fon, (0, 0))
                    enemy_group.update()
                    touch = player.update(273, vx, i)
                    all_sprites.draw(screen)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    tiles_group.update()
                    for elem in enemy_group:
                        if pygame.sprite.spritecollideany(elem, player_group):
                            dead = elem.update('check')
                            if dead == 'dead':
                                continue

                            elif dead == 'alive':
                                fin = death_screen()
                    pygame.display.flip()
                    if i > 16 and touch == 'fall':
                        break

            if event.key == pygame.K_z:
                touch = player.update('shoot', vx)
                for i in range(32):
                    # обновляем положение всех спрайтов
                    for sprite in all_sprites:
                        camera.apply(sprite)
                    clock.tick()
                    pygame.display.flip()
                    enemy_group.update()
                    fireball_group.update()
                    shoot_sprite_group.update(vx)
                    screen.blit(fon, (0, 0))
                    player_group.update('image', vx)
                    all_sprites.draw(screen)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    tiles_group.update()
                    for elem in enemy_group:
                        if pygame.sprite.spritecollideany(elem, player_group):
                            dead = elem.update('check')
                            if dead == 'dead':
                                continue

                            elif dead == 'alive':
                                fin = death_screen()
                    camera.update(player)
                for spr in shoot_sprite_group:
                    spr.kill()

            if event.key == pygame.K_ESCAPE:
                start_screen()
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    tiles_group.update()
    all_sprites.update()
    pygame.display.flip()

    if pygame.sprite.spritecollideany(player, fireball_group):
        pygame.mixer.music.load('death.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1)
        fin = death_screen()

    for elem in enemy_group:
        if pygame.sprite.spritecollideany(elem, player_group):
            dead = elem.update('check')
            if dead == 'dead':
                continue

            elif dead == 'alive':
                pygame.mixer.music.load('death.wav')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(1)
                fin = death_screen()

    if pygame.sprite.spritecollideany(player, finish_group):
        if level_number == 0:
            first_time = pygame.time.get_ticks() // 1000
            record = record_check(level_number, first_time)
            first_time = 0
            fin = finish_screen(record)

        elif level_number == 1:
            second_time = pygame.time.get_ticks() // 1000
            record = record_check(level_number, second_time)
            second_time = 0
            fin = finish_screen(record)

        elif level_number == 2:
            third_time = pygame.time.get_ticks() // 1000
            record = record_check(level_number, third_time)
            third_time = 0
            fin = finish_screen(record)

    if fin == 'menu':
        command = start_screen()
        player, level_x, level_y = generate_level(load_level('map.txt'))

    elif fin == 'restart':
        for i in all_sprites:
            i.kill()

        screen = pygame.display.set_mode((800, 550))

        if level_number == 0:
            player, level_x, level_y = generate_level(load_level('map.txt'))

        if level_number == 1:
            player, level_x, level_y = generate_level(load_level('map2.txt'))

        if level_number == 2:
            player, level_x, level_y = generate_level(load_level('map3.txt'))

        elif level_number == 3:
            level_number = 0
            start_screen()
            player, level_x, level_y = generate_level(load_level('map.txt'))
        fin = 'noth'

    elif fin == 'next level':
        level_number += 1
        for i in all_sprites:
            i.kill()
        screen = pygame.display.set_mode((800, 550))

        if level_number == 1:
            player, level_x, level_y = generate_level(load_level('map2.txt'))

        if level_number == 2:
            player, level_x, level_y = generate_level(load_level('map3.txt'))

        elif level_number == 3:
            level_number = 0
            start_screen()
            player, level_x, level_y = generate_level(load_level('map.txt'))
        fin = 'noth'

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    clock.tick(FPS)
