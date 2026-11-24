import pygame

from core.constants import MAX_WAVE, VIEW_WIDTH

class UIManager:
    def __init__(self):
        self.ui_font=pygame.font.SysFont('Arial', 64, bold=True)
        self.score_font=pygame.font.SysFont('Arial', 32, bold=True)
        self.wave_font=pygame.font.SysFont('Arial', 32, bold=True)
        self.restart_font=pygame.font.SysFont('Arial', 32, bold=True)
        self.controls_font=pygame.font.SysFont('Arial', 22, bold=True)

    def draw(self, view: pygame.Surface, score:int, wave:int, is_game_over: bool, is_game_won: bool):
        self._show_game_controls(view)
        score_text=self.score_font.render(f"SCORE: {score}", True, (255, 255, 255))
        wave_text=self.wave_font.render(f"WAVE: {wave}", True, (255, 255, 255))
        view.blit(score_text, (VIEW_WIDTH /2, 20))
        view.blit(wave_text, (20, 20))
        pygame.draw.rect(view, (255, 255, 255), (0, 0, VIEW_WIDTH, wave_text.get_height()+20), 2)
        
        if is_game_over:
            endgame_message= "G A M E  O V E R"

            if wave == MAX_WAVE:
                endgame_message= "Y O U  W O N ! "

            game_over_surface=self.ui_font.render(endgame_message, True, (255,0,0))
            restart_surface=self.restart_font.render("Press space to restart ", True, (255,255,255))
            text_x=(view.get_width() - game_over_surface.get_width()) /2
            text_y=(view.get_height() - game_over_surface.get_height()) /2
            view.blit(game_over_surface, (text_x, text_y))

            restart_x=(view.get_width() - restart_surface.get_width()) /2
            view.blit(restart_surface,(restart_x, text_y+100))

    def _show_game_controls(self, view: pygame.Surface):
        lines=(

            "LEFT / RIGHT      Turn",
            "UP                     Thrust",
            "SPACEBAR          Fire",
        )

        panel=pygame.Surface((245,132), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 170))

        x= view.get_width() - panel.get_width() - 16
        y= view.get_height() - panel.get_height() - 16
        view.blit(panel, (x, y))
        pygame.draw.rect(view, (255, 255, 255), (x, y, panel.get_width(), panel.get_height() - 20), width=2)
        

        for row, text in enumerate(lines):
            label = self.controls_font.render(text, True, (255, 255, 255))
            view.blit(label, (x + 12, y + 10  + row * 28))

        


