#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import random

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]

img_dir = os.path.join(main_dir, 'sprites')

def load_image(name, colorkey=None):
    fullname = os.path.join(img_dir, name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('batmovile.png', -1)
        self.rect = self.image.get_rect()
        self.rect.y = 200
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = 9
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.lives = self.startingLife()
        self.fuel = 3000
        self.score = 0

    def update(self):
        return True

    def move_down(self):
        if self.rect.y <= 360:
            self.rect = self.rect.move((0,self.move))

    def move_up(self):
        if self.rect.y >= 135:
            self.rect = self.rect.move((0,-self.move))

    def addFuelCan(self):
        if self.fuel < 2500:
            self.fuel += 500

    def addPoint(self):
        self.score += 1

    def addLife(self):
        if (self.lives < self.startingLife()):
            self.lives += 1

    def startingLife(self):
        return 3

class Shoot(pygame.sprite.Sprite):
    def __init__(self, y, sprite, animation_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y + 40
        self.move = 15
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_tick = 0
        self.animation_sprites = animation_sprites
        self.y = y

    def update(self):
        self._move()
        screen = pygame.display.get_surface()
        if self.animation_tick <= 25:
            self.animate()
        if not screen.get_rect().contains(self.rect):
            self.kill()

    def animate(self):
        # Maybe do not use magic numbers
        screen = pygame.display.get_surface()
        fire_sprite = self.animation_tick
        if fire_sprite >= 20:
            fire_sprite_number = 3
        elif fire_sprite >= 10:
            fire_sprite_number = 2
        elif fire_sprite >= 5:
            fire_sprite_number = 1
        else:
            fire_sprite_number = 0

        screen.blit(self.animation_sprites[fire_sprite_number], (340, self.y))
        self.animation_tick += 1

    def _move(self):
        newpos = self.rect.move((self.move, 0))
        self.rect = newpos

class Can(pygame.sprite.Sprite):
    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 800, self.generate_random_y_position()
        self.move = 10
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((-self.move, 0))
        self.rect = newpos

    def generate_random_y_position(self):
        return random.randint(3, 8) * 5 * 10

class FuelCan(pygame.sprite.Sprite):
    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 800, self.generate_random_y_position()
        self.move = 10
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((-self.move, 0))
        self.rect = newpos

    def generate_random_y_position(self):
        return random.randint(3, 8) * 5 * 10

class Life(pygame.sprite.Sprite):
    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 800, self.generate_random_y_position()
        self.move = 10
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((-self.move, 0))
        self.rect = newpos

    def generate_random_y_position(self):
        return random.randint(3, 8) * 5 * 10


class Misile(pygame.sprite.Sprite):
    def __init__(self, y, sprite, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites[0]
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y
        self.move = 15
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.launching = True
        self.animation_tick = 0
        self.animation_sprites = sprites
        self.y = y

    def update(self):
        if not self.launching:
            self._move()
        else:
            self.animate()

        screen = pygame.display.get_surface()
        if not screen.get_rect().contains(self.rect):
            self.kill()

    def _move(self):
        newpos = self.rect.move((self.move, 0))
        self.rect = newpos
        self.animation_tick += 1
        if self.animation_tick >= 10:
            self.image = self.animation_sprites[5]
            self.animation_tick = 0
        else:
            self.image = self.animation_sprites[4]


    def animate(self):
        screen = pygame.display.get_surface()
        tick = self.animation_tick
        if tick >= 40:
            sprite = 5
            self.launching = False
        if tick >= 30:
            sprite = 4
        if tick >= 20:
            sprite = 3
        elif tick >= 10:
            sprite = 2
        elif tick >= 5:
            sprite = 1
        else:
            sprite = 0

        self.image = self.animation_sprites[sprite]
        self.rect.topleft = 300, self.y - 50
        self.animation_tick += 1

class Test(pygame.sprite.Sprite):
    def __init__(self, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.get_image(0,0,145,75)
        self.spritesheet = spritesheet
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y
        self.move = 15
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_tick = 0
        self.launching = True
        self.spritesheet = spritesheet
        self.y = y
        self.sprite_h = 75
        self.sprite_w = 145

    def update(self):

        if not self.launching:
            self._move()
        else:
            self.animate()

        screen = pygame.display.get_surface()
        if not screen.get_rect().contains(self.rect):
            self.kill()

    def _move(self):
        newpos = self.rect.move((self.move, 0))
        self.rect = newpos
        self.animation_tick += 1

        if self.animation_tick >= 10:
            sprite = 5
            self.image = self.spritesheet.get_image(0,self.sprite_h * sprite,self.sprite_w,self.sprite_h)
            self.animation_tick = 0
        else:
            sprite = 4
            self.image = self.spritesheet.get_image(0,self.sprite_h * sprite,self.sprite_w,self.sprite_h)


    def animate(self):
        screen = pygame.display.get_surface()
        tick = self.animation_tick
        if tick >= 40:
            sprite = 5
            self.launching = False
        if tick >= 30:
            sprite = 4
        if tick >= 20:
            sprite = 3
        elif tick >= 10:
            sprite = 2
        elif tick >= 5:
            sprite = 1
        else:
            sprite = 0

        self.image = self.spritesheet.get_image(0,self.sprite_h * sprite,self.sprite_w,self.sprite_h)
        #self.image = self.animation_sprites[sprite]
        self.rect.topleft = 300, self.y - 50
        self.animation_tick += 1

class SpriteSheet(object):
    def __init__(self, image):
        self.sprite_sheet = image


    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(image.get_at((0,0)), RLEACCEL)

        return image

class Shock(pygame.sprite.Sprite):
    def __init__(self, y, sprite, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites[0]
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y
        self.move = 15
        self.dizzy = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_tick = 0
        self.animation_sprites = sprites
        self.y = y

    def update(self):
        self.animate()

        screen = pygame.display.get_surface()
        if self.animation_tick >= 23:
            self.kill()

    def animate(self):
        screen = pygame.display.get_surface()
        sprite = self.animation_tick
        if sprite >= 23:
            sprite = 22

        self.image = self.animation_sprites[sprite]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = 300, self.y - 50
        self.animation_tick += 1

def draw_background(x, bridge, screen):
    rel_x = x % bridge.get_rect().width
    screen.blit(bridge, (rel_x - bridge.get_rect().width, 0))
    w, h = pygame.display.get_surface().get_size()
    if rel_x < w:
        screen.blit(bridge, (rel_x, 0))

def draw_bottom_bar(screen, bar):
    w, h = pygame.display.get_surface().get_size()
    bar_w, bar_h = bar.get_size()
    screen.blit(bar, (w - bar_w, h - bar_h))

def draw_bathead(screen, bathead):
    w, h = pygame.display.get_surface().get_size()
    sprite_w, sprite_h = bathead.get_size()
    screen.blit(bathead, (w - 410, h - sprite_h - 10))

def draw_fuel(screen, sprites, fuel):
    w, h = pygame.display.get_surface().get_size()

    if fuel >= 2500:
        sprite = sprites[0]
    elif fuel >= 2000:
        sprite = sprites[1]
    elif fuel >= 1500:
        sprite = sprites[2]
    elif fuel >= 1000:
        sprite = sprites[3]
    else:
        sprite = sprites[4]

    sprite_w, sprite_h = sprite.get_size()
    screen.blit(sprite, (w - 505, h - sprite_h - 20))


def draw_cannon_fire(fire, screen, y, fire_sprite):
    # Maybe do not use magic numbers
    if fire_sprite >= 20:
        fire_sprite_number = 3
    elif fire_sprite >= 10:
        fire_sprite_number = 2
    elif fire_sprite >= 5:
        fire_sprite_number = 1
    else:
        fire_sprite_number = 0

    screen.blit(fire[fire_sprite_number], (340, y))

# Check if the given array of sprites is off the screen
# and removeit from the array
def check_all_sprites_off_screen(sprites_groups):
    for sprites_group in sprites_groups:
        if not isinstance(sprites_group, Player):
            for sprite in sprites_group:
                if sprite.rect.x <= -100 or sprite.rect.x >= 900:
                    sprites_group.remove(sprite)
    return sprites_groups

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('batmetal')
    pygame.mouse.set_visible(0)

    clock = pygame.time.Clock()

    batmovile = Player()

    background_x = 0
    sky_x = 0

    bridge = load_image('bridge.png', -1)
    sky = load_image("sky.png")
    bottom_bar = load_image("bottom_bar.png")
    cannon_fire_0 = load_image("shoot_0.png", -1)
    cannon_fire_1 = load_image("shoot_1.png", -1)
    cannon_fire_2 = load_image("shoot_2.png", -1)
    cannon_fire_3 = load_image("shoot_3.png", -1)
    cannon_fire = [cannon_fire_0, cannon_fire_1, cannon_fire_2, cannon_fire_3]

    misil_0 = load_image("misil_0.png", -1)
    misil_1 = load_image("misil_1.png", -1)
    misil_2 = load_image("misil_2.png", -1)
    misil_3 = load_image("misil_3.png", -1)
    misil_4 = load_image("misil_4.png", -1)
    misil_5 = load_image("misil_5.png", -1)
    misile_animation = [misil_0, misil_1, misil_2, misil_3, misil_4, misil_5]

    shock_1 = load_image("shock_1.png", -1)
    shock_2 = load_image("shock_2.png", -1)
    shock_3 = load_image("shock_3.png", -1)
    shock_4 = load_image("shock_4.png", -1)
    shock_5 = load_image("shock_5.png", -1)
    shock_6 = load_image("shock_6.png", -1)
    shock_7 = load_image("shock_7.png", -1)
    shock_8 = load_image("shock_8.png", -1)
    shock_9 = load_image("shock_9.png", -1)
    shock_10 = load_image("shock_10.png", -1)
    shock_11 = load_image("shock_11.png", -1)
    shock_12 = load_image("shock_12.png", -1)
    shock_13 = load_image("shock_13.png", -1)
    shock_14 = load_image("shock_14.png", -1)
    shock_15 = load_image("shock_15.png", -1)
    shock_16 = load_image("shock_16.png", -1)
    shock_17 = load_image("shock_17.png", -1)
    shock_18 = load_image("shock_18.png", -1)
    shock_19 = load_image("shock_19.png", -1)
    shock_20 = load_image("shock_20.png", -1)
    shock_21 = load_image("shock_21.png", -1)
    shock_22 = load_image("shock_22.png", -1)
    shock_23 = load_image("shock_23.png", -1)

    shock_animation = [shock_1, shock_2, shock_3, shock_4, shock_5, shock_6, shock_7, shock_8, shock_9, shock_10, shock_11, shock_12, shock_13, shock_14, shock_15, shock_16, shock_17, shock_18, shock_19, shock_20, shock_21, shock_22, shock_23]

    shoot_sprite = load_image("shoot.png", -1)
    misile_sprite = load_image("misil.png", -1)
    can_sprite = load_image("can.png", -1)
    fuel_can_sprite = load_image("fuel_can.png", -1)
    life_sprite = load_image("life.png", -1)

    bathead_1 = load_image("bathead_1.png",-1)
    bathead_2 = load_image("bathead_2.png",-1)
    bathead_3 = load_image("bathead_3.png",-1)
    bathead_4 = load_image("bathead_4.png",-1)

    fuel_1 = load_image("fuel_1.png",-1)
    fuel_2 = load_image("fuel_2.png",-1)
    fuel_3 = load_image("fuel_3.png",-1)
    fuel_4 = load_image("fuel_4.png",-1)
    fuel_5 = load_image("fuel_5.png",-1)

    test = load_image("test.png",-1)

    lives_heads = [bathead_4, bathead_3, bathead_2, bathead_1]
    fuel_sprites = [fuel_1, fuel_2, fuel_3, fuel_4, fuel_5]

    shoots = pygame.sprite.Group()
    misils = pygame.sprite.Group()
    shock = pygame.sprite.Group()
    cans = pygame.sprite.Group()
    fuel_cans = pygame.sprite.Group()
    lives = pygame.sprite.Group()

    going = True
    while going:
        all_sprites_tuple = []
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                shoot = Shoot(batmovile.rect.y, shoot_sprite, cannon_fire)
                shoots.add(shoot)
            elif event.type == KEYDOWN and event.key == K_a:
                if batmovile.score >= 10:
                    misil = Misile(batmovile.rect.y, misile_sprite, misile_animation)
                    misils.add(misil)
            elif event.type == KEYDOWN and event.key == K_s:
                new_sock = Shock(batmovile.rect.y, misile_sprite, shock_animation)
                shock.add(new_sock)
            elif event.type == KEYDOWN and event.key == K_d:
                sprite_sheet = SpriteSheet(test)
                new_sock = Test(batmovile.rect.y, sprite_sheet)
                misils.add(new_sock)


        k = pygame.key.get_pressed()

        if k[K_DOWN]:
            batmovile.move_down()
        elif k[K_UP]:
            batmovile.move_up()

        # 1/20 chances to generate a can and only two cans on the screen
        # this method is actually prety bad
        random_number = random.randint(1, 20)
        if len(cans) <= 1 and int(random_number) == 1:
            can = Can(can_sprite)
            cans.add(can)

        # 1/500 chances to generate a fuel can
        # this method is actually prety bad
        random_number = random.randint(1, 500)
        if len(fuel_cans) <= 0 and int(random_number) == 1:
            fuel_can = FuelCan(fuel_can_sprite)
            fuel_cans.add(fuel_can)

        # 1/500 chances to generate life
        # this method is actually prety bad
        random_number = random.randint(1, 500)
        if len(lives) <= 0 and int(random_number) == 3:
            life = Life(life_sprite)
            lives.add(life)


        all_sprites_tuple.append(batmovile)
        all_sprites_tuple.append(cans)
        all_sprites_tuple.append(fuel_cans)
        all_sprites_tuple.append(misils)
        all_sprites_tuple.append(shoots)
        all_sprites_tuple.append(shock)
        all_sprites_tuple.append(lives)


        all_sprites_tuple = check_all_sprites_off_screen(all_sprites_tuple)

        allsprites = pygame.sprite.RenderPlain(all_sprites_tuple)

        draw_background(sky_x, sky, screen)
        draw_background(background_x, bridge, screen)

        allsprites.update()

        allsprites.draw(screen)

        draw_bottom_bar(screen, bottom_bar)
        draw_bathead(screen, lives_heads[batmovile.lives])
        draw_fuel(screen, fuel_sprites, batmovile.fuel)

        pygame.display.flip()

        background_x -= 5
        sky_x -= 1
        batmovile.fuel -= 1

        blocks_hit_list = pygame.sprite.spritecollide(batmovile, lives, True, pygame.sprite.collide_mask)
        if len(blocks_hit_list):
            batmovile.addLife()

        blocks_hit_list = pygame.sprite.spritecollide(batmovile, cans, True, pygame.sprite.collide_mask)

        if len(blocks_hit_list):
            batmovile.lives -= 1
            # reset life, for development purposes
            if batmovile.lives < 0:
                batmovile.lives = 3


        blocks_hit_list = pygame.sprite.groupcollide(shoots, cans, True, True, pygame.sprite.collide_mask)
        if len(blocks_hit_list):
            batmovile.addPoint()

        blocks_hit_list = pygame.sprite.groupcollide(misils, cans, True, True, pygame.sprite.collide_mask)
        if len(blocks_hit_list):
            batmovile.addPoint()

        blocks_hit_list = pygame.sprite.groupcollide(shock, cans, True, True, pygame.sprite.collide_mask)
        if len(blocks_hit_list):
            batmovile.addPoint()

        blocks_hit_list = pygame.sprite.spritecollide(batmovile, fuel_cans, True, pygame.sprite.collide_mask)
        if len(blocks_hit_list):
            batmovile.addFuelCan()




    pygame.quit()


if __name__ == '__main__':
    main()
