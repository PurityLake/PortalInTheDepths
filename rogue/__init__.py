from .scene import Scene
from .scene.mapscene import MapScene
import pygame
from typing import Tuple

__all__ = ["Rogue"]


class Rogue:
    def __init__(self, gamedir, size: Tuple[int, int]):
        self.gamedir = gamedir
        self.surface: pygame.Surface
        self.size: Tuple[int, int] = size
        self._setup()
        self.dt: float = -1.0
        self.scene: Scene = MapScene(self.gamedir)
        self.clock: pygame.Clock = pygame.Clock()
        self.running: bool = True

    def run(self) -> None:
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                self.scene.get_event(e)
            self._update()
            self._render()
            self._tick()

    def _setup(self) -> None:
        pygame.init()
        pygame.font.init()
        self.surface: pygame.Surface = pygame.display.set_mode(self.size)

    def _update(self) -> None:
        if self.dt < 0.0:
            pass
        self.scene.update(self.dt)

    def _render(self) -> None:
        self.scene.render(self.surface)
        pygame.display.flip()

    def _tick(self) -> None:
        self.dt = self.clock.tick(60) / 1000
