from __future__ import annotations

from collections import defaultdict
from functools import reduce
from operator import mul
from typing import NamedTuple, Union, Tuple, List, Literal, Dict

test_content = "target area: x=20..30, y=-10..-5"
content = "target area: x=117..164, y=-140..-89"


def parse(_content):
    xy_str = [s.split("=")[-1].split("..") for s in _content.split(": ")[-1].split(", ")]
    x, y = [tuple(int(s) for s in ss) for ss in xy_str]
    return x, y


MAX_T = 1000
target = parse(content)
x_range, y_range = target

available_vx = defaultdict(list)
for vx in range(1, x_range[1] + 1):
    x_pos = 0
    vx_ = vx
    t = 0
    while x_pos <= x_range[1] and t <= MAX_T:
        t += 1
        x_pos += vx_
        vx_ = max(vx_ - 1, 0)
        if x_range[1] >= x_pos >= x_range[0]:
            available_vx[vx].append(t)
            print(x_pos)
        elif vx_ < 1:
            break

#%%
reversed_vx = defaultdict(set)
for k, v in available_vx.items():
    for t in v:
        reversed_vx[t].add(k)

vy2vx = defaultdict(set)
vy_max = y_range[0]
for vy in range(-MAX_T, MAX_T):
    y_pos = 0
    vy_ = vy
    t = 0
    while y_pos >= y_range[0]:
        t += 1
        y_pos += vy_
        vy_ -= 1
        if y_range[0] <= y_pos <= y_range[1] and t in reversed_vx:
            vy2vx[vy] |= reversed_vx[t]
            vy_max = max(vy_max, vy)


def max_pos(_vy: int) -> int:
    return (_vy ** 2 + abs(_vy)) // 2


#%%
print(target)
vx_max = next(iter(vy2vx[vy_max]))
print(available_vx[vx_max])
print(vx_max, vy_max)
print(max_pos(vy_max))
print(len(sum([list(v) for v in vy2vx.values()], [])))

#%%
pos_x = pos_y = 0
_vx_max = vx_max
_vy_max = vy_max
for t in range(available_vx[vx_max][-1] + 1):
    pos_x += _vx_max
    pos_y += _vy_max
    print(pos_y)
    _vx_max = max(_vx_max-1, 0)
    _vy_max -= 1
    if x_range[0] <= pos_x <= x_range[1] and y_range[0] <= pos_y <= y_range[1]:
        print(f"{pos_x}, {pos_y}")
        break
#%%
vy2vx

