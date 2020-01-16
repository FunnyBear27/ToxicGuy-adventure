import pygame
from Shoot import Shoot


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,
                 player_group, all_sprites,
                 player_image, tile_height,
                 tile_width, player_shoot,
                 go_image, killer_tiles_group,
                 vertical_borders,
                 horisontal_borders,
                 shoot_sprite_group, shoot):

        self.horizontal_borders = horisontal_borders
        self.shoot_sprite_group = shoot_sprite_group
        self.all_sprites = all_sprites
        self.shoot = shoot
        self.player_image = player_image
        self.player_shoot = player_shoot
        self.go_image = go_image
        self.killer_tiles_group = killer_tiles_group
        self.vertical_borders = vertical_borders
        self.horisontal_borders = horisontal_borders

        self.flag = True
        self.count = 0
        self.clock = pygame.time.Clock()
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)

    def update(self, *args):
        self.count += 1
        if 'shoot' in args:
            Shoot(self.rect.x + 30, self.rect.y + 15, self.shoot_sprite_group, self.all_sprites, self.shoot)

        if 'image' in args:
            self.image = self.player_shoot
            return True

        if 273 in args and 'K_RIGHT' in args:
            if args[2] < 16:
                self.rect.y -= 8
                self.rect.x += 6
                return True

            if args[2] > 16 and not self.flag:
                self.rect.y += 8
                self.rect.x += 6

            if args[2] == 31 and self.flag:
                self.rect.y -= 8
                return True

        if 273 in args and 'K_LEFT' in args:
            if args[2] < 16:
                print(args)
                self.rect.y -= 8
                self.rect.x -= 6
                return True

            if args[2] > 16 and not self.flag:
                print(args)
                self.rect.y += 8
                self.rect.x -= 6

            if args[2] == 31 and self.flag:
                self.rect.y -= 8
                return True

        elif 273 in args and 'K_LEFT' not in args and 'K_RIGHT' not in args:
            if args[2] < 16:
                self.rect.y -= 8
                return True

            if args[2] > 16 and not self.flag:
                self.rect.y += 8
                return True

            if args[2] == 31 and self.flag:
                self.rect.y -= 8
                return True

        if self.count % 2 == 0:
            self.image = self.go_image

        if self.count % 2 == 1:
            self.image = self.player_image

        if 'K_RIGHT' in args and self.flag:
            self.rect.x += 10

        if 'K_LEFT' in args and self.flag and self.rect.x > 250:
            self.rect.x -= 10
        elif not self.flag:
            self.rect.y += 10

        if pygame.sprite.spritecollideany(self, self.killer_tiles_group):
            if not pygame.sprite.spritecollideany(self, self.vertical_borders):
                if not pygame.sprite.spritecollideany(self, self.horizontal_borders):
                    self.flag = True
                    return False
        else:
            self.flag = False
            return True
