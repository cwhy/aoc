from typing import List


def run_prog(prog: List[int]):
    ptr = 0
    base_ptr = 0
    heap = {}

    def access(_ptr):
        if _ptr < len(prog):
            return prog[_ptr]
        elif _ptr in heap:
            return heap[_ptr]
        else:
            return 0

    def access_args(n):
        return tuple(access(ptr + 1 + i) for i in range(n))

    def assign_(_ptr, val, mode):
        nonlocal base_ptr
        if mode == "2":
            _ptr += base_ptr
        if _ptr < len(prog):
            prog[_ptr] = val
        else:
            heap[_ptr] = val

    def get(val, mode):
        nonlocal base_ptr
        if mode == "1":
            return val
        elif mode == "0":
            return access(val)
        elif mode == "2":
            return access(val + base_ptr)
        else:
            raise NotImplementedError("mode=1/0!")

    while True:
        op_param = access(ptr)
        op_str = str(op_param).zfill(5)
        op = op_str[-2:]
        m3, m2, m1 = op_str[:-2]

        if op == "99":
            return
        elif op == "01":
            in1, in2, ptr_out = access_args(3)
            val = get(in1, m1) + get(in2, m2)
            assign_(ptr_out, val, m3)
            ptr += 4
        elif op == "02":
            in1, in2, ptr_out = access_args(3)
            val = get(in1, m1) * get(in2, m2)
            assign_(ptr_out, val, m3)
            ptr += 4
        elif op == "07":
            in1, in2, ptr_out = access_args(3)
            val = int(get(in1, m1) < get(in2, m2))
            assign_(ptr_out, val, m3)
            ptr += 4
        elif op == "08":
            in1, in2, ptr_out = access_args(3)
            val = int(get(in1, m1) == get(in2, m2))
            assign_(ptr_out, val, m3)
            ptr += 4
        elif op == "03":
            ptr_out = access_args(1)[0]
            val = int(input(">> Input: "))
            assign_(ptr_out, val, m1)
            ptr += 2
        elif op == "04":
            in1 = access_args(1)[0]
            print(">> Output: ",  get(in1, m1))  # Out
            ptr += 2
        elif op == "05":
            in1, in2 = access_args(2)
            if get(in1, m1) != 0:
                ptr = get(in2, m2)
            else:
                ptr += 3
        elif op == "06":
            in1, in2 = access_args(2)
            if get(in1, m1) == 0:
                ptr = get(in2, m2)
            else:
                ptr += 3
        elif op == "09":
            in1 = access_args(1)[0]
            base_ptr += get(in1, m1)
            ptr += 2
        else:
            raise NotImplementedError("")


with open("input.txt") as f:
    prog_ = [int(l.strip()) for l in f.readline().split(",")]


run_prog(prog_.copy())
