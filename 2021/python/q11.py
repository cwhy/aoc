import numpy as np

content = """
4871252763
8533428173
7182186813
2128441541
3722272272
8751683443
3135571153
5816321572
2651347271
7788154252
"""


# with open('2021/input10.txt') as file:
#     content = file.read()
matrix = np.array([list(int(i) for i in r.strip()) for r in content.strip().split()])
x_len, y_len = matrix.shape
print("---------------")
print(matrix)

n_flashes = 0
for i in range(1000):
    matrix += 1
    to_flash = set((a, b) for a, b in np.argwhere(matrix > 9).tolist())
    while to_flash:
        x, y = to_flash.pop()
        for _x in range(max(x - 1, 0), min(x + 2, x_len)):
            for _y in range(max(y - 1, 0), min(y + 2, y_len)):
                matrix[_x, _y] += 1
                if matrix[_x, _y] == 10:
                    to_flash.add((_x, _y))
        n_flashes += 1
    if i == 100:
        print("flash @ 100", n_flashes)
    if (matrix == matrix[0]).all():
        print("sync! @ ", i)
        break

    matrix[matrix > 9] = 0
print(matrix)
