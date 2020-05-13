#import random

class Bullet:
    def __init__(self, image, posx, posy, angle, speed):
        #print("bullet created")
        #self.id = random.randint(0, 90000)
        self.image = image
        self.posx = posx
        self.posy = posy
        self.angle = angle
        self.speed = speed
        self.damage = 1
        self.rect = self.image.get_rect()
        self.rect.center = self.posx, self.posy

