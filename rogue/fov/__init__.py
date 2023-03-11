import dataclasses
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from typing import List, Set, Tuple

__all__ = []


class Octant(Enum):
    # UP
    NNW = auto()
    NNE = auto()
    # LEFT
    WNW = auto()
    WSW = auto()
    # DOWN
    SSW = auto()
    SSE = auto()
    # RIGHT
    ESE = auto()
    ENE = auto()


class FOVTile(metaclass=ABCMeta):
    @abstractmethod
    def set_visible(self, value: bool) -> None:
        pass

    @abstractmethod
    def is_wall(self) -> bool:
        pass


@dataclasses.dataclass
class Angles:
    start: float
    middle: float
    end: float


class FOV:
    def __init__(self, radius):
        self.radius = radius

    def check_visibility(self, x: int, y: int, tiles: List[List[FOVTile]]):
        tiles[y][x].set_visible(True)
        positions = self._check_y(x, y, -1, -1, tiles)
        positions.update(self._check_y(x, y, 1, -1, tiles))
        positions.update(self._check_y(x, y, -1, 1, tiles))
        positions.update(self._check_y(x, y, 1, 1, tiles))
        positions.update(self._check_x(x, y, -1, 1, tiles))
        positions.update(self._check_x(x, y, 1, 1, tiles))
        positions.update(self._check_x(x, y, -1, -1, tiles))
        positions.update(self._check_x(x, y, 1, -1, tiles))
        for row in positions:
            x, y = row
            tiles[y][x].set_visible(True)

    def _is_visible(self, angles: Angles, walls: List[Angles], is_wall: bool) -> bool:
        start_vis: bool = True
        mid_vis: bool = True
        end_vis: bool = True

        for wall in walls:
            if wall.start < angles.start < wall.end:
                start_vis = False
            if wall.start < angles.middle < wall.end:
                mid_vis = False
            if wall.start < angles.end < wall.end:
                end_vis = False

        if is_wall:
            return start_vis or mid_vis or end_vis
        else:
            return (start_vis and mid_vis) or (mid_vis and end_vis)

    def _add_wall(self, walls: List[Angles], new: Angles) -> List[Angles]:
        angle: Angles = Angles(new.start, new.middle, new.end)
        new_walls: List[Angles] = [wall for wall in walls if not self._combine(wall, angle)]
        new_walls.append(angle)
        return new_walls

    def _combine(self, old: Angles, new: Angles) -> bool:
        low: Angles
        high: Angles
        # if their near values are equal, they overlap
        if old.start < new.start:
            low = old
            high = new
        elif new.start < old.start:
            low = new
            high = old
        else:
            new.end = max(old.end, new.end)
            return True

        # If they overlap, combine and return True
        if low.end >= high.start:
            new.start = min(low.start, high.start)
            new.end = max(low.end, high.end)
            return True

        return False

    def _check_y(self, px: int, py: int, dx: int, dy: int, tiles: List[List[FOVTile]]) -> Set[Tuple[int, int]]:
        count = 1
        positions: Set[Tuple[int, int]] = set()
        start_y = py + dy
        height = len(tiles)
        width = len(tiles[0])
        walls: List[Angles] = []
        for y in range(0, self.radius):
            new_y = start_y + y * dy
            if 0 <= new_y < height:
                number_of_cells = count + abs(dx)
                for x in range(0, count * dx + dx, dx):
                    new_x = px + x
                    if 0 <= new_x < width:
                        angle_range = 1.0 / number_of_cells
                        start_angle = abs(x) * angle_range
                        middle_angle = start_angle + (angle_range / 2.0)
                        end_angle = start_angle + angle_range
                        print(f'{start_angle:.3f}, {middle_angle:.3f}, {end_angle:.3f}')
                        is_wall = tiles[new_y][new_x].is_wall()
                        obj: Angles = Angles(start_angle, middle_angle, end_angle)
                        if self._is_visible(obj, walls, is_wall):
                            positions.add((new_x, new_y))
                            if is_wall:
                                walls = self._add_wall(walls, Angles(start_angle, middle_angle, end_angle))
                        else:
                            walls = self._add_wall(walls, Angles(start_angle, middle_angle, end_angle))
            count += 1
        return positions

    def _check_x(self, px: int, py: int, dx: int, dy: int, tiles: List[List[FOVTile]]) -> Set[Tuple[int, int]]:
        count = 1
        positions: Set[Tuple[int, int]] = set()
        start_x = px + dx
        height = len(tiles)
        width = len(tiles[0])
        walls: List[Angles] = []
        for x in range(0, self.radius):
            new_x = start_x + x * dx
            if 0 <= new_x < width:
                number_of_cells = count + abs(dy)
                for y in range(0, count * dy + dy, dy):
                    new_y = py + y
                    if 0 <= new_y < height:
                        angle_range = 1.0 / number_of_cells
                        start_angle = abs(x) * angle_range
                        middle_angle = start_angle + (angle_range / 2.0)
                        end_angle = start_angle + angle_range
                        is_wall = tiles[new_y][new_x].is_wall()
                        obj: Angles = Angles(start_angle, middle_angle, end_angle)
                        if self._is_visible(obj, walls, is_wall):
                            positions.add((new_x, new_y))
                            if is_wall:
                                walls = self._add_wall(walls, Angles(start_angle, middle_angle, end_angle))
                        else:
                            walls = self._add_wall(walls, Angles(start_angle, middle_angle, end_angle))
            count += 1
        return positions
