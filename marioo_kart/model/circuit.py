from collections.abc import Iterable

from constants import GRID_COLS, GRID_ROWS, TILE_SIZE
from model.road_tile import RoadTile, TerrainType, TrackMarker


class Circuit:
    """A rectangular, row-major grid of terrain cells for one race track."""

    def __init__(self, grid: list[list[RoadTile]]):
        if not grid or not grid[0]:
            raise ValueError("A circuit grid cannot be empty")
        col_count = len(grid[0])
        if any(len(row) != col_count for row in grid):
            raise ValueError("Every circuit row must have the same number of tiles")

        self.grid = grid
        self.rows = len(grid)
        self.cols = col_count

    @classmethod
    def build_default(cls, cols: int = GRID_COLS, rows: int = GRID_ROWS) -> "Circuit":
        """Build a simple closed oval with grass infield and grass outside."""
        if cols < 8 or rows < 8:
            raise ValueError("Default circuit needs at least 8 columns and 8 rows")

        grid = [
            [RoadTile(col, row, TerrainType.GRASS) for col in range(cols)]
            for row in range(rows)
        ]


        for row in (1, 2, rows - 3, rows - 2):
            for col in range(1, cols - 1):
                grid[row][col].terrain = TerrainType.ROAD
        for col in (1, 2, cols - 3, cols - 2):
            for row in range(2, rows - 2):
                grid[row][col].terrain = TerrainType.ROAD

    
        grid[1][cols // 2].marker = TrackMarker.START_FINISH
        grid[rows // 2][cols - 2].marker = TrackMarker.CHECKPOINT
        grid[rows - 2][cols // 2].marker = TrackMarker.CHECKPOINT
        grid[rows // 2][1].marker = TrackMarker.CHECKPOINT
        grid[1][cols // 2 + 2].marker = TrackMarker.BOOST

        return cls(grid)

    @classmethod
    def from_layout(cls, layout: Iterable[str]) -> "Circuit":
        terrain_by_symbol = {
            "G": TerrainType.ROAD,
            ".": TerrainType.GRASS,
            "D": TerrainType.DIRT,
            "S": TerrainType.SAND,
            "I": TerrainType.ICE,
            "#": TerrainType.BARRIER,
        }
        marker_by_symbol = {
            "X": TrackMarker.START_FINISH,
            "A": TrackMarker.START,
            "F": TrackMarker.FINISH,
            "C": TrackMarker.CHECKPOINT,
            "B": TrackMarker.BOOST,
        }
        lines = list(layout)
        if not lines or not lines[0]:
            raise ValueError("Circuit layout cannot be empty")
        if any(len(line) != len(lines[0]) for line in lines):
            raise ValueError("Every layout row must have the same width")

        grid: list[list[RoadTile]] = []
        for row, line in enumerate(lines):
            tiles = []
            for col, symbol in enumerate(line):
                if symbol in marker_by_symbol:
                    tiles.append(RoadTile(col, row, TerrainType.ROAD, marker_by_symbol[symbol]))
                    continue
                if symbol not in terrain_by_symbol:
                    raise ValueError(f"Unknown terrain symbol {symbol!r} at ({col}, {row})")
                tiles.append(RoadTile(col, row, terrain_by_symbol[symbol]))
            grid.append(tiles)
        return cls(grid)

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        """Return the cell containing a world-space pixel coordinate."""
        if px < 0 or py < 0:
            return None
        return self.get_tile(int(px // TILE_SIZE), int(py // TILE_SIZE))

    def get_tile_at_position(self, x: float, y: float) -> RoadTile | None:
        return self.get_tile_at_pixel(x, y)

    def get_marker_at_pixel(self, px: float, py: float) -> TrackMarker:
        tile = self.get_tile_at_pixel(px, py)
        return tile.marker if tile is not None else TrackMarker.NONE

    def tiles_with_marker(self, marker: TrackMarker) -> list[RoadTile]:
        return [tile for row in self.grid for tile in row if tile.marker == marker]

    def get_markers_at_pixel(self, px: float, py: float) -> frozenset[TrackMarker]:
        marker = self.get_marker_at_pixel(px, py)
        if marker == TrackMarker.START_FINISH:
            return frozenset((TrackMarker.START, TrackMarker.FINISH))
        if marker == TrackMarker.NONE:
            return frozenset()
        return frozenset((marker,))

    def terrain_at_pixel(self, px: float, py: float) -> TerrainType | None:
        tile = self.get_tile_at_pixel(px, py)
        return tile.terrain if tile is not None else None

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
