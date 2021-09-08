import cv2
import time

def mouse_click(event, x, y, flags, param):
    is_black_space = grid[y][x].any() == 0
    if event == cv2.EVENT_LBUTTONDOWN and not is_black_space:
        if globals()["start_point"] is None:
            cv2.circle(grid, (x, y), 1, (42, 25, 84), -1)
            globals()["start_point"] = (x, y)
            
        elif globals()["end_point"] is None:
            cv2.circle(grid, (x, y), 1, (69, 23, 81), -1)
            globals()["end_point"] = (x, y)
            
        refresh_image()
        
def refresh_image():
    cv2.resize(grid, (1280, 1080)) 
    cv2.imshow('Occupancy Grid', grid)  
        
def handle_mouse_events(output_image_path: str):
    global grid, start_point, end_point
    start_point, end_point = None, None
    cv2.namedWindow('Occupancy Grid', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Occupancy Grid', mouse_click)
    grid = cv2.imread(output_image_path) 

    while True:
        cv2.imshow('Occupancy Grid', grid)
        k = cv2.waitKey(20) & 0xFF
        if k == 27 or start_point and end_point:
            refresh_image()
            cv2.imwrite(f"{output_image_path[:-4]}_with_initial_points.png", grid)
            time.sleep(1.5)
            cv2.destroyAllWindows()
            return start_point, end_point