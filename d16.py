import time
from collections import deque

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

REFLECT = {
    # char: {FROM: [NEW DIR1, NEWDIR2]}
    r".": {UP: [UP], DOWN: [DOWN], RIGHT: [RIGHT], LEFT: [LEFT]},
    r"-": {UP: [LEFT, RIGHT], DOWN: [LEFT, RIGHT], RIGHT: [RIGHT], LEFT: [LEFT]},
    r"|": {UP: [UP], DOWN: [DOWN], RIGHT: [DOWN, UP], LEFT: [DOWN, UP]},
    r"/": {UP: [RIGHT], DOWN: [LEFT], RIGHT: [UP], LEFT: [DOWN]},
    "\\": {UP: [LEFT], DOWN: [RIGHT], RIGHT: [DOWN], LEFT: [UP]}
}


def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        data.append(line)
    return data


def solve(rawinput):
    data = read(rawinput)
    n = len(data)
    m = len(data[0])

    def move(p, direction):
        return p[0] + direction[0], p[1] + direction[1]

    def check(sx, sy, delta, dbg=False):
        q = deque([((sx, sy), delta)])
        visited = set()
        visited.add(q[0])

        while q:
            xy, delta = q.popleft()
            c = data[xy[1]][xy[0]]
            for delta2 in REFLECT[c][delta]:
                xy2 = move(xy, delta2)
                if 0 <= xy2[0] < m and 0 <= xy2[1] < n and (xy2, delta2) not in visited:
                    visited.add((xy2, delta2))
                    q.append((xy2, delta2))

        coords = set(xy for xy, d in visited)
        if dbg:
            for y in range(n):
                print(''.join(
                    "#" if (x, y) in coords else "."
                    for x in range(m))
                )
        return len(coords)

    print("PART1:", check(0, 0, RIGHT))

    part2 = 0
    for y in range(m):
        part2 = max(part2, check(0, y, RIGHT), check(m - 1, y, LEFT))
    for x in range(m):
        part2 = max(part2, check(x, 0, DOWN), check(x, n-1, UP))
    print("part2 best", part2)


CASES = [
    r""".|...\....
    |.-.\.....
    .....|-...
    ........|.
    ..........
    .........\
    ..../.\\..
    .-.-/..|..
    .|....-|.\
    ..//.|....""",
    open("16.txt", "r").read()
]
for raw in CASES:
    tstart = time.time()
    solve(raw)
    print(f"Time={time.time() - tstart:.2f}s")
