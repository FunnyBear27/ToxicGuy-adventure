import pygame


class Shoot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, shoot_sprite_group, all_sprites, shoot):
        self.clock = pygame.time.Clock()
        super().__init__(shoot_sprite_group, all_sprites)
        self.image = shoot
        self.rect = self.image.get_rect().move(pos_x + 15, pos_y + 5)
        print(self.rect.x, self.rect.y)

    def update(self, *args):
        self.rect.x += 20
