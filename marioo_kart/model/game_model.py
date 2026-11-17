from constants import GameState
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile, TrackMarker


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None

    def load_circuit(self) -> None:
        self.circuit = Circuit.build_default()
        self.spawn_car()

    def spawn_car(self) -> None:
        start_line = self.circuit.tiles_with_marker(TrackMarker.START_FINISH)[0]
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
