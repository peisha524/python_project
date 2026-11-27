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
        elif model.state == GameState.TRACK_SELECT:
            self._draw_track_select(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
            self._draw_hud(model)

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

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        if model.circuit is None:
            return
        for car in model.cars:
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)


    def _draw_track_select(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title = self.font.render(
            "Choisir un circuit", True, COLOR_ACCENT
        )
        self.screen.blit(title, title.get_rect(center=(cx, 180)))

        for index, name in enumerate(model.circuit_names):
            selected = index == model.selected_circuit_index
            color = COLOR_ACCENT if selected else COLOR_TEXT
            label = "> " + name if selected else name

            text = self.font.render(label, True, color)
            self.screen.blit(
                text, text.get_rect(center=(cx, 320 + index * 70))
            )

        hint = self.font.render(
            "Haut/Bas : choisir | Enter : jouer | Esc : retour",
            True, COLOR_TEXT
        )
        self.screen.blit(hint, hint.get_rect(center=(cx, 550)))

    def _draw_hud(self, model: GameModel) -> None:
        if len(model.cars) < 2:
            return

        panel = pygame.Rect(10, 10, WINDOW_WIDTH - 20, 44)
        pygame.draw.rect(
            self.screen, COLOR_PANEL, panel, border_radius=8
        )

        circuit_name = model.circuit_names[
            model.selected_circuit_index
        ]
        title = self.font.render(
            circuit_name, True, COLOR_TEXT
        )
        self.screen.blit(title, (22, 20))

        hint = self.font.render(
            "Esc : circuits", True, COLOR_ACCENT
        )
        self.screen.blit(
            hint,
            hint.get_rect(topright=(WINDOW_WIDTH - 22, 18))
        )

        for index, car in enumerate(model.cars):
            text = self.font.render(
                f"P{index + 1} : {car.speed:.1f} px/frame",
                True, car.color
            )
            self.screen.blit(text, (300 + index * 250, 20))