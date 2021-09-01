import cv2
import numpy as np
from PIL import Image
from math import floor

RESOLUTION = 50
A_STAR_RESOLUTION = 4 

class ImageManipulator:  
    def __init__(self, image_path: str):
        self.image = (cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY) < 5).astype(int)
        self.height, self.width = self.image.shape[0], \
                                    self.image.shape[1]
        self.max_x = floor(self.width/RESOLUTION) * A_STAR_RESOLUTION
        self.max_y = floor(self.height/RESOLUTION) * A_STAR_RESOLUTION
        
        self.ROBOT_MAPS = {
            "initial_map": (np.ones(shape=(self.max_x, self.max_y)) * 2).astype(int).tolist(),
            "rgb": np.ones(shape=(self.max_x, self.max_y)).astype(int).tolist(),
            "flipped": np.ones(shape=(self.max_y, self.max_x)).astype(int).tolist()
        } 
        
    def create_robot_map(self):
        robot_map = self.ROBOT_MAPS["initial_map"]
        
        for x in range(self.width):
            for y in range(self.height):
                if self.check_wall(x, y):
                    x_value = floor(((x * (self.max_x))/self.width))
                    y_value = floor(((y * (self.max_y))/self.height))
                    robot_map[x_value][y_value] = -1
                
        return robot_map
    
    def array_to_RGB(self, robot_map: list):
        robot_map_rgb = self.ROBOT_MAPS["rgb"]
        
        for x in range(self.max_x):
            for y in range(self.max_y):
                if robot_map[x][y] == -1:
                    robot_map_rgb[x][y] = (0, 0, 0)
                elif robot_map[x][y] == 2:
                    robot_map_rgb[x][y] = (255, 255 ,255)
                    
        return robot_map_rgb
    
    def array_to_binary(self, robot_map: np.array):
        robot_map_flipped = self.ROBOT_MAPS["flipped"]
        
        for x in range(self.max_y):
            for y in range(self.max_x):
                if robot_map[x][y].any() == 0:
                    robot_map_flipped[x][y] = -1
                elif robot_map[x][y].any() == 255:
                    robot_map_flipped[x][y] = 2
                    
        return robot_map_flipped
    
    def plot_robot_map(self, robot_map: list):
        robot_map_image = self.array_to_RGB(robot_map)

        robot_map_matrix = np.uint8(robot_map_image)
        image_plot = Image.fromarray(robot_map_matrix, 'RGB')\
                        .transpose(Image.ROTATE_90)\
                        .transpose(Image.FLIP_TOP_BOTTOM)
        
        image_plot.save("output/cell_image.png")
        print(np.array(image_plot))
        robot_map_flipped = self.array_to_binary(np.array(image_plot))

        return robot_map_flipped

    def check_wall(self, x: int, y: int):
        return True if self.image[y, x] == 1 else False

image_manipulator = ImageManipulator('./data/mapa_robotica_inflado.bmp')

robot_map = image_manipulator.create_robot_map()
image_manipulator.plot_robot_map(robot_map)