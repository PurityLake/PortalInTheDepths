from dataclasses import dataclass
from typing import Self


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

    def is_out_of_bounds(self, width: int, height: int) -> bool:
        return (
            self.x < 0
            or self.y < 0
            or self.x + self.w >= width
            or self.y + self.h >= height
        )

    def collides(self, other: Self) -> bool:
        return (
            self.x < other.x + other.w
            and self.x + self.w > other.x
            and self.y < other.y + other.h
            and self.y + self.h > other.y
        )

    def collides_near(self, other: Self, padding: int = 1) -> bool:
        near_rect = Rect(
            max(0, self.x - padding),
            max(0, self.y - padding),
            self.w + padding * 2,
            self.h + padding * 2,
        )
        return (
            near_rect.x < other.x + other.w
            and near_rect.x + near_rect.w > other.x
            and near_rect.y < other.y + other.h
            and near_rect.y + near_rect.h > other.y
        )
