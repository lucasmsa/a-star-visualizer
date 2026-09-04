"""A* on a floor plan.

Headless:    python src/a_star.py --start 6 6 --goal 66 50
Interactive: python src/a_star.py            (click start, then goal)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from astar.grid import load_occupancy_grid  # noqa: E402
from astar.render import save_animation, save_grid_png  # noqa: E402
from astar.search import a_star  # noqa: E402


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--map", default="data/mapa_robotica.bmp", help="floor plan image, dark pixels are walls")
    parser.add_argument("--start", nargs=2, type=int, metavar=("X", "Y"), help="start cell; omit to click it")
    parser.add_argument("--goal", nargs=2, type=int, metavar=("X", "Y"), help="goal cell; omit to click it")
    parser.add_argument("--robot-radius", type=int, default=7, help="wall inflation in source pixels (default 7)")
    parser.add_argument("--connectivity", type=int, choices=[4, 8], default=8)
    parser.add_argument("--heuristic", choices=["manhattan", "euclidean", "chebyshev", "octile"], default="octile")
    parser.add_argument("--out", default="output", help="output folder")
    parser.add_argument("--show", action="store_true", help="also open the animation in a window")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    grid = load_occupancy_grid(args.map, erosion_size=args.robot_radius)
    grid_png = out / "cell_image.png"
    save_grid_png(grid, grid_png)

    if args.start and args.goal:
        start, goal = tuple(args.start), tuple(args.goal)
    else:
        from astar.picker import pick_start_and_goal

        start, goal = pick_start_and_goal(grid_png)
    for name, (x, y) in (("start", start), ("goal", goal)):
        if not grid.in_bounds(x, y) or grid.is_wall(x, y):
            print(f"{name} {x},{y} is outside the grid or inside a wall", file=sys.stderr)
            return 2
    save_grid_png(grid, out / "cell_image_with_initial_points.png", start, goal)

    result = a_star(grid, start, goal, connectivity=args.connectivity, heuristic=args.heuristic)
    print(f"grid {grid.width}x{grid.height}, {grid.wall_count()} wall cells")
    print(f"start {start} goal {goal} connectivity {args.connectivity} heuristic {args.heuristic}")
    if not result.found:
        print(f"no path, {len(result.expansion_order)} cells expanded")
        return 1
    frames = save_animation(grid, result, start, goal, out / "a_star_animation.gif", show=args.show)
    print(f"path {len(result.path)} cells, cost {result.cost:.4f}, {len(result.expansion_order)} expanded, {frames} frames -> {out / 'a_star_animation.gif'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
