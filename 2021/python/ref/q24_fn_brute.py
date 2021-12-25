from collections import defaultdict
from functools import lru_cache
from typing import List, Tuple, Callable, Dict, Union
from operator import add, mul, floordiv, eq, mod

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
    'add': add,
    'mul': mul,
    'div': floordiv,
    'mod': mod,
    'eql': lambda x, y: int(eq(x, y))}


def parse(_contents) -> List[List[str]]:
    return [row.strip().split(" ") for row in _contents.strip().split('\n')]


Vars = Tuple[int, int, int, int]
Instruction = Tuple[str, int, int]
Promise = Callable[[Vars], Instruction]


def update_tuple4(t: Vars, ix: int, val: int) -> Vars:
    if ix == 0:
        return val, t[1], t[2], t[3]
    elif ix == 1:
        return t[0], val, t[2], t[3]
    elif ix == 2:
        return t[0], t[1], val, t[3]
    else:
        assert ix == 3
        return t[0], t[1], t[2], val


def parse2(_contents: List[List[str]]) -> List[Promise]:
    ins = []
    for row in _contents:
        if row[0] == "inp":
            ins.append(lambda vars: (row[1], vars[0], vars[1], vars[2]))

        else:
            op, a, b = row

    return ins


@lru_cache
def f(registers: Vars, instruction: Instruction) -> Instruction:
    op, a, sb = instruction
    var_b = int(sb) if sb.isdecimal() else registers[translate[sb]]
    registers = update_tuple4(registers, a, op(registers[a], var_b))
    return registers
