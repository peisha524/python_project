import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    def handle_keydown(self, key: int) -> None:
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)

        elif state == GameState.TRACK_SELECT:
            self.handle_track_select_key(key)

        elif state == GameState.RACING:
            if key == pygame.K_ESCAPE:
                self.model.state = GameState.TRACK_SELECT

    def handle_menu_key(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self.model.state = GameState.TRACK_SELECT
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_track_select_key(self, key: int) -> None:
        count = len(self.model.circuit_names)

        if key == pygame.K_UP:
            self.model.selected_circuit_index = (
                self.model.selected_circuit_index - 1
            ) % count

        elif key == pygame.K_DOWN:
            self.model.selected_circuit_index = (
                self.model.selected_circuit_index + 1
            ) % count

        elif key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING

        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self) -> None:
        if self.model.state != GameState.RACING:
            return

        p1_input = self.input_handler.get_inputs()
        car = self.model.car
        if car is None or self.model.circuit is None:
            return
        self.apply_input(car, p1_input)
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        tile = self.model.circuit.get_tile_at_position(car.x, car.y)
        traction = tile.traction if tile is not None else 0.0
        if player_input['accelerate']:
            car.accelerate(traction)
        if player_input['brake']:
            car.brake(traction)
        if player_input['steer_left']:
            car.steer(-1, traction)
        if player_input['steer_right']:
            car.steer(1, traction)

    def render(self) -> None:
        self.view.draw(self.model)

    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
