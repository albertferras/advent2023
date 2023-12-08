import math
from itertools import cycle


def read(rawinput):
    lines = rawinput.split("\n")
    instructions = lines[0]
    graph = {}
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        current, paths = line.split(" = ")
        left, right = paths[1:-1].split(", ")
        graph[current] = {"L": left, "R": right}
    return instructions, graph


def solve(rawinput):
    instructions, graph = read(rawinput)
    steps = 0
    current = "AAA"
    if current not in graph:
        return
    for instruction in cycle(instructions):
        steps += 1
        current = graph[current][instruction]
        if current == "ZZZ":
            break
    print(f"{steps=}")


def solve2(rawinput):
    instructions, graph = read(rawinput)
    n = len(instructions)
    current = [node for node in graph.keys() if node.endswith("A")]

    def steps2Z(node, i):
        node = graph[node][instructions[i]]
        i = (i + 1) % n
        steps = 1
        while not node.endswith("Z"):
            node = graph[node][instructions[i]]
            i = (i + 1) % n
            steps += 1
        return steps, node

    start = [(node, steps2Z(node, 0)) for node in current]
    loopsteps = []
    for origin, (steps, node) in start:
        nextsteps, newnode = steps2Z(node, steps % n)
        print(f"{origin=} -> {node} ({steps}) -> {newnode} ({nextsteps})")
        loopsteps.append(nextsteps)
    print(math.lcm(*loopsteps))


CASES = [
        """RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)""",
        """LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)""",
    """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""",  # 6
    open("8.txt", "r").read()
]
for rawinput in CASES:
    print("-----------------")
    print(f"CASE {rawinput[:50]}...")
    solve(rawinput)
    solve2(rawinput)
