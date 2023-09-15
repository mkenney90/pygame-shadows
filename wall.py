import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), endcap = False):
        super().__init__()
        self.pos = pos
        self.start_pos = pos
        self.size = (32, 32)
        self.original = pygame.transform.scale(
            pygame.image.load("graphics/wall.png"), self.size
        )
        self.image = self.original
        self.rect = self.image.get_rect(topleft=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.tile_position = endcap

    def update(self):
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
