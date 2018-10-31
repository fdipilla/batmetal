#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import random

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]

# despues meter las imagenes en una carpeta separada
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
    def __init__(self, y, sprite):
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

    def update(self):
        self._move()
        screen = pygame.display.get_surface()
        if not screen.get_rect().contains(self.rect):
            self.kill()

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
        return random.randint(3, 10) * 5 * 10

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
        return random.randint(3, 10) * 5 * 10

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
        return random.randint(3, 10) * 5 * 10


class Misile(pygame.sprite.Sprite):
    def __init__(self, y, sprite):
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

    def update(self):
        self._move()
        screen = pygame.display.get_surface()
        if not screen.get_rect().contains(self.rect):
            self.kill()

    def _move(self):
        newpos = self.rect.move((self.move, 0))
        self.rect = newpos

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
    cannon_fire_tick = 26

    bridge = load_image('bridge.png', -1)
    sky = load_image("sky.png")
    bottom_bar = load_image("bottom_bar.png")
    cannon_fire_0 = load_image("shoot_0.png", -1)
    cannon_fire_1 = load_image("shoot_1.png", -1)
    cannon_fire_2 = load_image("shoot_2.png", -1)
    cannon_fire_3 = load_image("shoot_3.png", -1)
    cannon_fire = [cannon_fire_0, cannon_fire_1, cannon_fire_2, cannon_fire_3]
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

    lives_heads = [bathead_4, bathead_3, bathead_2, bathead_1]
    fuel_sprites = [fuel_1, fuel_2, fuel_3, fuel_4, fuel_5]

    shoots = pygame.sprite.Group()
    misils = pygame.sprite.Group()
    cans = pygame.sprite.Group()
    fuel_cans = pygame.sprite.Group()
    lives = pygame.sprite.Group()

    #all_sprites_tuple = []

    going = True
    while going:
        all_sprites_tuple = []
        clock.tick(60)
        must_draw_cannon_fire = False

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                shoot = Shoot(batmovile.rect.y, shoot_sprite)
                shoots.add(shoot)
            elif event.type == KEYDOWN and event.key == K_a:
                misil = Misile(batmovile.rect.y, misile_sprite)
                misils.add(misil)


        k = pygame.key.get_pressed()

        if k[K_DOWN]:
            batmovile.move_down()
        elif k[K_UP]:
            batmovile.move_up()
        if k[K_SPACE]:
            must_draw_cannon_fire = True
            cannon_fire_tick = 0

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
        all_sprites_tuple.append(lives)


        all_sprites_tuple = check_all_sprites_off_screen(all_sprites_tuple)

        allsprites = pygame.sprite.RenderPlain(all_sprites_tuple)

        draw_background(sky_x, sky, screen)
        draw_background(background_x, bridge, screen)

        allsprites.update()

        allsprites.draw(screen)

        if must_draw_cannon_fire:
            draw_cannon_fire(cannon_fire, screen, batmovile.rect.y, cannon_fire_tick)

        if cannon_fire_tick <= 25:
            draw_cannon_fire(cannon_fire, screen, batmovile.rect.y, cannon_fire_tick)
            cannon_fire_tick += 1


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

        blocks_hit_list = pygame.sprite.spritecollide(batmovile, fuel_cans, True, pygame.sprite.collide_mask)
        if len(blocks_hit_list):
            batmovile.addFuelCan()




    pygame.quit()


if __name__ == '__main__':
    main()
