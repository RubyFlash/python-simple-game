import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

game_background = pygame.transform.scale(
    pygame.image.load("background.png"),
    (WIDTH, HEIGHT)
)

game_background_x1 = 0
game_background_x2 = game_background.get_width()

game_background_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (182, 76)
player_image = pygame.image.load("player.png").convert_alpha()
player = pygame.transform.scale(player_image, player_size)
player_rect = pygame.Rect(
    100,
    HEIGHT/2,
    *player_size
)

player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]


def create_enemy():
    enemy_size = (60, 30)
    enemy_image = pygame.image.load("enemy.png").convert_alpha()
    enemy = pygame.transform.scale(enemy_image, enemy_size)
    enemy_rect = pygame.Rect(
        WIDTH,
        random.randint(100, 700),
        *enemy_size
    )
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_supply():
    supply_size = (100, 100)
    supply_image = pygame.image.load("bonus.png").convert_alpha()
    supply = pygame.transform.scale(supply_image, supply_size)
    supply_rect = pygame.Rect(
        random.randint(WIDTH/3, WIDTH),
        0,
        *supply_size
    )
    supply_move = [0, random.randint(4, 8)]
    return [supply, supply_rect, supply_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

CREATE_SUPPLY = CREATE_ENEMY + 1
pygame.time.set_timer(CREATE_SUPPLY, 3000)

supplies = []

CHANGE_IMAGE = CREATE_SUPPLY + 1
pygame.time.set_timer(CHANGE_IMAGE, 200)

score = 0

image_index = 0

playing = True

while playing:
    FPS.tick(240)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_SUPPLY:
            supplies.append(create_supply())
        if event.type == CHANGE_IMAGE:
            player_image = pygame.image.load(
                os.path.join(
                    IMAGE_PATH,
                    PLAYER_IMAGES[image_index]
                )
            )
            player = pygame.transform.scale(player_image, player_size)
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    game_background_x1 -= game_background_move
    game_background_x2 -= game_background_move

    if game_background_x1 < -game_background.get_width():
        game_background_x1 = game_background.get_width()

    if game_background_x2 < -game_background.get_width():
        game_background_x2 = game_background.get_width()

    main_display.blit(
        game_background, (game_background_x1, 0))

    main_display.blit(
        game_background, (game_background_x2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for supply in supplies:
        supply[1] = supply[1].move(supply[2])
        main_display.blit(supply[0], supply[1])

        if player_rect.colliderect(supply[1]):
            score += 1
            supplies.pop(supplies.index(supply))

    main_display.blit(FONT.render(
        str(score),
        True,
        COLOR_BLACK
    ), (WIDTH-50, 20))

    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for supply in supplies:
        if supply[1].bottom > HEIGHT:
            supplies.pop(supplies.index(supply))
