import sys

import pygame

from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from game_objects.asteroid import Asteroid

from game_objects.laser import Laser
from game_objects.ship import Ship

#intialize pygame engine
pygame.init()
view = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("Asteroids")
clock=pygame.time.Clock()

#instantiate game objects
ship=Ship(view.get_width()/2, view.get_height()/2)
asteroids={
    Asteroid(100, 100),
    Asteroid(VIEW_WIDTH-100, 100),
    Asteroid(100, VIEW_HEIGHT-100),
    Asteroid(VIEW_WIDTH-100, VIEW_HEIGHT-100)
}
lasers:list[Laser]= []

#game loop
running = True
while running:
    #handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    #get state of all keyboard keys
    keys=pygame.key.get_pressed()

    #pass keys list to ship, ship handles key press behavior
    new_laser = ship.handle_input(keys)

    if new_laser:
        lasers.append(new_laser)

    #update game objects position
    ship.update()

    for asteroid in asteroids:
        asteroid.update()

    for laser in lasers:
        laser.update()

    #clear screen
    view.fill((0,0,0))

    #draw the game objects
    ship.draw(view)

    for asteroid in asteroids:
        asteroid.draw(view)

    for laser in lasers:
        laser.draw(view)

    lasers=[laser for laser in lasers if laser.is_alive() ]
    
    #update the screen
    pygame.display.flip()

    #run the loop at 60 frames
    clock.tick(60)

pygame.quit()