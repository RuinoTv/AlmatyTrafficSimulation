"""Қиылысқа кіретін жолақтардың деректері мен экрандағы орналасуы."""

from dataclasses import dataclass
from typing import Dict, FrozenSet, Optional, Tuple

from . import config


@dataclass(frozen=True)
class Lane:
    """Кіру жолағын, қозғалыс рұқсаттарын және жуық орнын сипаттайды."""

    identifier: str
    approach: str
    position: int
    direction: str
    center: Tuple[float, float]
    movements: FrozenSet[str]
    vehicle_movements: Tuple[Tuple[str, FrozenSet[str]], ...] = ()
    special: bool = False
    note: Optional[str] = None

    def movements_for(self, vehicle_type: str = "passenger_car") -> FrozenSet[str]:
        """Көлік түріне сәйкес рұқсат етілген қозғалыстарды қайтарады."""
        for permitted_type, movements in self.vehicle_movements:
            if permitted_type == vehicle_type:
                return movements
        return self.movements


def _lane(
    approach: str,
    position: int,
    direction: str,
    center: Tuple[float, float],
    movements: FrozenSet[str],
    **kwargs: object,
) -> Lane:
    identifier = f"{approach}{position}"
    return Lane(identifier, approach, position, direction, center, movements, **kwargs)


def build_incoming_lanes() -> Dict[str, Lane]:
    """Пайдаланушы берген қозғалыс рұқсаттары бар 15 кіру жолағын жасайды."""
    lanes: Dict[str, Lane] = {}
    cx, cy = config.CENTER_X, config.CENTER_Y
    permissions = {
        "W1": frozenset({"left"}),
        "W2": frozenset({"straight"}),
        "W3": frozenset({"straight"}),
        "W4": frozenset({"right"}),
        "E1": frozenset({"left"}),
        "E2": frozenset({"straight"}),
        "E3": frozenset({"straight"}),
        "E4": frozenset({"right"}),
        "N1": frozenset({"straight"}),
        "N2": frozenset({"straight"}),
        "N3": frozenset({"straight", "right"}),
        "N4": frozenset(),
        "S1": frozenset({"straight", "left"}),
        "S2": frozenset({"straight"}),
        "S3": frozenset({"straight", "right"}),
    }

    # Нөмірлер жүргізушінің солдан оңға қарау ретімен берілді;
    # нақты далалық рет расталмағандықтан, бұл орын ауыстыру конфигурациясы.
    for order_key, approach, direction, travel_side in (
        ("west", "W", "west_to_east", 1),
        ("east", "E", "east_to_west", -1),
    ):
        lane_width = config.ABAY_LANE_WIDTH
        lane_order = config.APPROACH_LANE_ORDER[order_key]
        for position, identifier in enumerate(lane_order, 1):
            movements = permissions[identifier]
            lateral = config.MEDIAN_WIDTH / 2 + (position - 0.5) * lane_width
            y = cy + travel_side * lateral
            extra = {}
            if position == 4:
                extra["vehicle_movements"] = (
                    ("passenger_car", frozenset({"right"})),
                    ("bus", frozenset({"straight", "right"})),
                )
            lanes[identifier] = _lane(
                approach,
                position,
                direction,
                (cx - config.APPROACH_MARKER_OFFSET if approach == "W" else cx + config.APPROACH_MARKER_OFFSET, y),
                movements,
                **extra,
            )

    for order_key, approach, direction in (
        ("north", "N", "north_to_south"),
        ("south", "S", "south_to_north"),
    ):
        lane_width = config.SEIFULLIN_LANE_WIDTH
        lane_order = config.APPROACH_LANE_ORDER[order_key]
        for position, identifier in enumerate(lane_order, 1):
            movements = permissions[identifier]
            if approach == "N":
                x = cx - (position - 0.5) * lane_width
            else:
                x = cx + (position - 0.5) * lane_width
            lanes[identifier] = _lane(
                approach,
                position,
                direction,
                (x, cy - config.APPROACH_MARKER_OFFSET if approach == "N" else cy + config.APPROACH_MARKER_OFFSET),
                movements,
                special=approach == "N" and position == 4,
                note="Мақсаты белгісіз арнайы аймақ" if approach == "N" and position == 4 else None,
            )
    return lanes


INCOMING_LANES = build_incoming_lanes()
