from ..rand import Seed
from ..math.rect import Rect
from ..math import math

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
    left: Self | None
    right: Self | None
    root: bool = False
    room: Rect | None = None
    _debug_color: Tuple[int, int, int] | None = None

    def _get_debug_color(self) -> Tuple[int, int, int]:
        if self._debug_color is None:
            r = int(random.random() * 255)
            g = int(random.random() * 255)
            b = int(random.random() * 255)
            self._debug_color = (r, g, b)
        return self._debug_color


class BSP:
    def __init__(self, width: int, height: int, min_room_size: int, max_room_size: int):
        self.width: int = width
        self.height: int = height
        self.min_node_size: int = min_room_size
        self.max_room_size: int = max_room_size
        self.rooms: int = 0
        self.root: Node | None = None

    def generate(self, seed: str, max_depth: int) -> None:
        self.root = Node(False, False, self.width,
                         self.height, None, None, root=True)
        random.seed(Seed(seed).get())
        horizontal = bool(random.getrandbits(1))
        width, height = 0, 0
        if horizontal:
            width = random.randint(self.min_node_size, self.width)
            self.root.left = Node(True, horizontal, width,
                                  self.height, None, None)
            self.root.right = Node(
                False, horizontal, self.width - width, self.height - height, None, None
            )
        else:
            height = random.randint(self.min_node_size, self.height)
            self.root.left = Node(
                True, horizontal, self.width, height, None, None)
            self.root.right = Node(
                False, horizontal, self.width, self.height - height, None, None
            )

        self._generate(self.root.left, 1, max_depth)
        self._generate(self.root.right, 1, max_depth)

    def _generate(
        self,
        node: Node,
        depth: int,
        max_depth: int,
    ) -> None:
        if depth >= max_depth:
            return

        max_width = node.width - self.min_node_size
        max_height = node.height - self.min_node_size

        if max_width < self.min_node_size and max_height < self.min_node_size:
            return

        horizontal = False

        if max_width >= self.min_node_size and max_height >= self.min_node_size:
            horizontal = max_width > max_height
        elif max_width >= self.min_node_size:
            horizontal = True
        elif max_height >= self.min_node_size:
            horizontal = False

        next_width, next_height = 0, 0
        if horizontal:
            next_width = random.randint(self.min_node_size, max_width)
            next_height = node.height
        else:
            next_width = node.width
            next_height = random.randint(self.min_node_size, max_height)

        if horizontal:
            node.left = Node(True, horizontal, next_width,
                             node.height, None, None)
            node.right = Node(
                False, horizontal, node.width - next_width, node.height, None, None
            )
        else:
            node.left = Node(True, horizontal, node.width,
                             next_height, None, None)
            node.right = Node(
                False, horizontal, node.width, node.height - next_height, None, None
            )

        self._generate(node.left, depth + 1, max_depth)
        self._generate(node.right, depth + 1, max_depth)

    def generate_rooms(
        self, min_size: Tuple[int, int], max_size: Tuple[int, int]
    ) -> None:
        self.min_width, self.min_height = min_size
        self.max_width, self.max_height = max_size
        if self.root is not None:
            self._generate_rooms(self.root.left)
            self._generate_rooms(self.root.right)

    def _generate_rooms(self, node: Node | None) -> None:
        if node is not None:
            if node.left is None and node.right is None:
                if node.width > self.min_width and node.height > self.min_height:
                    width = math.clamp(
                        random.randint(self.min_width, self.max_width),
                        self.min_width,
                        node.width,
                    )
                    height = math.clamp(
                        random.randint(self.min_height, self.max_width),
                        self.min_height,
                        node.height,
                    )
                    x = random.randint(0, abs(node.width - width))
                    y = random.randint(0, abs(node.height - height))
                    node.room = Rect(x, y, width, height)
                    self.rooms += 1
            else:
                self._generate_rooms(node.left)
                self._generate_rooms(node.right)

    def prune(self, max_rooms: int) -> None:
        if self.rooms > max_rooms:
            while self.rooms > max_rooms:
                _ = self._prune(self.root, max_rooms)

    def _prune(self, node: Node | None, max_rooms: int) -> bool:
        if self.rooms <= max_rooms:
            return False

        if node is not None:
            if node.left is None and node.right is None:
                if node.room is not None:
                    if bool(random.getrandbits(1)):
                        self.rooms -= 1
                        node.room = None
                        return True

            if self._prune(node.left, max_rooms):
                self.left = None
            if self._prune(node.right, max_rooms):
                self.right = None

        return False

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

            pygame.draw.rect(
                surface,
                node._get_debug_color(),
                (x, y, node.width, node.height),
                width=2,
            )

            if node.room is not None:
                pygame.draw.rect(
                    surface,
                    node._get_debug_color(),
                    (
                        x + node.room.x,
                        y + node.room.y,
                        node.room.w,
                        node.room.h,
                    ),
                )

            self._debug_render(surface, node.left, node.right, x, y)
            self._debug_render(surface, node.right, node.left, x, y)
            self._debug_render(surface, node.right, node.left, x, y)
