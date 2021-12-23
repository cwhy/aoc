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
win_state_str = "abcdabcd"

#############
# 89012345678#
### 0#1#2#3###
##  4#5#6#7#
#########
state = tuple([state_table[i] for i in state_str] + [-1] * 11)
my_state = tuple([state_table[i] for i in my_state_str] + [-1] * 11)
win_state = tuple([state_table[i] for i in win_state_str] + [-1] * 11)
neighbours = {
    0: (10, 4),
    1: (12, 5),
    2: (14, 6),
    3: (16, 7),
    4: (0,),
    5: (1,),
    6: (2,),
    7: (3,),
    8: (9,),
    9: (8, 10),
    10: (0, 9, 11),
    11: (10, 12),
    12: (1, 11, 13),
    13: (12, 14),
    14: (2, 13, 15),
    15: (14, 16),
    16: (3, 15, 17),
    17: (16, 18),
    18: (17,),
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
hallways = {10, 12, 14, 16}
rooms = {0: (0, 4),
         1: (1, 5),
         2: (2, 6),
         3: (3, 7)}
for n in sum(rooms.values(), ()):
    for h in hallways:
        del short_cuts[n][h]

for room in rooms.values():
    a, b = room
    del short_cuts[a][b]
    del short_cuts[b][a]

to_rm = set()
for i in range(8, 19):
    for j in short_cuts[i]:
        # don't move around outside
        if j in range(8, 19):
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
        for agent_loc in locs:
            if rooms[agent_id][1] == agent_loc:
                continue
            if rooms[agent_id][0] == agent_loc and s[rooms[agent_id][1]] == agent_id:
                continue
            for target, path in short_cuts[agent_loc].items():
                if target in sum(rooms.values(), ()):
                    room = rooms[agent_id]
                    if ((target not in room)
                            or (target == room[0] and s[room[1]] != agent_id)
                            or (target == room[1] and s[room[0]] != -1)):
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
    print("##" + "".join(state_table_rev[i] for i in s[8:]))
    print("#" * 3 + "".join(f"|{state_table_rev[s[i]]}" for i in range(4)))
    print("#" * 3 + "".join(f"|{state_table_rev[s[i + 4]]}" for i in range(4)))
    print("#" * 20)


# %%
#############
# 89012345678#
### 0#1#2#3###
##  4#5#6#7#
#########
_state = state
cost_all = 0
for a in [(1, 2, 11), (2, 1, 2), (3, 5, 13), (1, 11, 5), (1, 0, 1),
          (3, 3, 15), (0, 7, 17), (3, 15, 7), (3, 13, 3), (0, 17, 0)]:
    options = model(_state)
    avail = [option.get_action() for option in options]
    print(a)
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
_state = state
old_states = {state}
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
state_queue = [(0, my_state)]
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
    else:
        for option in model(_state):
            if option.next_state not in old_states:
                heapq.heappush(state_queue,(cost + option.steps * energy_req[option.agent], option.next_state))


