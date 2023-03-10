import os.path

from . import Scene
from typing import List, Self, Tuple
import pygame


class MapScene(Scene):
    def __init__(self, gamedir):
        self.gamedir = gamedir
        self.atlas: dict = {}
        self.speed: float = 100
        self.font: pygame.Font = pygame.Font(size=20)
        self.surfaceToDraw: pygame.Surface
        self.pos: Tuple[int, int] = (400, 300)
        self.width: int
        self.height: int
        self._setup()

    def _setup(self):
        charsToCreate = set()
        lines = []
        dims = ()
        testmappath = os.path.join(self.gamedir, 'resources', 'testmap.map')
        with open(testmappath, 'r') as f:
            dimsarr = f.readline().split(',')
            dims = (int(dimsarr[0]) * 20, int(dimsarr[1]) * 20)
            for line in f.readlines():
                for c in line:
                    charsToCreate.add(c)
                lines.append(line)

        for c in charsToCreate:
            self.atlas[c] = self.font.render(c, True, (255, 255, 255))

        self.surfaceToDraw = pygame.Surface(dims)
        for row_idx, row in enumerate(lines):
            for c_idx, c in enumerate(row):
                print(c_idx, row_idx)
                self.surfaceToDraw.blit(self.atlas[c], (c_idx * 20, row_idx * 20))

    def update(self, dt: float) -> Self:
        keys = pygame.key.get_pressed()
        x, y = self.pos

        if keys[pygame.K_w]:
            y -= self.speed * dt
        if keys[pygame.K_s]:
            y += self.speed * dt
        if keys[pygame.K_a]:
            x -= self.speed * dt
        if keys[pygame.K_d]:
            x += self.speed * dt

        self.pos = (x, y)

        return self

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        surface.blit(self.surfaceToDraw, self.pos)

    def get_event(self, event: pygame.Event) -> None:
        pass
