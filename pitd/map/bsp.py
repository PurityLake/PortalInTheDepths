from ..rand import Seed
from dataclasses import dataclass

import pygame
import random
from typing import Self, Tuple


@dataclass
class Room:
    x: int
    y: int
    width: int
    height: int


@dataclass
class Node:
    is_left: bool
    horizontal: bool
    width: int
    height: int
    left: Self | None
    right: Self | None
    root: bool = False
    room: Room | None = None
    _debug_color: Tuple[int, int, int] | None = None

    def _get_debug_color(self) -> Tuple[int, int, int]:
        if self._debug_color is None:
            r = int(random.random() * 255)
            g = int(random.random() * 255)
            b = int(random.random() * 255)
            self._debug_color = (r, g, b)
        return self._debug_color


class BSP:
    def __init__(self, width: int, height: int, min_room_size: int):
        self.width: int = width
        self.height: int = height
        self.min_room_size: int = min_room_size
        self.root: Node | None = None

    def generate(self, seed: str, max_depth: int) -> None:
        node: Node = Node(False, False, self.width, self.height, None, None, root=True)
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
        left = Node(True, False, 0, 0, None, None)
        right = Node(False, False, 0, 0, None, None)

        rand_width = random.randint(0, width)
        rand_height = random.randint(0, height)

        left.horizontal = right.horizontal = bool(random.getrandbits(1))

        if left.horizontal:
            left.height = right.height = height
            data = [rand_width, width - rand_width]
            random.shuffle(data)
            left.width, right.width = data
        else:
            left.width = right.width = width
            data = [rand_height, height - rand_height]
            random.shuffle(data)
            left.height, right.height = data

        node.left = self._generate(left, left.width, left.height, depth + 1, max_depth)
        node.right = self._generate(
            right, right.width, right.height, depth + 1, max_depth
        )
        return node

    def generate_rooms(self) -> None:
        if self.root is not None:
            self._generate_rooms(self.root.left)
            self._generate_rooms(self.root.right)

    def _generate_rooms(self, node: Node | None) -> None:
        if node is not None:
            if node.left is None and node.right is None:
                if node.width > self.min_room_size and node.height > self.min_room_size:
                    width = random.randint(self.min_room_size, node.width)
                    height = random.randint(self.min_room_size, node.height)
                    x = random.randint(0, abs(node.width - width))
                    y = random.randint(0, abs(node.height - height))
                    node.room = Room(x, y, width, height)
            else:
                self._generate_rooms(node.left)
                self._generate_rooms(node.right)

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
                        node.room.width,
                        node.room.height,
                    ),
                )

            self._debug_render(surface, node.left, node.right, x, y)
            self._debug_render(surface, node.right, node.left, x, y)
