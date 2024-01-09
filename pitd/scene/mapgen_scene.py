from . import Scene
from ..map import map_gen

import pygame
from typing import Self, Any


class MapGenScene(Scene):
    def __init__(self):
        super().__init__()
        self._should_quit = False
        self.map_gen = map_gen.MapGen(50, 50)
        self.map_gen.generate(5, 9)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        self.map_gen._debug_render(surface, 10)
        pygame.display.flip()

    def update(self, dt: float) -> Self:
        return self

    def get_event(self, event: pygame.Event) -> None:
        pass

    def set_data(self, name: str, value: Any) -> None:
        pass

    def should_quit(self) -> bool:
        return self._should_quit
