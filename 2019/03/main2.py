from typing import List, Dict, Tuple


with open("input.txt") as f:
    wire1 = [l.strip() for l in f.readline().split(",")]
    wire2 = [l.strip() for l in f.readline().split(",")]


def walkwire(wire: List[str],
             path_store: Dict[Tuple[int, int], int],
             first: bool) -> List[Tuple[int, int]]:
    coord = (0, 0)
    if not first:
        overlaps = []
    walk_dist = 0

    for item in wire:
        direction = item[0]
        dist = int(item[1:])

        def move(_coord, move1):
            nonlocal walk_dist
            for _ in range(dist):
                _coord = move1(_coord)
                walk_dist += 1
                if first:
                    path_store[_coord] = walk_dist
                else:
                    if _coord in path_store:
                        min_walk_dist = walk_dist + path_store[_coord]
                        overlaps.append(min_walk_dist)
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


path_store_ = dict()
out = walkwire(wire1, path_store_, True)
print(out)
overlaps_ = walkwire(wire2, path_store_, False)
print(overlaps_)
minwd = min(z for z in overlaps_)
print(minwd)
