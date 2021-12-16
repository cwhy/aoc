import heapq
from functools import lru_cache

import matplotlib.pyplot as plt
import numpy as np

content = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

with open('2021/input15.txt') as file:
    content = file.read()
matrix = np.array([list(int(i) for i in r.strip()) for r in content.strip().split()])


# %%

def roll_out(mat):
    mats = [mat]
    new_matrix = mat.copy()
    for i in range(4):
        new_matrix += 1
        new_matrix[new_matrix == 10] = 1
        mats.append(new_matrix)
        new_matrix = new_matrix.copy()
    return mats


row = np.concatenate(roll_out(matrix), axis=1)
big_mat = np.concatenate(roll_out(row), axis=0)


# %%

@lru_cache
def graph(i, j, h, w):
    dots = {(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)}
    if i == 0:
        dots.remove((i - 1, j))
    if j == 0:
        dots.remove((i, j - 1))
    if i == h - 1:
        dots.remove((i + 1, j))
    if j == w - 1:
        dots.remove((i, j + 1))
    return tuple(dots)


def dijkstra_diag(mat):
    priority_queue = [(0, 0, 0)]
    visited = set()
    H, W = mat.shape
    while priority_queue:
        dist, i, j = heapq.heappop(priority_queue)
        if (i, j) == (H - 1, W - 1):
            return dist
        if (i, j) in visited:
            continue
        visited.add((i, j))
        for ni, nj in graph(i, j, H, W):
            if (ni, nj) in visited:
                continue
            heapq.heappush(priority_queue, (dist + big_mat[ni, nj], ni, nj))


print(dijkstra_diag(big_mat))
