
class Enemy:
    def __init__(self, image, posx, posy):
        self.image = image
        self.posx = posx
        self.posy = posy
        self.level = 0
        self.health = 2
        self.damage = 5
        self.speed = 0.2
        self.reward = 5
        self.rect = self.image.get_rect()
        self.rect.center = self.posx, self.posy

