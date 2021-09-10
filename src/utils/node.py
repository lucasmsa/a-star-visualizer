class Node:
    def __init__(self, coordinates, parent, distance_from_start=0, goal_distance=0):
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.parent = parent
        self.distance_from_start = distance_from_start
        self.goal_distance = goal_distance
        self.total_distance = self.distance_from_start + self.goal_distance