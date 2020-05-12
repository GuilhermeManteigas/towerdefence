import pygame

#window = pygame.display.set_mode([1366, 768])
#w = pygame.Surface([1920, 1080])
window = pygame.display.set_mode([192, 108])
w = pygame.Surface([192, 108])

def draw():
    frame = pygame.transform.scale(w, (192, 108))
    window.blit(frame, frame.get_rect())
    pygame.display.flip()

white = (255, 255, 255)
closed = False
while not closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

    w.fill(white)
    w.blit(pygame.image.load('player.png'), (96, 54))


    draw()


pygame.quit()
quit()
