from .scene import Scene

# from .scene.mapgen_scene import MapGenScene
from .scene.bsp_scene import BSPScene
import pygame
from typing import Tuple

__all__ = ["PITD"]


class PITD:
    def __init__(self, game_dir: str, size: Tuple[int, int]):
        self.game_dir: str = game_dir
        self.surface: pygame.Surface
        self.size: Tuple[int, int] = size
        self._setup()
        self.dt: float = -1.0
        self.scene: Scene = BSPScene()
        self.clock: pygame.Clock = pygame.Clock()
        self.running: bool = True

    def run(self) -> None:
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                self.scene.get_event(e)
                if self.running:
                    self.running = not self.scene.should_quit()
            self._update()
            self._render()
            self._tick()

    def _setup(self) -> None:
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("PITD")

    def _update(self) -> None:
        if self.dt < 0.0:
            pass
        self.scene.update(self.dt)

    def _render(self) -> None:
        self.scene.render(self.surface)
        pygame.display.flip()

    def _tick(self) -> None:
        self.dt = self.clock.tick(60) / 1000
