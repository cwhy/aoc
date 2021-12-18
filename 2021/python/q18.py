# Not optimized, because I am tired
import copy
from functools import reduce
from typing import List, Union

test_content1 = """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
"""
test_content2 = """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""

test_content3 = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

with open('2021/input18.txt') as file:
    content = file.read()


def parse(_content):
    return [eval(row) for row in _content.strip().split("\n")]


def reduce_(to_reduce: list, once: bool = False) -> list:
    def get_probe_indices(to_reduce_s: str) -> List[List[int]]:
        numbers = []
        pending_symbols = ""
        prev_is_digit = False
        for c in to_reduce_s:
            if c.isdigit():
                if not prev_is_digit:
                    prev_is_digit = True
                    numbers.append(pending_symbols)
            else:
                prev_is_digit = False
                if c == "]":
                    pending_symbols = "[".join(pending_symbols.split("[")[:-1])
                else:
                    pending_symbols += c

        def get_probe_index(code: str) -> List[int]:
            return list(map(int, "1".join(map(lambda x: "0" * len(x), code.split("[, ")))))

        return list(map(get_probe_index, numbers))

    def get_probe(index: int) -> int:
        indices = probe_indices[index]
        # print(index, indices, end=" -> ")
        to_get = to_reduce
        for i in indices:
            to_get = to_get[i]
        # print(to_get)
        return to_get

    def mutate_probe_(indices: List[int], val: Union[int, List[int]]) -> None:
        to_mutate = to_reduce
        for i in indices[:-1]:
            to_mutate = to_mutate[i]
        to_mutate[indices[-1]] = val

    def inc_probe_(index: int, inc: int) -> None:
        mutate_probe_(probe_indices[index], get_probe(index) + inc)

    def try_split_(i: int) -> bool:
        nonlocal probe_indices
        val = get_probe(i)

        if val >= 10:
            mutate_probe_(probe_indices[i], [val // 2, val - (val // 2)])
            # print("split")
            probe_indices = get_probe_indices(str(to_reduce))
            if chain:
                if not try_explode_(i):
                    try_split_(i)
            return True
        return False

    def try_explode_(i: int) -> bool:
        nonlocal probe_indices
        indices = probe_indices[i]
        if len(indices) >= 5:
            if i <= len(probe_indices) - 2:
                if len(probe_indices[i + 1]) == len(indices):
                    assert probe_indices[i][:-1] == probe_indices[i + 1][:-1]
                    l, r = get_probe(i), get_probe(i + 1)
                    mutate_probe_(probe_indices[i][:-1], 0)
                    in_l = in_r = False
                    if i >= 1:
                        inc_probe_(i - 1, l)
                        in_l = True
                    if i <= len(probe_indices) - 3:
                        inc_probe_(i + 2, r)
                        in_r = True
                    # print("explode")
                    probe_indices = get_probe_indices(str(to_reduce))
                    if chain:
                        if in_l:
                            if not try_explode_(i - 1):
                                try_split_(i - 1)
                        if in_r:
                            if not try_explode_(i + 1):
                                try_split_(i + 1)
                    return True
        return False

    def explode_and_split_() -> bool:
        for i, indices in enumerate(probe_indices):
            if try_explode_(i):
                return True
        else:
            for i, indices in enumerate(probe_indices):
                if try_split_(i):
                    return True
            else:
                return False

    # print("enter, ", to_reduce)
    probe_indices = get_probe_indices(str(to_reduce))
    # print(probe_indices)
    # print("<---------------------")
    # print([get_probe(i) for i in range(len(probe_indices))])
    # print("--------------------->")
    while explode_and_split_():
        # print(to_reduce)
        # print("<---------------------")
        # print([get_probe(i) for i in range(len(probe_indices))])
        # print("--------------------->")
        probe_indices = get_probe_indices(str(to_reduce))
        if once:
            break
    return to_reduce


def red(_content):
    return reduce_(reduce(lambda a, b: reduce_([a, b]), parse(_content)))


chain = False
assert reduce_([[[[[9, 8], 1], 2], 3], 4], True) == [[[[0, 9], 2], 3], 4]
assert reduce_([7, [6, [5, [4, [3, 2]]]]], True) == [7, [6, [5, [7, 0]]]]
assert reduce_([[6, [5, [4, [3, 2]]]], 1], True) == [[6, [5, [7, 0]]], 3]
print(reduce_([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], True))
assert reduce_([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], True) == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
assert reduce_([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], True) == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]

assert reduce_([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
assert reduce_([[[[[1, 1], [2, 2]], [3, 3]], [4, 4]], [5, 5]]) == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
assert red(test_content1) == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]
assert reduce_([parse(test_content2)[0]] + [parse(test_content2)[1]]) == [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]],
                                                                          [[8, [7, 7]], [[7, 9], [5, 0]]]]
assert red(test_content2) == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]],
                              [[[0, 7], [6, 6]], [8, 7]]]

reduce_(reduce(lambda a, b: reduce_([a, b]), parse(content)))


def val(sf_num: list) -> int:
    vals = [val(n) if isinstance(n, list) else n for n in sf_num]
    return vals[0] * 3 + vals[1] * 2


assert val(red(test_content2)) == 3488
assert val(red(test_content3)) == 4140
print("Q1:", val(red(content)))


def max_sum(_content: str) -> int:
    content_list = parse(_content)
    best_pair = None
    max_val = 0
    for a in content_list:
        for b in content_list:
            if a != b:
                final_val = val(reduce_([copy.deepcopy(a), copy.deepcopy(b)]))
                if max_val < final_val:
                    best_pair = a, b
                    max_val = final_val
    print(best_pair)
    return max_val


print(max_sum(test_content3))

print("Q2", max_sum(content))
