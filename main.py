import pygame
import math
import threading
import time
from bullet import Bullet
from tower import Tower
from enemy import Enemy
import sys
from pygame.locals import *

pygame.init()

monitor_info = pygame.display.Info()
display_width = 640#monitor_info.current_w #800
display_height = 360#monitor_info.current_h #600
FPS = 120
scale_multiplier = 1
game_tick = 0.01
gameDisplay = pygame.Surface([640, 360])
pygame.display.set_caption('Tower defence')

black = (0, 0, 0)
white = (255, 255, 255)
transparent = (0, 255, 255, 255)
red = (255, 0, 0)


clock = pygame.time.Clock()
closed = False
personImg = pygame.image.load('player.png')
enemyImg = pygame.image.load('enemy.png')
bulletImg = pygame.image.load('bullet.png')
towerplaceholderImg = pygame.image.load('towerplaceholder.png')
towerplaceholdermouseoverImg = pygame.image.load('towerplaceholder_mouseover.png')
cursorImg = pygame.image.load('cursor.png')


###########################################
#######         Map creation        #######
###########################################
tower_placeholder_list = []

px = int(display_width/4)
py = int(display_height/4)
tower = Tower(towerplaceholderImg, px, py)
tower_placeholder_list.append(tower)

px = int(display_width/4)
py = int(display_height - display_height/4)
tower = Tower(towerplaceholderImg, px, py)
tower_placeholder_list.append(tower)

px = int(display_width - display_width/4)
py = int(display_height/4)
tower = Tower(towerplaceholderImg, px, py)
tower_placeholder_list.append(tower)

px = int(display_width - display_width/4)
py = int(display_height - display_height/4)
tower = Tower(towerplaceholderImg, px, py)
tower_placeholder_list.append(tower)




###########################################


def mouse_angle(x, y):
    mouse_x, mouse_y = get_mouse_position()
    #mouse_x, mouse_y = pygame.mouse.get_pos()
    #mouse_x = mouse_x / scale_multiplier
    #mouse_y = mouse_y / scale_multiplier
    angle = math.atan2(x - mouse_x+13, y - mouse_y+10)
    return angle


def rotate_image_by_angle(img, angle):
    orig_rect = img.get_rect()
    rot_image = pygame.transform.rotate(img, angle * 55)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def person(x, y):
    angle = mouse_angle(x, y)
    #img = pygame.transform.rotate(personImg, angle*55)
    rot_image = rotate_image_by_angle(personImg, angle)

    gameDisplay.blit(rot_image, (x, y))

############# Y = MX + b


def update_bullets_position():
    while True:
        #print("bulet pos updated")
        for b in bullet_list:
            if 0 < b.posx < display_width and 0 < b.posy < display_height:
                b.posx = b.posx + (b.speed * (-math.sin(b.angle)))
                b.posy = b.posy + (b.speed * (-math.cos(b.angle)))
            else:
                bullet_list.pop(bullet_list.index(b))
        time.sleep(game_tick)


def update_bullets():
    for b in bullet_list:
        if 0 < b.posx < display_width and 0 < b.posy < display_height:
            gameDisplay.blit(b.image, (b.posx, b.posy))
        else:
            bullet_list.pop(bullet_list.index(b))


def update_placeholder_towers():
    for t in tower_placeholder_list:
        rect = t.image.get_rect()
        rect.center = t.posx, t.posy
        gameDisplay.blit(t.image, rect)
        if t.mouseover:
            pygame.draw.circle(gameDisplay, red, (t.posx, t.posy), t.range, 1)




def update_screen():
        person(x, y)
        update_bullets()
        update_placeholder_towers()

button_pressed = False

def auto_shoot():
    while button_pressed:
        bullet = Bullet(rotate_image_by_angle(bulletImg, mouse_angle(x, y)), x, y, mouse_angle(x, y), 5)
        bullet_list.append(bullet)
        time.sleep(0.1)

x = int(display_width * 0.5)
y = int(display_height * 0.5)
bullet_list = []

FPS_FONT = pygame.font.SysFont("Verdana", 20)
GOLDENROD = pygame.Color("goldenrod")


