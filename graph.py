from collections import deque
import math


class Node:
    def __init__(self, id_, name_):
        self.id = id_
        self.name = name_
        self.neighbors = []

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"Node({self.id}, {self.name})"

    def __repr__(self):
        return f"Node({self.id}, {self.name})"


def bfs(u, get_neighbors, f, max_depth=math.inf):
    depth = 0
    queue = deque()
    visited = set()
    queue.append(u)
    queue.append(None)

    while (len(queue) > 0 and depth < max_depth):
        x = queue.popleft()
        if x is None:
            depth += 1
            queue.append(None)
            continue
        visited.add(x)
        for v in get_neighbors(x):
            if v not in visited and v not in queue:
                queue.append(v)
        f(x)

    return visited


def dfs(u, get_neighbors, max_depth=math.inf, f=lambda *args: None):
    if max_depth is None:
        max_depth = math.inf
    visited = set()
    visited.add(u)
    f(None, u)
    u.neighbors = dfs_traverse(u, get_neighbors, visited, max_depth, f)
    return u


def dfs_traverse(u, get_neighbors, visited, depth, f):
    neighbors = []

    if (depth > 0):
        for v in get_neighbors(u):
            if v not in visited:
                visited.add(v)
                f(u, v)
                neighbors.append(v)
                v.neighbors = dfs_traverse(v, get_neighbors, visited,
                                           depth - 1, f)

    return neighbors
