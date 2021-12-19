import os
try:
    import pygame
except ImportError:
    os.system('pip install pygame')
import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()
font40 = pygame.font.Font('assets/fonts/Lovelo.otf', 40)

w, h = 1200, 800
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('AquaShield')

bg = pygame.image.load('assets/backgrounds/bgo.png')
go = pygame.image.load('assets/backgrounds/goo.png')

fish64 = pygame.image.load(f'assets/fish/fish{random.randrange(1, 7)}.png')
swatch = pygame.image.load('assets/icons/stopwatch.png')
quit = pygame.image.load('assets/icons/quit.png')
q_rect = quit.get_rect()
q_rect.left, q_rect.top = 1126, 10

pygame.display.set_icon(fish64)

pygame.mouse.set_visible(False)

timer = 0
t = 0

playing = True
bagspeed = [200, 300]
fishnum = 30

def fmt_time(t):
    millis = t % 1000
    seconds = int(t / 1000 % 60)
    minutes = int(t / 60000 % 24)
    return f'{minutes:02d}:{seconds:02d}.{str(millis)[:2]}'


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    pygame.font.init()
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    pygame.font.init()
    pygame.init()
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        if y + fontHeight > rect.bottom:
            break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left + 15, y))
        y += fontHeight + lineSpacing
        text = text[i:]
    return text

def play_music(music, vol):
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play(-1)

def fmt_text(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, True, textColor)

    return newText

f = open('assets/facts.txt', 'r')
lines = f.readlines()
dyktext = random.choice(lines)
dyktext2 = random.choice(lines)
f.close()


def main_menu():
    global st
    play_music('assets/sound/mmmusic.mp3',0.1)
    breakflag = False
    mm = pygame.image.load('assets/backgrounds/mainmenu.png')
    clicky = pygame.image.load('assets/icons/clicker.png')
    clicky_rect = clicky.get_rect()
    pygame.mouse.set_visible(True)
    while True:
        screen.blit(mm, (0, 0))
        mouse = pygame.mouse.get_pos()
        if 796 < mouse[0] < 1134 and 222 < mouse[1] < 333:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)
            clicky_rect.center = mouse
            screen.blit(clicky, clicky_rect)
        else:
            if not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 796 < mouse[0] < 1134 and 222 < mouse[1] < 333:
                    st = pygame.time.get_ticks()
                    pygame.mouse.set_visible(False)
                    breakflag = True

        if breakflag:
            break

        drawText(screen, dyktext, (255, 255, 255), pygame.Rect(0, 680, 1200, 80),font40)
        pygame.display.flip()

def pre_over(t):
    breakflag = False
    pygame.mouse.set_visible(True)
    font = pygame.font.Font('assets/fonts/Lovelo.otf', 80)
    ren = font.render(t, True   , (255, 255, 255))
    clicky = pygame.image.load('assets/icons/clicker.png')
    clicky_rect = clicky.get_rect()
    while True:
        screen.blit(go, (0, 0))
        screen.blit(ren, ren.get_rect(left=612, top=80))
        mouse = pygame.mouse.get_pos()
        if 45 < mouse[0] < 1155 and 250 < mouse[1] < 445:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)
            clicky_rect.center = mouse
            screen.blit(clicky, clicky_rect)
        else:
            if not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                breakflag = True
        if breakflag:
            break
        pygame.display.flip()
    breakflag = False
    game_over()

def game_over():
    breakflag = False
    play_music('assets/sound/mmmusic.mp3',0.1)
    pygame.mouse.set_visible(True)
    clicky = pygame.image.load('assets/icons/clicker.png')
    clicky_rect = clicky.get_rect()
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(pygame.image.load('assets/backgrounds/gameover.png'), (0, 0))
        if (638 < mouse[0] < 1148 and 211 < mouse[1] < 295) or (930 < mouse[0] < 1161 and 354 < mouse[1] < 439):
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)
            clicky_rect.center = mouse
            screen.blit(clicky, clicky_rect)
        else:
            if not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 638 < mouse[0] < 1148 and 211 < mouse[1] < 295:
                    setup()
                    breakflag = True
                if 930 < mouse[0] < 1161 and 354 < mouse[1] < 439:
                    pygame.quit()

        if breakflag:
            break

        drawText(screen, dyktext2, (255, 255, 255), pygame.Rect(0, 680, 1200, 80),font40)
        pygame.display.flip()


