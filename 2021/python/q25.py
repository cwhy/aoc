test_contents = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""

with open('2021/input25.txt') as file:
    contents = file.read()

rows = [row.strip() for row in contents.strip().split('\n')]
h, w = len(rows), len(rows[0])


def from_south(i, j):
    return (i - 1) % h, j


def from_east(i, j):
    return i, (j - 1) % w


def move_(spaces, all_pts_in_dir, fn):
    new = set()
    old = set()
    for i, j in spaces:
        old_pt = fn(i, j)
        if old_pt in all_pts_in_dir:
            new.add((i, j))
            old.add(old_pt)

    all_pts_in_dir -= old
    all_pts_in_dir |= new
    spaces |= old
    spaces -= new
    mob = len(new)
    return mob



def visualize_(s, e):
    for i in range(h):
        for j in range(w):
            print("|", end="")
            if (i, j) in s:
                print('v', end='')
            elif (i, j) in e:
                print('>', end='')
            else:
                print('.', end='')
        print()
    print()


# visualize_(souths, easts)
# move_(dots, easts, from_east)
# visualize_(souths, easts)
# move_(dots, souths, from_south)
# visualize_(souths, easts)

#%%
def calc(rows):
    dots = set()
    easts = set()
    souths = set()
    for i, row in enumerate(rows):
        for j, e in enumerate(row):
            if e == 'v':
                souths.add((i, j))
            elif e == '>':
                easts.add((i, j))
            else:
                assert e == '.'
                dots.add((i, j))

    i = 1
    while True:
        mobe = move_(dots, easts, from_east)
        mobs = move_(dots, souths, from_south)
        mob = mobs + mobe
        if mob == 0:
            break
        i += 1
    return i
print(calc(rows))