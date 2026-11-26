from constants import GameState, TOTAL_LAPS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile, TrackMarker
from model.race_progress import RaceProgress


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.race_progress: RaceProgress | None = None

    def load_circuit(self) -> None:
        self.circuit = Circuit.build_default()
        self.spawn_car()
        self.race_progress = RaceProgress(
            checkpoints=self.circuit.checkpoint_tiles(),
            laps_to_finish=TOTAL_LAPS,
            start_tile=self.player_tile(),
        )

    def spawn_car(self) -> None:
        start_tiles = self.circuit.tiles_with_marker(TrackMarker.START_FINISH)
        if not start_tiles:
            start_tiles = self.circuit.tiles_with_marker(TrackMarker.START)
        if not start_tiles:
            raise ValueError("Circuit must contain a start or start/finish marker")
        start_line = start_tiles[0]
        self.car = Car(start_line.col, start_line.row)
        self.car.angle = 90.0

    def player_tile(self) -> RoadTile | None:
        if self.car is None or self.circuit is None:
            return None
        return self.circuit.get_tile_at_position(self.car.x, self.car.y)

    def player_markers(self) -> frozenset[TrackMarker]:
        if self.car is None or self.circuit is None:
            return frozenset()
        return self.circuit.get_markers_at_pixel(self.car.x, self.car.y)

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        if self.car is not None:
            self.car.update_position(self.circuit)
            if self.race_progress is not None:
                self.race_progress.update(self.player_tile())
                if self.race_progress.finished:
                    self.state = GameState.FINISHED
