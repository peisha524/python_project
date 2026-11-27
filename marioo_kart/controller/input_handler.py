import pygame


PLAYER_MAPPINGS = {
    1: {
        pygame.K_z: "accelerate",
        pygame.K_w: "accelerate",
        pygame.K_s: "brake",
        pygame.K_q: "steer_left",
        pygame.K_a: "steer_left",
        pygame.K_d: "steer_right",
    },
    2: {
        pygame.K_UP: "accelerate",
        pygame.K_DOWN: "brake",
        pygame.K_LEFT: "steer_left",
        pygame.K_RIGHT: "steer_right",
    },
}


class InputHandler:
    """Read driving controls for both players."""

    def __init__(self):
        self.mappings = PLAYER_MAPPINGS

    def get_inputs(self, player_id: int = 2) -> dict:
        """Return the current driving inputs for one player."""
        keys = pygame.key.get_pressed()
        mapping = self.mappings[player_id]

        inputs = {
            action: False
            for action in mapping.values()
        }

        for key, action in mapping.items():
            if keys[key]:
                inputs[action] = True

        return inputs