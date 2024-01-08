from dataclasses import dataclass
from random import randint
from typing import Self


@dataclass
class Node:
    is_left: bool
    horizontal: bool
    percent: float
    left: Self | None
    right: Self | None


class BSP:
    def __init__(self, width: int, height: int, min_size: int, max_size: int):
        self.width: int = width
        self.height: int = height
        self.min_size: int = min_size
        self.max_size: int = max_size
        self.root: Node | None = None

    def generate(self, seed: str, max_depth: int) -> None:
        pass
