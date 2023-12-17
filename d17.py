import heapq
import math
import time
from collections import defaultdict

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

MOVES = {
    UP: [UP, RIGHT, LEFT],
    DOWN: [DOWN, RIGHT, LEFT],
    RIGHT: [DOWN, RIGHT, UP],
    LEFT: [DOWN, LEFT, UP],
}


def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        data.append([int(x) for x in line])
    return data


def solve(rawinput):
    data = read(rawinput)
    n = len(data)
    m = len(data[0])

    def move(p, direction):
        return p[0] + direction[0], p[1] + direction[1]

    def find(start, end, maxk, mink=0):
        q = []
        visited = defaultdict(lambda: math.inf)
        prev = {}
        for delta in (RIGHT, DOWN):
            q.append((0, start, delta, 0))
            visited[(start, delta, 0)] = 0

        heapq.heapify(q)
        while q:
            cost, xy, delta, k = heapq.heappop(q)
            if xy == end and mink <= k <= maxk:
                return cost
            vkey = (xy, delta, k)
            if cost > visited[vkey]:
                continue

            for delta2 in MOVES[delta]:
                if delta2 == delta:
                    k2 = k + 1
                    if k2 > maxk:
                        continue
                elif k < mink:
                    continue
                else:
                    k2 = 1
                xy2 = move(xy, delta2)
                if 0 <= xy2[0] < m and 0 <= xy2[1] < n:
                    cost2 = cost + data[xy2[1]][xy2[0]]
                    vkey2 = (xy2, delta2, k2)
                    if cost2 < visited.get(vkey2, math.inf):
                        visited[vkey2] = cost2
                        prev[xy2] = xy
                        heapq.heappush(q, (cost2, xy2, delta2, k2))
        return -1
    print("PART1:", find((0, 0), (m-1, n-1), maxk=3))
    print("PART2:", find((0, 0), (m - 1, n - 1), mink=4, maxk=10))


CASES = [
    r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""",
    """111111111111
999999999991
999999999991
999999999991
999999999991""",
    open("17.txt", "r").read()
]
for raw in CASES:
    tstart = time.time()
    solve(raw)
    print(f"Time={time.time() - tstart:.2f}s")
