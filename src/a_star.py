import re
import cv2
import math
import numpy as np
from PIL import Image
from math import sqrt
from math import floor
from typing import Sized
from utils.node import Node
from scipy.spatial import distance
from utils.insert_open import insert_open
import utils.set_start_and_end_points as ssp
from utils.image_manipulator import ImageManipulator


class A_Star:
    def __init__(self, image_manipulator: ImageManipulator):
        self.image_manipulator = image_manipulator
        self.robot_map = self.image_manipulator.execute()
        self.change_start_and_end_points_values()
        self.open_list: list[Node] = [
            Node(self.current_point, 
                self.current_point, 
                0, 
                self.distance(self.current_point, self.end_point))]
        self.closed_list: list[Node] = [] 
        self.closed_count = len(self.closed_list)
        self.start_node = 0
        self.goal_node = 0

    def change_start_and_end_points_values(self):
        self.start_point, self.end_point = self.image_manipulator.set_start_and_end_points(ssp)
        self.robot_map[self.start_point[1]][self.start_point[0]] = 0
        self.robot_map[self.end_point[1]][self.end_point[0]] = 1
        
    def fetch_spaces(self, space_number):
        spaces = set()
        for x in range(len(self.robot_map)):
            for y in range(len(self.robot_map[0])):
                if self.robot_map[x][y] == space_number:
                    coordinates = (x, y)
                    spaces.add(coordinates)
        
        return spaces

    def distance(self, initial_points, end_points):
        return distance.euclidean(initial_points, end_points)
    
    def fetch_smallest_total_distance(self):
        smallest_total_distance = {
            "index": 0,
            "value": float("inf")
        }
        
        for index, node in enumerate(self.open_list):
            if node.total_distance < smallest_total_distance["value"]:
                smallest_total_distance["index"] = index
                smallest_total_distance["value"] = node.total_distance
                
        return smallest_total_distance["index"]
            
    def algorithm(self):
        no_path_found = False
        current_node = None
        
        while self.open_list:
            smallest_distance_index = self.fetch_smallest_total_distance()
            current_node = self.open_list[smallest_distance_index]
            self.open_list.pop(smallest_distance_index)
            self.closed_list.append(current_node)
            
            if current_node.x == self.end_point[0] and current_node.y == self.end_point[1]:
                print("Congrats my friend you found the path")
                break
            
            # TODO: Generate children (adjacent nodes)
            
        print(self.current_point, self.end_point)

image_manipulator = ImageManipulator(image_path="./data/mapa_robotica.bmp",
                                     inflated_image_path="./data/mapa_inflado.bmp",
                                     output_image_path="./output/cell_image.png")
a_star = A_Star(image_manipulator)
a_star.algorithm()