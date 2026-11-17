from enum import Enum

import pygame

from constants import TILE_SIZE


class TerrainType(Enum):
    """[TERRA-7] Terrain definitions and their effects on car traction."""

    ROAD = ("road", 1.00, True)
    GRASS = ("grass", 0.72, True)
    DIRT = ("dirt", 0.55, True)
    SAND = ("sand", 0.42, True)
    ICE = ("ice", 0.12, True)
    BARRIER = ("barrier", 0.00, False)

    def __init__(self, label: str, traction: float, drivable: bool):
        self.label = label
        self.traction = traction
        self.drivable = drivable


_TERRAIN_COLORS = {
    TerrainType.GRASS: (67, 145, 73),
    TerrainType.ROAD: (75, 78, 87),
    TerrainType.DIRT: (160, 119, 70),
    TerrainType.SAND: (212, 184, 116),
    TerrainType.ICE: (165, 218, 232),
    TerrainType.BARRIER: (190, 65, 55),
}


class RoadTile:
    """[TERRA-7] A terrain cell with a grid coordinate and driving properties."""

    def __init__(
        self,
        col: int,
        row: int,
        terrain: TerrainType = TerrainType.GRASS,
    ):
        if col < 0 or row < 0:
            raise ValueError("Tile coordinates must be non-negative")
        self.col = col
        self.row = row
        self.terrain = terrain
        self.sprite: pygame.Surface | None = None
        self._sprite_size: int | None = None

    @property
    def is_drivable(self) -> bool:
        return self.terrain.drivable

    @property
    def traction(self) -> float:
        return self.terrain.traction

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        if tile_size <= 0:
            raise ValueError("tile_size must be positive")
        if self.sprite is not None and self._sprite_size == tile_size:
            return self.sprite

        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(_TERRAIN_COLORS[self.terrain])
        border_color = (48, 52, 59) if self.terrain == TerrainType.ROAD else (45, 100, 50)
        pygame.draw.rect(surface, border_color, surface.get_rect(), 1)
        self.sprite = surface
        self._sprite_size = tile_size
        return surface
