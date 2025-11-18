# pyright:strict

import os
import random
import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, player_surface: pg.surface.Surface,
                 laser_surface: pg.surface.Surface,
                 group: pg.sprite.Group[pg.sprite.Sprite]):
        super().__init__(group)

        self.image = player_surface
        self.rect: pg.FRect = self.image.get_frect(center = SCREEN_CENTER)
        self.direction = pg.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        self.laser_surface = laser_surface

        # mask
        self.mask = pg.mask.from_surface(self.image)

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
            Laser(self.rect.midtop, self.laser_surface,
                  [all_sprites, laser_sprites])
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
                 groups: list[pg.sprite.Group[pg.sprite.Sprite]]):
        super().__init__(groups)
        self.image = surface
        self.rect: pg.FRect = self.image.get_frect(midbottom = position)

        self.speed = 400

        # mask
        self.mask = pg.mask.from_surface(self.image)

    def update(self, dt: int):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pg.sprite.Sprite):
    def __init__(self, surface: pg.surface.Surface,
                 groups: list[pg.sprite.Group[pg.sprite.Sprite]]):
        super().__init__(groups)
        self.original_surface = surface
        self.image = surface

        (x,y) = random.randint(0, SCREEN_WIDTH), 0
        self.rect: pg.FRect = self.image.get_frect(midbottom = (x,y))

        self.speed = 400
        self.creation_time = pg.time.get_ticks()
        self.lifetime = 3000
        self.direction = pg.Vector2(random.uniform(-0.5, 0.5), 1)
        self.rotation = 0
        self.rotation_speed = random.randint(1, 500)

        # mask
        self.mask = pg.mask.from_surface(self.image)

    def update(self, dt: int):
        self.rect.center += self.direction * self.speed * dt
        current_time = pg.time.get_ticks()
        if current_time - self.creation_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pg.transform.rotozoom(self.original_surface,
                                           self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)


def collisions():
    global running

    player_collisions = pg.sprite.spritecollide(player, meteor_sprites, True,
                                                pg.sprite.collide_mask)
    if player_collisions:
        running = False

    for laser_sprite in laser_sprites:
        meteor_collisions = pg.sprite.spritecollide(laser_sprite,
                                                    meteor_sprites, True)
        if meteor_collisions:
            laser_sprite.kill()


def display_score():
    game_time = pg.time.get_ticks() // 100

    font = pg.font.Font(None, 50)
    text_surface = font.render(str(game_time), True, (240,240,240))
    text_rect: pg.FRect = text_surface.get_frect(
        midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
    display_surface.blit(text_surface, text_rect)
    pg.draw.rect(display_surface, (240,240,240),
                 text_rect.inflate(30,15).move(0, -1), 4, 5)


# window constants
(SCREEN_WIDTH, SCREEN_HEIGHT) = 1280, 720
SCREEN_CENTER: tuple[float,float] = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

# setup
pg.init()
display_surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Space Shooter")
running = True
clock: pg.Clock = pg.time.Clock()

# import
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
player = Player(player_surface, laser_surface, all_sprites)

meteor_sprites: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()
laser_sprites: pg.sprite.Group[pg.sprite.Sprite] = pg.sprite.Group()

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
            Meteor(meteor_surface, [all_sprites, meteor_sprites])

    all_sprites.update(dt)

    # fill screen with color to wipe last frame
    display_surface.fill("#3a2e3f")
    all_sprites.draw(display_surface)

    display_score()
    collisions()

    pg.display.update()

pg.quit()

