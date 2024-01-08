from dataclasses import dataclass
from typing import Self


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    def collides(self, other: Self) -> bool:
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )
