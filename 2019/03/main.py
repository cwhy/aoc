from typing import List, Set, Tuple


with open("input.txt") as f:
    wire1 = [l.strip() for l in f.readline().split(",")]
    wire2 = [l.strip() for l in f.readline().split(",")]


def walkwire(wire: List[str],
             path_store: Set[Tuple[int, int]],
             first: bool) -> List[Tuple[int, int]]:
    coord = (0, 0)
    if not first:
        overlaps = []

    for item in wire:
        direction = item[0]
        dist = int(item[1:])

        def move(_coord, move1):
            for _ in range(dist):
                _coord = move1(_coord)
                if first:
                    path_store.add(_coord)
                else:
                    if _coord in path_store:
                        overlaps.append(_coord)
            return _coord

        if direction == "R":
            coord = move(coord, lambda c: (c[0] + 1, c[1]))
        elif direction == "L":
            coord = move(coord, lambda c: (c[0] - 1, c[1]))
        elif direction == "U":
            coord = move(coord, lambda c: (c[0], c[1] + 1))
        elif direction == "D":
            coord = move(coord, lambda c: (c[0], c[1] - 1))
        else:
            raise NotImplementedError("UDRL!")
    if not first:
        return overlaps


path_store_ = set()
out = walkwire(wire1, path_store_, True)
print(out)
overlaps_ = walkwire(wire2, path_store_, False)
minman = min(abs(z[0]) + abs(z[1]) for z in overlaps_)
print(minman)
