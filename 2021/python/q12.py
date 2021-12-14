from collections import defaultdict

content = """
he-JK
wy-KY
pc-XC
vt-wy
LJ-vt
wy-end
wy-JK
end-LJ
start-he
JK-end
pc-wy
LJ-pc
at-pc
xf-XC
XC-he
pc-JK
vt-XC
at-he
pc-he
start-at
start-XC
at-LJ
vt-JK
"""

"""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

graph = defaultdict(list)

for s in content.strip().split("\n"):
    a, b = s.strip().split("-")
    graph[a].append(b)
    graph[b].append(a)
print(graph)

#%%
stack = [('start', ['start'])]
paths = []
while stack:
    node, path = stack.pop()
    if node == 'end':
        paths.append(path)
        continue
    for n in graph[node]:
        if n not in path or n.isupper():
            stack.append((n, path + [n]))
print(len(paths))

#%%
paths = set()
for fav_node in graph.keys():
    if fav_node not in ['start', 'end'] and fav_node.islower():
        stack = [('start', ('start',))]
        while stack:
            node, path = stack.pop()
            if node == 'end':
                paths.add(path)
                continue
            for n in graph[node]:
                if n not in path or n.isupper() or (
                        n == fav_node and sum(1 if n == fav_node else 0 for n in path) <= 1):
                    stack.append((n, tuple(list(path) + [n])))
print(len(paths))

