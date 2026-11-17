from enum import Enum

import pygame

from constants import TILE_SIZE


class TerrainType(Enum):

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


class TrackMarker(Enum):

    NONE = "none"
    START = "start"
    FINISH = "finish"
    START_FINISH = "start_finish"
    CHECKPOINT = "checkpoint"
    BOOST = "boost"


_TERRAIN_COLORS = {
    TerrainType.GRASS: (67, 145, 73),
    TerrainType.ROAD: (75, 78, 87),
    TerrainType.DIRT: (160, 119, 70),
    TerrainType.SAND: (212, 184, 116),
    TerrainType.ICE: (165, 218, 232),
    TerrainType.BARRIER: (190, 65, 55),
}


class RoadTile:

    def __init__(
        self,
        col: int,
        row: int,
        terrain: TerrainType = TerrainType.GRASS,
        marker: TrackMarker = TrackMarker.NONE,
    ):
        if col < 0 or row < 0:
            raise ValueError("Tile coordinates must be non-negative")
        self.col = col
        self.row = row
        self.terrain = terrain
        self.marker = marker
        self.sprite: pygame.Surface | None = None
        self._sprite_cache_key: tuple[int, TerrainType, TrackMarker] | None = None

    @property
    def is_drivable(self) -> bool:
        return self.terrain.drivable

    @property
    def traction(self) -> float:
        return self.terrain.traction

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        if tile_size <= 0:
            raise ValueError("tile_size must be positive")
        cache_key = (tile_size, self.terrain, self.marker)
        if self.sprite is not None and self._sprite_cache_key == cache_key:
            return self.sprite

        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(_TERRAIN_COLORS[self.terrain])
        border_color = (48, 52, 59) if self.terrain == TerrainType.ROAD else (45, 100, 50)
        pygame.draw.rect(surface, border_color, surface.get_rect(), 1)
        center = tile_size // 2
        if self.marker in (TrackMarker.START, TrackMarker.START_FINISH):
            pygame.draw.line(surface, (245, 245, 245), (center, 0), (center, tile_size), max(3, tile_size // 12))
            for y in range(0, tile_size, max(2, tile_size // 8)):
                color = (25, 25, 25) if (y // max(2, tile_size // 8)) % 2 == 0 else (245, 245, 245)
                pygame.draw.rect(surface, color, (center - 3, y, 6, max(2, tile_size // 8)))
        elif self.marker == TrackMarker.FINISH:
            pygame.draw.line(surface, (255, 215, 0), (center, 0), (center, tile_size), max(4, tile_size // 10))
        elif self.marker == TrackMarker.CHECKPOINT:
            pygame.draw.circle(surface, (70, 190, 255), (center, center), max(5, tile_size // 6), 3)
        elif self.marker == TrackMarker.BOOST:
            pygame.draw.polygon(surface, (255, 125, 35), [(center - 7, center - 12), (center + 7, center - 12), (center + 3, center - 2), (center + 10, center - 2), (center - 5, center + 14), (center - 2, center + 3), (center - 9, center + 3)])
        self.sprite = surface
        self._sprite_cache_key = cache_key
        return surface
