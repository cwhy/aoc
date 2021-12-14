from __future__ import annotations

from collections import defaultdict
from typing import Optional, Union


content = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
with open('2021/input10.txt') as file:
    content = file.read()

lines = content.strip().split('\n')

match = {
    '{': '}',
    '[': ']',
    '(': ')',
    '<': '>'
}


def parse_line(line: str) -> dict[str, int]:
    stack = []
    wrongs = defaultdict(int)
    for c in line:
        if c in '({[<':
            stack.append(c)
        else:
            to_match = stack.pop()
            if c != match[to_match]:
                wrongs[c] += 1
    return wrongs


def parse_line1(line: str) -> Union[str, list[str]]:
    stack = []
    for c in line:
        if c in '({[<':
            stack.append(c)
        else:
            to_match = stack.pop()
            if c != match[to_match]:
                return c
    else:
        stack.reverse()
        return stack


correction_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
complete_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


wrongs = defaultdict(int)
scores = []
for line in lines:
    c = parse_line1(line)
    if isinstance(c, str):
        wrongs[c] += 1
    else:
        assert isinstance(c, list)
        score = 0
        for i in c:
            score = score*5 + complete_points[match[i]]
        scores.append(score)


result1 = sum(correction_points[c] * wrongs[c] for c in wrongs)
print(result1)
print(scores)
scores.sort()
print(scores[(len(scores)-1)//2])

