from __future__ import annotations

from dataclasses import dataclass
from math import floor
from pathlib import Path

WALL = "#"
FREE = "."


@dataclass(frozen=True)
class Grid:
    """Occupancy grid indexed as cells[y][x]; True means wall."""

    width: int
    height: int
    cells: tuple[tuple[bool, ...], ...]

    @classmethod
    def from_strings(cls, rows: list[str]) -> "Grid":
        if not rows:
            raise ValueError("grid needs at least one row")
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("all rows must have the same length")
        cells = tuple(tuple(ch == WALL for ch in row) for row in rows)
        return cls(width=width, height=len(rows), cells=cells)

    @classmethod
    def from_bool_rows(cls, rows: list[list[bool]]) -> "Grid":
        return cls(width=len(rows[0]), height=len(rows), cells=tuple(tuple(r) for r in rows))

    def to_strings(self) -> list[str]:
        return ["".join(WALL if wall else FREE for wall in row) for row in self.cells]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x: int, y: int) -> bool:
        return self.cells[y][x]

    def wall_count(self) -> int:
        return sum(1 for row in self.cells for wall in row if wall)


def load_occupancy_grid(
    image_path: str | Path,
    erosion_size: int = 7,
    resolution: int = 50,
    cells_per_block: int = 8,
    wall_threshold: int = 5,
) -> Grid:
    """Floor plan image to occupancy grid.

    1. Erode the image with a (2r+1)^2 rectangle so dark walls grow by the robot
       radius r in pixels (the robot is treated as a point afterwards).
    2. Threshold: gray < wall_threshold is wall.
    3. Downsample: the plan is split into floor(width / resolution) blocks per
       axis, each block becomes cells_per_block cells; a cell is a wall if any
       source pixel that maps to it is a wall.

    Defaults reproduce the 2021 run: 450x360 px plan, r = 7 px, 9x7 blocks of
    8x8 cells, so a 72x56 grid.
    """
    import cv2
    import numpy as np

    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(image_path)
    if erosion_size > 0:
        size = 2 * erosion_size + 1
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size), (erosion_size, erosion_size))
        image = cv2.erode(image, element)
    walls = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) < wall_threshold
    height, width = walls.shape
    grid_w = floor(width / resolution) * cells_per_block
    grid_h = floor(height / resolution) * cells_per_block

    cells = np.zeros((grid_h, grid_w), dtype=bool)
    ys, xs = np.nonzero(walls)
    cx = np.floor(xs * grid_w / width).astype(int)
    cy = np.floor(ys * grid_h / height).astype(int)
    cells[cy, cx] = True
    return Grid.from_bool_rows(cells.tolist())
