from collections import defaultdict
from pprint import pprint

import numpy as np

pos = (4, 2)
test_pos = (4, 8)

max_try = 3001
stuff = np.arange(1, max_try).reshape(-1, 3).sum(axis=1)[:max_try // 3].reshape(-1, 2)
a_pos, b_pos = pos
a_score = b_score = 0
for i, (a, b) in enumerate(stuff.tolist()):
    a_pos = (a_pos + a - 1) % 10 + 1
    a_score += a_pos
    print(a, b, a_pos, b_pos, a_score, b_score)
    if a_score >= 1000:
        n_roll = i * 6 + 3
        print(b_score, n_roll)
        print(b_score * n_roll)
        break
    b_pos = (b_pos + b - 1) % 10 + 1
    b_score += b_pos
    if b_score >= 1000:
        n_roll = i * 6 + 6
        print(a_score, n_roll)
        print(a_score * n_roll)
        break

# %%
evolve_table = {}
directions = set()
for i in range(10):
    idx = i + 1
    for j1 in (1, 2, 3):
        dest1 = (idx + j1 - 1) % 10 + 1
        for j2 in (1, 2, 3):
            dest2 = (dest1 + j2 - 1) % 10 + 1
            for j3 in (1, 2, 3):
                dest3 = (dest2 + j3 - 1) % 10 + 1
                directions.add((j1, j2, j3))
                evolve_table[(idx, (j1, j2, j3))] = dest3

pprint(evolve_table)


# %%
MAXSCORE = 21
t_max = MAXSCORE * 2
a_pos, b_pos = pos
curr_universe = {(a_pos, 0, b_pos, 0): [1, 1]}
win_table = [defaultdict(int), defaultdict(int)]
t = 0
while True:
    t += 1
    new_universe = {}
    for (old_pos_a, old_score_a, old_pos_b, old_score_b), (n_path_a, n_path_b) in curr_universe.items():
        for p in directions:
            new_pos_a = evolve_table[(old_pos_a, p)]
            new_score_a = old_score_a + new_pos_a
            if new_score_a >= MAXSCORE:
                win_table[0][t] += n_path_a
                continue
            for q in directions:
                new_pos_b = evolve_table[(old_pos_b, q)]
                new_score_b = old_score_b + new_pos_b
                if new_score_b >= MAXSCORE:
                    win_table[1][t] += n_path_b
                    continue
                if (new_pos_a, new_score_a, new_pos_b, new_score_b) in new_universe:
                    new_universe[(new_pos_a, new_score_a, new_pos_b, new_score_b)][0] += n_path_a
                    new_universe[(new_pos_a, new_score_a, new_pos_b, new_score_b)][1] += n_path_b
                else:
                    new_universe[(new_pos_a, new_score_a, new_pos_b, new_score_b)] = [n_path_a, n_path_b]
    curr_universe = new_universe
    if t >= t_max:
        break
print(sum(win_table[0].values()))
print(sum(win_table[1].values()))
