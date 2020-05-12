import pygame
import math
import threading
import time
from bullet import Bullet
from tower import Tower

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Tower defence')

black = (0, 0, 0)
white = (255, 255, 255)


clock = pygame.time.Clock()
closed = False
personImg = pygame.image.load('player.png')
bulletImg = pygame.image.load('bullet.png')
towerplaceholderImg = pygame.image.load('towerplaceholder.png')
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
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = math.atan2(x - mouse_x, y - mouse_y)
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


def update_bullets():
    for b in bullet_list:
        if 0 < b.posx < display_width and 0 < b.posy < display_height:
            b.posx = b.posx + (b.speed * (-math.sin(b.angle)))
            b.posy = b.posy + (b.speed * (-math.cos(b.angle)))
            gameDisplay.blit(b.image, (b.posx, b.posy))
        else:
            bullet_list.pop(bullet_list.index(b))


def update_placeholder_towers():
    for t in tower_placeholder_list:
        rect = t.image.get_rect()
        rect.center = t.posx, t.posy
        gameDisplay.blit(t.image, rect)


def update_screen():
    gameDisplay.fill(white)
    person(x, y)
    update_bullets()
    update_placeholder_towers()

button_pressed = False

def auto_shoot():
    while button_pressed:
        bullet = Bullet(rotate_image_by_angle(bulletImg, mouse_angle(x, y)), x, y, mouse_angle(x, y), 5)
        bullet_list.append(bullet)
        print("a")
        time.sleep(0.1)

x = int(display_width * 0.5)
y = int(display_height * 0.5)
bullet_list = []


while not closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not button_pressed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
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




        #print(event)


    update_screen()

    pygame.mouse.set_visible(False)
    pointerImg_rect = cursorImg.get_rect()
    pointerImg_rect.center = pygame.mouse.get_pos()
    gameDisplay.blit(cursorImg, pygame.mouse.get_pos())

    pygame.display.update()
    clock.tick(120)


pygame.quit()
quit()
