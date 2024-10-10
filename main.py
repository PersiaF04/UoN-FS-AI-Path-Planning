import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

def create_overlapping_delaunay_triangulation(cone_positions, n):
    """
    Creates Delaunay triangulation with overlapping sets of points.

    :param cone_positions: List of (x, y) coordinates of the cones.
    :param n: Number of points to use in each set, with overlap.
    :return: List of triangulations.
    """
    triangulations = []
    
    # Process overlapping sets of n points, with 2-point overlap
    for i in range(0, len(cone_positions) - 2, n - 2):
        points_subset = cone_positions[i:i + n]
        if len(points_subset) >= 3:  # Need at least 3 points to form a triangle
            tri = Delaunay(points_subset)
            triangulations.append((points_subset, tri))
    
    return triangulations

def calculate_triangle_centroids(triangulations):
    """
    Calculates the centroids of each triangle in the triangulation.

    :param triangulations: List of triangulations.
    :return: List of centroids of triangles.
    """
    centroids = []
    for points_subset, tri in triangulations:
        for simplex in tri.simplices:
            triangle = points_subset[simplex]
            centroid = np.mean(triangle, axis=0)  # Calculate the centroid of the triangle
            centroids.append(centroid)
    return np.array(centroids)

def plot_triangulation_and_path(cone_positions, triangulations, path_centroids):
    """
    Plots the Delaunay triangulations and the calculated path.

    :param cone_positions: List of (x, y) coordinates of the cones.
    :param triangulations: List of triangulations.
    :param path_centroids: List of path centroids to be plotted as the path.
    """
    plt.figure(figsize=(10, 10))
    plt.plot(cone_positions[:, 0], cone_positions[:, 1], 'o', color='red', label='Cones')

    # Plot each triangulation
    for points_subset, tri in triangulations:
        plt.triplot(points_subset[:, 0], points_subset[:, 1], tri.simplices.copy(), color='blue')

    # Plot the path as a line connecting the centroids
    plt.plot(path_centroids[:, 0], path_centroids[:, 1], '-o', color='green', label='Path Centroids')

    plt.title("Delaunay Triangulation and Path of Centroids")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.show()

# Example cone positions (x, y coordinates)
cone_positions = np.array([
    [0, 0], [1, 2], [2, 1], [3, 3],
    [4, 1], [5, 2], [6, 0], [7, 2],
    [8, 3], [9, 1], [10, 2]
])

n = 4  # Number of points in each overlapping set
triangulations = create_overlapping_delaunay_triangulation(cone_positions, n)
path_centroids = calculate_triangle_centroids(triangulations)
plot_triangulation_and_path(cone_positions, triangulations, path_centroids)

# Check Delaunay property (optional step to validate triangulation)
def is_point_in_circumcircle(triangle, point):
    """Check if a point is inside the circumcircle of a triangle."""
    ax, ay = triangle[0]
    bx, by = triangle[1]
    cx, cy = triangle[2]
    
    # Calculate the circumcircle center and radius
    A = np.array([[ax - point[0], ay - point[1]], 
                   [bx - point[0], by - point[1]], 
                   [cx - point[0], cy - point[1]]])
    
    # Calculate the determinant to determine if point is inside circumcircle
    det = np.linalg.det(A)
    return det < 0  # If the determinant is negative, the point is inside the circumcircle

def check_delaunay_property(triangulations):
    """Check if all triangles in the triangulation satisfy the Delaunay property."""
    for points_subset, tri in triangulations:
        for simplex in tri.simplices:
            triangle = points_subset[simplex]
            for point in points_subset:
                if point not in triangle and is_point_in_circumcircle(triangle, point):
                    return False
    return True

valid_delaunay = check_delaunay_property(triangulations)
print(f"Delaunay property satisfied: {valid_delaunay}")
