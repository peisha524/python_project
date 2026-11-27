from constants import GameState
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile, TrackMarker, TerrainType


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.cars: list[Car] = []
        self.circuit_names = ["Circuit classique", "Circuit mixte"]
        self.selected_circuit_index = 0

    def load_circuit(self) -> None:
        self.circuit = Circuit.build_default()

        if self.selected_circuit_index == 1:
            for col in range(3, self.circuit.cols - 3):
                for row in (1, 2):
                    self.circuit.grid[row][col].terrain = TerrainType.DIRT

                for row in (self.circuit.rows - 3, self.circuit.rows - 2):
                    self.circuit.grid[row][col].terrain = TerrainType.ICE

        self.spawn_car()

    def spawn_car(self) -> None:
        start_line = self.circuit.tiles_with_marker(
            TrackMarker.START_FINISH
        )[0]

        car1 = Car(
            start_line.col,
            start_line.row,
            color=(255, 0, 0),
        )
        car2 = Car(
            start_line.col,
            start_line.row + 1,
            color=(0, 150, 255),
        )

        car1.angle = 90.0
        car2.angle = 90.0

        self.cars = [car1, car2]
        self.car = car1

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

        for car in self.cars:
            car.update_position(self.circuit)
