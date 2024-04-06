#импорты------------------------------------------------------------------------------------------------
import pygame
import random
image_pass = ''
clock = pygame.time.Clock()
pygame.init()


#параметры экрана------------------------------------------------------------------------------------------------
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Kartashov_Cards")
icon =pygame.image.load(image_pass + 'images/1778592.png')
pygame.display.set_icon(icon)




gameplay = True
running = True
while running:
# начало цикла-----------------------------------------------------------------------



# конец цикла-----------------------------------------------------------------------
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()



    clock.tick(10)