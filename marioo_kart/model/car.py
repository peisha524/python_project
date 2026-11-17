import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKING, CAR_TURN_RATE, CAR_MAX_SPEED,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)
from model.circuit import Circuit
from model.road_tile import TrackMarker


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self._was_on_boost = False
        self.sprite = self.build_sprite()

    def accelerate(self, traction: float = 1.0) -> None:
        self.speed = min(CAR_MAX_SPEED, self.speed + CAR_ACCELERATION * traction)

    def brake(self, traction: float = 1.0) -> None:
        self.speed = max(0.0, self.speed - CAR_BRAKING * traction)

    def steer(self, direction: int, traction: float = 1.0) -> None:
        if direction not in (-1, 0, 1):
            raise ValueError("direction must be -1, 0, or 1")
        self.angle = (self.angle - direction * CAR_TURN_RATE * traction) % 360

    def update_position(self, circuit: Circuit) -> None:
        """Move forward, applying barriers and boost cells from the track map."""
        radians = math.radians(self.angle)
        next_x = self.x + math.sin(radians) * self.speed
        next_y = self.y + math.cos(radians) * self.speed
        next_tile = circuit.get_tile_at_position(next_x, next_y)

        if next_tile is None or not next_tile.is_drivable:
            self.speed = 0.0
            self._was_on_boost = False
            return

        self.x = next_x
        self.y = next_y
        on_boost = next_tile.marker == TrackMarker.BOOST
        if on_boost and not self._was_on_boost:
            self.speed = min(CAR_MAX_SPEED, self.speed + 1.0)
        self._was_on_boost = on_boost

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
