from . import Scene
from ..map import bsp

import pygame
from typing import Self, Any


class BSPScene(Scene):
    def __init__(self):
        super().__init__()
        self._should_quit = False
        self.bsp = bsp.BSP(600, 600, 20)
        self.bsp.generate("test", 5)
        self.bsp.generate_rooms()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        self.bsp.debug_render(surface)
        pygame.display.flip()

    def update(self, dt: float) -> Self:
        return self

    def get_event(self, event: pygame.Event) -> None:
        pass

    def set_data(self, name: str, value: Any) -> None:
        pass

    def should_quit(self) -> bool:
        return self._should_quit
