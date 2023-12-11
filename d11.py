import bisect
EXPAND = 1


def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        data.append(list('X' if c == '#' else '.' for c in line))
    return data[::-1]


def expand(data):
    expandsx = []
    expandsy = []
    newdata = []
    for y, row in enumerate(data):
        newdata.append(row)
        if all(c != 'X' for c in row):
            expandsy.append(y)

    j = 0
    while j < len(data[0]):
        if all(row[j] != 'X' for row in data):
            expandsx.append(j)
        j += 1
    return newdata, expandsx, expandsy


def draw(data):
    for row in data[::-1]:
        print(''.join(row))


def solve(rawinput):
    data = read(rawinput)
    data, expandx, expandy = expand(data)
    if len(data) < 1000:
        draw(data)

    # Find galaxies
    n = len(data)
    m = len(data[0])
    galaxies = []
    for y in range(n):
        for x in range(m):
            if data[y][x] == "X":
                galaxies.append((y, x))

    g = len(galaxies)

    def dist(a, b):
        gy, gx = galaxies[a]
        gy2, gx2 = galaxies[b]
        d = abs(gy-gy2) + abs(gx - gx2)

        y0 = min(gy, gy2)
        y1 = max(gy, gy2)
        x0 = min(gx, gx2)
        x1 = max(gx, gx2)

        ey1 = bisect.bisect_left(expandy, y0)
        ey2 = bisect.bisect_left(expandy, y1)
        d += (EXPAND-1)*(ey2-ey1)
        ex1 = bisect.bisect_left(expandx, x0)
        ex2 = bisect.bisect_left(expandx, x1)
        d += (EXPAND - 1) * (ex2 - ex1)
        return d

    print("Num Galaxies = ", g)
    print("Expansions", expandx, expandy)
    ans = 0
    for i in range(g-1):
        for j in range(i+1, g):
            distance = dist(i, j)
            ans += distance
    print("Part1", ans)


CASES = [
    """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""",
    open("11.txt", "r").read()  # 6806
]
for raw in CASES:
    print("=" * 100)
    EXPAND = 2
    solve(raw)

    EXPAND = 1000000
    solve(raw)
