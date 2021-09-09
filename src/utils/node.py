class Node:
    def __init__(self, coordinates, parent, distance_from_start, goal_distance):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.parent_x = parent[0]
        self.parent_y = parent[1]
        self.distance_from_start = distance_from_start
        self.goal_distance = goal_distance
        self.total_distance = self.distance_from_start + self.goal_distance