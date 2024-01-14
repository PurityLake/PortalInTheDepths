from . import Scene
from ..fov import FOV

import math
import os.path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List, Self, Tuple
import pygame


class MapScene(Scene):
    def __init__(self, game_dir: str):
        self.surfaceToDraw: pygame.Surface
        self.game_dir = game_dir
        self.font: pygame.Font = pygame.Font(size=20)
        self.pos: Tuple[int, int] = (0, 0)
        self.the_map: Map = Map(self.game_dir, os.path.join("resources", "testmap.map"))
        self.player_pos: Tuple[int, int] = self.the_map.player_pos
        self.player_keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        self.radius: int = 5
        self.max_dist: float = -1.0
        self._should_quit: bool = False
        self.fov: FOV = FOV(self.radius, Tile.is_wall, Tile.set_visible)
        self._setup()

    def _setup(self) -> None:
        self._create_map()

    def _create_map(self) -> None:
        self._write_to_surface()

    def _write_to_surface(self) -> None:
        if self.the_map.should_update_surface:
            self.surfaceToDraw = pygame.Surface(
                (self.the_map.width, self.the_map.height)
            )
            self.the_map.should_update_surface = False
        self.surfaceToDraw.fill((0, 0, 0))
        for row in self.the_map.map_lines:
            for col in row:
                col.set_visible(False)
        px, py = self.player_pos
        self.fov.check_visibility(px, py, self.the_map.map_lines)
        for row in self.the_map.map_lines:
            for col in row:
                if col.visible:
                    c = col.c
                    if col.has_player:
                        c = self.the_map.player_str
                        self.surfaceToDraw.blit(
                            self.font.render(c, True, (255, 255, 255)),
                            (col.x * 20, col.y * 20),
                        )
                    elif col.tile_type != TileType.EMPTY:
                        surf = self.font.render(
                            c,
                            True,
                            self._calc_color_from_distance(px, py, col.x, col.y),
                            _calc_color_from_distance(px, py, col.x, col.y),
                            _calc_color_from_distance(px, py, col.x, col.y),
                        )
                        self.surfaceToDraw.blit(surf, (col.x * 20, col.y * 20))

    def _calc_color_from_distance(
        self, px: int, py: int, tile_x: int, tile_y: int, alpha: int = 255
    ):
        if self.max_dist < 0.0:
            self.max_dist = math.sqrt(
                self.radius * self.radius + self.radius * self.radius
            )
        delta_x = px - tile_x
        delta_y = py - tile_y
        val = int(
            (1 - (math.sqrt(delta_x * delta_x + delta_y * delta_y) / self.max_dist))
            * 200
            % 200
        )
        return pygame.Color(val, val, val, alpha)

    def update(self, dt: float) -> Self:
        keys = pygame.key.get_pressed()
        x, y = self.player_pos

        if keys[pygame.K_w] and not self.player_keys[pygame.K_w]:
            y -= 1
        if keys[pygame.K_s] and not self.player_keys[pygame.K_s]:
            y += 1
        if keys[pygame.K_a] and not self.player_keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_d] and not self.player_keys[pygame.K_d]:
            x += 1

        if keys[pygame.K_ESCAPE]:
            self._should_quit = True

        self.player_keys = keys

        if self.player_pos != (x, y):
            if not self.the_map.map_lines[y][x].tile_type == TileType.WALL:
                px, py = self.player_pos
                self.the_map.set(px, py, "has_player", False)
                self.the_map.set(x, y, "has_player", True)
                self.player_pos = x, y
                self._write_to_surface()

        return self

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        surface.blit(self.surfaceToDraw, self.pos)

    def get_event(self, event: pygame.Event) -> None:
        pass

    def set_data(self, name: str, value: Any) -> Any:
        if name == "map":
            self.the_map.parse(value)
            self._create_map()

    def should_quit(self) -> bool:
        return self._should_quit


class TileType(Enum):
    FLOOR = auto()
    WALL = auto()
    EMPTY = auto()


@dataclass
class Tile:
    x: int
    y: int
    c: str
    tile_type: TileType
    has_player: bool = False
    visible: bool = True

    def set_visible(self, value: bool) -> None:
        self.visible = value

    def is_wall(self) -> bool:
        return self.tile_type == TileType.WALL


class Map:
    def __init__(self, game_dir: str, filename: str):
        self.filename: str = ""
        self.game_dir: str = game_dir
        self.chars: set = set()
        self.map_lines: List[List[Tile]] = []
        self.new_info: bool = True
        self.width: int = -1
        self.height: int = -1
        self.should_update_surface: bool = True
        self._mode: str = ""
        self.tile_data: dict = {}
        self.player_pos: Tuple[int, int] = (0, 0)
        self.player_str: str = "@"
        self.parse(os.path.join(self.game_dir, filename))

    def parse(self, filename: str) -> None:
        self.filename = os.path.join(self.game_dir, filename)
        with open(self.filename, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue

                if line == "[mapinfo]":
                    self._mode = "info"
                    continue
                elif line == "[defs]":
                    self._mode = "defs"
                    continue
                elif line == "[map]":
                    self._mode = "map"
                    continue
                elif line.startswith("[/"):
                    self._mode = ""
                    continue

                if self._mode == "info":
                    self._read_info(line)
                elif self._mode == "defs":
                    self._read_defs(line)
                elif self._mode == "map":
                    self._read_map(line)

    def set(self, x: int, y: int, key: str, value: Any) -> None:
        setattr(self.map_lines[y][x], key, value)

    def _read_info(self, line: str) -> None:
        split = line.split("=")
        if len(split) == 2:
            name = split[0]
            value = split[1]
            if name == "size":
                dims = value.split(",")
                width, height = (int(dims[0]) * 20, int(dims[1]) * 20)
                self.should_update_surface = (
                    self.width != width and self.height != height
                )
                self.width, self.height = width, height

    def _read_defs(self, line: str) -> None:
        split = line.split("=")
        if len(split) == 2:
            name = split[0]
            value = split[1]
            self.tile_data[value] = name

    def _read_map(self, line: str) -> None:
        row = []
        y = max(0, len(self.map_lines))
        for x, c in enumerate(line):
            self.chars.add(c)
            data = self.tile_data.get(c)
            if not data:
                row.append(Tile(x, y, " ", TileType.EMPTY, visible=False))
            else:
                self.chars.add(c)
                if data == "player":
                    self.player_pos = x, y
                    self.player_str = c
                    row.append(Tile(x, y, ".", TileType.FLOOR, True))
                elif data == "floor":
                    row.append(Tile(x, y, c, TileType.FLOOR))
                elif data == "wall":
                    row.append(Tile(x, y, c, TileType.WALL))
        self.map_lines.append(row)
