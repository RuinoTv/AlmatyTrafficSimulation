"""Абай мен Сейфуллин қиылысының статикалық картасын құрастыру және сызу."""
import pygame
from . import config
from .geometry import draw_lane_markings, draw_median, draw_road_surface
from .lanes import INCOMING_LANES
class Intersection:
    """Қиылыстың бастапқы статикалық үлгісін экран бетіне сызады."""
    def __init__(self) -> None:
        self.lanes = INCOMING_LANES
        self._font: pygame.font.Font | None = None
        self._small_font: pygame.font.Font | None = None
    def draw(self, surface: pygame.Surface) -> None:
        """Жерді, жолдарды, белгілерді, медиананы және түсіндірме жазуларды сызады."""
        surface.fill(config.GROUND_COLOR)
        draw_road_surface(surface)
        draw_lane_markings(surface)
        draw_median(surface)
        self._draw_labels(surface)
    def _draw_labels(self, surface: pygame.Surface) -> None:
        if self._font is None:
            self._font = pygame.font.SysFont("arial", 20, bold=True)
            self._small_font = pygame.font.SysFont("arial", 16)
        assert self._small_font is not None
        self._label(surface, "СОЛТҮСТІК · Сейфуллин", (config.CENTER_X, 28), self._font, centered=True)
        self._label(surface, "ОҢТҮСТІК · Сейфуллин", (config.CENTER_X, config.WINDOW_HEIGHT - 28), self._font, centered=True)
        self._label(surface, "БАТЫС · Абай", (24, config.CENTER_Y - config.ABAY_HALF_WIDTH - 30), self._small_font)
        self._label(surface, "ШЫҒЫС · Абай", (config.WINDOW_WIDTH - 145, config.CENTER_Y - config.ABAY_HALF_WIDTH - 30), self._small_font)
        legend = "Кіру жолақтары: Б 4  |  Ш 4  |  С 5  |  О 5  (барлығы 18)"
        panel = pygame.Rect(config.CENTER_X - 207, config.WINDOW_HEIGHT - 47, 414, 30)
        pygame.draw.rect(surface, (37, 43, 38), panel, border_radius=5)
        self._label(surface, legend, panel.center, self._small_font, centered=True)
    @staticmethod
    def _label(
        surface: pygame.Surface,
        text: str,
        position: tuple[int, int],
        font: pygame.font.Font,
        centered: bool = False,
    ) -> None:
        """Жазуды көлеңкесімен бірге экран бетіне орналастырады."""
        shadow = font.render(text, True, config.TEXT_SHADOW_COLOR)
        label = font.render(text, True, config.TEXT_COLOR)
        rect = label.get_rect()
        rect.center = position if centered else rect.center
        if not centered:
            rect.topleft = position
        shadow_rect = rect.move(1, 2)
        surface.blit(shadow, shadow_rect)
        surface.blit(label, rect)