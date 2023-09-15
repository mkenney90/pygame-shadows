import pygame as pg
from pygame.math import Vector2


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

def generate_shadows(player, wall_group, boundary, surface):

    prect = player.rect

    for wall in wall_group:
        wrect = wall.rect

        if not wrect.colliderect(boundary): continue

        if prect.centerx > wrect.centerx:
            if prect.centery > wrect.centery:
                p1 = wrect.topright
                p2 = wrect.bottomleft
                p1_distance = Vector2(Vector2(p1) - Vector2(boundary.bottomleft)).length() * 1.2
                p2_distance = Vector2(Vector2(p2) - Vector2(boundary.bottomleft)).length() * 1.2
            else:
                p1 = wrect.bottomright
                p2 = wrect.topleft
                p1_distance = Vector2(Vector2(p1) - Vector2(boundary.topleft)).length() * 1.2
                p2_distance = Vector2(Vector2(p2) - Vector2(boundary.left)).length() * 1.2
        else:
            if prect.centery > wrect.centery:
                p1 = wrect.topleft
                p2 = wrect.bottomright
                p1_distance = Vector2(Vector2(p1) - Vector2(boundary.topright)).length() * 1.2
                p2_distance = Vector2(Vector2(p2) - Vector2(boundary.topright)).length() * 1.2
            else:
                p1 = wrect.bottomleft
                p2 = wrect.topright
                p1_distance = Vector2(Vector2(p1) - Vector2(boundary.bottomright)).length() * 1.2
                p2_distance = Vector2(Vector2(p2) - Vector2(boundary.bottomright)).length() * 1.2

        shadow_direction_1 = Vector2(Vector2(p1) - Vector2(prect.center)).normalize()
        shadow_direction_2 = Vector2(Vector2(p2) - Vector2(prect.center)).normalize()

        # if p3:
        #     pg.draw.polygon(shadow_surface, BLACK, (p1, p2, p3, p3 + shadow_direction_2 * p2_distance, p1 + shadow_direction_1 * p1_distance))
        # else:    
        pg.draw.polygon(surface, BLACK, (p1, p2, p2 + shadow_direction_2 * p2_distance, p1 + shadow_direction_1 * p1_distance))