from_ = 372304
to_ = 847060


def req1(x):
    s = str(x)
    return any(a == b for a, b in zip(s[:-1], s[1:]))


def req2(x):
    s = str(x)
    return all(a <= b for a, b in zip(s[:-1], s[1:]))


def req3(x):
    s = str(x)
    oldc = s[0]
    count = 1
    for c in s[1:]:
        if c == oldc:
            count += 1
        else:
            if count == 2:
                return True
            else:
                count = 1
        oldc = c

    else:
        return count == 2


pws = []
for i in range(from_, to_ + 1):
    if req1(i):
        if req2(i):
            pws.append(i)

print(len(pws))

pws = []
for i in range(from_, to_ + 1):
    if req2(i):
        if req3(i):
            pws.append(i)

print(len(pws))
print(pws)
