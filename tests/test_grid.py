from pathlib import Path

import pytest

from astar.grid import Grid, load_occupancy_grid

ROOT = Path(__file__).resolve().parents[1]


def test_from_strings_round_trips():
    rows = ["..#", "#..", "..."]
    grid = Grid.from_strings(rows)
    assert grid.width == 3 and grid.height == 3
    assert grid.is_wall(2, 0) and grid.is_wall(0, 1)
    assert not grid.is_wall(1, 1)
    assert grid.to_strings() == rows


def test_from_strings_rejects_ragged_rows():
    with pytest.raises(ValueError):
        Grid.from_strings(["..", "..."])


def test_mapa_robotica_downsamples_to_72_by_56():
    grid = load_occupancy_grid(ROOT / "data" / "mapa_robotica.bmp")
    assert (grid.width, grid.height) == (72, 56)
    walls = sum(1 for y in range(grid.height) for x in range(grid.width) if grid.is_wall(x, y))
    assert 0 < walls < grid.width * grid.height
    # inflating walls by the robot radius can only add wall cells
    thin = load_occupancy_grid(ROOT / "data" / "mapa_robotica.bmp", erosion_size=0)
    thin_walls = sum(1 for y in range(thin.height) for x in range(thin.width) if thin.is_wall(x, y))
    assert walls >= thin_walls
