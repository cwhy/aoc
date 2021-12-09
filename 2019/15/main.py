from typing import List, Tuple


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
            val = (yield)
            assign_(ptr_out, val, m1)
            ptr += 2
        elif op == "04":
            in1 = access_args(1)[0]
            yield get(in1, m1)  # Out
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

server = run_prog(prog_.copy())


def request_(x: int):
    next(server)
    out = server.send(x)
    # print(x, out)
    return out


back = {1: 2, 2: 1, 3: 4, 4: 3}


def try_steps_(steps: List[int], target: bool):
    def _rewind(_path):
        for x in reversed(_path):
            response = request_(back[x])
            if response != 1 and response != 2:
                print(response)
                raise NotImplementedError("")
    for i, x in enumerate(steps):
        response = request_(x)
        if response == 0:
            _rewind(steps[:i])
            return None
        elif response == 2:
            if target:
                return True
            else:
                continue
    else:
        _rewind(steps[:i+1])
        return False


def pos_calc(steps: List[int]) -> Tuple[int, int]:
    orig = [0, 0]
    for d in steps:
        if d == 1:
            orig[0] += 1
        elif d == 2:
            orig[0] -= 1
        elif d == 3:
            orig[1] += 1
        elif d == 4:
            orig[1] -= 1
        else:
            raise NotImplementedError("")
    return tuple(orig)


def bfs_(target):
    # r = 0
    tried_pos = set()
    max_r = 0
    q = [[i] for i in (1, 2, 3, 4)]
    while len(q) > 0:
        d = q.pop(0)
        max_r = max(max_r, len(d))
        # if len(d) > r:
        #     r = len(d)
        #     print(q)
        tried_pos.add(pos_calc(d))
        resp = try_steps_(d, target)
        if resp is not None:
            if resp:
                return len(d)
            else:
                q += [d + [i] for i in (1, 2, 3, 4)
                      if pos_calc(d + [i]) not in tried_pos]
        else:
            continue
    return len(d)


print(bfs_(True))
print(bfs_(False))
