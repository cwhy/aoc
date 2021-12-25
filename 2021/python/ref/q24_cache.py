from collections import defaultdict
from functools import lru_cache
from typing import List, Tuple, Callable, Dict
from operator import add, mul, floordiv, eq, mod

import numpy as np

test_contents = """
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""

with open('2021/input24.txt') as file:
    contents = file.read()

operators: Dict[str, Callable[[int, int], int]] = {
    'add': add, 'mul': mul, 'div': floordiv, 'mod': mod, 'eql': lambda x, y: int(eq(x, y))}


def parse(_contents) -> List[List[str]]:
    return [row.strip().split(" ") for row in _contents.strip().split('\n')]


Vars = Tuple[int, int, int, int]
Procs = List[Tuple[str, str, str]]
Funcs = List[Tuple[str, Procs]]


def parse2(_contents: List[List[str]]) -> Funcs:
    procs = []
    param = proc = None
    for row in _contents:
        if row[0] == "inp":
            if proc is not None:
                assert param is not None
                procs.append((param, proc))
            proc = []
            param = row[1]
        else:
            assert proc is not None
            op, a, b = row
            proc.append((op, a, b))
    if proc is not None:
        procs.append((param, proc))
    return procs


translate = {
    'w': 0, 'x': 1, 'y': 2, 'z': 3,
}


def eval_stuff(inputs: List[int], procs: Funcs) -> Dict[str, int]:
    vars_ = defaultdict(int)
    for param, proc in procs:
        vars_[param] = inputs.pop(0)
        for op, a, b in proc:
            var_b = int(b) if b.strip('-').isnumeric() else vars_[b]
            vars_[a] = operators[op](vars_[a], var_b)

    return dict(vars_)


def update_vars(t: Vars, ix: int, val: int) -> Vars:
    if ix == 0:
        return val, t[1], t[2], t[3]
    elif ix == 1:
        return t[0], val, t[2], t[3]
    elif ix == 2:
        return t[0], t[1], val, t[3]
    else:
        assert ix == 3
        return t[0], t[1], t[2], val


def get_function(proc: Procs) -> Callable[[Vars], Vars]:
    @lru_cache
    def f(registers: Vars) -> Vars:
        for op, sa, sb in proc:
            a = translate[sa]
            var_b = int(sb) if sb.strip('-').isdigit() else registers[translate[sb]]
            registers = update_vars(registers, a, operators[op](registers[a], var_b))
        return registers

    return f


# eval_stuff([12], procs_)


def get_process(_contents: str) -> Callable[[Tuple[int, ...], Vars], Vars]:
    funcs = parse2(parse(_contents))
    fns = [(translate[param], get_function(procs)) for param, procs in funcs]

    @lru_cache
    def _process(inputs: Tuple[int, ...], v: Vars) -> Vars:
        step = len(inputs)
        param, proc = fns[-step]
        val = inputs[0]
        if step == 1:
            return proc(update_vars(v, param, val))
        else:
            v = _process(inputs[:-1], v)
            return proc(update_vars(v, param, val))

    return _process


process1 = lambda x: get_process(test_contents)(tuple(x), (0, 0, 0, 0))
print(process1([12]))

process2 = lambda x: get_process(contents)(tuple(x), (0, 0, 0, 0))

max_digit = 8
digits = [max_digit] * 14
num = int("".join([str(i) for i in digits]), 9)

while process2(digits)[-1] != 0:
    # print(f(digits))
    num -= 1
    num_repr = np.base_repr(num, 9)
    digits = [int(i) + 1 for i in num_repr]
    # print(x_pos)
