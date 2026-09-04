from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

from astar.grid import Grid
from astar.heuristics import HEURISTICS, SQRT2

Point = tuple[int, int]

# Orthogonal moves first, then diagonals. The web port uses the same order so
# that expansion order matches the fixtures.
NEIGHBOR_ORDER: tuple[Point, ...] = (
    (0, -1), (0, 1), (-1, 0), (1, 0),
    (-1, -1), (-1, 1), (1, -1), (1, 1),
)


@dataclass
class SearchResult:
    found: bool
    path: list[Point]
    expansion_order: list[Point]
    cost: float
    closed: set[Point] = field(default_factory=set)


def a_star(
    grid: Grid,
    start: Point,
    goal: Point,
    connectivity: int = 8,
    heuristic: str = "octile",
    weight: float = 1.0,
) -> SearchResult:
    """A* over an occupancy grid.

    Step cost is 1 orthogonally and sqrt(2) diagonally. Diagonal moves may not
    cut a corner: both orthogonal neighbours of the move must be free. Ties on
    f break on lower h, then on insertion order, so the expansion order is
    deterministic and reproducible in other languages.
    """
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    h_fn = HEURISTICS[heuristic]
    moves = NEIGHBOR_ORDER[:4] if connectivity == 4 else NEIGHBOR_ORDER

    def h(p: Point) -> float:
        return weight * h_fn(abs(p[0] - goal[0]), abs(p[1] - goal[1]))

    g_score: dict[Point, float] = {start: 0.0}
    parent: dict[Point, Point] = {}
    closed: set[Point] = set()
    expansion_order: list[Point] = []
    counter = 0
    heap: list[tuple[float, float, int, Point]] = [(h(start), h(start), counter, start)]

    while heap:
        f, _, _, current = heapq.heappop(heap)
        if current in closed:
            continue
        closed.add(current)
        expansion_order.append(current)

        if current == goal:
            return SearchResult(True, _reconstruct(parent, current), expansion_order, g_score[current], closed)

        cx, cy = current
        for dx, dy in moves:
            nx, ny = cx + dx, cy + dy
            if not grid.in_bounds(nx, ny) or grid.is_wall(nx, ny):
                continue
            if dx and dy and (grid.is_wall(cx + dx, cy) or grid.is_wall(cx, cy + dy)):
                continue
            neighbor = (nx, ny)
            if neighbor in closed:
                continue
            tentative = g_score[current] + (SQRT2 if dx and dy else 1.0)
            if tentative < g_score.get(neighbor, math.inf):
                g_score[neighbor] = tentative
                parent[neighbor] = current
                counter += 1
                hn = h(neighbor)
                heapq.heappush(heap, (tentative + hn, hn, counter, neighbor))

    return SearchResult(False, [], expansion_order, math.inf, closed)


def _reconstruct(parent: dict[Point, Point], node: Point) -> list[Point]:
    path = [node]
    while node in parent:
        node = parent[node]
        path.append(node)
    path.reverse()
    return path
