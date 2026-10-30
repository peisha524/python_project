import pygame
import math
from dataclasses import dataclass
from pygame.math import Vector2
from constants import (
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)
from model.physics import (
    BOOST_ACCELERATION,
    BRAKE_DECELERATION,
    ENGINE_ACCELERATION,
    MAX_REVERSE_SPEED,
    MAX_SPEED,
    REVERSE_ACCELERATION,
)
from model.terrain import Terrain

@dataclass
class CarControls:
    """The controls of one player for the current frame."""

    accelerate: bool = False
    brake: bool = False
    turn_left: bool = False
    turn_right: bool = False
    item: bool = False

    @property
    def throttle(self) -> int:
        """Return 1 to accelerate, -1 to brake and 0 when neutral."""
        if self.accelerate and not self.brake:
            return 1
        if self.brake and not self.accelerate:
            return -1
        return 0

    @property
    def steering(self) -> int:
        """Return 1 for left, -1 for right and 0 when not steering."""
        return int(self.turn_left) - int(self.turn_right)
    
class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.velocity = Vector2(0.0, 0.0)
        self.angle: float = 0.0
        self.controls = CarControls()
        self.boost_time = 0.0
        self.sprite = self.build_sprite()

    @property
    def speed(self) -> float:
        """Norm of the velocity, in pixels per second."""
        return self.velocity.length()
        
    @property
    def forward_speed(self) -> float:
        """Longitudinal speed, positive forward and negative in reverse."""
        heading = Vector2(math.cos(self.angle), math.sin(self.angle))
        return self.velocity.dot(heading)

    def set_controls(self, controls: CarControls) -> None:
        """Replace the controls applied during the next physics step."""
        self.controls = controls

    def _longitudinal_acceleration(
        self,
        terrain: Terrain,
        forward_speed: float,
    ) -> float:
        """Return the longitudinal acceleration for the current inputs."""
        throttle = self.controls.throttle
        traction = terrain.traction
        acceleration = 0.0

        if throttle > 0:
            if forward_speed < -1.0:
                acceleration = BRAKE_DECELERATION * traction
            else:
                acceleration = ENGINE_ACCELERATION * traction
        elif throttle < 0:
            if forward_speed > 1.0:
                acceleration = -BRAKE_DECELERATION * traction
            else:
                acceleration = -REVERSE_ACCELERATION * traction

        if self.boost_time > 0.0:
            acceleration += BOOST_ACCELERATION
        return acceleration

    def update_position(self) -> None:
        self.y += self.speed

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
