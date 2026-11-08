"""Жол беттерін, жолақ белгілерін және жаяу жүргінші өткелдерін сызу."""

from typing import Mapping

import pygame

from . import config
from .lanes import Lane


def road_rectangles() -> tuple[pygame.Rect, pygame.Rect]:
    """Көлденең және тік жолдардың негізгі пішіндерін қайтарады."""
    horizontal = pygame.Rect(config.MAP_LEFT, config.CENTER_Y - config.ABAY_HALF_WIDTH, config.MAP_SIZE, config.ABAY_HALF_WIDTH * 2)
    vertical_left = config.CENTER_X - config.NORTH_LANES * config.SEIFULLIN_LANE_WIDTH
    vertical_width = (config.NORTH_LANES + config.SOUTH_LANES) * config.SEIFULLIN_LANE_WIDTH
    vertical = pygame.Rect(vertical_left, config.MAP_TOP, vertical_width, config.MAP_SIZE)
    return horizontal, vertical


def draw_road_surface(surface: pygame.Surface) -> None:
    """Жалғанған асфальт жолдарды және жұмырланған қиылыс бұрыштарын сызады."""
    horizontal, vertical = road_rectangles()
    pygame.draw.rect(surface, config.ASPHALT_COLOR, horizontal)
    pygame.draw.rect(surface, config.ASPHALT_COLOR, vertical)

    left = config.CENTER_X - config.INTERSECTION_HALF_WIDTH
    right = config.CENTER_X + config.INTERSECTION_HALF_WIDTH
    top = config.CENTER_Y - config.INTERSECTION_HALF_HEIGHT
    bottom = config.CENTER_Y + config.INTERSECTION_HALF_HEIGHT
    radius = config.CORNER_RADIUS
    for center in ((left, top), (right, top), (left, bottom), (right, bottom)):
        pygame.draw.circle(surface, config.GROUND_COLOR, center, radius)

    pygame.draw.rect(surface, config.ROAD_EDGE_COLOR, horizontal, 2)
    pygame.draw.rect(surface, config.ROAD_EDGE_COLOR, vertical, 2)
    map_rect = pygame.Rect(config.MAP_LEFT, config.MAP_TOP, config.MAP_SIZE, config.MAP_SIZE)
    pygame.draw.rect(surface, config.ROAD_EDGE_COLOR, map_rect, 2)


def draw_lane_markings(surface: pygame.Surface) -> None:
    """Бағыттарға сай жолақ бөлгіштерді, өткелдер мен тоқтау сызықтарын сызады."""
    _draw_abay_markings(surface)
    _draw_seifullin_markings(surface)
    _draw_pedestrian_crossings(surface)
    _draw_south_hatched_area(surface)


def _draw_abay_markings(surface: pygame.Surface) -> None:
    center_x, center_y = config.CENTER_X, config.CENTER_Y
    seifullin_left = center_x - config.NORTH_LANES * config.SEIFULLIN_LANE_WIDTH
    seifullin_right = center_x + config.SOUTH_LANES * config.SEIFULLIN_LANE_WIDTH
    west_crossing_start = seifullin_left - config.PEDESTRIAN_CROSSING_OFFSET
    east_crossing_end = seifullin_right + config.PEDESTRIAN_CROSSING_CLEARANCE + config.PEDESTRIAN_CROSSING_DEPTH
    dash = config.LANE_DASH_LENGTH
    step = dash + config.LANE_DASH_GAP
    for separator in range(1, config.ABAY_LANES_PER_DIRECTION):
        offset = config.MEDIAN_WIDTH / 2 + separator * config.ABAY_LANE_WIDTH
        for y in (center_y - offset, center_y + offset):
            for start in range(config.MAP_LEFT, west_crossing_start - dash, step):
                pygame.draw.line(surface, config.LANE_MARKING_COLOR, (start, y), (start + dash, y), 2)
            for start in range(east_crossing_end, config.MAP_RIGHT, step):
                pygame.draw.line(surface, config.LANE_MARKING_COLOR, (start, y), (min(start + dash, config.MAP_RIGHT), y), 2)


def _draw_seifullin_markings(surface: pygame.Surface) -> None:
    center_x, center_y = config.CENTER_X, config.CENTER_Y
    for separator in range(1, config.NORTH_LANES + 1):
        _draw_vertical_dashes(surface, center_x - separator * config.SEIFULLIN_LANE_WIDTH, center_y)
    for separator in range(1, config.SOUTH_LANES + 1):
        _draw_vertical_dashes(surface, center_x + separator * config.SEIFULLIN_LANE_WIDTH, center_y)
    # Қос үзік сызық қарсы бағыттағы қозғалысты физикалық медианасыз ажыратады.
    _draw_vertical_dashes(surface, center_x - 4, center_y)
    _draw_vertical_dashes(surface, center_x + 4, center_y)


