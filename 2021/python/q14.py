from collections import Counter, defaultdict

content = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

with open('2021/input14.txt') as file:
    content = file.read()

head, tail = content.strip().split("\n\n")
base = head
tail_gen = [line.split(' -> ') for line in tail.split("\n")]
parse_table = {k: v for k, v in tail_gen}
process_table = {k: f"{k[0]}{v}" for k, v in tail_gen}

# %%

end = base[-1]
new = base
for i in range(10):
    new = "".join(process_table[a + b] for a, b in zip(new[:-1], new[1:])) + end
    ranked = Counter(new).most_common()
    print(ranked)
    print(ranked[0][1] - ranked[-1][1])

# %%
count_go = {k: (f"{k[0]}{v}", f"{v}{k[1]}") for k, v in tail_gen}

counts = Counter(f"{a}{b}" for a, b in zip(base[:-1], base[1:]))
old_counts = counts

letter_counter = Counter(base)
for i in range(40):
    new_counts = defaultdict(int)
    print(old_counts)
    for k, v in old_counts.items():
        a, b = count_go[k]
        new_counts[a] += v
        new_counts[b] += v
        letter_counter.update({a[1]: v})
    old_counts = new_counts
    ranked = letter_counter.most_common()
    print(ranked)
    print(ranked[0][1] - ranked[-1][1])
