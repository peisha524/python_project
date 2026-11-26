from time import perf_counter

from model.road_tile import RoadTile, TrackMarker


class RaceProgress:
    """Tracks ordered checkpoints, completed laps, and the finish time."""

    def __init__(
        self,
        checkpoints: list[RoadTile] | None = None,
        laps_to_finish: int = 3,
        start_tile: RoadTile | None = None,
    ):
        if laps_to_finish < 1:
            raise ValueError("laps_to_finish must be at least 1")
        self.checkpoints = tuple((tile.col, tile.row) for tile in checkpoints or [])
        self.laps_to_finish = laps_to_finish
        self.start_cell = self._cell_of(start_tile)
        self.last_cell = self.start_cell
        self.laps_completed = 0
        self.next_checkpoint_index = 0
        self.left_start_line = False
        self.finished = False
        self.started_at = perf_counter()
        self.finished_at: float | None = None

    @staticmethod
    def _cell_of(tile: RoadTile | None) -> tuple[int, int] | None:
        if tile is None:
            return None
        return tile.col, tile.row

    @property
    def current_lap(self) -> int:
        return min(self.laps_completed + 1, self.laps_to_finish)

    @property
    def next_checkpoint_number(self) -> int | None:
        if self.next_checkpoint_index >= len(self.checkpoints):
            return None
        return self.next_checkpoint_index + 1

    def update(self, tile: RoadTile | None, now: float | None = None) -> None:
        """Consume a newly entered cell; repeated frames in one cell do nothing."""
        if self.finished:
            return

        cell = self._cell_of(tile)
        if cell is None or cell == self.last_cell:
            return

        left_start_cell = self.last_cell == self.start_cell
        self.last_cell = cell
        if left_start_cell:
            self.left_start_line = True

        if tile.marker == TrackMarker.CHECKPOINT:
            if (
                self.next_checkpoint_index < len(self.checkpoints)
                and cell == self.checkpoints[self.next_checkpoint_index]
            ):
                self.next_checkpoint_index += 1
            return

        if tile.marker not in (TrackMarker.FINISH, TrackMarker.START_FINISH):
            return

        if not self.left_start_line or self.next_checkpoint_index < len(self.checkpoints):
            return

        self.laps_completed += 1
        self.next_checkpoint_index = 0
        self.left_start_line = False
        # A separate FINISH cell becomes the line to leave before the next lap.
        self.start_cell = cell
        if self.laps_completed >= self.laps_to_finish:
            self.finished = True
            self.finished_at = perf_counter() if now is None else now

    def elapsed_seconds(self, now: float | None = None) -> float:
        end = self.finished_at
        if end is None:
            end = perf_counter() if now is None else now
        return max(0.0, end - self.started_at)
