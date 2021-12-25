from __future__ import annotations
from collections import defaultdict
from operator import add, mul, floordiv, eq, mod
from pprint import pprint
from typing import List, Callable, Dict, NamedTuple, Literal, Union, Optional, Tuple

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

    inputs_tag: Literal['INPUTS'] = 'INPUTS'

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


def get_range(opc: OpC, graph: Dict[Ref, TOp]) -> Tuple[int, int]:
    if isinstance(opc, Inputs) or hasattr(opc, "inputs_tag"):
        return 1, 9
    elif isinstance(opc, int):
        return opc, opc
    elif isinstance(opc, Ref):
        return get_range(opc.get(graph), graph)
    elif isinstance(opc, Op) or isinstance(opc, NestedOp) or hasattr(opc, "op"):
        return opc.rrange(graph)
    else:
        print(opc)
        print(isinstance(opc, Inputs))
        print(type(opc))
        raise ValueError(f'Unknown opc type: {type(opc)}')


class Op(NamedTuple):
    op: Ops
    a: OpC
    b: OpC

    def rrange(self, graph: Dict[Ref, TOp]) -> Tuple[int, int]:
        arange = get_range(self.a, graph)
        brange = get_range(self.b, graph)
        if self.op == 'eql':
            if arange[1] < brange[0] or brange[1] < arange[0]:
                return 0, 0
            elif arange[1] == brange[0] == arange[0] == brange[1]:
                return 1, 1
            else:
                return 0, 1
        elif self.op == 'mod':
            return 0, brange[1]
        elif self.op == 'div':
            if brange[0] > arange[1] > arange[0] > 0:
                return 0, 0
            vals = arange[0] // brange[1], arange[1] // brange[0], arange[1] // brange[1], arange[0] // brange[0]
            return min(vals), max(vals)
        elif self.op == 'mul':
            vals = arange[0] * brange[0], arange[1] * brange[1], arange[0] * brange[1], arange[1] * brange[0]
            return min(vals), max(vals)
        else:
            assert self.op == 'add'
            return arange[0] + brange[0], arange[1] + brange[1]

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
            elif isinstance(a, Inputs):
                if isinstance(b, int):
                    return int(1 <= b <= 9)
            elif isinstance(b, Inputs):
                if isinstance(a, int):
                    return int(1 <= a <= 9)
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

    def rrange(self, graph: Dict[Ref, TOp]) -> Tuple[int, int]:
        if isinstance(self.a, Op) or isinstance(self.a, NestedOp):
            arange = self.a.rrange(graph)
        else:
            arange = get_range(self.a, graph)

        if isinstance(self.b, Op) or isinstance(self.b, NestedOp):
            brange = self.b.rrange(graph)
        else:
            brange = get_range(self.b, graph)

        if self.op == 'eql':
            if arange[1] < brange[0] or brange[1] < arange[0]:
                return 0, 0
            elif arange[1] == brange[0] == arange[0] == brange[1]:
                return 1, 1
            else:
                return 0, 1
        elif self.op == 'mod':
            return 0, brange[1]
        elif self.op == 'div':
            vals = arange[0] // brange[1], arange[1] // brange[0], arange[1] // brange[1], arange[0] // brange[0]
            return min(vals), max(vals)
        elif self.op == 'mul':
            vals = arange[0] * brange[0], arange[1] * brange[1], arange[0] * brange[1], arange[1] * brange[0]
            return min(vals), max(vals)
        else:
            assert self.op == 'add'
            return arange[0] + brange[0], arange[1] + brange[1]

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
ops_graph: Dict[Ref, Op] = {k: v.eval(compute_graph) for k, v in compute_graph.items() if isinstance(v, Op)}
ops_graph
# %%
# pprint(forward_ref)
# trimmed_graph = {k: v for k, v in compute_graph.items() if (k in forward_ref) or k == final}
# pprint(trimmed_graph)
# print(len(trimmed_graph), len(ops_graph))
# %%
ops_graph[ops_graph[final].a], ops_graph[ops_graph[final].b]

