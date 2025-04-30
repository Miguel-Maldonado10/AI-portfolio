import math
import matplotlib.pyplot as plt



def distance(v1, v2):
    """Calculates the Euclidean distance between two vertices."""
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)

def line_intersects_polygon(v1, v2, polygon):
    """Checks if the line segment (v1, v2) intersects any edge of the polygon,
       excluding the edge that connects v1 and v2 if they are adjacent."""
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        # Skip the edge that connects v1 and v2 if they are adjacent
        if v1 in polygon and v2 in polygon:
            v1_index = polygon.index(v1)
            v2_index = polygon.index(v2)
            if (v1_index + 1) % len(polygon) == v2_index or (v2_index + 1) % len(polygon) == v1_index:
                if (p1, p2) == (v1, v2) or (p1, p2) == (v2, v1):
                    continue
        #print(f"Checking line ({v1}, {v2}) against edge ({p1}, {p2})")
        if line_segments_intersect(v1, v2, p1, p2):
            #check to see if the intersection is just a vertex touching.
            if v1 == p1 or v1 == p2 or v2 == p1 or v2 == p2:
                continue
            #print(f"Intersection found: ({v1}, {v2}) and ({p1}, {p2})")
            return True
    return False

def line_segments_intersect(v1, v2, p1, p2):
    """Checks if line segments (v1, v2) and (p1, p2) intersect."""
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = p1
    x4, y4 = p2

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return False  # Lines are parallel

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return True  # Intersection found

    return False

def on_segment(p, q, r):
    """Checks if point q lies on line segment pr."""
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    return False

def is_visible(v1, v2, polygons):
    """Checks if v2 is visible from v1 without intersecting any polygons."""
    #print(f"Checking visibility between {v1} and {v2}")
    for polygon in polygons:
        if line_intersects_polygon(v1, v2, polygon):
            #print(f"Not visible due to intersection with: {polygon}")
            return False
    return True

def ACTIONS(vertex, vertices, polygons):
    """Returns a list of actions (vertices) from the given vertex."""
    actions = []
    for other_vertex in vertices:
        #print(f"Checking other_vertex: {other_vertex}")
        if vertex == other_vertex:
            continue
        if is_visible(vertex, other_vertex, polygons):
            #print(f"Checking visibility from {vertex} to {other_vertex}")
            actions.append(other_vertex)
            print(actions)
    # Add neighbors on the same polygon:
    for polygon in polygons:
        if vertex in polygon:
            index = polygon.index(vertex)
            actions.append(polygon[(index - 1) % len(polygon)])  # Previous vertex
            actions.append(polygon[(index + 1) % len(polygon)])  # Next vertex
    return actions

def heuristic(vertex, goal):
    """Calculates the straight-line distance heuristic."""
    return distance(vertex, goal)

def test_functions():
    """Tests the functions with sample data."""

    # Sample polygon data (replace with actual data from your image)
    polygons = [
        [(1, 1), (3, 1), (3, 3), (1, 3)],  # Example square
        [(5, 5), (7, 5), (6, 7)],  # Example triangle
    ]
 
    # Sample vertices
    vertices = [(1, 1), (3, 1), (3, 3), (1, 3), (5, 5), (7, 5), (6, 7), (0, 0), (8, 8)]

    # Sample start and goal
    start = (0, 0)
    goal = (8, 8)

    # Test line_intersects_polygon
    print("Testing line_intersects_polygon:")
    print(line_intersects_polygon((0, 0), (0, 4), polygons[0]))  # Should be False
    print(line_intersects_polygon((2, 2), (4, 4), polygons[0])) # Should be True
    print()

    # Test is_visible
    print("Testing is_visible:")
    print(is_visible((0, 0), (1, 1), polygons))  # Should be True
    print(is_visible((2, 2), (6, 6), polygons)) # Should be False
    print()

    # Test ACTIONS
    print("Testing ACTIONS:")
    print(ACTIONS((3, 3), vertices, polygons))
    print()

    # Test heuristic
    print("Testing heuristic:")
    print(heuristic((0, 0), (8, 8)))
    print()

    # Test DFS
    print("Testing DFS")
    print(depth_first_search_with_distance(start,goal,vertices,polygons))
    # Test BFS
    print("Testing BFS")
    print(breadth_first_search_with_distance(start,goal,vertices,polygons))
    # Test A*
    print("Tesing A* Search")
    print(a_star_search_with_distance(start,goal,vertices,polygons))

def depth_first_search_with_distance(start, goal, vertices, polygons):
    """Implements Depth-First Search and returns path and distance."""
    stack = [(start, [start], 0)]  # (current_vertex, path_so_far, distance_so_far)
    visited = set()

    while stack:
        current_vertex, path, distance = stack.pop()

        if current_vertex == goal:
            return path, distance  # Goal found, return path and distance

        if current_vertex not in visited:
            visited.add(current_vertex)
            neighbors = ACTIONS(current_vertex, vertices, polygons)
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_distance = distance + distance_between_points(current_vertex, neighbor)
                    stack.append((neighbor, path + [neighbor], new_distance))

    return None, None  # Goal not found

def distance_between_points(p1, p2):
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

from collections import deque

def breadth_first_search_with_distance(start, goal, vertices, polygons):
    """Implements Breadth-First Search and returns path and distance."""
    queue = deque([(start, [start], 0)])  # (current_vertex, path_so_far, distance_so_far)
    visited = set()

    while queue:
        current_vertex, path, distance = queue.popleft()

        if current_vertex == goal:
            return path, distance

        if current_vertex not in visited:
            visited.add(current_vertex)
            neighbors = ACTIONS(current_vertex, vertices, polygons)
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_distance = distance + distance_between_points(current_vertex, neighbor)
                    queue.append((neighbor, path + [neighbor], new_distance))

    return None, None

import heapq

def a_star_search_with_distance(start, goal, vertices, polygons):
    """Implements A* Search and returns path and distance."""
    open_list = [(heuristic(start, goal), 0, start, [start], 0)]  # (f_score, g_score, current_vertex, path, distance)
    closed_set = set()

    while open_list:
        f_score, g_score, current_vertex, path, distance = heapq.heappop(open_list)

        if current_vertex == goal:
            return path, distance

        if current_vertex in closed_set:
            continue

        closed_set.add(current_vertex)
        neighbors = ACTIONS(current_vertex, vertices, polygons)
        for neighbor in neighbors:
            new_g_score = g_score + distance_between_points(current_vertex, neighbor)
            new_distance = distance + distance_between_points(current_vertex, neighbor)
            new_f_score = new_g_score + heuristic(neighbor, goal)
            heapq.heappush(open_list, (new_f_score, new_g_score, neighbor, path + [neighbor], new_distance))

    return None, None

# Run the tests
test_functions()