def show_fps(window, clock):
    fps_overlay = FPS_FONT.render(str(clock.get_fps()), True, GOLDENROD)
    window.blit(fps_overlay, (0, 0))

def mouse_pointer():
    pygame.mouse.set_visible(True)
    pointerImg_rect = cursorImg.get_rect()
    #mouse_x, mouse_y = pygame.mouse.get_pos()
    #mouse_x = mouse_x / scale_multiplier
    #mouse_y = mouse_y / scale_multiplier
    pointerImg_rect.center = get_mouse_position()
    gameDisplay.blit(cursorImg, pointerImg_rect)


def upscale_screen():
    w = int(640 * scale_multiplier)
    h = int(360 * scale_multiplier)
    #print(w)
    #print(h)
    window = pygame.display.set_mode((w, h))
    frame = pygame.transform.scale(gameDisplay, (w, h))
    window.blit(frame, frame.get_rect())
    pygame.display.flip()
    #pygame.display.update()

def get_mouse_position():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = mouse_x / scale_multiplier
    mouse_y = mouse_y / scale_multiplier
    return mouse_x, mouse_y

enemy_list = []

def is_enemy_in_range():
    for t in tower_placeholder_list:
        for e in enemy_list:
            if math.sqrt((t.posx - e.posx) ^ 2 + (t.posy - e.posy) ^ 2) <= t.range:
                print("atack")

def create_enemy():
    enemy = Enemy(enemyImg, display_width, display_height/2)




#threading.Thread(target=update_bullets_position()).start()
update = threading.Thread(target=update_bullets_position)
update.start()

fullscreen = False

while not closed:

    gameDisplay.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not button_pressed:
            mouse_x, mouse_y = get_mouse_position()
            notTower = True
            for t in tower_placeholder_list:
                if t.posx - t.tower_width/2 < mouse_x < t.posx + t.tower_width/2 and t.posy - t.tower_height/2 < mouse_y < t.posy + t.tower_height/2:
                    t.levelup()
                    notTower = False
                    break
            if notTower:
                button_pressed = True
                bullet = Bullet(rotate_image_by_angle(bulletImg, mouse_angle(x, y)), x, y, mouse_angle(x, y), 5)
                bullet_list.append(bullet)
                btndown = threading.Thread(target=auto_shoot)
                btndown.start()
                #print(math.degrees(mouse_angle(x, y)) % 360)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = get_mouse_position()
            for t in tower_placeholder_list:
                if t.level == 0:
                    if t.posx - t.tower_width/2 < mouse_x < t.posx + t.tower_width/2 and t.posy - t.tower_height/2 < mouse_y < t.posy + t.tower_height/2:
                        t.image = towerplaceholdermouseoverImg
                    else:
                        t.image = towerplaceholderImg
                elif t.level > 0:
                    if t.posx - t.tower_width / 2 < mouse_x < t.posx + t.tower_width / 2 and t.posy - t.tower_height / 2 < mouse_y < t.posy + t.tower_height / 2:
                        t.mouseover = True
                    else:
                        t.mouseover = False
                        #pygame.draw.circle(gameDisplay, red, (t.posx, t.posy), 200, 1)
                        #print((t.posx, t.posy))

        #elif event.type == pygame.VIDEORESIZE:
            #old_surface_saved = gameDisplay
            #gameDisplay = pygame.display.set_mode((event.w, event.h),
             #                                 pygame.RESIZABLE)
            # On the next line, if only part of the window
            # needs to be copied, there's some other options.
            #gameDisplay.blit(old_surface_saved, (0, 0))
            #del old_surface_saved
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                scale_multiplier = 2
            if event.key == pygame.K_2:
                scale_multiplier = 2.4
            if event.key == pygame.K_3:
                scale_multiplier = 2.5
            if event.key == pygame.K_4:
                scale_multiplier = 3





        #print(event)


    update_screen()




    mouse = threading.Thread(target=mouse_pointer)
    mouse.start()


    show_fps(gameDisplay, clock)

    #pygame.display.update()
    upscale_screen()


    clock.tick(FPS)


pygame.quit()
quit()
