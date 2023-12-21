import numpy as np
from collections import deque, defaultdict


def read(rawinput):
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue

        yield line


def neighbors(p: complex):
    return (
        p + 1,
        p - 1,
        p + 1j,
        p - 1j
    )


def draw(n, m, rocks, positions):
    for y in range(n):
        line = []
        for x in range(m):
            p = complex(x, y)
            c = '.'
            if p in rocks:
                c = "#"
            elif p in positions:
                c = "O"
            line.append(c)
        print(''.join(line))


def solve_part1(steps, rawinput, overr_start=None):
    rawmap = list(read(rawinput))
    n = len(rawmap)
    m = len(rawmap[0])

    # coords complx
    rocks = set()
    start = None
    for y in range(n):
        for x in range(m):
            p = complex(x, y)
            c = rawmap[y][x]
            if c == "S":
                start = p
            elif c == "#":
                rocks.add(p)
    if overr_start is not None:  # Override start point (used for debugging)
        start = overr_start

    positions = {start}
    for _ in range(steps):
        positions2 = set()
        for p in positions:
            for pn in neighbors(p):
                if 0 <= pn.imag < n and 0 <= pn.real < m and pn not in rocks:
                    positions2.add(pn)
        positions = positions2
    print("PART 1", len(positions))


def solve_infinite_logged(steps, rawinput, output_path):
    """ Very slow method, but will be used to generate a history of (k, numplots) visited after each step """
    rawmap = list(read(rawinput))
    n = len(rawmap)
    m = len(rawmap[0])

    # coords complx
    rocks = set()
    start = None
    for y in range(n):
        for x in range(m):
            p = complex(x, y)
            c = rawmap[y][x]
            if c == "S":
                start = p
            elif c == "#":
                rocks.add(p)

    f = open(output_path, "w")
    positions = {start}
    for k in range(steps):
        positions2 = set()
        for p in positions:
            for pn in neighbors(p):
                pnr = complex(pn.real % m, pn.imag % n)
                if pnr not in rocks:
                    positions2.add(pn)
        positions = positions2
        print(f"{(k + 1)},{len(positions)}")
        f.write(f"{(k + 1)},{len(positions)}\n")
    print("Part2 Bruteforce", len(positions))
    f.flush()
    f.close()


