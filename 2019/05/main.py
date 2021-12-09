from typing import List


def run_prog(prog: List[int]):
    ptr = 0

    def get(val, mode):
        if mode == "1":
            return val
        elif mode == "0":
            return prog[val]
        else:
            raise NotImplementedError("mode=1/0!")

    while True:
        op_param = prog[ptr]
        op_str = str(op_param).zfill(5)
        op = op_str[-2:]
        m3, m2, m1 = op_str[:-2]

        if op == "99":
            return
        elif op == "01":
            in1, in2, ptr_out = prog[ptr + 1: ptr + 4]
            prog[ptr_out] = get(in1, m1) + get(in2, m2)
            ptr += 4
        elif op == "02":
            in1, in2, ptr_out = prog[ptr + 1: ptr + 4]
            prog[ptr_out] = get(in1, m1) * get(in2, m2)
            ptr += 4
        elif op == "07":
            in1, in2, ptr_out = prog[ptr + 1: ptr + 4]
            prog[ptr_out] = int(get(in1, m1) < get(in2, m2))
            ptr += 4
        elif op == "08":
            in1, in2, ptr_out = prog[ptr + 1: ptr + 4]
            prog[ptr_out] = int(get(in1, m1) == get(in2, m2))
            ptr += 4
        elif op == "03":
            ptr_out = prog[ptr + 1]
            prog[ptr_out] = int(input(">> Input: "))
            ptr += 2
        elif op == "04":
            in1 = prog[ptr + 1]
            print(get(in1, m1))
            ptr += 2
        elif op == "05":
            in1, in2 = prog[ptr + 1], prog[ptr + 2]
            if get(in1, m1) != 0:
                ptr = get(in2, m2)
            else:
                ptr += 3
        elif op == "06":
            in1, in2 = prog[ptr + 1], prog[ptr + 2]
            if get(in1, m1) == 0:
                ptr = get(in2, m2)
            else:
                ptr += 3
        else:
            raise NotImplementedError("")


with open("input.txt") as f:
    prog_ = [int(l.strip()) for l in f.readline().split(",")]


run_prog(prog_.copy())
