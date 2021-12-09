from typing import List


def run_prog(prog: List[int], _noun: int, _verb: int):
    prog[1] = _noun
    prog[2] = _verb
    ptr = 0
    while prog[ptr] != 99:
        op, ptr_in1, ptr_in2, ptr_out = prog[ptr: ptr + 4]
        if op == 1:
            prog[ptr_out] = prog[ptr_in1] + prog[ptr_in2]
        elif op == 2:
            prog[ptr_out] = prog[ptr_in1] * prog[ptr_in2]
        else:
            raise NotImplementedError("")
        ptr += 4
    return prog[0]


with open("input.txt") as f:
    prog_ = [int(l.strip()) for l in f.readline().split(",")]

print(run_prog(prog_.copy(), 12, 2))

for noun in range(100):
    for verb in range(100):
        val = run_prog(prog_.copy(), noun, verb)
        if val == 19690720:
            print(noun * 100 + verb)