def quickfind(steps, rawinput, overr_start=None):
    """ Fast (2s) to compute until ~10000 steps
    Useful to quickly check expected amount of garden plots reached at exactly K steps.
    NOT GOOD to generate a history of (k, numplots), which will be used to extrapolate.

    It's a fail attempt to solve the problem because it's still too slow.
    Turned out to be useful once I had it to validate, but not worth the time spent for this
    """
    rawmap = list(read(rawinput))
    n = len(rawmap)
    m = len(rawmap[0])

    # coords complx
    rocks = set()
    start = None
    for y in range(n):
        for x in range(m):
            p = complex(x, y)
            c = rawmap[y][x]
            if c == "S":
                start = p
            elif c == "#":
                rocks.add(p)

    mem = {}
    if overr_start is not None:
        start = overr_start

    invasion_ids = {}

    def get_invasion_id(invasions):
        key = tuple(invasions)
        if key in invasion_ids:
            return invasion_ids[key]
        invasion_ids[key] = iid = len(invasion_ids)
        return iid

    def boundedsteps(binvasion: list[tuple[int, complex]], numsteps):
        if numsteps <= 0:
            if len(binvasion) > 0:
                positions = {pin for kstart, pin in binvasion if kstart == 0}
                return len(positions), {}, 0
            return 0, set(), 0
        key = get_invasion_id(binvasion)
        if key not in mem or numsteps < mem[key][2]:
            positions = {pin for kstart, pin in binvasion if kstart == 0}
            nextpositions = set()
            q = set().union(positions)
            nextq = set()
            oob = set()  # out of bounds (invading neighbor tile)
            k = 0
            filled = False
            i = len(positions)
            for k in range(1, numsteps + 1):
                while i < len(binvasion) and k >= binvasion[i][0]:
                    pin = binvasion[i][1]
                    if pin not in nextpositions:
                        nextpositions.add(pin)
                        nextq.add(pin)
                    i += 1
                if not q and i == len(binvasion):
                    filled = True
                    break
                for p in q:
                    for pn in neighbors(p):
                        if not (0 <= pn.imag < n and 0 <= pn.real < m):
                            # out of bounds
                            oob.add((k, pn))
                            continue
                        if pn not in rocks and pn not in nextpositions:
                            nextpositions.add(pn)
                            nextq.add(pn)
                q.clear()
                positions, nextpositions = nextpositions, positions
                q, nextq = nextq, q
            neighbortiles = defaultdict(list)
            for kk, p2 in sorted(oob, key=lambda o: (o[0], o[1].real, o[1].imag)):
                # at step K new tile starts at pos p2 (%n %m)
                tx2 = int(p2.real // m)
                ty2 = int(p2.imag // n)
                nt = neighbortiles[(tx2, ty2)]
                if nt and abs(nt[-1][1] - p2) == (kk - nt[-1][0]):
                    continue
                nt.append((kk, p2))

            steps_left = numsteps - k
            if filled and steps_left > 0:
                mem[key] = [(len(nextpositions), len(positions)), neighbortiles, k]
            else:
                return len(positions), neighbortiles, k

        ss, o, k = mem[key]
        return ss[(numsteps + k) % 2], o, numsteps

    print(f"{m=} {n=}")
    result = 0
    start_invasions = [(0, start)]
    tiles_visited = {(0, 0): None}
    qtiles = deque([(0, 0, start_invasions)])
    while qtiles:
        tx, ty, invasions = qtiles.popleft()
        if tiles_visited.get((tx, ty)) is not None:
            continue

        step_start = invasions[0][0]
        invasions_bounded = [(k - step_start, complex(p.real % m, p.imag % n)) for k, p in invasions]
        tiles_visited[(tx, ty)] = get_invasion_id(invasions_bounded)
        reach, oob, stepstofill = boundedsteps(invasions_bounded, steps - step_start)

        for (tx2, ty2), invasions2 in oob.items():
            tx2 += tx
            ty2 += ty
            if (tx2, ty2) not in tiles_visited:
                invasions2 = [(k + step_start, p) for k, p in invasions2]
                tiles_visited[tx2, ty2] = None
                qtiles.append((tx2, ty2, invasions2))
        result += reach
    print("Part2 (fast for <15k steps): ", result)


D21_INPUT = open("scratch.txt", "r").read()

# PART 1
part1sample = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
solve_part1(6, part1sample)
solve_part1(64, D21_INPUT)

# part 2
logpath = "logs_part2.csv"
# solve_infinite_logged(200, D21_INPUT, logpath)  # Takes a couple minutes

rawlogs = open(logpath, "r").read()
logs = [(0, 1)] + [(int(x.split(",")[0]), int(x.split(",")[1])) for x in rawlogs.split()]

times = []
values = []
for k in range(131, len(logs)):
    if k % 131 == 65:
        times.append(k)
        assert logs[k][0] == k
        values.append(logs[k][1])

# Numpy model
model = np.poly1d(np.polyfit(times, values, 2))
# Or, using https://www.dcode.fr/lagrange-interpolating-polynomial to find the formula instead, then manually edit flagrange lambda:
# Each constant of the equation corresponds to model[0], model[1] and model[2]
# In my case, it turned out to be more accurate that np.polyfit (and produced the correct result)
flagrange = lambda x: (14483*x*x)/17161 + 30203*x/17161 + 32932/17161
print("Part2: numpy approx =", float(model([26501365])))
print("Part2:     lagrange =", flagrange(26501365))

print("Factors:::")
print("numpy model", list(model))
print("lagrange", 14483/17161, 30203/17161, 32932/17161)
