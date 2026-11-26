import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        elif model.state == GameState.FINISHED:
            self._draw_finished(model)
        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        if model.circuit is None or model.car is None:
            return
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        surf, rect = model.car.get_rotated_sprite()
        self.screen.blit(surf, rect)

        progress = model.race_progress
        if progress is not None:
            elapsed = progress.elapsed_seconds()
            minutes, seconds = divmod(int(elapsed), 60)
            hud = self.font.render(
                f"Lap {progress.current_lap}/{progress.laps_to_finish}   {minutes:02d}:{seconds:02d}",
                True,
                COLOR_TEXT,
            )
            background = pygame.Rect(12, 12, hud.get_width() + 20, hud.get_height() + 12)
            pygame.draw.rect(self.screen, COLOR_PANEL, background, border_radius=6)
            self.screen.blit(hud, (background.x + 10, background.y + 6))

    def _draw_finished(self, model: GameModel) -> None:
        progress = model.race_progress
        elapsed = progress.elapsed_seconds() if progress is not None else 0.0
        minutes, seconds = divmod(int(elapsed), 60)
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        title = self.font.render("COURSE TERMINEE !", True, COLOR_ACCENT)
        result = self.font.render(f"Temps : {minutes:02d}:{seconds:02d}", True, COLOR_TEXT)
        hint = self.font.render("ENTREE : revenir au menu", True, COLOR_TEXT)
        self.screen.blit(title, title.get_rect(center=(cx, cy - 70)))
        self.screen.blit(result, result.get_rect(center=(cx, cy)))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 70)))
