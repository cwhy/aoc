from __future__ import annotations

from functools import reduce
from operator import mul
from typing import NamedTuple, Union, Tuple, List, Literal, Dict

to_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}
reversed_binary = {v: k for k, v in to_binary.items()}

Ops = Literal['+', '*', 'min', 'max', '`', '>', '<', '=']

ops_table: Dict[str, Ops] = {f"{k:03b}": v for k, v in {
    0: "+",
    1: "*",
    2: "min",
    3: "max",
    4: "`",
    5: ">",
    6: "<",
    7: "="
}.items()}


# %%

class Result(NamedTuple):
    version: int
    ops: Ops
    content: Union[List[Result], int]
    rest: str


list_ops = {
    '+': sum,
    '*': lambda l: reduce(mul, l),
    'min': min,
    'max': max
}


def eval_res(packet: Result) -> int:
    if packet.ops == "`":
        return packet.content
    elif packet.ops in "=":
        return int(eval_res(packet.content[0]) == eval_res(packet.content[1]))
    elif packet.ops == ">":
        return int(eval_res(packet.content[0]) > eval_res(packet.content[1]))
    elif packet.ops == "<":
        return int(eval_res(packet.content[0]) < eval_res(packet.content[1]))
    else:
        assert packet.ops in ("*", "+", "min", "max")
        return list_ops[packet.ops]([eval_res(x) for x in packet.content])


def read_packet(b) -> Result:
    version = int(b[:3], 2)
    op = ops_table[b[3:6]]
    rest = b[6:]
    if op == "`":
        s = ""
        while True:
            char, rest = rest[:5], rest[5:]
            s += char[1:]
            if char[0] == '0':
                break
        return Result(version, op, int(s, 2), rest)
    else:
        type_id, rest = rest[0], rest[1:]
        if type_id == "0":
            len_packets = int(rest[:15], 2)
            inside = rest[15:15 + len_packets]
            contents = []
            while inside:
                packet_res = read_packet(inside)
                contents.append(packet_res)
                inside = packet_res.rest
            return Result(version, op, contents, rest[15 + len_packets:])
        else:
            n_packets = int(rest[:11], 2)
            rest = rest[11:]
            contents = []
            while n_packets > 0:
                packet_res = read_packet(rest)
                contents.append(packet_res)
                rest = packet_res.rest
                n_packets -= 1
            return Result(version, op, contents, rest)


def test(_content, _expected):
    binary = _content.translate(str.maketrans(to_binary))
    print(read_packet(binary))

    assert read_packet(binary) == _expected


test("D2FE28",
     Result(version=6, ops="`", content=2021, rest='000'))

test("38006F45291200",
     Result(version=1, ops='<', content=[
         Result(version=6, ops='`', content=10, rest='0101001000100100'),
         Result(version=2, ops='`', content=20, rest='')], rest='0000000'))

test("EE00D40C823060", Result(version=7, ops='max', content=[
    Result(version=2, ops='`', content=1, rest='100100000100011000001100000'),
    Result(version=4, ops='`', content=2, rest='0011000001100000'),
    Result(version=1, ops='`', content=3, rest='00000')], rest='00000'))

test("8A004A801A8002F478", Result(version=4, ops='min', content=[
    Result(version=1, ops='min', content=[
        Result(version=5, ops='min', content=[
            Result(version=6, ops='`', content=15, rest='')], rest='000')], rest='000')], rest='000'))


def version_sum(packet: Result) -> int:
    if isinstance(packet.content, list):
        return packet.version + sum(version_sum(p) for p in packet.content)
    else:
        return packet.version


def get_v_sum(_content: str) -> int:
    binary = _content.translate(str.maketrans(to_binary))
    return version_sum(read_packet(binary))


def get_eval(_content: str) -> int:
    binary = _content.translate(str.maketrans(to_binary))
    return eval_res(read_packet(binary))


assert get_v_sum("8A004A801A8002F478") == 16
assert get_v_sum("620080001611562C8802118E34") == 12
assert get_v_sum("C0015000016115A2E0802F182340") == 23
assert get_v_sum("A0016C880162017C3686B18A3D4780") == 31
assert get_eval("C200B40A82") == 3
assert get_eval("04005AC33890") == 54
assert get_eval("880086C3E88112") == 7
assert get_eval("CE00C43D881120") == 9
assert get_eval("D8005AC2A8F0") == 1
assert get_eval("F600BC2D8F") == 0
assert get_eval("9C005AC2F8F0") == 0
assert get_eval("9C0141080250320F1802104A08") == 1

with open('2021/input16.txt') as file:
    content = file.read()
print(get_v_sum(content))
print(get_eval(content))
