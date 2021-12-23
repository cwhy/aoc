import heapq
import random
from typing import NamedTuple, Tuple, List

import numpy as np

state_table = dict(a=0, b=1, c=2, d=3)
state_table_rev = {v: k for k, v in state_table.items()}
state_table_rev[-1] = '.'
energy_req = [10 ** i for i in state_table.values()]
print(energy_req)
state_str = "bcbdadca"
my_state_str = "accdbdab"


#############
# 67890123456#
### 0#1#2#3###
##  4#5#6#7#
##  8#9#0#1#
##  2#3#4#5#
#########
def parse_state2(s_str):
    return tuple([state_table[i] for i in s_str[:4] + "dcbadbac" + s_str[4:]] + [-1] * 11)


win_state = tuple([state_table[i] for i in "abcd" * 4] + [-1] * 11)

neighbours = {
    0: (18, 4),
    1: (20, 5),
    2: (22, 6),
    3: (24, 7),
    4: (0, 8),
    5: (1, 9),
    6: (2, 10),
    7: (3, 11),
    8: (4, 12),
    9: (5, 13),
    10: (6, 14),
    11: (7, 15),
    12: (8,),
    13: (9,),
    14: (10,),
    15: (11,),
    16: (17,),
    17: (16, 18),
    18: (0, 17, 19),
    19: (18, 20),
    20: (1, 19, 21),
    21: (20, 22),
    22: (2, 21, 23),
    23: (22, 24),
    24: (3, 23, 25),
    25: (24, 26),
    26: (25,),
}
short_cuts = {}

for k in neighbours:
    pos_queue = [(v, {v}) for v in neighbours[k]]
    short_cut = {}
    while pos_queue:
        pos, path = pos_queue.pop(0)
        short_cut[pos] = path
        for n in neighbours[pos]:
            if n not in short_cut and n != k:
                pos_queue.append((n, path | {n}))
    short_cuts[k] = short_cut

hallways = {18, 20, 22, 24}
rooms = {0: (0, 4, 8, 12),
         1: (1, 5, 9, 13),
         2: (2, 6, 10, 14),
         3: (3, 7, 11, 15)}
outside = range(16, 27)

for n in sum(rooms.values(), ()):
    for h in hallways:
        del short_cuts[n][h]

for room in rooms.values():
    for c1 in room:
        for c2 in room:
            if c1 != c2:
                del short_cuts[c1][c2]

to_rm = set()
for i in outside:
    for j in short_cuts[i]:
        # don't move around outside
        if j in outside:
            to_rm.add((i, j))

for i, j in to_rm:
    del short_cuts[i][j]
short_cuts


# %%

def get_agent_loc(s_arr):
    return [np.where(s_arr == i)[0] for i in range(4)]


class Option(NamedTuple):
    agent: int
    from_to: Tuple[int, int]
    next_state: Tuple[int, ...]
    steps: int

    def get_action(self):
        return (self.agent,) + self.from_to


def action_model(s, a):
    s_arr = np.array(s)
    new_s = s_arr.copy()
    new_s[a[1]] = -1
    new_s[a[-1]] = a[0]
    return new_s, len(short_cuts[a[1]][a[-1]]) * energy_req[a[0]]


def model(s):
    s_arr = np.array(s)
    options: List[Option] = []
    for agent_id, locs in enumerate(get_agent_loc(s_arr)):
        room = rooms[agent_id]
        room_val = s_arr[np.array(room)]
        for agent_loc in locs:
            if room[-1] == agent_loc:
                continue
            skip_flag = False
            for i in range(3):
                if room[i] == agent_loc and (room_val[i + 1:] == agent_id).all():
                    skip_flag = True
                    break
            if skip_flag:
                continue
            for target, path in short_cuts[agent_loc].items():
                if target in sum(rooms.values(), ()):
                    if target not in room:
                        continue
                    else:
                        tpl_match = -np.ones(4, dtype=int)
                        tpl_match[:room.index(target) + 1] = agent_id
                        if not (room_val + tpl_match == agent_id - 1).all():
                            continue

                for p in path:
                    if s[p] != -1:
                        break
                else:
                    new_s = s_arr.copy()
                    new_s[agent_loc] = -1
                    new_s[target] = agent_id
                    options.append(Option(agent_id, (agent_loc, target), tuple(new_s), len(path)))

    return options


def vis_(s):
    print("#" * 20)
    print("##" + "".join(state_table_rev[i] for i in s[16:]))
    print("#" * 3 + "".join(f"|{state_table_rev[s[i]]}" for i in range(4)))
    print("#" * 3 + "".join(f"|{state_table_rev[s[i + 4]]}" for i in range(4)))
    print("#" * 3 + "".join(f"|{state_table_rev[s[i + 8]]}" for i in range(4)))
    print("#" * 3 + "".join(f"|{state_table_rev[s[i + 12]]}" for i in range(4)))
    print("#" * 20)


# %%
#############
# 67890123456#
### 0#1#2#3###
##  4#5#6#7#
##  8#9#0#1#
##  2#3#4#5#
#########
_state = parse_state2(state_str)
cost_all = 0
for a in [(3, 3, 26), (0, 7, 16), (1, 2, 25), (1, 6, 23), (0, 10, 17), (2, 1, 10), (2, 5, 6)]:
    options = model(_state)
    avail = [option.get_action() for option in options]
    print(a)
    if a not in avail:
        print(get_agent_loc(np.array(_state)))
        print(short_cuts[a[1]][a[2]])
        print(avail)
    assert a in avail
    _state, cost = action_model(_state, a)
    opt_cost = 0
    for option in options:
        if option.get_action() == a:
            opt_cost += option.steps * energy_req[option.agent]
    cost_all += cost
    print(opt_cost, cost, cost_all)
    assert cost == opt_cost
    vis_(_state)

# %%
_state = parse_state2(state_str)
old_states = {_state}
cost = 0
for _ in range(100):
    if _state == win_state:
        vis_(_state)
        print(f"Win in cost of {cost}")
        break
    vis_(_state)
    options = [option for option in model(_state) if option.next_state not in old_states]
    if len(options) == 0:
        print("No options")
        break
    else:
        if len(options) == 1:
            option = options[0]
            print(option)
        else:
            option = random.choice(options)
            print("random, ", option)
        _state = option.next_state
        cost_n = option.steps * energy_req[option.agent]
        cost += cost_n
        print(f"Cost: {cost_n}, total cost: {cost}")
    old_states.add(_state)

# %%
state_queue = [(0, parse_state2(my_state_str))]
old_states = set()
win_states = {}
while state_queue:
    cost, _state = heapq.heappop(state_queue)
    if _state in old_states:
        continue
    old_states.add(_state)
    if _state == win_state:
        win_states[_state] = cost
        print(f"Win in cost {cost}")
        break
    else:
        for option in model(_state):
            if option.next_state not in old_states:
                heapq.heappush(state_queue, (cost + option.steps * energy_req[option.agent], option.next_state))
