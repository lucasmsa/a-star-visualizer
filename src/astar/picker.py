"""Interactive start and goal picking on the occupancy grid image (needs an OpenCV GUI build)."""
from __future__ import annotations

from pathlib import Path

WINDOW = "Occupancy Grid"


def pick_start_and_goal(grid_png: str | Path) -> tuple[tuple[int, int], tuple[int, int]]:
    import cv2

    image = cv2.imread(str(grid_png))
    picked: list[tuple[int, int]] = []

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and image[y][x].any() and len(picked) < 2:
            picked.append((x, y))

    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW, 1280, 1000)
    cv2.setMouseCallback(WINDOW, on_mouse)
    while len(picked) < 2:
        cv2.imshow(WINDOW, image)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    if len(picked) < 2:
        raise SystemExit("start and goal were not both picked")
    return picked[0], picked[1]
