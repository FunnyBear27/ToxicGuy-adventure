import pygame


class Shoot(pygame.sprite.Sprite):
    def __init__(self, vx, pos_x, pos_y,
                 shoot_sprite_group, all_sprites,
                 shoot, enemy_group, left_border,
                 right_border):
        self.left_border = left_border
        self.right_border = right_border
        self.enemy_group = enemy_group
        self.x = pos_x
        self.clock = pygame.time.Clock()
        super().__init__(shoot_sprite_group, all_sprites)
        self.image = shoot
        self.rect = self.image.get_rect().move(pos_x + 15, pos_y + 5)

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, self.right_border)\
                or pygame.sprite.spritecollideany(self, self.left_border)\
                or pygame.sprite.spritecollideany(self, self.enemy_group):
            pygame.sprite.Sprite.kill(self)

        if 'K_RIGHT' in args:
            self.rect.x += 20

        if 'K_LEFT' in args:
            self.rect.x -= 20

