from __future__ import annotations

import math
from typing import Callable

SQRT2 = math.sqrt(2.0)

Heuristic = Callable[[int, int], float]


def manhattan(dx: int, dy: int) -> float:
    return float(dx + dy)


def euclidean(dx: int, dy: int) -> float:
    return math.sqrt(dx * dx + dy * dy)


def chebyshev(dx: int, dy: int) -> float:
    return float(max(dx, dy))


def octile(dx: int, dy: int) -> float:
    return (dx + dy) + (SQRT2 - 2.0) * min(dx, dy)


HEURISTICS: dict[str, Heuristic] = {
    "manhattan": manhattan,
    "euclidean": euclidean,
    "chebyshev": chebyshev,
    "octile": octile,
}