def _draw_vertical_dashes(surface: pygame.Surface, x: int, center_y: int) -> None:
    dash = config.LANE_DASH_LENGTH
    step = dash + config.LANE_DASH_GAP
    north_crossing_start = center_y - config.INTERSECTION_HALF_HEIGHT - config.PEDESTRIAN_CROSSING_OFFSET
    south_crossing_end = center_y + config.INTERSECTION_HALF_HEIGHT + config.PEDESTRIAN_CROSSING_CLEARANCE + config.PEDESTRIAN_CROSSING_DEPTH
    for start in range(config.MAP_TOP, north_crossing_start - dash, step):
        pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, start), (x, start + dash), 2)
    for start in range(south_crossing_end, config.MAP_BOTTOM, step):
        pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, start), (x, min(start + dash, config.MAP_BOTTOM)), 2)


def _draw_pedestrian_crossings(surface: pygame.Surface) -> None:
    """Төрт кіреберісте зебра жолақтарын және олардың алдындағы стоп-сызықтарды сызады."""
    center_x, center_y = config.CENTER_X, config.CENTER_Y
    stripe_width, stripe_gap = 7, 6
    cross_depth = config.PEDESTRIAN_CROSSING_DEPTH
    seifullin_left = center_x - config.NORTH_LANES * config.SEIFULLIN_LANE_WIDTH
    seifullin_right = center_x + config.SOUTH_LANES * config.SEIFULLIN_LANE_WIDTH
    abay_top = center_y - config.ABAY_HALF_WIDTH
    abay_bottom = center_y + config.ABAY_HALF_WIDTH

    for y in (
        center_y - config.INTERSECTION_HALF_HEIGHT - config.PEDESTRIAN_CROSSING_OFFSET,
        center_y + config.INTERSECTION_HALF_HEIGHT + config.PEDESTRIAN_CROSSING_CLEARANCE,
    ):
        for x in range(seifullin_left + 3, seifullin_right - 3, stripe_width + stripe_gap):
            stripe = pygame.Rect(x, y, stripe_width, cross_depth)
            pygame.draw.rect(surface, config.ZEBRA_COLOR, stripe)
        stop_y = y - config.PEDESTRIAN_CROSSING_CLEARANCE // 2 if y < center_y else y + cross_depth + config.PEDESTRIAN_CROSSING_CLEARANCE // 2
        pygame.draw.line(surface, config.STOP_LINE_COLOR, (seifullin_left, stop_y), (seifullin_right, stop_y), 4)

    for x in (
        seifullin_left - config.PEDESTRIAN_CROSSING_OFFSET,
        seifullin_right + config.PEDESTRIAN_CROSSING_CLEARANCE,
    ):
        for y in range(abay_top + 3, abay_bottom - 3, stripe_width + stripe_gap):
            stripe = pygame.Rect(x, y, cross_depth, stripe_width)
            pygame.draw.rect(surface, config.ZEBRA_COLOR, stripe)
        stop_x = x - config.PEDESTRIAN_CROSSING_CLEARANCE // 2 if x < center_x else x + cross_depth + config.PEDESTRIAN_CROSSING_CLEARANCE // 2
        pygame.draw.line(surface, config.STOP_LINE_COLOR, (stop_x, abay_top), (stop_x, abay_bottom), 4)


def _draw_south_hatched_area(surface: pygame.Surface) -> None:
    """Көрсетілген оңтүстік аймақты мақсатын белгілемей штрихтайды."""
    center_x = config.CENTER_X
    x = center_x + config.SEIFULLIN_HALF_WIDTH + 14
    y = config.CENTER_Y + config.INTERSECTION_HALF_HEIGHT + 65
    rect = pygame.Rect(x, y, config.HATCHED_AREA_WIDTH, config.HATCHED_AREA_LENGTH)
    for start_y in range(rect.top, rect.bottom, 12):
        pygame.draw.line(surface, config.HATCH_COLOR, (rect.left, start_y), (rect.right, min(start_y + 12, rect.bottom)), 2)


