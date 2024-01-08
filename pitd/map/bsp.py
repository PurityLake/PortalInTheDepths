from ..rand import Seed
from dataclasses import dataclass

import pygame
import random
from typing import Self, Tuple


@dataclass
class Node:
    is_left: bool
    horizontal: bool
    width: int
    height: int
    parent: Self | None
    left: Self | None
    right: Self | None
    root: bool = False
    _debug_color: Tuple[int, int, int] | None = None

    def _get_debug_color(self) -> Tuple[int, int, int]:
        if self._debug_color is None:
            r = int(random.random() * 255)
            g = int(random.random() * 255)
            b = int(random.random() * 255)
            self._debug_color = (r, g, b)
        return self._debug_color


class BSP:
    def __init__(self, width: int, height: int, min_width: int, max_size: int):
        self.width: int = width
        self.height: int = height
        self.min_width: int = min_width
        self.min_height: int = min_width
        self.max_size: int = max_size
        self.root: Node | None = None

    def debug_render(self, surface: pygame.Surface) -> None:
        if self.root is not None:
            self._debug_render(surface, self.root.left, self.root.right, 0, 0)
            self._debug_render(surface, self.root.right, self.root.left, 0, 0)

    def _debug_render(
        self,
        surface: pygame.Surface,
        node: Node | None,
        other: Node | None,
        x: int,
        y: int,
    ) -> None:
        if node is not None and other is not None:
            if not node.is_left and node.horizontal:
                x += other.width
            elif not node.is_left and not node.horizontal:
                y += other.height
            if node.width > self.min_height and node.height > self.min_width:
                pygame.draw.rect(
                    surface,
                    node._get_debug_color(),
                    (x, y, node.width, node.height),
                    width=2,
                )

            self._debug_render(surface, node.left, node.right, x, y)
            self._debug_render(surface, node.right, node.left, x, y)

    def generate(self, seed: str, max_depth: int) -> None:
        node: Node = Node(False, False, self.width, self.height, None, None, None, True)
        random.seed(Seed(seed).get())
        self.root = self._generate(node, self.width, self.height, 0, max_depth)

    def _generate(
        self,
        node: Node,
        width: int,
        height: int,
        depth: int,
        max_depth: int,
    ) -> Node | None:
        if depth >= max_depth:
            return None
        left = Node(True, False, 0, 0, node, None, None)
        right = Node(False, False, 0, 0, node, None, None)

        left.horizontal = right.horizontal = bool(random.getrandbits(1))

        if left.horizontal:
            left.height = right.height = height
            left.width = min(max(int(random.random() * width), 0), width)
            right.width = width - left.width
        else:
            left.width = right.width = width
            left.height = min(max(int(random.random() * height), 0), height)
            right.height = height - left.height

        node.left = self._generate(left, left.width, left.height, depth + 1, max_depth)
        node.right = self._generate(
            right, right.width, right.height, depth + 1, max_depth
        )
        return node
