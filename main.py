import pygame as pg
import random
from math import degrees, atan2
from pygame.math import Vector2
from player import Player
from wall import Wall
from pygame import Color
from levels import level_1
from environment import generate_shadows

WIDTH = 800
HEIGHT = 640
FPS = 60
SCREEN_RECT = pg.Rect((0,0),(WIDTH, HEIGHT))
STARTING_POINT = (0,0)

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# initialize pygame and create window
pg.init()
pg.mixer.init()  # For sound
pg.display.set_caption("POS: ")
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])
screen = pg.display.set_mode((WIDTH, HEIGHT))
alt = pg.Surface((WIDTH, HEIGHT))
alt.set_alpha(140)
shadow_surface = pg.Surface((WIDTH, HEIGHT))
shadow_surface.set_alpha(180)
shadow_surface.set_colorkey((255,255,255))
clock = pg.time.Clock()  # For syncing the FPS

# for camera scrolling
scroll = [0, 0]

# sprite groups
player = pg.sprite.GroupSingle()
player.add(Player((SCREEN_RECT.center)))

wall_group = pg.sprite.Group()

def generate_level(level):
    # build level
    level_layout = level.layout

    # build exterior walls
    # for i in range(0, level.width, 32):
    #     walls.add(Wall((i, 0)))
    #     walls.add(Wall((i, level.height - 32)))
    # for i in range(0, level.height, 32):
    #     walls.add(Wall((0, i)))
    #     walls.add(Wall((level.width - 32, i)))

    for y, value in enumerate(level_layout):
        previous_tile = None
        for x, tile in enumerate(level_layout[y]):
            above_tile = (level_layout[y-1][x] if y > 0 else None)
            below_tile = (level_layout[y+1][x] if y < len(level_layout) - 1 else None)
            next_tile = (level_layout[y][x+1] if x < len(level_layout[y]) - 1 else None)
            tile_position = None
            if tile == 1:
                if previous_tile == 1 and next_tile != 1:
                    tile_position = "R"
                elif previous_tile != 1 and next_tile == 1:
                    tile_position = "L"
                elif above_tile == 1 and below_tile != 1:
                    tile_position = "D"
                elif above_tile != 1 and below_tile == 1:
                    tile_position = "U"
                wall_group.add(Wall((x * 32, y * 32), tile_position))
            elif tile == 9:
                player.sprite.rect.topleft = (x * 32, y * 32)
            previous_tile = tile
            print(tile_position)
    return player.sprite.rect.topleft

# set player starting point and center screen

STARTING_POINT = generate_level(level_1)
player.sprite.rect.center = SCREEN_RECT.center
prect = player.sprite.collide_rect
scroll = [SCREEN_RECT.centerx - STARTING_POINT[0], SCREEN_RECT.centery - STARTING_POINT[1]]

# get the whole family together

all_sprites = pg.sprite.LayeredUpdates(wall_group)

def draw_grid():
    for i in range(0, WIDTH, 50):
        pg.draw.line(alt, Color(0, 100, 200), (i, 0), (i, HEIGHT))

    for i in range(0, HEIGHT, 50):
        pg.draw.line(alt, Color(0, 100, 200), (0, i), (WIDTH, i))

def scroll_screen(player_pos, player_start, screen_rect):
    ppx, ppy = player_pos
    psx, psy = player_start
    sw, sh = screen_rect.size

    return [ppx - psx + sw / 2, ppy - psy + sh / 2]

def quit_game():
    pg.quit()
    
## Game loop
while 1:

    # 1 Process input/events
    clock.tick(FPS)  ## will make the loop run at the same speed all the time
    for event in pg.event.get():  # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pg.QUIT:
            quit_game()

    # 2 Update
    player.update(wall_group)

    scroll = scroll_screen(player.sprite.pos, STARTING_POINT, SCREEN_RECT)

    # 3 Draw/render
    screen.fill(BLACK)
    alt.fill((90, 180, 40))

    if player.sprite.rect.center != pg.mouse.get_pos():
        vec1 = Vector2(player.sprite.rect.center)
        vec2 = Vector2(pg.mouse.get_pos())
        pg.draw.line(
            alt, Color(220, 0, 0, 0), vec1 + (
                (vec2 - vec1).normalize() if vec1 else Vector2(2, 2)
            ) * 30, vec1 + (vec2 - vec1).normalize() * 100, 2
        )

    screen.blit(alt, (0, 0))
    shadow_surface.fill((255,255,255))

    for wall in wall_group:
        wrect = wall.rect
        wrect.x = wall.start_pos[0] + scroll[0]
        wrect.y = wall.start_pos[1] + scroll[1]

    generate_shadows(player.sprite, wall_group, SCREEN_RECT, shadow_surface)

    screen.blit(shadow_surface, (0,0))
    for wall in wall_group:
        if wall.rect.colliderect(SCREEN_RECT):
            wall.draw(screen)

    player.draw(screen)

    pg.draw.rect(screen, WHITE, SCREEN_RECT, 2)

    for wall in wall_group:
        #pg.draw.rect(screen, RED, wall.rect, 1)
        wall.update()

    pg.display.set_caption(f"POS: {str(player.sprite.pos)}   {str(clock.get_fps())}")

    ## Done after drawing everything to the screen
    pg.display.flip()

