import pygame
import math
import threading
import time
from bullet import Bullet
from tower import Tower
from enemy import Enemy
import cProfile

pygame.init()

monitor_info = pygame.display.Info()
display_width = 640
display_height = 360
upscale_rez_w = 640
upscale_rez_h = 360
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


window = pygame.display.set_mode((display_width, display_height))

if monitor_info.current_w == 1920 and monitor_info.current_h == 1080:
    False
    #scale_multiplier = 3


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
    rot_image = rotate_image_by_angle(personImg, angle)
    gameDisplay.blit(rot_image, (x, y))


def update_bullets_position():
    while True:
        for b in bullet_list:
            if 0 < b.posx < display_width and 0 < b.posy < display_height:
                b.posx = b.posx + (b.speed * (-math.sin(b.angle)))
                b.posy = b.posy + (b.speed * (-math.cos(b.angle)))
                b.rect.center = int(b.posx), int(b.posy)
                #print(b.posx)
                #print((b.speed * (-math.sin(b.angle))))
            else:
                bullet_list.pop(bullet_list.index(b))
        time.sleep(game_tick)


def detect_bullet_colision():
    while True:
        for e in enemy_list:
            for index, b in enumerate(bullet_list):
                if pygame.sprite.collide_rect(b, e):
                    print(pygame.sprite.collide_rect(b, e))
                    e.health -= b.damage
                    bullet_list.pop(index)
                    if e.health <= 0:
                        enemy_list.pop(enemy_list.index(e))
                break
        #print("Done! list = " + str(len(bullet_list)))
        time.sleep(game_tick)



def update_bullets():
    for b in bullet_list:
        if 0 < b.posx < display_width and 0 < b.posy < display_height:
            gameDisplay.blit(b.image, (int(b.posx), int(b.posy)))
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
    update_enemies()
    update_placeholder_towers()

button_pressed = False


def auto_shoot():
    while button_pressed:
        #bullet = Bullet(rotate_image_by_angle(bulletImg, mouse_angle(x, y)), x, y, mouse_angle(x, y), 5)
        #bullet_list.append(bullet)
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
    pointerImg_rect.center = get_mouse_position()
    gameDisplay.blit(cursorImg, pointerImg_rect)


def upscale_processing(w,h,window):
    frame = pygame.transform.scale(gameDisplay, (w, h))
    window.blit(frame, frame.get_rect())
    pygame.display.flip()

def change_resolution():
    upscale_rez_w = int(640 * scale_multiplier)
    upscale_rez_h = int(360 * scale_multiplier)
    print(upscale_rez_w)
    window = pygame.display.set_mode((upscale_rez_w, upscale_rez_h))
    #if upscale_rez_w == monitor_info.current_w:
        #window = pygame.display.set_mode((upscale_rez_w, upscale_rez_h), pygame.FULLSCREEN)
    #else:
        #window = pygame.display.set_mode((upscale_rez_w, upscale_rez_h))

def upscale_screen():
    show_fps(gameDisplay, clock)
    #mouse = threading.Thread(target=mouse_pointer)
    #mouse.start()
    mouse_pointer()
    update_screen()
    w = int(640 * scale_multiplier)
    h = int(360 * scale_multiplier)
    #if w == monitor_info.current_w:
        #window = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    #else:
        #window = pygame.display.set_mode((w, h))
    #upscale = threading.Thread(target=upscale_processing, args=(w,h,window,))
    #upscale.start()
    #print(upscale_rez_w)
    frame = pygame.transform.scale(gameDisplay, (w, h))
    window.blit(frame, frame.get_rect())
    pygame.display.flip()

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
    while True:
        #print("creating")
        enemy = Enemy(enemyImg, display_width, display_height/2)
        enemy_list.append(enemy)
        time.sleep(game_tick*1000)

