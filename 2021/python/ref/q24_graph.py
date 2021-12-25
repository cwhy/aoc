from operator import add, mul, floordiv, eq, mod
from pprint import pprint
from typing import List, Callable, Dict

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


def eval_add(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a + b
    elif a == 0 and isinstance(b, tuple):
        return b
    elif b == 0 and isinstance(a, tuple):
        return a
    else:
        return 'add', a, b


def eval_mul(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a * b
    elif a == 0 or b == 0:
        return 0
    elif a == 1 and isinstance(b, tuple):
        return b
    elif b == 1 and isinstance(a, tuple):
        return a
    else:
        return 'mul', a, b


def eval_div(a, b):
    if b == 0:
        raise Exception("Division by zero")
    elif isinstance(a, int) and isinstance(b, int):
        return a // b
    elif a == 0 and isinstance(b, tuple):
        return 0
    elif b == 1 and isinstance(a, tuple):
        return a
    else:
        return 'div', a, b


def eval_eql(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    else:
        return 'eql', a, b


def eval_mod(a, b):
    if a < 0 or b <= 0:
        raise Exception("Invalid modulo")
    elif isinstance(a, int) and isinstance(b, int):
        return a // b
    elif a == 0 and isinstance(b, tuple):
        return 0
    elif a == 1 and isinstance(b, tuple):
        return 1
    elif b == 1 and isinstance(a, tuple):
        return 0
    else:
        return 'mod', a, b


def parse(_contents) -> List[List[str]]:
    return [row.strip().split(" ") for row in _contents.strip().split('\n')]


compute_graph = {('x', 0): 0, ('y', 0): 0, ('z', 0): 0}
step = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
n = 0
input_port = None
for row in parse(contents):
    if row[0] == 'inp':
        input_port = f'w{n}'
        step[input_port] = 0
        n += 1
    else:
        op, s, t = row
        if s == 'w':
            compute_graph[(s, step[s])] = input_port
        else:
            prev_value = compute_graph[(s, step[s])]

            if prev_value == 0 and op not in ['add', 'eql']:
                continue

            if t == 'w':
                if prev_value == 0:
                    step[s] += 1
                    compute_graph[(s, step[s])] = input_port
                else:
                    step[s] += 1
                    compute_graph[(s, step[s])] = (op, prev_value, input_port)
            else:
                if t in 'xyz':
                    val = compute_graph[(t, step[t])]
                else:
                    val = int(t)
                    if val == 0:
                        if op == 'add':
                            continue
                        elif op == 'mul':
                            step[s] += 1
                            compute_graph[(s, step[s])] = 0
                            continue

                    if prev_value == 0:
                        if op == 'add':
                            step[s] += 1
                            compute_graph[(s, step[s])] = val
                            continue
                    elif isinstance(prev_value, int):
                        if isinstance(val, int):
                            step[s] += 1
                            compute_graph[(s, step[s])] = operators[op](prev_value, val)
                        else:
                            step[s] += 1
                            compute_graph[(s, step[s])] = (op, prev_value, (t, step[t]))
                    elif isinstance(val, int):
                        step[s] += 1
                        compute_graph[(s, step[s])] = (op, (s, step[s] - 1), val)

                    step[s] += 1
                    compute_graph[(s, step[s])] = (op, (s, step[s] - 1), (t, step[t]))

pprint(compute_graph)
# print(compute_graph[('z', step['z'])])
