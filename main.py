

import pygame

from core.game_manager import GameManager
from core.ui_manager import UIManager


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    view = pygame.display.set_mode((1024, 576))
    clock = pygame.time.Clock()
    game_manager = GameManager(view)
    game_manager.init_game_objects()
    ui_manager = UIManager()

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                    and game_manager.is_game_over):
                game_manager.init_game_objects()

        keys = pygame.key.get_pressed()
        game_manager.process_inputs(keys, delta_time)
        game_manager.update(delta_time)
        game_manager.check_colisions()
        game_manager.clean_up_objects()

        view.fill((0, 0, 0))
        game_manager.draw(view)
        ui_manager.draw(view, game_manager.score, game_manager.is_game_over)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()