from abc import ABCMeta, abstractmethod
from typing import List, Tuple

__all__ = []


class FOVTile(metaclass=ABCMeta):
    @abstractmethod
    def set_visible(self, value: bool) -> None:
        pass

    @abstractmethod
    def is_wall(self) -> bool:
        pass

class FOV:
    def __init__(self, radius):
        self.radius = radius

    def check_visibility(self, x: int, y: int, tiles: List[List[FOVTile]]):
        tiles[y][x].set_visible(True)
        # positions = self._check_y(x, y, 0, -1, tiles)
        # positions.extend(self._check_y(x, y, 0, 1, tiles))
        positions = self._check_x(x, y, -1, 0, tiles)
        positions.extend(self._check_x(x, y, 1, 0, tiles))
        for row in positions:
            for col in row:
                x, y = col
                tiles[y][x].set_visible(True)

    def _check_y(self, px: int, py: int, dx: int, dy: int, tiles: List[List[FOVTile]]) -> List[List[Tuple[int, int]]]:
        count = 1
        positions: List[List[Tuple[int, int]]] = []
        start_y = py + dy
        height = len(tiles)
        width = len(tiles[0])
        for y in range(0, self.radius):
            row: List[Tuple[int, int]] = []
            new_y = start_y + y * dy
            if 0 <= new_y < height:
                for x in range(-count, count+1):
                    new_x = px + x
                    if 0 <= new_x < width:
                        row.append((new_x, new_y))
                positions.append(row)
            count += 1
        return positions

    def _check_x(self, px: int, py: int, dx: int, dy: int, tiles: List[List[FOVTile]]) -> List[List[Tuple[int, int]]]:
        count = 1
        positions: List[List[Tuple[int, int]]] = []
        start_x = px + dx
        height = len(tiles)
        width = len(tiles[0])
        for x in range(0, self.radius):
            row: List[Tuple[int, int]] = []
            new_x = start_x + x * dx
            if 0 <= new_x < width:
                for y in range(-count, count + 1):
                    new_y = py + y
                    if 0 <= new_y < height:
                        row.append((new_x, new_y))
                positions.append(row)
            count += 1
        return positions
