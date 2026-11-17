from collections.abc import Iterable

from constants import GRID_COLS, GRID_ROWS, TILE_SIZE
from model.road_tile import RoadTile, TerrainType


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

        # The two-cell-wide loop leaves a visible infield and has connected corners.
        for row in (1, 2, rows - 3, rows - 2):
            for col in range(1, cols - 1):
                grid[row][col].terrain = TerrainType.ROAD
        for col in (1, 2, cols - 3, cols - 2):
            for row in range(2, rows - 2):
                grid[row][col].terrain = TerrainType.ROAD

        return cls(grid)

    @classmethod
    def from_layout(cls, layout: Iterable[str]) -> "Circuit":
        """Create rows of cells: G road, . grass, D dirt, S sand, I ice, # barrier."""
        terrain_by_symbol = {
            "G": TerrainType.ROAD,
            ".": TerrainType.GRASS,
            "D": TerrainType.DIRT,
            "S": TerrainType.SAND,
            "I": TerrainType.ICE,
            "#": TerrainType.BARRIER,
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

    def terrain_at_pixel(self, px: float, py: float) -> TerrainType | None:
        tile = self.get_tile_at_pixel(px, py)
        return tile.terrain if tile is not None else None

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
