import pygame
from math import degrees, atan2


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_center, pos=(0, 0)):
        super().__init__()
        self.pos = list(pos)
        self.size = (36, 48)
        self.speed = 4
        self.original = pygame.transform.scale(pygame.image.load(
            "graphics/player.png"), self.size).convert()
        self.original.set_colorkey((0, 0, 0))
        self.image = self.original
        self.rect = self.image.get_rect(center=screen_center)
        self.mask = pygame.mask.from_surface(pygame.image.load(
            "graphics/player_mask.png").convert_alpha())
        self.collide_rect = pygame.Rect((self.rect.topleft), (32, 32))
        self.radius = 150

    def player_input(self, obstacles):
        keys = pygame.key.get_pressed()

        input_left = keys[pygame.K_LEFT] | keys[pygame.K_a]
        input_right = keys[pygame.K_RIGHT] | keys[pygame.K_d]
        input_up = keys[pygame.K_UP] | keys[pygame.K_w]
        input_down = keys[pygame.K_DOWN] | keys[pygame.K_s]

        dx = 0
        dy = 0

        for i in range(self.speed):

            if pygame.Rect.collidelist(self.collide_rect.move(0, (input_down - input_up) * i), obstacles.sprites()) == -1:
                dy = (input_up - input_down) * i

            if (
                pygame.Rect.collidelist(self.collide_rect.move(
                    (input_right - input_left) * i, 0), obstacles.sprites())
                == -1
            ):
                dx = (input_left - input_right) * i

        if dx or dy:
            self.player_move(dx, dy)

    def player_move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

    def update(self, obstacles):
        mouse_pos = pygame.mouse.get_pos()

        self.image = pygame.transform.rotate(
            self.original, degrees(
                atan2(self.rect.centerx - mouse_pos[0], self.rect.centery - mouse_pos[1]))
        )
        self.rect = self.image.get_rect(center=self.rect.center)

        self.player_input(obstacles)
        self.collide_rect.center = self.rect.center
