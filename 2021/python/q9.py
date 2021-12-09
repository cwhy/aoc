from collections import Counter

import numpy as np

with open('../input9.txt') as file:
    content = file.readlines()
matrix = np.array([list(int(i) for i in r.strip()) for r in content])

# matrix[:-1, :].shape
# np.full((1, 100), 10).shape
max_i, max_j = matrix.shape

# %%
low_pts = ((matrix < np.r_[np.full((1, max_j), 10), matrix[:-1, :]]) *
           (matrix < np.r_[matrix[1:, :], np.full((1, max_j), 10)]) *
           (matrix < np.c_[matrix[:, 1:], np.full((max_i, 1), 10)]) *
           (matrix < np.c_[np.full((max_i, 1), 10), matrix[:, :-1]]))

matrix[low_pts].sum() + low_pts.sum()

# %%

# get all the nonzero indexes for low_pts
indices = set((a, b) for a, b in np.argwhere(low_pts).tolist())

# get all the 9s for matrix
hills = set((a, b) for a, b in np.argwhere(matrix == 9).tolist())
boundaries = (set((-1, b) for b in range(max_j))
              | set((a, -1) for a in range(max_i))
              | set((a, max_j) for a in range(max_i))
              | set((max_i, b) for b in range(max_j)))
blocks = hills | boundaries
# %%

cat_dict = {}
pt_dict = {}
cat = 0
while len(indices) > 0:
    pt = next(iter(indices))
    indices.remove(pt)

    frontiers = [pt]
    cat_pts = {pt}
    while frontiers:
        pt = frontiers.pop()
        new_frontiers = [pt for pt in ((pt[0] + 1, pt[1]),
                                       (pt[0] - 1, pt[1]),
                                       (pt[0], pt[1] + 1),
                                       (pt[0], pt[1] - 1))
                         if pt not in blocks | cat_pts]
        frontiers += new_frontiers
        indices -= set(new_frontiers)
        cat_pts |= set(new_frontiers)

    cat_dict[cat] = len(cat_pts)
    pt_dict[cat] = pt
    cat += 1

# %%
counter = Counter(cat_dict)
print(counter)
print(np.prod([v for k, v in counter.most_common(3)]))
