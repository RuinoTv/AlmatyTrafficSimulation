"""Pygame арқылы жол мен қиылыстың статикалық пішіндерін сызу құралдары."""
import pygame
from . import config
def road_rectangles() -> tuple[pygame.Rect, pygame.Rect]:
    """Шығыс-батыс және солтүстік-оңтүстік жолдарының тік төртбұрыштарын қайтарады."""
    horizontal = pygame.Rect(
        0,
        config.CENTER_Y - config.ABAY_HALF_WIDTH,
        config.WINDOW_WIDTH,
        config.ABAY_HALF_WIDTH * 2,
    )
    vertical = pygame.Rect(
        config.CENTER_X - config.SEIFULLIN_HALF_WIDTH,
        0,
        config.SEIFULLIN_HALF_WIDTH * 2,
        config.WINDOW_HEIGHT,
    )
    return horizontal, vertical
def draw_road_surface(surface: pygame.Surface) -> None:
    """Жалғасқан жол беттерін және жұмырланған сыртқы бұрыштарды сызады."""
    horizontal, vertical = road_rectangles()
    pygame.draw.rect(surface, config.ASPHALT_COLOR, horizontal)
    pygame.draw.rect(surface, config.ASPHALT_COLOR, vertical)
    # Ширек шеңберлі ойықтар жол қиылысындағы төртбұрышты бұрыштарды жұмсартады.
    left, right = config.CENTER_X - config.INTERSECTION_HALF_WIDTH, config.CENTER_X + config.INTERSECTION_HALF_WIDTH
    top, bottom = config.CENTER_Y - config.INTERSECTION_HALF_HEIGHT, config.CENTER_Y + config.INTERSECTION_HALF_HEIGHT
    radius = config.CORNER_RADIUS
    for rect in (
        pygame.Rect(left - radius, top - radius, radius * 2, radius * 2),
        pygame.Rect(right - radius, top - radius, radius * 2, radius * 2),
        pygame.Rect(left - radius, bottom - radius, radius * 2, radius * 2),
        pygame.Rect(right - radius, bottom - radius, radius * 2, radius * 2),
    ):
        pygame.draw.circle(surface, config.GROUND_COLOR, rect.center, radius)
    # Жіңішке жиек жол мен оның айналасындағы жердің шекарасын айқындайды.
    pygame.draw.rect(surface, config.ROAD_EDGE_COLOR, horizontal, 2)
    pygame.draw.rect(surface, config.ROAD_EDGE_COLOR, vertical, 2)
def draw_lane_markings(surface: pygame.Surface) -> None:
    """Ашық қиылыс аймағынан тыс жолақ бөлгіш үзік сызықтарды сызады."""
    cx, cy = config.CENTER_X, config.CENTER_Y
    start_x = config.INTERSECTION_HALF_WIDTH
    start_y = config.INTERSECTION_HALF_HEIGHT
    dash, gap = config.LANE_DASH_LENGTH, config.LANE_DASH_GAP
    # Абай даңғылының медианасы қарсы бағыттарды бөліп, әр жағында төрт жолақ қалдырады.
    for lane in range(1, config.ABAY_LANES_PER_DIRECTION):
        offset = config.MEDIAN_WIDTH / 2 + lane * config.ABAY_LANE_WIDTH
        for y in (cy - offset, cy + offset):
            for x in range(0, cx - start_x - dash, dash + gap):
                pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, y), (x + dash, y), 2)
            for x in range(cx + start_x, config.WINDOW_WIDTH, dash + gap):
                pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, y), (min(x + dash, config.WINDOW_WIDTH), y), 2)
    # Сейфуллин даңғылында физикалық медиананың орнына қос үзік орта сызық қолданылады.
    for lane in range(1, config.SEIFULLIN_LANES_PER_DIRECTION):
        x = cx - config.SEIFULLIN_HALF_WIDTH + lane * config.SEIFULLIN_LANE_WIDTH
        for y in range(0, cy - start_y - dash, dash + gap):
            pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, y), (x, y + dash), 2)
        for y in range(cy + start_y, config.WINDOW_HEIGHT, dash + gap):
            pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, y), (x, min(y + dash, config.WINDOW_HEIGHT)), 2)
    for x in (cx - 4, cx + 4):
        for y in range(0, cy - start_y - dash, dash + gap):
            pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, y), (x, y + dash), 2)
        for y in range(cy + start_y, config.WINDOW_HEIGHT, dash + gap):
            pygame.draw.line(surface, config.LANE_MARKING_COLOR, (x, y), (x, min(y + dash, config.WINDOW_HEIGHT)), 2)
def draw_median(surface: pygame.Surface) -> None:
    """Абай даңғылының медианасын көгалдандырылған екі бөлек бөлік етіп сызады."""
    half_length = config.MEDIAN_HALF_LENGTH
    opening = config.MEDIAN_OPENING_HALF_LENGTH
    median_rects = (
        pygame.Rect(config.CENTER_X - half_length, config.CENTER_Y - config.MEDIAN_WIDTH // 2, half_length - opening, config.MEDIAN_WIDTH),
        pygame.Rect(config.CENTER_X + opening, config.CENTER_Y - config.MEDIAN_WIDTH // 2, half_length - opening, config.MEDIAN_WIDTH),
    )
    for rect in median_rects:
        pygame.draw.rect(surface, config.MEDIAN_COLOR, rect, border_radius=7)
        # Қарапайым бұталар медиананы сыртқы сурет файлдарынсыз көрнекі етеді.
        for x in range(rect.left + 14, rect.right - 6, 32):
            pygame.draw.circle(surface, config.MEDIAN_DETAIL_COLOR, (x, rect.centery), 5)