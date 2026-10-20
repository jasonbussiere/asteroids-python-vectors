import sys

import pygame

from game_objects.ship import Ship


pygame.init()
view = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("Asteroids")
clock=pygame.time.Clock()


ship=Ship(view.get_width()/2, view.get_height()/2)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    keys=pygame.key.get_pressed()
    ship.handle_input(keys)
    ship.update()

    view.fill((0,0,0))

    ship.draw(view)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()