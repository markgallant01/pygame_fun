import pygame
import os
import random

# window constants
(SCREEN_WIDTH, SCREEN_HEIGHT) = 1280, 720
SCREEN_CENTER: tuple = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

# setup
pygame.init()
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

# load images
player_surface = pygame.image.load(
    os.path.join('images', 'player.png')).convert_alpha()
player_rect = player_surface.get_frect(center = SCREEN_CENTER)

star_surface = pygame.image.load(
    os.path.join('images', 'star.png')).convert_alpha()

meteor_surface = pygame.image.load(
    os.path.join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = SCREEN_CENTER)

laser_surface = pygame.image.load(
    os.path.join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft = (0,SCREEN_HEIGHT))

# create list of star coords
star_coords: list[tuple] = []
for i in range(0, 20):
    (x,y) = random.randint(0, 1280), random.randint(0, 720)
    star_coords.append((x,y))

bounce = False
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill screen with color to wipe last frame
    display_surface.fill("darkgrey")

    # display stars
    for star_coord in star_coords:
        display_surface.blit(star_surface, star_coord)

    if not bounce:
        player_rect.right += 0.1
        if player_rect.right >= SCREEN_WIDTH:
            bounce = True
    else:
        player_rect.left -= 0.1
        if player_rect.left <= 0:
            bounce = False

    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(player_surface, player_rect)
    display_surface.blit(laser_surface, laser_rect)
    pygame.display.update()

pygame.quit()

