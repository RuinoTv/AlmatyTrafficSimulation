"""Бағдарламаның негізгі іске қосу нүктесі."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

import pygame

from traffic_sim.map import Intersection
from traffic_sim.map.config import WINDOW_SIZE, WINDOW_TITLE


def main() -> None:
    """Қиылыстың статикалық көрінісін көрсетіп, оқиғалар циклін іске қосады."""
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    intersection = Intersection()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        intersection.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
