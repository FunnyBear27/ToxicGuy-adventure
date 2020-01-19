import pygame
from Shoot import Shoot
import sys
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,
                 player_group, all_sprites,
                 player_image, tile_height,
                 tile_width, player_shoot,
                 go_image, killer_tiles_group,
                 left_border, right_border, upper_border,
                 shoot_sprite_group, shoot,
                 enemy_group, finish_group):

        self.upper_border = upper_border
        self.right_border = right_border
        self.enemy_group = enemy_group
        self.left_borders = left_border
        self.shoot_sprite_group = shoot_sprite_group
        self.all_sprites = all_sprites
        self.shoot = shoot
        self.player_image = player_image
        self.player_shoot = player_shoot
        self.go_image = go_image
        self.killer_tiles_group = killer_tiles_group
        self.finish_group = finish_group

        self.flag = True
        self.count = 0
        self.clock = pygame.time.Clock()
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + 5)

    def update(self, *args):
        if 'K_RIGH' in args or 'K_LEF' in args:
            self.count += 1

        if 'shoot' in args:
            Shoot(args[1], self.rect.x + 30, self.rect.y + 15,
                  self.shoot_sprite_group, self.all_sprites,
                  self.shoot, self.enemy_group, self.left_borders,
                  self.right_border)

        if 'image' in args and 'K_RIGHT' in args:
            self.image = self.player_shoot
            return True

        if 'image' in args and 'K_LEFT' in args:
            self.image = pygame.transform.flip(self.player_shoot, 180, 0)
            return True

        if 273 in args and 'K_RIGHT' in args:
            if args[2] > 16 and not self.flag:
                if pygame.sprite.spritecollideany(self, self.right_border):
                    self.flag = False
                    self.rect.x -= 10
                    return 'fall'
                self.rect.y += 12
                self.rect.x += 6
                if pygame.sprite.spritecollideany(self, self.killer_tiles_group):
                    self.flag = True
                    self.rect.y -= 10
                    return 'fall'

            if args[2] < 16 and not pygame.sprite.spritecollideany(self, self.upper_border):
                if pygame.sprite.spritecollideany(self, self.right_border):
                    self.flag = True
                    self.rect.y -= 30
                    return 'fall'
                self.rect.y -= 12
                self.rect.x += 6
                return False
            else:
                self.flag = False
                return False

        if 273 in args and 'K_LEFT' in args:
            if args[2] > 16 and not self.flag:
                if pygame.sprite.spritecollideany(self, self.left_borders):
                    self.flag = False
                    self.rect.x += 7
                    return True
                self.rect.y += 12
                self.rect.x -= 6
                if pygame.sprite.spritecollideany(self, self.killer_tiles_group):
                    self.flag = True
                    return 'fall'

            if args[2] < 16 and\
                    not pygame.sprite.spritecollideany(self, self.upper_border):
                if pygame.sprite.spritecollideany(self, self.left_borders):
                    self.flag = False
                    self.rect.x += 7
                    return True
                self.rect.y -= 8
                self.rect.x -= 6
                return False
            else:
                self.flag = False
                return False

        # elif 273 in args and 'K_LEFT' not in args and 'K_RIGHT'\
        #         not in args:
        #     if args[2] > 16 and not self.flag:
        #         if pygame.sprite.spritecollideany(self, self.left_borders):
        #             self.flag = False
        #             return True
        #         self.rect.y += 8
        #         if pygame.sprite.spritecollideany(self, self.killer_tiles_group):
        #             self.flag = True
        #             return 'fall'
        #
        #     if args[2] < 16 and\
        #             not pygame.sprite.spritecollideany(self, self.upper_border):
        #         self.rect.y -= 8
        #         return False
        #     else:
        #         self.flag = False
        #         return False

        if self.count % 2 == 0 and 'K_RIGH' in args:
            self.image = self.go_image

        if self.count % 2 == 1 and 'K_RIGH' in args:
            self.image = self.player_image

        if self.count % 2 == 0 and 'K_LEF' in args:
            self.image = pygame.transform.flip(self.go_image, 180, 0)

        if self.count % 2 == 1 and 'K_LEF' in args:
            self.image = pygame.transform.flip(self.player_image, 180, 0)

        if 'K_RIGHT' in args and self.flag \
                and not pygame.sprite.spritecollideany(self, self.right_border):
            self.rect.x += 20

        if 'K_LEFT' in args and self.flag\
                and not pygame.sprite.spritecollideany(self, self.left_borders):
            self.rect.x -= 20
        elif not self.flag:
            self.rect.y += 10

        if pygame.sprite.spritecollideany(self, self.killer_tiles_group):
            self.flag = True
            return False
        else:
            self.flag = False
            return True
        return True