# %%
fixed = {
         Ref('x', 11): 0,
         Ref('x', 17): 0,
         Ref('x', 23): 0,
         Ref('x', 41): 0,
         Ref('x', 53): 0,
         Ref('x', 65): 0,
         Ref('x', 12): 1,
         Ref('x', 18): 1,
         Ref('x', 24): 1,
         Ref('x', 42): 1,
         Ref('x', 54): 1,
         Ref('x', 66): 1,
    #   Ref('x', 72): 0,
    #    Ref('x', 78): 0,
    #     Ref('x', 84): 0,
}
val_graph = ops_graph.copy()
val_graph.update(fixed)
old_len = len(val_graph)
val_graph = {k: v.eval(val_graph) for k, v in val_graph.items() if isinstance(v, Op)}
while old_len != len(val_graph):
    old_len = len(val_graph)
    val_graph = {k: v.eval(val_graph) for k, v in val_graph.items() if isinstance(v, Op)}
    if isinstance(val_graph[final], Ref):
        val_graph[final] = val_graph[val_graph[final]]
    print(len(val_graph), val_graph[final])

# %%
inputs = {
     Inputs(0): 5,
     Inputs(1): 1,
     Inputs(2): 9,
#       Inputs(3): 3,
#  #     Inputs(4): 9,
#  #     Inputs(5): 3,
#       Inputs(6): 9,
#       Inputs(7): 7,
#       Inputs(8): 9,
#       Inputs(9): 8,
# #      Inputs(10): 9,
#  #     Inputs(11): i,
#  #     Inputs(12): i,
#  #    Inputs(13): 9,
}
val_graph = val_graph.copy()
val_graph = {k: v.calc(val_graph, inputs) for k, v in val_graph.items()}
old_len = len(val_graph)
val_graph = {k: v.eval(val_graph) for k, v in val_graph.items() if isinstance(v, Op)}
while old_len != len(val_graph):
    old_len = len(val_graph)
    val_graph = {k: v.eval(val_graph) for k, v in val_graph.items() if isinstance(v, Op)}
    if isinstance(val_graph[final], Ref):
        val_graph[final] = val_graph[val_graph[final]]
    print(len(val_graph), val_graph[final])
print(val_graph[final].rrange(val_graph))


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
    return graph


nested_g = visualize(val_graph)
print(nested_g[final].rrange(nested_g))
print(nested_g[Ref('z', 39)].rrange(nested_g))
# pprint(compute_graph)
# print(compute_graph[('z', step['z'])])
for k, v in nested_g.items():
    a, b = v.rrange(nested_g)
    if a == b:
        nested_g[k] = a
pprint(nested_g)

# %%
# by hand we can find
# 20 -> 21 * 26 - 9 (537) -> 526 * 26 - 12 (13976) ->
# z39 -> z36 ->              z33
# (13976 -6) //26 (537) -> 538 * 26 - 13 -> (13975 -4)//26 ( 537) -> 538 * 26 - 14 -> (13974 -2) //26 (537) ->
#            z30 ->           z27               z24                      z21          z18
# 538 * 26 - 7 -> 13982 * 26 -9 (363523) ->  (363523 -4)//26 (13981) -> (13981 - 5) //26 (537) -> (537 - 17) //26 (20)
#        z15                 z12                    z9                    z6                          y7
# => w0 + 15 <= 20 => w0 <= 5
# try w0 = 5 => w1 <= 1 => w2 <=9 try w2=9 =>
#x84 = 0
range_of_z39 = 12, 20
corresbonding_w13 = 1, 9
# further deduction with forward range bound:


# %%
# if x78 == 0
# range_of_z36 = 26 * range_of_z39[0], 26 * range_of_z39[1]
# add restrition of x
# range_of_z36 = 26 * 9, 26 * 17
# hence
range_of_z36 = 26 * 12, 26 * 17
corresbonding_w12 = 4, 9

# if x78 == 1
# the forward range of z36 is too large

# if x72 == 1
# range_of_z33 = 26 * range_of_z36[0], 26 * range_of_z36[1]
# range_of_z33 = 26 * 12, 26 * 15
corresbonding_w11 = 7, 9
# range of z30 = range_of_z33 - w10 - 5
# range of z30 = (26 * 12 - 14, 26 * 15 - 6) / 26 = 13, 14
# corresbonding w10 = 1, 9
# range of z27 =