class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load(f'assets/fish/fish{random.randrange(1, 7)}.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.x <= 0 or self.rect.x >= 1180:
            self.speed = -self.speed
            self.image = pygame.transform.flip(self.image, True, False)

        if self.rect.y <= 560:
            self.rect.y += 10

        if self.rect.y >= 760:
            self.rect.y -= 10

        if random.random() <= 0.1:
            if random.random() >= 0.5:
                self.rect.y += 3
            else:
                self.rect.y -= 3

        if len(fish_group) > fishnum:
            self.kill()


def fish_initialize(grp):
    for _ in range(fishnum):
        fi = Fish(random.randint(30, 1170), random.randint(550, 760), 0)
        if random.choice([0, 1]):
            fi.image = pygame.image.load(f'assets/fish/fish{random.randrange(1, 7)}.png')
            fi.speed = random.randrange(5, 9)
        else:
            fi.image = pygame.transform.flip(pygame.image.load(f'assets/fish/fish{random.randrange(1, 7)}.png'), True,
                                             False)
            fi.speed = -(random.randrange(5, 9))
        grp.add(fi)


def remove_fish(num):
    global fishnum
    fishnum -= num


class Trash(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load(f'assets/trash/trash{random.randrange(1, 7)}.png'),
                                             random.randrange(-45, 45))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.y >= 500:
            try:
                chan = pygame.mixer.find_channel()
                chan.set_volume(0.1)
                chan.play(pygame.mixer.Sound(f'assets/sound/splash{random.randrange(1, 3)}.mp3'))
            except Exception:
                pass
            self.kill()
            create_bags(1, bagspeed, trash_group)
            remove_fish(random.randrange(1, 4))
            if fishnum <= 0:
                a = t
                pre_over(fmt_time(a))


def create_bags(num, speedlis, grp):
    for _ in range(num):
        speed = random.randrange(speedlis[0], speedlis[1]) / 100
        tr = Trash(random.randrange(300, 1180), random.randrange(-100, 0),speed)
        grp.add(tr)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.img = pygame.image.load(image)
        self.clicker = pygame.image.load('assets/icons/clicker.png')
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def update(self):
        mouse = pygame.mouse.get_pos()
        self.rect.center = mouse
        if 1126 < mouse[0] < 1200 and 0 < mouse[1] < 74:
            self.image = self.clicker
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_over()
        else:
            self.image = self.img
        col = pygame.sprite.spritecollide(cr, trash_group, False)
        if col:
            try:
                pygame.mixer.find_channel().play(pygame.mixer.Sound(f'assets/sound/crush{random.randrange(1, 3)}.mp3'))
            except Exception:
                pass
            for i in col:
                i.kill()
                create_bags(1, bagspeed, trash_group)



cr = Cursor(f'assets/icons/bin.png')
cursorgroup = pygame.sprite.Group()
cursorgroup.add(cr)

trash_group = pygame.sprite.Group()
create_bags(4, bagspeed, trash_group)

fish_group = pygame.sprite.Group()
fish_initialize(fish_group)


def setup():
    global timer, trash_group, bagspeed, fish_group, fishnum, t, st
    pygame.mouse.set_visible(False)
    play_music('assets/sound/bgocean.mp3',0.5)
    timer = 0
    t = 0
    st = pygame.time.get_ticks()
    bagspeed = [200, 300]
    fishnum = 30
    fish_group = pygame.sprite.Group()
    fish_initialize(fish_group)
    trash_group = pygame.sprite.Group()
    create_bags(4, bagspeed, trash_group)

main_menu()
play_music('assets/sound/bgocean.mp3',0.5)
while playing:
    screen.blit(bg, (0, 0))
    screen.blit(fish64, (10, 5))
    screen.blit(fmt_text(str(len(fish_group)), 'assets/fonts/Lovelo.otf', 70, (255, 255, 255)), (90, 10))
    screen.blit(swatch, (10, 85))
    screen.blit(fmt_text(fmt_time(t), 'assets/fonts/Lovelo.otf', 50, (255, 255, 255)), (80, 100))

    trash_group.draw(screen)
    trash_group.update()
    screen.blit(quit, (q_rect))

    cursorgroup.draw(screen)
    cursorgroup.update()

    fish_group.draw(screen)
    fish_group.update()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    dt = clock.tick(60)
    timer += dt
    t = pygame.time.get_ticks() - st

    if timer > 1000:
        bagspeed[0] += 10
        bagspeed[1] += 15
        timer = 0

    pygame.display.flip()
