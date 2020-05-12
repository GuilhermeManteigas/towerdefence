import pygame


class Tower:
    def __init__(self, image, posx, posy):
        self.image = image
        self.posx = posx
        self.posy = posy
        self.level = 0
        self.tower_height = 25
        self.tower_width = 25
        self.range = 100
        self.mouseover = False

    def levelup(self):
        if self.level == 0:
            self.image = pygame.image.load('tower.png')
            self.tower_height = self.tower_height * 3
            self.level += 1


