#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import random

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]

# despues meter las imagenes en una carpeta separada
img_dir = os.path.join(main_dir, '')

def load_image(name, colorkey=None):
    fullname = os.path.join(img_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('batmovile.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = 9
        self.dizzy = 0

    def update(self):
        return True

    def move_down(self):
        self.rect = self.rect.move((0,self.move))

    def move_up(self):
        self.rect = self.rect.move((0,-self.move))


class Shoot(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('shoot.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y + 40
        self.move = 15
        self.dizzy = 0

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((self.move, 0))
        self.rect = newpos

class Can(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('can.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 850, self.generate_random_y_position()
        self.move = 10
        self.dizzy = 0

    def update(self):
        self._move()

    def off_the_screen(self):
        return self.rect.x <= 0

    def _move(self):
        newpos = self.rect.move((-self.move, 0))
        self.rect = newpos

    def generate_random_y_position(self):
        return random.randint(3, 10) * 5 * 10


class Misile(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('misil.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Maybe do not use magic numbers
        self.rect.topleft = 300, y + 40
        self.move = 15
        self.dizzy = 0

    def update(self):
        self._move()

    def _move(self):
        newpos = self.rect.move((self.move, 0))
        self.rect = newpos

def draw_background(x, bridge, screen):
    rel_x = x % bridge.get_rect().width
    screen.blit(bridge, (rel_x - bridge.get_rect().width, 0))
    w, h = pygame.display.get_surface().get_size()
    if rel_x < w:
        screen.blit(bridge, (rel_x, 0))

def draw_cannon_fire(fire, screen, y):
    # Maybe do not use magic numbers
    screen.blit(fire, (340, y + 30))
    
def check_cans_position(cans):
    for can in cans:
        if can.off_the_screen():
            cans.remove(can)
    return cans

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('batmetal')
    pygame.mouse.set_visible(0)

    clock = pygame.time.Clock()

    batmovile = Player()

    all_sprites_tuple = [batmovile]
    allsprites = pygame.sprite.RenderPlain(all_sprites_tuple)
    background_x = 0

    bridge = pygame.image.load("bridge.png").convert()
    cannon_fire = pygame.image.load("cannon_fire.png").convert_alpha()

    shoots = []
    misils = []
    cans = []

    going = True
    while going:
        clock.tick(60)
        must_draw_cannon_fire = False

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                shoot = Shoot(batmovile.rect.y)
                all_sprites_tuple.append(shoot)
                shoots.append(shoot)
            if event.type == KEYDOWN and event.key == K_a:
                misil = Misile(batmovile.rect.y)
                all_sprites_tuple.append(misil)
                misils.append(misil)


        k = pygame.key.get_pressed()

        if k[K_DOWN]:
            batmovile.move_down()
        if k[K_UP]:
            batmovile.move_up()
        if k[K_SPACE]:
            must_draw_cannon_fire = True

        # 1/20 chances to generate a can and only two cans on the screen
        # this method is actually prety bad
        random_number = random.randint(1, 20)
        if len(cans) <= 1 and int(random_number) == 1:
            can = Can()
            all_sprites_tuple.append(can)
            cans.append(can)

        # if one of the cans is off the screen I remove it from the list
        cans = check_cans_position(cans)

        allsprites = pygame.sprite.RenderPlain(all_sprites_tuple)

        draw_background(background_x, bridge, screen)
        allsprites.update()

        allsprites.draw(screen)

        if must_draw_cannon_fire:
            draw_cannon_fire(cannon_fire, screen, batmovile.rect.y)


        pygame.display.flip()

        background_x -= 5

    pygame.quit()


if __name__ == '__main__':
    main()
