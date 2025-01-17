import pygame
from enemy import Enemy

class Tower:
    def __init__(self, image, posx, posy):
        self.image = image
        self.ammunition = pygame.image.load('arrow.png')
        self.posx = posx
        self.posy = posy
        self.level = 0
        self.tower_height = 25
        self.tower_width = 25
        self.range = 150
        self.fire_rate = 1
        self.mouseover = False
        self.target = Enemy(self.image, 0, 0)
        #self.rect = self.image.get_rect()
        #self.rect = pygame.Rect(0, 0, self.range, self.range)
        #self.rect.center = self.posx, self.posy


    def levelup(self):
        if self.level == 0:
            self.image = pygame.image.load('tower.png')
            #self.tower_height = self.tower_height * 3
            self.level += 1


