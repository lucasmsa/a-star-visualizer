import math
import random
import heapq

import pytest

from astar.grid import Grid
from astar.search import a_star, SQRT2


def open_grid(width, height):
    return Grid.from_strings(["." * width] * height)


def brute_force_cost(grid, start, goal, connectivity):
    """Independent Dijkstra used only to check optimality of the A* result."""
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    if connectivity == 8:
        moves += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    dist = {start: 0.0}
    heap = [(0.0, start)]
    while heap:
        d, (x, y) = heapq.heappop(heap)
        if (x, y) == goal:
            return d
        if d > dist[(x, y)]:
            continue
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if not grid.in_bounds(nx, ny) or grid.is_wall(nx, ny):
                continue
            if dx and dy and (grid.is_wall(x + dx, y) or grid.is_wall(x, y + dy)):
                continue
            step = SQRT2 if dx and dy else 1.0
            nd = d + step
            if nd < dist.get((nx, ny), math.inf):
                dist[(nx, ny)] = nd
                heapq.heappush(heap, (nd, (nx, ny)))
    return math.inf


def test_diagonal_steps_cost_sqrt2():
    result = a_star(open_grid(5, 5), (0, 0), (4, 4), connectivity=8)
    assert result.found
    assert result.path[0] == (0, 0) and result.path[-1] == (4, 4)
    assert len(result.path) == 5
    assert result.cost == pytest.approx(4 * SQRT2)


def test_four_connectivity_has_no_diagonals():
    result = a_star(open_grid(5, 5), (0, 0), (4, 4), connectivity=4)
    assert result.found
    assert result.cost == pytest.approx(8.0)
    for (x0, y0), (x1, y1) in zip(result.path, result.path[1:]):
        assert abs(x0 - x1) + abs(y0 - y1) == 1


def test_start_equals_goal():
    result = a_star(open_grid(3, 3), (1, 1), (1, 1))
    assert result.found
    assert result.path == [(1, 1)]
    assert result.cost == 0.0
    assert result.expansion_order == [(1, 1)]


def test_no_path_returns_empty_path_and_full_expansion():
    grid = Grid.from_strings([
        "..#..",
        "..#..",
        "..#..",
    ])
    result = a_star(grid, (0, 0), (4, 0))
    assert not result.found
    assert result.path == []
    assert math.isinf(result.cost)
    assert set(result.expansion_order) == {(x, y) for x in range(2) for y in range(3)}


def test_no_corner_cutting_between_two_walls():
    grid = Grid.from_strings([
        ".#",
        "#.",
    ])
    result = a_star(grid, (0, 0), (1, 1), connectivity=8)
    assert not result.found


def test_neighbors_never_leave_the_grid():
    grid = open_grid(4, 3)
    result = a_star(grid, (0, 0), (3, 2))
    for x, y in result.expansion_order:
        assert grid.in_bounds(x, y)


def test_tie_breaking_prefers_lower_h_then_insertion_order():
    result = a_star(open_grid(2, 2), (0, 0), (1, 1), connectivity=4, heuristic="manhattan")
    assert result.expansion_order == [(0, 0), (0, 1), (1, 1)]


@pytest.mark.parametrize("connectivity", [4, 8])
@pytest.mark.parametrize("seed", range(12))
def test_a_star_is_optimal_against_dijkstra(seed, connectivity):
    rng = random.Random(seed)
    width, height = 12, 9
    rows = ["".join("#" if rng.random() < 0.28 else "." for _ in range(width)) for _ in range(height)]
    grid = Grid.from_strings(rows)
    free = [(x, y) for y in range(height) for x in range(width) if not grid.is_wall(x, y)]
    start, goal = rng.sample(free, 2)
    result = a_star(grid, start, goal, connectivity=connectivity)
    expected = brute_force_cost(grid, start, goal, connectivity)
    if math.isinf(expected):
        assert not result.found
    else:
        assert result.found
        assert result.cost == pytest.approx(expected)
        for (x0, y0), (x1, y1) in zip(result.path, result.path[1:]):
            assert max(abs(x0 - x1), abs(y0 - y1)) == 1
            assert not grid.is_wall(x1, y1)


def test_heuristics_are_admissible_on_open_grid():
    grid = open_grid(7, 7)
    for name in ["manhattan", "euclidean", "chebyshev", "octile"]:
        connectivity = 4 if name == "manhattan" else 8
        result = a_star(grid, (0, 0), (6, 3), connectivity=connectivity, heuristic=name)
        assert result.found
        assert result.cost == pytest.approx(brute_force_cost(grid, (0, 0), (6, 3), connectivity))