def draw_median(surface: pygame.Surface) -> None:
    """Абай даңғылының көгалдандырылған медианасын қиылыс алдында үзеді."""
    half_length = config.MEDIAN_HALF_LENGTH
    opening = config.MEDIAN_OPENING_HALF_LENGTH
    segments = (
        pygame.Rect(config.CENTER_X - half_length, config.CENTER_Y - config.MEDIAN_WIDTH // 2, half_length - opening, config.MEDIAN_WIDTH),
        pygame.Rect(config.CENTER_X + opening, config.CENTER_Y - config.MEDIAN_WIDTH // 2, half_length - opening, config.MEDIAN_WIDTH),
    )
    for rect in segments:
        pygame.draw.rect(surface, config.MEDIAN_COLOR, rect, border_radius=7)
        for x in range(rect.left + 14, rect.right - 6, 32):
            pygame.draw.circle(surface, config.MEDIAN_DETAIL_COLOR, (x, rect.centery), 5)


def draw_movement_arrows(surface: pygame.Surface, lanes: Mapping[str, Lane]) -> None:
    """Жолақ деректерінде көрсетілген рұқсатты бағыттарды жебемен сызады."""
    for lane in lanes.values():
        if lane.special:
            center_x, center_y = int(lane.center[0]), int(lane.center[1])
            for offset in (-10, -3, 4):
                pygame.draw.line(surface, config.HATCH_COLOR, (center_x + offset, center_y - 10), (center_x + offset + 8, center_y + 10), 2)
            continue
        movements = lane.movements_for("passenger_car")
        _draw_lane_arrows(surface, lane.center, lane.direction, movements)
        bus_movements = lane.movements_for("bus") - movements
        if bus_movements:
            side = _left_vector(lane.direction)
            bus_center = (lane.center[0] + side[0] * 8, lane.center[1] + side[1] * 8)
            _draw_lane_arrows(surface, bus_center, lane.direction, bus_movements, config.BUS_ARROW_COLOR)


def _draw_lane_arrows(
    surface: pygame.Surface,
    center: tuple[float, float],
    direction: str,
    movements: frozenset[str],
    color: tuple[int, int, int] = config.ARROW_COLOR,
) -> None:
    if not movements:
        return
    x, y = int(center[0]), int(center[1])
    vector = {"west_to_east": (1, 0), "east_to_west": (-1, 0), "north_to_south": (0, 1), "south_to_north": (0, -1)}[direction]
    if "straight" in movements:
        forward = _scale(vector, 13)
        tail = (x - forward[0], y - forward[1])
        head = (x + forward[0], y + forward[1])
        pygame.draw.line(surface, color, tail, head, 3)
        pygame.draw.polygon(surface, color, _arrow_head(head, vector, 8))

    if "left" in movements:
        _draw_turn_arrow(surface, (x, y), vector, "left", color)
    if "right" in movements:
        _draw_turn_arrow(surface, (x, y), vector, "right", color)


def _draw_turn_arrow(
    surface: pygame.Surface,
    center: tuple[int, int],
    forward: tuple[int, int],
    turn: str,
    color: tuple[int, int, int],
) -> None:
    side = (forward[1], -forward[0])
    if turn == "right":
        side = (-side[0], -side[1])
    start = (center[0] - forward[0] * 3, center[1] - forward[1] * 3)
    bend = (center[0] + forward[0] * 7 + side[0] * 8, center[1] + forward[1] * 7 + side[1] * 8)
    end = (center[0] + forward[0] * 12 + side[0] * 11, center[1] + forward[1] * 12 + side[1] * 11)
    pygame.draw.lines(surface, color, False, (start, bend, end), 2)
    pygame.draw.polygon(surface, color, _arrow_head(end, side, 6))


def _left_vector(direction: str) -> tuple[int, int]:
    forward = {"west_to_east": (1, 0), "east_to_west": (-1, 0), "north_to_south": (0, 1), "south_to_north": (0, -1)}[direction]
    return forward[1], -forward[0]


def _arrow_head(tip: tuple[int, int], direction: tuple[int, int], size: int) -> tuple[tuple[int, int], ...]:
    perpendicular = (-direction[1], direction[0])
    base = (tip[0] - direction[0] * size, tip[1] - direction[1] * size)
    half = size * 0.55
    return (
        tip,
        (int(base[0] + perpendicular[0] * half), int(base[1] + perpendicular[1] * half)),
        (int(base[0] - perpendicular[0] * half), int(base[1] - perpendicular[1] * half)),
    )


def _scale(vector: tuple[int, int], amount: int) -> tuple[int, int]:
    return vector[0] * amount, vector[1] * amount
