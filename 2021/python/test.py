with open('../input4.txt') as f:
    k = f.readlines()
r = k[0].strip().split(",")
nblocks = (len(k) - 1)//6
pre_blocks = [k[1:][i*6: 6+i*6] for i in range(nblocks)]
blocks = [[s.strip().split() for s in b[1:]] for b in pre_blocks]
blocks_check = [b + list(map(list, zip(*b))) for b in blocks]

block_n = [[0]*10 for _ in range(nblocks)]

break_flag = False
records = []
bingo = [False] * nblocks
nbingo = 0
ss = sum(int(ch) for ch in sum(blocks[40],[]))
while not break_flag:
    new = r.pop(0)
    print("new", new)
    records.append(new)
    for i, b in enumerate(blocks_check):
        if not bingo[i]:
            done = False
            for j, c in enumerate(b):
                if new in c:
                    block_n[i][j] += 1
                    if i == 40 and not done:
                        ss -= int(new)
                        print("ss: ", ss)
                        done = True
                    if block_n[i][j] == 5:
                        bingo[i] = True
                        nbingo += 1
                        if nbingo == 100:
                            print(i, j)
                            break_flag = True
                        break
        if break_flag:
            break

k = sum(blocks[i],[])
final = sum(int(ch) for ch in list(filter(lambda x: x not in records, k)))
finalb = sum(int(ch) for ch in k)
print(new, final, i, finalb)
print(final*int(new))


