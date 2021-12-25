from __future__ import annotations
from collections import defaultdict
from operator import add, mul, floordiv, eq, mod
from pprint import pprint
from typing import List, Callable, Dict, NamedTuple, Literal, Union

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

int_ops: Dict[str, Callable[[int, int], int]] = {
    'add': add, 'mul': mul, 'div': floordiv, 'mod': mod, 'eql': lambda x, y: int(eq(x, y))}

Var = Literal['x', 'y', 'z']
Ops = Literal['add', 'mul', 'div', 'mod', 'eql']


class Inputs(NamedTuple):
    n: int

    def __repr__(self):
        return f'w{self.n}'


class Ref(NamedTuple):
    var: Union[Var, Inputs]
    t: int

    def get(self, graph: Dict[Ref, TOp]) -> TOp:
        return graph[self]

    def __repr__(self):
        return f'{self.var}.{self.t}'


OpC = Union[Ref, int, Inputs]

op_symbols = {'add': '+', 'mul': '*', 'div': '/', 'mod': '%', 'eql': '='}


class Op(NamedTuple):
    op: Ops
    a: OpC
    b: OpC

    def refs(self):
        if isinstance(self.a, Ref):
            yield self.a
        if isinstance(self.b, Ref):
            yield self.b

    @property
    def nest(self):
        return NestedOp(self.op, self.a, self.b)

    def eval(self, graph: Dict[Ref, TOp]):
        return self.calc(graph, {})

    def calc(self, graph: Dict[Ref, TOp], inputs: Dict[Inputs, int]) -> TOp:
        op, a, b = self
        a_res = a
        while isinstance(a_res, Ref):
            a_res = a.get(graph)
            if not isinstance(a_res, Op):
                a = a_res
        if isinstance(a, Inputs) and a in inputs:
            a = inputs[a]

        b_res = b
        while isinstance(b_res, Ref):
            b_res = b.get(graph)
            if not isinstance(b_res, Op):
                b = b_res
        if isinstance(b, Inputs) and b in inputs:
            b = inputs[b]

        if isinstance(a, int) and isinstance(b, int):
            if op == 'mod':
                if a < 0 or b <= 0:
                    raise Exception("Invalid modulo")
            return int_ops[op](a, b)
        if op == 'add':
            if b == 0:
                return a
            if a == 0:
                return b
            return Op(op, a, b)
        elif op == 'mul':
            if a == 0 or b == 0:
                return 0
            else:
                if a == 1:
                    return b
                if b == 1:
                    return a
                return Op(op, a, b)
        elif op == 'div':
            if b == 0:
                raise Exception("Division by zero")
            elif a == 0:
                return 0
            elif b == 1:
                return a
            else:
                return Op(op, a, b)
        elif op == 'mod':
            if a == 0:
                return 0
            elif a == 1:
                return 1
            elif b == 1:
                return 0
            else:
                return Op(op, a, b)
        else:
            assert op == 'eql'
            if a == b:
                return 1
            else:
                return Op(op, a, b)

    def __repr__(self):
        return f'{self.a} {op_symbols[self.op]} {self.b}'


class NestedOp(NamedTuple):
    op: Ops
    a: Union[OpC, NestedOp, Op]
    b: Union[OpC, NestedOp, Op]

    @property
    def nest(self):
        return self

    def __repr__(self):
        a = f"({self.a})" if isinstance(self.a, NestedOp) or isinstance(self.a, Op) else repr(self.a)
        b = f"({self.b})" if isinstance(self.b, NestedOp) or isinstance(self.b, Op) else repr(self.b)
        return f'{a} {op_symbols[self.op]} {b}'

    def deref(self, ref: Ref, content: Union[OpC, NestedOp, Op]) -> NestedOp:
        if self.a == ref:
            return NestedOp(self.op, content, self.b)
        elif self.b == ref:
            return NestedOp(self.op, self.a, content)
        else:
            raise ValueError(f'{ref} not found in {self}')


TOp = Union[Op, int, Inputs]


def parse(_contents) -> List[List[str]]:
    return [row.strip().split(" ") for row in _contents.strip().split('\n')]


compute_graph: Dict[Ref, TOp] = {Ref('x', 0): 0, Ref('y', 0): 0, Ref('z', 0): 0}
step = {'x': 0, 'y': 0, 'z': 0}
n = 0
input_port = None
stawp = 0
for row in parse(contents):
    if row[0] == 'inp':
        input_port = Inputs(n)
        step[input_port] = 0
        compute_graph[Ref(input_port, 0)] = input_port
        n += 1
    else:
        op_str, s, t = row
        if t == 'w':
            t = input_port
        if s == 'w':
            s = input_port
        s_ref = Ref(s, step[s])

        if t not in step:
            t_ref = int(t)
        else:
            t_ref = Ref(t, step[t])
        op = Op(op_str, s_ref, t_ref)

        opt_val = op.eval(compute_graph)
        compute_graph[Ref(s, step[s] + 1)] = opt_val
        step[s] += 1

pprint(compute_graph)
final = Ref('z', step['z'])
print(len(compute_graph))
# %%
ops_graph = {k: v.eval(compute_graph) for k, v in compute_graph.items() if isinstance(v, Op)}
ops_graph
# %%
# pprint(forward_ref)
# trimmed_graph = {k: v for k, v in compute_graph.items() if (k in forward_ref) or k == final}
# pprint(trimmed_graph)
# print(len(trimmed_graph), len(ops_graph))
# %%
inputs = {
    Inputs(0): 9,
    Inputs(1): 9,
    Inputs(2): 9,
    Inputs(3): 9,
    Inputs(4): 9,
    Inputs(5): 9,
    Inputs(6): 9,
    Inputs(7): 9,
    Inputs(8): 9,
    Inputs(9): 9,
    Inputs(10): 9,
    Inputs(11): 9,
    Inputs(12): 9,
    Inputs(13): 9
}
val_graph = ops_graph.copy()
val_graph = {k: v.calc(val_graph, inputs) for k, v in val_graph.items()}
old_len = len(val_graph)
val_graph = {k: v.eval(val_graph) for k, v in val_graph.items() if isinstance(v, Op)}
while old_len != len(val_graph):
    old_len = len(val_graph)
    val_graph = {k: v.eval(val_graph) for k, v in val_graph.items() if isinstance(v, Op)}
    print(len(val_graph), val_graph[final])



# %%
def visualize(in_graph):
    forward_ref = defaultdict(list)
    for k, val in in_graph.items():
        if isinstance(val, Op):
            for ref in val.refs():
                forward_ref[ref].append(k)

    graph: Dict[Ref, Union[TOp, NestedOp]] = in_graph.copy()
    for ref, fwd_refs in forward_ref.items():
        fwd_refs = set(fwd_refs) & graph.keys()
        if len(fwd_refs) == 1:
            next_ref = next(iter(fwd_refs))
            graph[next_ref] = graph[next_ref].nest.deref(ref, graph[ref])
            del graph[ref]
    pprint(graph)


visualize(val_graph)
# pprint(compute_graph)
# print(compute_graph[('z', step['z'])])
