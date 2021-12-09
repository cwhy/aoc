import numpy as np

with open('../input5.txt') as f:
    k = f.readlines()

table = np.zeros((1000, 1000))
for z in k:
    lp, rp = z.strip().split("->")
    a, b = [int(i) for i in lp.strip().split(",")]
    c, d = [int(i) for i in rp.strip().split(",")]
    x0 = min(a, c)
    y0 = min(b, d)
    x1 = max(a, c)
    y1 = max(b, d)
    if a == c:
        table[a, y0:y1+1] += 1
    elif b == d:
        table[x0:x1+1, b] += 1
    else:
        assert x1 - x0 == y1 - y0
        if a - c == b - d:
            table[x0:x1+1, y0:y1+1] += np.eye(x1-x0+1)
        else:
            table[x0:x1+1, y0:y1+1] += np.fliplr(np.eye(x1-x0+1))

print((table >= 2).sum())
print(table.T)
