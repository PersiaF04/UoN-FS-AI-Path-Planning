import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

def create_delaunay_triangulation(cone_positions, n):
    """
    Creates Delaunay triangulation for every nth cone position.

    :param cone_positions: List of (x, y) coordinates of the cones.
    :param n: Interval for selecting cones.
    :return: List of triangulations.
    """
    triangulations = []
    
    # Process every nth cone
    for i in range(0, len(cone_positions), n):
        if i <= len(cone_positions):
            points_subset = cone_positions[i:i + n]
            tri = Delaunay(points_subset)
            triangulations.append((points_subset, tri))
    print(tri.points)
    return triangulations

def plot_triangulation(cone_positions, triangulations):
    """
    Plots the Delaunay triangulations.

    :param cone_positions: List of (x, y) coordinates of the cones.
    :param triangulations: List of triangulations.
    """
    plt.figure(figsize=(10, 10))
    plt.plot(cone_positions[:, 0], cone_positions[:, 1], 'o', color='red', label='Cones')

    for points_subset, tri in triangulations:
        plt.triplot(points_subset[:, 0], points_subset[:, 1], tri.simplices.copy(), color='blue')

    plt.title("Delaunay Triangulation of Cone Positions")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.show()

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

# Example cone positions (x, y coordinates)
cone_positions = np.array([
    [0, 0], [1, 2], [2, 1], [3, 3],
    [4, 1], [5, 2], [6, 0], [7, 2],
    [8, 3], [9, 1], [10, 2], [11, 3]
])

n = 4  # Interval for cone selection
triangulations = create_delaunay_triangulation(cone_positions, n)
plot_triangulation(cone_positions, triangulations)

# Check Delaunay property
valid_delaunay = check_delaunay_property(triangulations)
print(f"Delaunay property satisfied: {valid_delaunay}")
