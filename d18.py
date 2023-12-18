import math
from collections import defaultdict
from progressbar import progressbar

MOVES = {
    "U": (0, -1),
    "D": (0, 1),
    "R": (1, 0),
    "L": (-1, 0)
}


def read(rawinput, newencoding=False):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        m, x, color = line.split()
        if not newencoding:
            yield m, int(x)
        if newencoding:
            hex = color[2:-1]
            dist = int(hex[:5], 16)
            m = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[hex[5]]
            print(m, dist)
            yield m, dist
    return data


def solve(rawinput, newencoding=False):
    xlist = defaultdict(list)

    x = y = 0
    for m, k in read(rawinput, newencoding=newencoding):
        delta = MOVES[m]
        if m in "RL":
            x0 = x
            y0 = y
            x = x0 + delta[0] * k
            y = y0 + delta[1] * k
            if x < x0:
                xlist[y].append((x, x0))
            else:
                xlist[y].append((x0, x))
        else:
            for _ in range(k):
                x += delta[0]
                y += delta[1]
                xlist[y].append((x, x))
    print("VISITED generated")
    for y, xs in progressbar(xlist.items()):
        newx = []
        xs.sort()
        n = len(xs)
        for i in range(n):
            if xs[i][0] == xs[i][1]:
                if i - 1 >= 0 and xs[i - 1][1] == xs[i][0]:
                    continue
                if i + 1 < n and xs[i][1] == xs[i + 1][0]:
                    continue
            newx.append(xs[i])
        xs[:] = newx
    print("XS generated")

    def ud(x, y):
        u = any(a <= x <= b for (a, b) in xlist[y - 1])
        d = any(a <= x <= b for (a, b) in xlist[y + 1])
        if u and d:
            return "UD"
        elif u:
            return "U"
        elif d:
            return "D"
        return "-"

    print("counting...")
    ans = 0
    for y, xs in progressbar(sorted(xlist.items())):
        # print(f"--------{y=}----- {xs}")
        n = len(xs)
        inside = False
        rans = 0
        prev = -math.inf
        i = 0
        while i < n:
            x0, x = xs[i]
            udstart = ud(x0, y)
            if x0 == x:
                udend = udstart
            else:
                udend = ud(x, y)

            k = x - x0
            rans += k+1
            if inside:
                fill = x0 - (prev + 1)
                # print(f"+{fill} fill {prev} to {x}")
                rans += fill

            if udstart == "UD" or f"{udstart}:{udend}" in ("D:U", "U:D"):
                inside = not inside
                # print(f"FLIP {x0}({udstart}) to {x}({udend}): {'INSIDE' if inside else 'OUT'}")
            i += 1
            prev = x
        # print("sum=+", rans)
        ans += rans

    print("SOL", ans)


CASES = [
    """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""",
    open("18.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve(raw, newencoding=False)
    solve(raw, newencoding=True)
