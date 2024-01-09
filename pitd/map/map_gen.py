from ..rand import Seed
from .rect import Rect

from typing import List

import pygame
import random


def _random_offset(min: int, max: int) -> int:
    return random.randint(min, max)


class MapGen:
    def __init__(self, map_width: int, map_height: int, map_seed: str | None = None):
        self.map_width = map_width
        self.map_height = map_height
        self.map_seed = Seed(map_seed)
        self.map = [[0 for x in range(self.map_width)] for y in range(self.map_height)]

    def generate(self, min_size: int, max_size: int) -> None:
        random.seed(self.map_seed.get())
        rects: List[Rect] = []
        should_create = 0
        for y in range(1, self.map_height - 1):
            for x in range(1, self.map_width - 1):
                should_create = max(0, should_create - 1)
                if should_create == 0:
                    new_rect = self._create_random_rect(
                        x, y + _random_offset(0, 2), min_size, max_size
                    )
                    if not new_rect.is_out_of_bounds(self.map_width, self.map_width):
                        found = False
                        for rect in rects:
                            if rect.collides_near(new_rect):
                                found = True
                                should_create = rect.w + _random_offset(2, 3)
                                break
                        if not found:
                            rects.append(new_rect)
                            should_create = new_rect.w + _random_offset(3, 5)

        for rect in rects:
            if bool(random.getrandbits(1)):
                self._apply_rect(rect)

    def _create_random_rect(self, x: int, y: int, min_size: int, max_size: int) -> Rect:
        width = random.randint(min_size, max_size)
        height = random.randint(min_size, max_size)
        return Rect(x, y, width, height)

    def _apply_rect(self, rect: Rect) -> None:
        for y in range(rect.y, rect.y + rect.h):
            for x in range(rect.x, rect.x + rect.w):
                self.map[y][x] = 1

    def _debug_render(self, surface: pygame.Surface, tile_size: int) -> None:
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.map[y][x] == 0:
                    pygame.draw.rect(
                        surface,
                        (255, 0, 0),
                        (x * tile_size, y * tile_size, tile_size, tile_size),
                    )
                else:
                    pygame.draw.rect(
                        surface,
                        (255, 255, 255),
                        (x * tile_size, y * tile_size, tile_size, tile_size),
                    )
