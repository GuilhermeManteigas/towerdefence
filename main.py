import pygame
import math
from bullet import Bullet

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
        b.posx = b.posx + (b.speed * (-math.sin(b.angle)))
        b.posy = b.posy + (b.speed * (-math.cos(b.angle)))
        gameDisplay.blit(b.image, (b.posx, b.posy))


x = int(display_width * 0.5)
y = int(display_height * 0.5)
bullet_list = []

while not closed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(rotate_image_by_angle(bulletImg, mouse_angle(x, y)), x, y, mouse_angle(x, y), 2)
            bullet_list.append(bullet)
            print(math.degrees(mouse_angle(x, y)) % 360)



        #print(event)


    gameDisplay.fill(white)
    person(x, y)
    update_bullets()



    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()
