import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

def create_delaunay_triangulation(cone_positions, n):
    triangulations = []
    
    for i in range(0, len(cone_positions) - 2, n - 2):
        points_subset = cone_positions[i:i + n]
        if len(points_subset) >= 3:
            tri = Delaunay(points_subset)
            triangulations.append((points_subset, tri))
    
    return triangulations

def find_edges(triangulations, cone_positions):
    """
    Finds all edges across all triangulations and adds first/last edges.
    
    :param triangulations: List of triangulations.
    :param cone_positions: Complete list of cone positions.
    :return: Dictionary of edges and their occurrence count, and edge points.
    """
    edge_count = {}
    edge_points = {}
    
    # Add first and last edges
    first_edge = tuple(sorted([tuple(cone_positions[0]), tuple(cone_positions[1])]))
    last_edge = tuple(sorted([tuple(cone_positions[-2]), tuple(cone_positions[-1])]))
    
    edge_count[first_edge] = 1
    edge_count[last_edge] = 1
    edge_points[first_edge] = (cone_positions[0], cone_positions[1])
    edge_points[last_edge] = (cone_positions[-2], cone_positions[-1])
    
    for points_subset, tri in triangulations:
        for simplex in tri.simplices:
            for i in range(3):
                p1_idx, p2_idx = simplex[i], simplex[(i+1)%3]
                p1, p2 = points_subset[p1_idx], points_subset[p2_idx]
                
                edge_key = tuple(sorted([tuple(p1), tuple(p2)]))
                
                edge_count[edge_key] = edge_count.get(edge_key, 0) + 1
                edge_points[edge_key] = (p1, p2)
    
    return edge_count, edge_points

def find_path_edges(triangulations, cone_positions):
    """
    Finds all edges for the path, including first and last edges.

    :param triangulations: List of triangulations.
    :param cone_positions: Complete list of cone positions.
    :return: List of edge midpoints in order.
    """
    edge_count, edge_points = find_edges(triangulations, cone_positions)
    
    # Get all midpoints, including first and last edges
    midpoints = []
    for edge_key, count in edge_count.items():
        if count > 1 or edge_key == tuple(sorted([tuple(cone_positions[0]), tuple(cone_positions[1])])) or \
            edge_key == tuple(sorted([tuple(cone_positions[-2]), tuple(cone_positions[-1])])):
            p1, p2 = edge_points[edge_key]
            midpoint = (p1 + p2) / 2
            midpoints.append(midpoint)
    
    # Sort midpoints roughly from left to right
    midpoints.sort(key=lambda x: x[0])
    
    return np.array(midpoints)

def interpolate_path(midpoints, num_points=10):
    if len(midpoints) < 2:
        return np.array([])
    
    path = []
    for i in range(len(midpoints) - 1):
        start = midpoints[i]
        end = midpoints[i + 1]
        
        for t in np.linspace(0, 1, num_points):
            point = start + t * (end - start)
            path.append(point)
    
    return np.array(path)

def plot_triangulation_and_path(cone_positions, triangulations, midpoints, path):
    plt.figure(figsize=(10, 10))
    
    # Plot triangulations
    for points_subset, tri in triangulations:
        plt.triplot(points_subset[:, 0], points_subset[:, 1], tri.simplices.copy(), color='blue')
    
    # Plot cones
    plt.plot(cone_positions[:, 0], cone_positions[:, 1], 'o', color='red', label='Cones')

    # Plot midpoints
    if len(midpoints) > 0:
        plt.plot(midpoints[:, 0], midpoints[:, 1], 'o', color='green', label='Edge Midpoints')

    # Plot interpolated path
    if len(path) > 0:
        plt.plot(path[:, 0], path[:, 1], '-', color='orange', label='Interpolated Path')

    plt.title("Delaunay Triangulation with Edge Midpoints and Interpolated Path")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.show()

# Example usage
cone_positions = np.array([
    [0, 0], [1, 2], [2, 1], [3, 3],
    [4, 1], [5, 2], [6, 0], [7, 2],
    [9, 1], [8, 3], [10, 2], [11, 3]
])

n = 4  # Number of points in each overlapping set
triangulations = create_delaunay_triangulation(cone_positions, n)
midpoints = find_path_edges(triangulations, cone_positions)
interpolated_path = interpolate_path(midpoints)
plot_triangulation_and_path(cone_positions, triangulations, midpoints, interpolated_path)