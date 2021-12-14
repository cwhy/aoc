import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

content = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

with open('2021/input13.txt') as file:
    content = file.read()

head, tail = content.strip().split("\n\n")
dots = [tuple(map(int, line.split(","))) for line in head.split("\n")]
folds = [tuple(line.strip().split(" ")[-1].split("=")) for line in tail.split("\n")]
folds = [(0 if ax == 'x' else 1, int(val)) for ax, val in folds]

dots_arr = np.array(dots)
ax_max = np.amax(dots_arr, axis=0)
ax_min = np.amin(dots_arr, axis=0)
assert ax_min.tolist() == [0, 0]
arr = np.zeros((ax_max[0] + 1, ax_max[1] + 1))
for dot in dots:
    arr[dot] = 1

folds


# %%

def process_fold(_arr, fold) -> npt.NDArray:
    axis, val = fold
    slice_all = slice(None)
    slice_rest = slice(val + 1, None)
    slice_head = slice(None, val)
    slice_rest_r = slice(-(ax_max[axis] - val), None, None)
    if axis == 0:
        head = (slice_head, slice_all)
        rest = (slice_rest, slice_all)
        rest_r = (slice_rest_r, slice_all)
    else:
        head = (slice_all, slice_head)
        rest = (slice_all, slice_rest)
        rest_r = (slice_all, slice_rest_r)

    if ax_max[axis] - val >= val - 1:
        new_arr = np.flip(_arr[rest], axis)
        new_arr[head] += _arr[head]
    else:
        assert ax_max[axis] - val < val - 1
        new_arr = _arr[head]
        new_arr[rest_r] += np.flip(rest, axis)
    return new_arr


new_arr = arr.copy()
new_arr = process_fold(new_arr, folds[0])
print(np.count_nonzero(new_arr))

new_arr = arr.copy()
for fold in folds:
    new_arr = process_fold(new_arr, fold)
    plt.imshow(new_arr.T > 0)
    plt.show()
# %%

