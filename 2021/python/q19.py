import operator
from collections import defaultdict, Counter
from pprint import pprint
from typing import List, Tuple, Callable, Dict, Set, Any

import numpy as np
import numpy.typing as npt
from numpy import ndarray, dtype
from numpy.typing._generic_alias import ScalarType

test_content1 = """
--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1
"""

test_content2 = """

--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8
"""

test_content3 = """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""

with open('2021/input19.txt') as file:
    content = file.read()


Data = List[Tuple[int, int, int]]
def parse(_content) -> List[Tuple[int, Data]]:
    _scanner_datas = _content.strip().split('\n\n')
    scanner_content = []
    for scanner_data_raw in _scanner_datas:
        scanner_lines = scanner_data_raw.split('\n')
        scanner_n = int(scanner_lines[0].split(' ')[2])
        scanner_data = [tuple(int(i) for i in l.split(",")) for l in scanner_lines[1:]]
        scanner_content.append((scanner_n, scanner_data))
    return scanner_content


def find_dist(data):
    data_t = data.reshape(data.shape[0], 1, data.shape[1])
    return np.einsum('ijk, ijk->ij', data - data_t, data - data_t)


def process_scanner_all(scanner_data):
    scanner_no, raw_data = scanner_data
    n_data = len(raw_data)
    dist_matrix = find_dist(np.array(raw_data))
    la, lb = np.array(np.triu_indices(n_data, k=1))
    dist_dict = {
        dist_matrix[a, b]: (a, b) for a, b in zip(la, lb)
    }
    index_dict = defaultdict(set)
    for k, (a, b) in dist_dict.items():
        index_dict[a].add(k)
    return scanner_no, dist_dict, index_dict




def process_scanner(raw_data: Data) -> Dict[int, Set[int]]:
    dist_matrix = find_dist(np.array(raw_data))
    la, lb = np.array(np.triu_indices(len(raw_data), k=1))
    index_dict = defaultdict(set)
    for a, b in zip(la, lb):
        index_dict[a].add(dist_matrix[a, b])
    return index_dict


def get_overlap(data1: Data, data2: Data) -> List[Tuple[Tuple[int, int], int]]:
    result1 = process_scanner(data1)
    result2 = process_scanner(data2)

    overlap = {}
    for k, v in result1.items():
        for k2, v2 in result2.items():
            overlap_len = len(v & v2)
            if overlap_len > 0:
                overlap[(k, k2)] = overlap_len
    return Counter(overlap).most_common(3)


def get_transpose_fn(_data_all: Data,
                     _data_new: Data,
                     overlap3: List[Tuple[Tuple[int, int], int]]) -> Callable[[Data], Data]:
    apa = np.array([_data_all[a] for (a, _), _ in overlap3])
    bpa = np.array([_data_new[b] for (_, b), _ in overlap3])
    assert np.equal(find_dist(apa), find_dist(bpa)).all()
    diffs = np.stack([apa - np.roll(bpa, s, axis=1) for s in range(3)])
    sums = np.stack([apa + np.roll(bpa, s, axis=1) for s in range(3)])
    # print("apa: \n", apa)
    # print("bpa: \n", bpa)
    ops = {}
    for shift, idx in zip(*np.where(np.std(diffs, axis=1) == 0)):
        val = int(np.mean(diffs, axis=1)[shift, idx])
        ops[idx] = (val, (idx - shift) % 3, 1)

    for shift, idx in zip(*np.where(np.std(sums, axis=1) == 0)):
        val = int(np.mean(sums, axis=1)[shift, idx])
        ops[idx] = (-val, (idx - shift) % 3, -1)

    # print(ops)
    def apply_ops_arr(data_arr: npt.NDArray) -> npt.NDArray:
        return np.stack([ops[i][-1] * (ops[i][0] + data_arr[:, ops[i][1]]) for i in range(3)]).T

    assert (apply_ops_arr(bpa) == apa).all()

    def _apply_ops(data: Data) -> Data:
        return list(map(tuple, apply_ops_arr(np.array(data))))

    # print(np.array(apply_ops(bpa)))

    return _apply_ops


def score_overlap(overlap3) -> int:
    if not overlap3:
        return 0
    else:
        return overlap3[-1][-1]


scanner_datas = parse(content)
all_data_ = scanner_datas.pop(0)[-1]
origins = {}
while scanner_datas:
    overlaps = [get_overlap(all_data_, scanner_data[-1]) for scanner_data in scanner_datas]
    if len(scanner_datas) > 1:
        max_val = 0
        next_scanner_i = 0
        for i in range(len(scanner_datas)):
            if score_overlap(overlaps[i]) > max_val:
                next_scanner_i = i
                max_val = score_overlap(overlaps[i])
        print("score:", max_val)
    else:
        next_scanner_i = 0
    scanner_n, new_data_ = scanner_datas.pop(next_scanner_i)
    apply_ops = get_transpose_fn(all_data_, new_data_, overlaps[next_scanner_i])
    origins[scanner_n] = apply_ops([(0, 0, 0)])[0]
    all_data_ = list(set(apply_ops(new_data_)) | set(all_data_))

    print(len(all_data_))

# %%
print(origins)
max_dist = 0
for i in origins.values():
    for j in origins.values():
        max_dist = max(max_dist, abs(i[0] - j[0]) + abs(i[1] - j[1]) + abs(i[2] - j[2]))
    max_dist = max(max_dist, abs(i[0]) + abs(i[1]) + abs(i[2]))
max_dist
