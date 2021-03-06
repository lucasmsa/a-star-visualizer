import cv2
from utils.node import Node
import matplotlib.pyplot as plt
from scipy.spatial import distance
import matplotlib.animation as animation
import utils.set_start_and_end_points as ssp
from utils.image_manipulator import ImageManipulator


class A_Star:
    ADJACENT_SQUARES = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    def __init__(self, image_manipulator: ImageManipulator, output_cell_path: str, output_cell_with_initial_points: str, animation_output: str):
        self.fig, self.ax = plt.subplots()
        self.image_manipulator = image_manipulator
        self.output_cell_path = output_cell_path
        self.robot_map = self.image_manipulator.execute()
        self.animation_output = animation_output
        self.change_start_and_end_points_values()
        self.output_cell_with_initial_points = output_cell_with_initial_points
        self.animation_grid = cv2.imread(self.output_cell_with_initial_points)
        self.open_list = {
            f"{self.start_point}": Node(coordinates=self.start_point, 
                parent=None, 
                distance_from_start=0, 
                goal_distance=self.distance(self.start_point, self.end_point))
        }
        
        self.closed_list = {}
        self.path_to_goal = []

    def change_start_and_end_points_values(self):
        self.start_point, self.end_point, self.cell_image_path = self.image_manipulator.set_start_and_end_points(ssp)
        self.robot_map[self.start_point[1]][self.start_point[0]] = 0
        self.robot_map[self.end_point[1]][self.end_point[0]] = 1
  
    def distance(self, initial_points, end_points):
        return distance.euclidean(initial_points, end_points)
    
    def check_boundaries_and_obstacles(self, child_node_coordinates):
        x, y = child_node_coordinates
        if x >= len(self.robot_map[0]) \
            or y >= len(self.robot_map) \
                or self.robot_map[y][x] == -1:
            return True
        
        return False
        
    def fetch_smallest_total_distance(self):
        smallest = {
            "coordinates": (0, 0), 
            "node": Node(coordinates=(0, 0), parent=None)
        }
        smallest["node"].total_distance = float("inf")
        
        for coordinates, node in self.open_list.items():
            if node.total_distance < smallest["node"].total_distance:
                smallest["coordinates"] = coordinates
                smallest["node"] = node

        return smallest
            
    def execute(self):
        current_node = None
        frame = self.ax.imshow(self.animation_grid, animated=True)
        animation_frames = []
        while self.open_list:
            current = self.fetch_smallest_total_distance()
            
            del self.open_list[f"{current['coordinates']}"]
            self.closed_list[f"{current['coordinates']}"] = current["node"]
            
            current_node = current["node"]
            
            if current_node.coordinates == self.end_point:
                path_node = current_node
                
                while path_node is not None:
                    self.path_to_goal.append(path_node)
                    path_node = path_node.parent

                self.image_manipulator.paint_main_path(self.path_to_goal, self.animation_grid, self.ax, animation_frames)
                self.image_manipulator.save_animation(self.fig, animation, animation_frames, plt, self.animation_output)
                
                return self.path_to_goal
            
            offspring: list[Node] = []
            for adjacent_square in self.ADJACENT_SQUARES:
                child_node_coordinates = (current_node.x + adjacent_square[0], current_node.y + adjacent_square[1])
                
                if self.check_boundaries_and_obstacles(child_node_coordinates):
                    continue
                
                child_node = Node(coordinates=child_node_coordinates, parent=current_node)
                offspring.append(child_node)
            
            for child_node in offspring:                
                if f"{child_node.coordinates}" in self.closed_list: continue
                    
                child_node.goal_distance = self.distance(child_node_coordinates, self.end_point)
                child_node.distance_from_start = current_node.distance_from_start + 1
                child_node.total_distance = child_node.distance_from_start + child_node.goal_distance
                 
                if f"{child_node.coordinates}" in self.open_list:
                    open_list_node_total_distance = self.open_list[f"{child_node.coordinates}"].total_distance
                    if child_node.total_distance > open_list_node_total_distance:
                        continue   
                if child_node.coordinates != self.end_point:
                    self.image_manipulator.paint_search(self.animation_grid, child_node, self.ax, animation_frames,"SEARCH")
                    
                self.open_list[f"{child_node.coordinates}"] = child_node 
           

image_manipulator = ImageManipulator(image_path="./data/mapa_robotica.bmp",
                                     inflated_image_path="./data/mapa_inflado.bmp",
                                     output_image_path="./output/cell_image.png")

a_star = A_Star(image_manipulator, 
                output_cell_path="./output/cell_image_path.png", 
                output_cell_with_initial_points="./output/cell_image_with_initial_points.png",
                animation_output="./output/a_star_animation.gif")
a_star.execute()