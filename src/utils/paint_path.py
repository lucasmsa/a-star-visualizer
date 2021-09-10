import cv2

def paint_path(path_to_goal: "list[(int, int)]", path: str, output_path: str):
    grid = cv2.imread(path)
    path_to_goal = path_to_goal[1:-1]
    for node in path_to_goal:
        cv2.circle(grid, (node[0], node[1]), 1, (30, 0, 200), -2)
    cv2.imshow("Path painted 🎨", grid)
    cv2.imwrite(output_path, grid)