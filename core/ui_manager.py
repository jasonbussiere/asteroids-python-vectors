import pygame

class UIManager:
    def __init__(self):
        self.ui_font=pygame.font.SysFont('Arial', 64, bold=True)
        self.score_font=pygame.font.SysFont('Arial', 32, bold=True)
        self.restart_font=pygame.font.SysFont('Arial', 32, bold=True)

    def draw(self, view: pygame.Surface, score:int, is_game_over: bool):
        score_text=self.score_font.render(f"SCORE: {score}", True, (255, 255, 255))
        view.blit(score_text, (20, 20))
        
        if is_game_over:
            game_over_surface=self.ui_font.render("G A M E  O V E R", True, (255,0,0))
            restart_surface=self.restart_font.render("Press space to restart ", True, (255,255,255))
            text_x=(view.get_width() - game_over_surface.get_width()) /2
            text_y=(view.get_height() - game_over_surface.get_height()) /2
            view.blit(game_over_surface, (text_x, text_y))

            restart_x=(view.get_width() - restart_surface.get_width()) /2
            view.blit(restart_surface,(restart_x, text_y+100))
