from __future__ import annotations

from pathlib import Path

import numpy as np

from astar.grid import Grid
from astar.search import SearchResult

# RGB values kept from the 2021 animation.
SEARCH_COLOR = (230, 0, 126)
PATH_COLOR = (80, 200, 120)
START_COLOR = (42, 25, 84)
GOAL_COLOR = (69, 23, 81)
WALL_COLOR = (0, 0, 0)
FREE_COLOR = (255, 255, 255)


def grid_to_rgb(grid: Grid) -> np.ndarray:
    image = np.full((grid.height, grid.width, 3), FREE_COLOR, dtype=np.uint8)
    for y, row in enumerate(grid.cells):
        for x, wall in enumerate(row):
            if wall:
                image[y, x] = WALL_COLOR
    return image


def save_grid_png(grid: Grid, path: str | Path, start=None, goal=None) -> None:
    from PIL import Image

    image = grid_to_rgb(grid)
    if start:
        image[start[1], start[0]] = START_COLOR
    if goal:
        image[goal[1], goal[0]] = GOAL_COLOR
    Image.fromarray(image, "RGB").save(path)


def save_animation(grid: Grid, result: SearchResult, start, goal, path: str | Path, interval_ms: int = 25, show: bool = False) -> int:
    """Write a GIF: one frame per expanded cell, then one per path cell. Returns the frame count."""
    import matplotlib

    if not show:
        matplotlib.use("Agg")
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt

    canvas = grid_to_rgb(grid)
    canvas[start[1], start[0]] = START_COLOR
    canvas[goal[1], goal[0]] = GOAL_COLOR

    fig, ax = plt.subplots()
    ax.set_axis_off()
    frames = [[ax.imshow(canvas.copy(), animated=True)]]
    for x, y in result.expansion_order:
        if (x, y) in (start, goal):
            continue
        canvas[y, x] = SEARCH_COLOR
        frames.append([ax.imshow(canvas.copy(), animated=True)])
    for x, y in result.path[1:-1]:
        canvas[y, x] = PATH_COLOR
        frames.append([ax.imshow(canvas.copy(), animated=True)])

    ani = animation.ArtistAnimation(fig, artists=frames, interval=interval_ms, blit=True, repeat=False)
    if show:
        plt.show()
    ani.save(str(path), writer="pillow")
    plt.close(fig)
    return len(frames)
