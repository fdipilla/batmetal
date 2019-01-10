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
        self.move = 9
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
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y + 40
        self.move = 15
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
    def __init__(self, sprite, game_w):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.rect.topleft = game_w + 10 , self.generate_random_y_position()
        self.move = 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((-self.move, 0))
        self.rect = newpos

    def generate_random_y_position(self):
        return random.randint(3, 8) * 5 * 10

class FuelCan(pygame.sprite.Sprite):
    def __init__(self, sprite, game_w):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.rect.topleft = game_w + 10, self.generate_random_y_position()
        self.move = 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((-self.move, 0))
        self.rect = newpos

    def generate_random_y_position(self):
        return random.randint(3, 8) * 5 * 10

class Life(pygame.sprite.Sprite):
    def __init__(self, sprite, game_w):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        screen = pygame.display.get_surface()
        self.rect.topleft = game_w + 10, self.generate_random_y_position()
        self.move = 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((-self.move, 0))
        self.rect = newpos

    def generate_random_y_position(self):
        return random.randint(3, 8) * 5 * 10



class Misile(pygame.sprite.Sprite):
    def __init__(self, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.get_image(0,0,145,75)
        self.spritesheet = spritesheet
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y
        self.move = 15
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
        self.rect.topleft = 300, self.y - 50
        self.animation_tick += 1

class Shock(pygame.sprite.Sprite):
    def __init__(self, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_h = 221
        self.sprite_w = 952
        self.image = spritesheet.get_image(0,0,self.sprite_w,self.sprite_h)
        self.spritesheet = spritesheet
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y
        self.move = 15
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_tick = 0
        self.spritesheet = spritesheet
        self.y = y


    def update(self):
        screen = pygame.display.get_surface()
        if self.animation_tick >= 23:
            self.kill()

        self.animate()

    def animate(self):
        screen = pygame.display.get_surface()
        tick = self.animation_tick

        self.image = self.spritesheet.get_image(0,self.sprite_h * tick,self.sprite_w,self.sprite_h)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = 300, self.y - 50
        self.animation_tick += 1

class Batarang(pygame.sprite.Sprite):
    def __init__(self, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_h = 344
        self.sprite_w = 1138
        self.image = spritesheet.get_image(0,0,self.sprite_w,self.sprite_h)
        self.spritesheet = spritesheet
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        # Maybe do not use magic numbers
        self.rect.topleft = 200, y
        self.move = 15
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_tick = 0
        self.spritesheet = spritesheet
        self.y = y


    def update(self):
        screen = pygame.display.get_surface()
        if self.animation_tick >= 17:
            self.kill()

        self.animate()

    def animate(self):
        screen = pygame.display.get_surface()
        tick = self.animation_tick

        self.image = self.spritesheet.get_image(0,self.sprite_h * tick,self.sprite_w,self.sprite_h)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = 50, self.y - 200
        self.animation_tick += 1

class SpriteSheet(object):
    def __init__(self, image):
        self.sprite_sheet = image


    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(image.get_at((0,0)), RLEACCEL)

        return image

def draw_background(x, bridge, screen):
    rel_x = x % bridge.get_rect().width
    screen.blit(bridge, (rel_x - bridge.get_rect().width, 0))
    w, h = pygame.display.get_surface().get_size()
    if rel_x < w:
        screen.blit(bridge, (rel_x, 0))

def draw_bottom_bar(screen, bar):
    w, h = pygame.display.get_surface().get_size()
    bar = pygame.transform.scale(bar, (w, 92))
    bar_w, bar_h = bar.get_size()
    screen.blit(bar, (w - bar_w, h - bar_h))

def draw_bathead(screen, bathead, lives):
    w, h = pygame.display.get_surface().get_size()
    w_displacement = ((48.5*w) / 100)
    sprite_w, sprite_h = (55, 52)
    image = bathead.get_image(0,sprite_h * lives,sprite_w,sprite_h)
    screen.blit(image, (w_displacement, h - sprite_h - 10))

def draw_fuel(screen, spritesheet, fuel):
    w, h = pygame.display.get_surface().get_size()
    sprite_h = 30
    sprite_w = 58

    if fuel >= 2500:
        sprite = 4
    elif fuel >= 2000:
        sprite = 3
    elif fuel >= 1500:
        sprite = 2
    elif fuel >= 1000:
        sprite = 1
    else:
        sprite = 0

    image = spritesheet.get_image(0,sprite_h * sprite,sprite_w,sprite_h)

    w_displacement = ((38 * w) / 100)
    screen.blit(image, (w_displacement, h - sprite_h - 20))


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
def check_all_sprites_off_screen(sprites_groups, game_w):
    max_w = game_w + 100
    for sprites_group in sprites_groups:
        if not isinstance(sprites_group, Player):
            for sprite in sprites_group:
                if sprite.rect.x <= -100 or sprite.rect.x >= max_w:
                    sprites_group.remove(sprite)
    return sprites_groups

def main():
    pygame.init()
    game_w = 1200
    game_h = 600
    screen = pygame.display.set_mode((game_w, game_h))
    pygame.display.set_caption('batmetal')
    pygame.mouse.set_visible(0)
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()

    batmovile = Player()

    background_x = 0
    sky_x = 0

    bridge = load_image('bridge.png', -1)
    sky = load_image("sky.png")
    bottom_bar = load_image("bottom_bar2.png")
    cannon_fire_0 = load_image("shoot_0.png", -1)
    cannon_fire_1 = load_image("shoot_1.png", -1)
    cannon_fire_2 = load_image("shoot_2.png", -1)
    cannon_fire_3 = load_image("shoot_3.png", -1)
    cannon_fire = [cannon_fire_0, cannon_fire_1, cannon_fire_2, cannon_fire_3]

    misile_sprite_image = load_image("misile_animation.png",-1)
    misile_sprite_sheet = SpriteSheet(misile_sprite_image)

    shock_sprite_image = load_image("shock_spritesheet.png",-1)
    shock_sprite_sheet = SpriteSheet(shock_sprite_image)

    batarang_sprite_image = load_image("bata_spritesheet.png",-1)
    batarang_sprite_sheet = SpriteSheet(batarang_sprite_image)

    shoot_sprite = load_image("shoot.png", -1)
    can_sprite = load_image("can.png", -1)
    fuel_can_sprite = load_image("fuel_can.png", -1)
    life_sprite = load_image("life.png", -1)

    bathead_sprite_image = load_image("bathead_spritesheet.png",-1)
    bathead_sprite_sheet = SpriteSheet(bathead_sprite_image)
    
    fuel_sprites_image = load_image("fuel_spritesheet.png")
    fuel_sprites = SpriteSheet(fuel_sprites_image)

    shoots = pygame.sprite.Group()
    misils = pygame.sprite.Group()
    shock = pygame.sprite.Group()
    batarang = pygame.sprite.Group()
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
                    misil = Misile(batmovile.rect.y, misile_sprite_sheet)
                    misils.add(misil)
            elif event.type == KEYDOWN and event.key == K_s:
                if len(shock) == 0:
                    new_sock = Shock(batmovile.rect.y, shock_sprite_sheet)
                    shock.add(new_sock)
            elif event.type == KEYDOWN and event.key == K_d:
                if len(batarang) == 0:
                    new_batarang = Batarang(batmovile.rect.y, batarang_sprite_sheet)
                    batarang.add(new_batarang)


        k = pygame.key.get_pressed()

        if k[K_DOWN]:
            batmovile.move_down()
        elif k[K_UP]:
            batmovile.move_up()

        # 1/20 chances to generate a can and only two cans on the screen
        # this method is actually prety bad
        random_number = random.randint(1, 20)
        if len(cans) <= 1 and int(random_number) == 1:
            can = Can(can_sprite, game_w)
            cans.add(can)

        # 1/500 chances to generate a fuel can
        # this method is actually prety bad
        random_number = random.randint(1, 500)
        if len(fuel_cans) <= 0 and int(random_number) == 1:
            fuel_can = FuelCan(fuel_can_sprite, game_w)
            fuel_cans.add(fuel_can)

        # 1/500 chances to generate life
        # this method is actually prety bad
        random_number = random.randint(1, 500)
        if len(lives) <= 0 and int(random_number) == 3:
            life = Life(life_sprite, game_w)
            lives.add(life)


        all_sprites_tuple.append(batmovile)
        all_sprites_tuple.append(cans)
        all_sprites_tuple.append(fuel_cans)
        all_sprites_tuple.append(misils)
        all_sprites_tuple.append(shoots)
        all_sprites_tuple.append(shock)
        all_sprites_tuple.append(batarang)
        all_sprites_tuple.append(lives)


        all_sprites_tuple = check_all_sprites_off_screen(all_sprites_tuple, game_w)

        allsprites = pygame.sprite.RenderPlain(all_sprites_tuple)

        draw_background(sky_x, sky, screen)
        draw_background(background_x, bridge, screen)

        allsprites.update()

        allsprites.draw(screen)

        draw_bottom_bar(screen, bottom_bar)
        draw_bathead(screen, bathead_sprite_sheet, batmovile.lives)
        draw_fuel(screen, fuel_sprites, batmovile.fuel)

        pygame.display.flip()

        background_x -= 10
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
