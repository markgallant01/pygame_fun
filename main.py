# pyright:strict

import pygame
from pygame.sprite import Group, Sprite
import os
import random

# window constants
(SCREEN_WIDTH, SCREEN_HEIGHT) = 1280, 720
SCREEN_CENTER: tuple[float,float] = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

# setup
pygame.init()
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock: pygame.Clock = pygame.time.Clock()

class Player(Sprite):
    def __init__(self, group: Group[Sprite]):
        super().__init__(group)
        self.image: pygame.Surface = pygame.image.load(
            os.path.join('images', 'player.png')).convert_alpha()

        self.rect: pygame.FRect = self.image.get_frect(center = SCREEN_CENTER)
        self.direction: pygame.Vector2 = pygame.Vector2()
        self.speed: int = 300

    def update(self, dt: int):
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_f]) - int(keys[pygame.K_s])
        self.direction.y = int(keys[pygame.K_d]) - int(keys[pygame.K_e])
        self.direction = (self.direction.normalize()
                          if self.direction else self.direction)
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print('fire laser')

class Star(Sprite):
    surface = pygame.image.load(
        os.path.join('images', 'star.png')).convert_alpha()

    def __init__(self, group: Group[Sprite]):
        super().__init__(group)

        self.image = Star.surface
        (x,y) = random.randint(0, 1280), random.randint(0, 720)
        self.rect: pygame.FRect = Star.surface.get_frect(center = (x,y))

all_sprites: Group[Sprite] = Group()
for i in range(0, 20):
    Star(all_sprites)
player = Player(all_sprites)

meteor_surface = pygame.image.load(
    os.path.join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = SCREEN_CENTER)

laser_surface = pygame.image.load(
    os.path.join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft = (0,SCREEN_HEIGHT))

bounce = False
while running:
    dt = clock.tick() / 1000

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)

    # fill screen with color to wipe last frame
    display_surface.fill("darkgrey")
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()

