import re
from typing import Sized
import cv2
import numpy as np
import math
from PIL import Image
from math import sqrt
from math import floor
from scipy.spatial import distance
from utils.image_manipulator import ImageManipulator
from utils.node import Node


class A_Star:
    def __init__(self, image_manipulator: ImageManipulator):
        self.image_manipulator = image_manipulator
        self.robot_map = self.image_manipulator.execute()
        self.open_list = self.fetch_spaces(space_number=2)
        self.closed_list = self.fetch_spaces(space_number=-1)
        self.closed_count = 0
        self.start_node = 0
        self.goal_node = 0

    def fetch_spaces(self, space_number):
        spaces = set()
        for x in range(len(self.robot_map)):
            for y in range(len(self.robot_map[0])):
                if self.robot_map[x][y] == space_number:
                    coordinates = (x, y)
                    spaces.add(coordinates)

        return spaces

    def get_input(self):
        self.starting_point = (0, 0)
        self.arrival_point = (0, 0)

        print("Por favor digite o ponto de partida do roboto:")
        points = re.findall(r'[0-9]+', input())
        try:
            x, y = points[0], points[1]
            self.starting_point = (x, y)
            self.robot_map[self.starting_point[0]
                           ][self.starting_point[1]] = 1
        except:
            print("\nDigite dois valores para a posição")

        while(self.robot_map[int(self.starting_point[0])][int(self.starting_point[1])] != 2):
            print(
                f"Valores inválidos, tente outro, algunas exemplos são: {list(self.open_list)[0:4]}")
            points = re.findall(r'[0-9]+', input())
            try:
                x, y = points[0], points[1]
                self.starting_point = (x, y)
                self.robot_map[self.arrival_point[0]
                               ][self.arrival_point[1]] = 1
                self.start_node = Node(points[0], points[1], 0.0, -1)
            except:
                print("\nDigite dois valores para a posição")

        print("_"*20)

        print("Por favor digite o ponto de chegada do robotík:")
        points = re.findall(r'[0-9]+', input())
        try:
            x, y = points[0], points[1]
            self.arrival_point = (x, y)
            self.robot_map[self.arrival_point[0]
                           ][self.arrival_point[1]] = 0
        except:
            print("\nDigite dois valores para a posição")

        while(self.robot_map[int(self.arrival_point[0])][int(self.arrival_point[1])] != 2):
            print(
                f"Valores inválidos, tente outro, algunas exemplos são: {self.list(open_list)[0:3]}")
            points = re.findall(r'[0-9]+', input())
            try:
                x, y = points[0], points[1]
                self.arrival_point = (x, y)
                self.robot_map[self.arrival_point[0]
                               ][self.arrival_point[1]] = 0

            except:
                print("\nDigite dois valores para a posição")

    # joga duro!!!
    def distance(x1, y1, x2, y2):
        return distance.euclidian((x1, y1), (x2, y2))

    def Algorithm():
        self.closed_count = size(self.closed_list, 1)
        open_count = 0


image_manipulator = ImageManipulator(image_path="../data/mapa_robotica.bmp",
                                     inflated_image_path="../data/mapa_inflado.bmp",
                                     output_image_path="../output/cell_image.png")
image_manipulator.execute()
a_star = A_Star(image_manipulator)
a_star.get_input()
