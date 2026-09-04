"""Regenerate the golden fixtures consumed by the web port.

Run from the repo root: python scripts/make_fixtures.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astar.grid import Grid, load_occupancy_grid  # noqa: E402
from astar.search import NEIGHBOR_ORDER, a_star  # noqa: E402

OPEN_ROOM = [
    "..........",
    "..........",
    "....##....",
    "....##....",
    "....##....",
    "....##....",
    "..........",
    "..........",
]

CORRIDORS = [
    "....................",
    ".######.#######.###.",
    ".#....#.#.....#...#.",
    ".#.##.#.#.###.###.#.",
    ".#.#..#...#.#.....#.",
    ".#.#.####.#.#####.#.",
    ".#.#......#.......#.",
    ".#.#############.##.",
    ".#..............#...",
    ".################.#.",
    "..................#.",
    ".###############.##.",
    "...............#....",
    "##############.#.##.",
    "...............#....",
]


def fixture(name: str, grid: Grid, start, goal, connectivity=8, heuristic="octile", provenance=None):
    result = a_star(grid, start, goal, connectivity=connectivity, heuristic=heuristic)
    data = {
        "name": name,
        "connectivity": connectivity,
        "heuristic": heuristic,
        "cornerCutting": False,
        "neighborOrder": [list(m) for m in NEIGHBOR_ORDER[: 4 if connectivity == 4 else 8]],
        "width": grid.width,
        "height": grid.height,
        "grid": grid.to_strings(),
        "start": list(start),
        "goal": list(goal),
        "found": result.found,
        "cost": result.cost if result.found else None,
        "pathLength": len(result.path),
        "expansions": len(result.expansion_order),
        "path": [list(p) for p in result.path],
        "expansionOrder": [list(p) for p in result.expansion_order],
    }
    if provenance:
        data["provenance"] = provenance
    out = ROOT / "fixtures" / f"{name}.json"
    out.write_text(json.dumps(data, indent=1) + "\n")
    print(f"{name}: {grid.width}x{grid.height}, cost {result.cost:.6f}, path {len(result.path)}, expansions {len(result.expansion_order)}")


def main():
    fixture("open_room", Grid.from_strings(OPEN_ROOM), (1, 1), (8, 6))
    fixture("corridors", Grid.from_strings(CORRIDORS), (0, 0), (19, 14), connectivity=4, heuristic="manhattan")
    plan = ROOT / "data" / "mapa_robotica.bmp"
    fixture(
        "mapa_robotica",
        load_occupancy_grid(plan),
        (6, 6),
        (66, 50),
        provenance={
            "sourceImage": "data/mapa_robotica.bmp",
            "sourceSize": [450, 360],
            "erosionSize": 7,
            "resolution": 50,
            "cellsPerBlock": 8,
            "wallThreshold": 5,
        },
    )


if __name__ == "__main__":
    main()
