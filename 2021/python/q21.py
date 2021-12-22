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
de_evolve_table = {}
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
                de_evolve_table[(dest3, (j1, j2, j3))] = idx

pprint(evolve_table)
# %%
MAXSCORE = 21
t_max = MAXSCORE
a_pos, b_pos = test_pos
_pos = a_pos


def find_path_table(_pos):
    # path_table = defaultdict(int)
    # path_table[(0, _pos)] = 1
    path_table_t = defaultdict(int)
    curr_pos_score = defaultdict(int)
    curr_pos_score[(_pos, 0)] = 1
    t = 0
    while True:
        t += 1
        new_pos_score = defaultdict(int)
        for (old_pos, old_score), n_paths in curr_pos_score.items():
            for p in directions:
                new_pos = evolve_table[(old_pos, p)]
                new_score = old_score + new_pos
                new_pos_score[(new_pos, new_score)] += n_paths
                if new_score < MAXSCORE:
                    path_table_t[t] += n_paths
        curr_pos_score = new_pos_score
        if t >= t_max:
            break
    pprint(path_table_t)
    return path_table_t


a_path_table = find_path_table(a_pos)
b_path_table = find_path_table(b_pos)
# %%
max_a_t = max(a_path_table.keys())
max_b_t = max(b_path_table.keys())
a_lose_cum = [a_path_table[i] for i in range(1, max_a_t + 1)]
b_lose_cum = [b_path_table[i] for i in range(1, max_b_t + 1)]
# a_win_cum = [27*(27 ** (i+1) - e) for i, e in enumerate(a_lose_cum)]
# b_win_cum = [27 ** (i+1) - e for i, e in enumerate(b_lose_cum)]
a_lose_prob = [e / (27 ** (i + 1)) for i, e in enumerate(a_lose_cum)]
b_lose_prob = [e / (27 ** (i + 1)) for i, e in enumerate(b_lose_cum)]
print(a_lose_prob)
print(b_lose_prob)

# %%
print(a_lose_prob)
print(b_lose_prob)

t = 0
awus = []
bwus = []
continue_prob_a_ = 1
continue_prob_b_ = 1
continue_prob_ = 1
old_wins = 0
all_u = 1
while True:
    print(t)
    if t >= min(max_b_t, max_a_t):
        break
    if t == 0:
        awu = bwu = 0
    else:
        all_u *= 27
        awu = int(round(all_u * (1 - a_lose_prob[t])))
        continue_prob_a_ *= (1 - awu / all_u)
        print(continue_prob_a_, all_u)

        all_u *= 27
        bwu = int(round(all_u * (1 - b_lose_prob[t]))) * continue_prob_a_
        # continue_prob_b_ *= (1 - bwu / all_u)
        # continue_prob_ = (1 - bwu / all_u)
    print(awu)
    print(bwu)
    awus.append(awu)
    bwus.append(bwu)
    print("_____")
    t += 1
print(sum(awus))
print(sum(bwus))
print("_____")
