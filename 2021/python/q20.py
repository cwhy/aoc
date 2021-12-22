from typing import Tuple, Dict

import numpy as np
import numpy.typing as npt

test_content1 = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


def process_img(_img, code_dict, darkness):
    h, w = _img.shape
    n_pad = 4
    pic_extend = 2
    img_padded = np.pad(_img, ((n_pad, n_pad), (n_pad, n_pad)), 'constant', constant_values=darkness)
    _new_img = np.zeros((h + pic_extend, w + pic_extend), dtype=int) + darkness
    h += pic_extend
    w += pic_extend
    mod_b = n_pad - pic_extend
    mod_e = mod_b + 3
    for i in range(h):
        for j in range(w):
            bin_index = "".join(str(b) for b in img_padded[i + mod_b:i + mod_e, j + mod_b:j + mod_e].reshape(-1))
            _new_img[i, j] = code_dict[bin_index]

    return _new_img


with open('2021/input20.txt') as file:
    content = file.read()


def parse(_content: str) -> Tuple[npt.NDArray, Dict[str, int], bool]:
    __code, __img = _content.strip().split("\n\n")
    _img = np.array([[1 if c == "#" else 0 for c in line.strip()] for line in __img.split("\n")])
    _code = "".join(__code.split("\n")).strip()
    _code_dict = {f"{k:09b}": 1 if v == "#" else 0 for k, v in enumerate(_code)}
    _flip = _code[0] == "#"
    return _img, _code_dict, _flip


def process(_content: str, n: int) -> npt.NDArray:
    img, code_dict, flip = parse(content)

    for i in range(n):
        img = process_img(img, code_dict, i % 2 if flip else 0)
    return img


print(process(content, 2).sum())
print(process(content, 50).sum())