def update_enemies_position():
    while True:
        #print("updating position")
        for e in enemy_list:
            if e.posx != (display_width/2) or e.posy != display_height/2:
                e.posx = e.posx + (e.speed * (-math.sin(math.atan2(e.posx - x, e.posy - y))))
                e.posy = e.posy + (e.speed * (-math.cos(math.atan2(e.posx - x, e.posy - y))))
                e.rect.center = int(e.posx), int(e.posy)
            else:
                enemy_list.pop(enemy_list.index(e))
        time.sleep(game_tick)


def update_enemies():
    #print("update image")
    for e in enemy_list:
        if e.posx != display_width/2 or e.posy != display_height/2:
            gameDisplay.blit(e.image, (int(e.posx), int(e.posy)))

def tower_search_enemy():
    while True:
        detected_list = []
        for t in tower_placeholder_list:
            if t.level > 0:
                for e in enemy_list:
                    print(e.posx)
                    print(e.posy)
                    print(math.sqrt(abs(int(t.posx - e.posx) * int(t.posx - e.posx) + int(t.posy - e.posy) * int(t.posy - e.posy))))
                    if math.sqrt(abs(int(t.posx - e.posx) * int(t.posx - e.posx) + int(t.posy - e.posy) * int(t.posy - e.posy))) <= t.range: #pygame.sprite.collide_rect(t, e):
                        detected_list.append(e)
                        #print("detected")
                if len(detected_list) > 0:
                    closest = detected_list[0]
                    for idx, e in enumerate(detected_list):
                        if idx > 0:
                            #test = math.sqrt(-1)
                            #one = math.sqrt(abs(int(x - closest.posx) ^ 2 + int(y - closest.posy) ^ 2))
                            #two = math.sqrt(abs(int(x - e.posx) ^ 2 + int(y - e.posy) ^ 2))
                            #three = one > two
                            if math.sqrt(abs(int(x - closest.posx) ^ 2 + int(y - closest.posy) ^ 2)) > math.sqrt(abs(int(x - e.posx) ^ 2 + int(y - e.posy) ^ 2)):
                                closest = e

                    bullet = Bullet(rotate_image_by_angle(bulletImg, math.atan2(t.posx - closest.posx, t.posy - closest.posy)), t.posx, t.posy, math.atan2(t.posx - closest.posx, t.posy - closest.posy), 5)
                    bullet_list.append(bullet)
                    print("fired")

        # e.posx = e.posx + (e.speed * (-math.sin(math.atan2(e.posx - x, e.posy - y))))
        # e.posy = e.posy + (e.speed * (-math.cos(math.atan2(e.posx - x, e.posy - y))))
        # e.rect.center = int(e.posx), int(e.posy)

        time.sleep(1)



#threading.Thread(target=update_bullets_position()).start()
bullet_updates = threading.Thread(target=update_bullets_position)
bullet_updates.start()
detect_colision = threading.Thread(target=detect_bullet_colision)
detect_colision.start()
enemy_updates = threading.Thread(target=update_enemies_position)
enemy_updates.start()
enemy_creator = threading.Thread(target=create_enemy)
enemy_creator.start()
tower_detection = threading.Thread(target=tower_search_enemy)
tower_detection.start()

fullscreen = False

scale_multiplier = 1
change_resolution()
while not closed:
    #print(len(bullet_list))
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                scale_multiplier = 2
                change_resolution()
            if event.key == pygame.K_2:
                scale_multiplier = 2.4
                change_resolution()
            if event.key == pygame.K_3:
                scale_multiplier = 2.5
                change_resolution()
            if event.key == pygame.K_4:
                scale_multiplier = 3
                change_resolution()





        #print(event)


    #update_screen()




    #mouse = threading.Thread(target=mouse_pointer)
    #mouse.start()


    #show_fps(gameDisplay, clock)

    #pygame.display.update()

    upscale = threading.Thread(target=upscale_screen)
    upscale.run()

    #cProfile.run('upscale.run()')
    #upscale_screen()

    #clock.tick(5)
    clock.tick(FPS)


pygame.quit()
quit()
