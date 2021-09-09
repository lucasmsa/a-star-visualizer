from scipy.spatial import distance


def insert_open(node_coordinates, parent_node_coordinates, distance_from_start, goal_distance, total_distance):
    new_row = {
        "robot": 1,
        "x": node_coordinates[0],
        "y": node_coordinates[1],
        "parent_x": parent_node_coordinates[0],
        "parent_y": parent_node_coordinates[1],
        "distance_from_start": distance_from_start,
        "goal_distance": goal_distance,
        "total_distance": total_distance
    }
    
    return new_row