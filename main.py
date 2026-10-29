

import pygame

from core.game_manager import GameManager
from core.ui_manager import UIManager


#intialize pygame engine
pygame.init()
pygame.display.set_caption("Asteroids")
view = pygame.display.set_mode((1024, 576))
clock=pygame.time.Clock()
game_manager=GameManager(view)
game_objects=game_manager.init_game_objects()
ui_manager=UIManager()

#game loop
running = True
while running:
    # calculate delta time and tick the clock
    delta_time=clock.tick(60)/1000.0
    # get state of all keyboard keys
    keys=pygame.key.get_pressed()
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif keys[pygame.K_SPACE] and game_manager.is_game_over:
            game_manager.init_game_objects()

    game_manager.process_inputs(keys, delta_time)
    # Update movement
    game_manager.update(delta_time)

    # Check colisions & state
    game_manager.check_colisions()
    game_manager.clean_up_objects()

    # Render
    view.fill((0,0,0))
    game_manager.draw(view)
    # Draw the UI overlay using data from the GameManager
    ui_manager.draw(view, game_manager.score, game_manager.is_game_over)
    pygame.display.flip() #update the screen

pygame.quit()