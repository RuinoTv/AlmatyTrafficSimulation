"""Статическая карта перекрестка с подписями за пределами дорожной схемы."""

from typing import Iterable, Sequence

import pygame

from . import config
from .geometry import draw_lane_markings, draw_median, draw_movement_arrows, draw_road_surface
from .lanes import INCOMING_LANES


class Intersection:
    """Рисует дорожную схему и отдельные поля подписей вокруг нее."""

    def __init__(self) -> None:
        self.lanes = INCOMING_LANES
        self._map_surface: pygame.Surface | None = None
        self._scaled_map: pygame.Surface | None = None
        self._scaled_size: int | None = None
        self._title_font: pygame.font.Font | None = None
        self._body_font: pygame.font.Font | None = None
        self._legend_font: pygame.font.Font | None = None

    def draw(self, surface: pygame.Surface) -> None:
        """Масштабирует квадратную карту и размещает подписи снаружи рамки."""
        self._ensure_map()
        width, height = surface.get_size()
        map_size = self._fit_map_size(width, height)
        map_rect = pygame.Rect((width - map_size) // 2, (height - map_size) // 2, map_size, map_size)

        surface.fill(config.GROUND_COLOR)
        assert self._map_surface is not None
        if self._scaled_size != map_size:
            self._scaled_map = pygame.transform.smoothscale(self._map_surface, (map_size, map_size))
            self._scaled_size = map_size
        assert self._scaled_map is not None
        surface.blit(self._scaled_map, map_rect)
        self._draw_annotations(surface, map_rect)

    def _ensure_map(self) -> None:
        if self._map_surface is not None:
            return
        self._map_surface = pygame.Surface((config.MAP_SIZE, config.MAP_SIZE))
        self._map_surface.fill(config.SIDEWALK_COLOR)
        draw_road_surface(self._map_surface)
        draw_lane_markings(self._map_surface)
        draw_median(self._map_surface)
        draw_movement_arrows(self._map_surface, self.lanes)

    @staticmethod
    def _fit_map_size(window_width: int, window_height: int) -> int:
        side_reserve = min(280, max(64, window_width // 5))
        vertical_reserve = min(110, max(44, window_height // 10))
        return max(1, min(window_width - 2 * side_reserve, window_height - 2 * vertical_reserve))

    def _draw_annotations(self, surface: pygame.Surface, map_rect: pygame.Rect) -> None:
        self._ensure_fonts(map_rect.width)
        assert self._title_font is not None
        assert self._body_font is not None
        assert self._legend_font is not None

        top_area = pygame.Rect(map_rect.left, 0, map_rect.width, map_rect.top)
        bottom_area = pygame.Rect(map_rect.left, map_rect.bottom, map_rect.width, surface.get_height() - map_rect.bottom)
        west_area = pygame.Rect(0, map_rect.top, map_rect.left, map_rect.height)
        east_area = pygame.Rect(map_rect.right, map_rect.top, surface.get_width() - map_rect.right, map_rect.height)

        self._draw_block(
            surface,
            top_area,
            ("СЕВЕР · УЛИЦА СЕЙФУЛЛИНА", "Въезд N1–N4 · 4 полосы"),
            centered=True,
        )
        self._draw_block(
            surface,
            bottom_area,
            ("ЮГ · УЛИЦА СЕЙФУЛЛИНА", "Въезд S1–S3 · 3 полосы · Алматинские горы"),
            centered=True,
        )
        self._draw_block(
            surface,
            west_area,
            ("ЗАПАД", "ПРОСПЕКТ АБАЯ", "Въезд W1–W4 · 4 полосы"),
            centered=True,
        )
        self._draw_block(
            surface,
            east_area,
            ("ВОСТОК", "ПРОСПЕКТ АБАЯ", "Въезд E1–E4 · 4 полосы"),
            centered=True,
            y_offset=map_rect.height // 12,
        )

    def _ensure_fonts(self, map_width: int) -> None:
        if self._title_font is not None:
            return
        title_size = max(13, min(18, map_width // 48))
        body_size = max(12, title_size - 2)
        legend_size = max(11, body_size - 1)
        font_path = pygame.font.match_font("arial") or pygame.font.match_font("dejavusans")
        self._title_font = pygame.font.Font(font_path, title_size)
        self._body_font = pygame.font.Font(font_path, body_size)
        self._legend_font = pygame.font.Font(font_path, legend_size)

    def _draw_block(
        self,
        surface: pygame.Surface,
        area: pygame.Rect,
        lines: Sequence[str],
        *,
        centered: bool,
        y_offset: int = 0,
        legend: bool = False,
    ) -> None:
        assert self._title_font is not None
        assert self._body_font is not None
        assert self._legend_font is not None
        padding = 8
        available_width = max(1, area.width - padding * 2)
        rendered_lines: list[tuple[str, pygame.font.Font, bool]] = []
        for line_index, line in enumerate(lines):
            is_heading = line_index == 0
            font = self._title_font if is_heading else self._legend_font if legend else self._body_font
            rendered_lines.extend((part, font, is_heading) for part in self._wrap_text(line, font, available_width))

        line_gap = 3
        total_height = sum(font.get_linesize() + line_gap for _, font, _ in rendered_lines) - line_gap
        y = area.top + (area.height - total_height) // 2 + y_offset
        for text, font, is_heading in rendered_lines:
            image = font.render(text, True, config.TEXT_COLOR)
            if centered:
                x = area.left + (area.width - image.get_width()) // 2
            else:
                x = area.left + padding
            if is_heading:
                pygame.draw.line(
                    surface,
                    config.MEDIAN_DETAIL_COLOR,
                    (x, y + font.get_linesize() + 2),
                    (min(area.right - padding, x + image.get_width()), y + font.get_linesize() + 2),
                    2,
                )
            surface.blit(image, (x, y))
            y += font.get_linesize() + line_gap

    @staticmethod
    def _wrap_text(text: str, font: pygame.font.Font, max_width: int) -> Iterable[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and font.size(candidate)[0] > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines
