# pyright:strict

import os
import random
import pygame as pg

# window constants
(SCREEN_WIDTH, SCREEN_HEIGHT) = 1280, 720
SCREEN_CENTER: tuple[float,float] = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2


class Player(pg.sprite.Sprite):
    def __init__(self, surface: pg.surface.Surface,
                 group: pg.sprite.Group[pg.sprite.Sprite]):
        super().__init__(group)

        self.image = surface
        self.rect: pg.FRect = self.image.get_frect(center = SCREEN_CENTER)
        self.direction = pg.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pg.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt: int):
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_f]) - int(keys[pg.K_s])
        self.direction.y = int(keys[pg.K_d]) - int(keys[pg.K_e])
        self.direction = (self.direction.normalize()
                          if self.direction else self.direction)
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pg.key.get_just_pressed()
        if recent_keys[pg.K_SPACE] and self.can_shoot:
            Laser(self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pg.time.get_ticks()

        self.laser_timer()


class Star(pg.sprite.Sprite):
    def __init__(self, surface: pg.surface.Surface,
                 group: pg.sprite.Group[pg.sprite.Sprite]):
        super().__init__(group)

        self.image = surface
        (x,y) = (random.randint(0, SCREEN_WIDTH),
                 random.randint(0, SCREEN_HEIGHT))
        self.rect: pg.FRect = self.image.get_frect(center = (x,y))


class Laser(pg.sprite.Sprite):
    def __init__(self, position: tuple[float,float],
                 surface: pg.surface.Surface,
                 group: pg.sprite.Group[pg.sprite.Sprite]):
        super().__init__(group)
        self.image = surface
        self.rect: pg.FRect = self.image.get_frect(midbottom = position)

        self.speed = 400

    def update(self, dt: int):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pg.sprite.Sprite):
    def __init__(self, surface: pg.surface.Surface,
                 group: pg.sprite.Group[pg.sprite.Sprite]):
        super().__init__(group)
        self.image = surface

        (x,y) = random.randint(0, SCREEN_WIDTH), 0
        self.rect: pg.FRect = self.image.get_frect(midbottom = (x,y))

        self.speed = 200
        self.creation_time = pg.time.get_ticks()
        self.lifetime = 2000

    def update(self, dt: int):
        self.rect.centery += self.speed * dt
        current_time = pg.time.get_ticks()
        if current_time - self.creation_time >= self.lifetime:
            self.kill()


# setup
pg.init()
display_surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Space Shooter")
running = True
clock: pg.Clock = pg.time.Clock()

# load surfaces
player_surface = pg.image.load(
    os.path.join('images', 'player.png')).convert_alpha()

star_surface = pg.image.load(
    os.path.join('images', 'star.png')).convert_alpha()

laser_surface = pg.image.load(
    os.path.join('images', 'laser.png')).convert_alpha()

meteor_surface = pg.image.load(
    os.path.join('images', 'meteor.png')).convert_alpha()

all_sprites: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()
for i in range(0, 20):
    Star(star_surface, all_sprites)
player = Player(player_surface, all_sprites)

# custom events -> meteor event
meteor_event = pg.event.custom_type()
pg.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000

    # poll for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, all_sprites)

    all_sprites.update(dt)

    # fill screen with color to wipe last frame
    display_surface.fill("darkgrey")
    all_sprites.draw(display_surface)

    pg.display.update()

pg.quit()

