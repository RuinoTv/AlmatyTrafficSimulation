"""Кіру бағыттарындағы расталған жолақтардың деректері мен орналасу құралдары."""
from dataclasses import dataclass
from typing import Dict, Tuple
from . import config
@dataclass(frozen=True)
class Lane:
    """Жүргізуші қиылысқа қарағанда солдан оңға қарай нөмірленген бір кіру жолағы."""
    identifier: str
    approach: str
    lane_number: int
    direction: str
    center: Tuple[float, float]
def build_incoming_lanes() -> Dict[str, Lane]:
    """Барлық бағытқа арналған жолақ сипаттамалары мен жуық орталықтарын жасайды."""
    lanes: Dict[str, Lane] = {}
    cx, cy = config.CENTER_X, config.CENTER_Y
    # Қиылысқа қарағанда батыс бағытта жолақтар оңтүстіктен солтүстікке,
    # ал шығыс бағытта солтүстіктен оңтүстікке қарай нөмірленеді.
    for number in range(1, config.ABAY_LANES_PER_DIRECTION + 1):
        offset = config.MEDIAN_WIDTH / 2 + (number - 0.5) * config.ABAY_LANE_WIDTH
        lanes[f"W{number}"] = Lane(f"W{number}", "W", number, "west_to_east", (cx - 360, cy + offset))
        lanes[f"E{number}"] = Lane(f"E{number}", "E", number, "east_to_west", (cx + 360, cy - offset))
    # Солтүстік бағытта жолақтар батыстан шығысқа,
    # ал оңтүстік бағытта шығыстан батысқа қарай нөмірленеді.
    for number in range(1, config.SEIFULLIN_LANES_PER_DIRECTION + 1):
        offset = (number - 0.5) * config.SEIFULLIN_LANE_WIDTH
        lanes[f"N{number}"] = Lane(f"N{number}", "N", number, "north_to_south", (cx - offset, cy - 350))
        lanes[f"S{number}"] = Lane(f"S{number}", "S", number, "south_to_north", (cx + offset, cy + 350))
    return lanes
INCOMING_LANES = build_incoming_lanes()