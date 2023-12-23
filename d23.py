import heapq
from collections import defaultdict, deque
from functools import cache


def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        yield line
    return data


MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(rawinput, sx=1, sy=0, endx=-2, endy=-1):
    mat = list(read(rawinput))
    n = len(mat)
    m = len(mat[0])
    endx = m + endx
    endy = n + endy

    q = []
    dist = defaultdict(int)
    q.append((0, sx, sy, -1, -1))
    dist[(sx, sy)] = 0
    while q:
        cost, x, y, prevx, prevy = heapq.heappop(q)
        if cost < dist[(x, y)]:
            continue
        if (x, y) == (endx, endy):
            continue

        c = mat[y][x]
        if c == ".":
            moves = MOVES
        elif c == ">":
            moves = [(1, 0)]
        elif c == "<":
            moves = [(-1, 0)]
        elif c == "v":
            moves = [(0, 1)]
        elif c == "^":
            moves = [(0, -1)]
        else:
            raise Exception(f"unexpected c={c}")

        cost2 = cost + 1
        for dx, dy in moves:
            x2 = x + dx
            y2 = y + dy
            if mat[y2][x2] == "#" or not (0 <= y2 < n and 0 <= x2 < m) or (x2, y2) == (prevx, prevy):
                continue
            oldcost = dist[(x2, y2)]
            if cost2 > oldcost:
                dist[(x2, y2)] = cost2
                heapq.heappush(q, (cost2, x2, y2, x, y))
    print(dist[(endx, endy)])


def solve2(rawinput, sx=1, sy=0, endx=-2, endy=-1):
    mat = list(read(rawinput))
    n = len(mat)
    m = len(mat[0])
    endx = m + endx
    endy = n + endy

    @cache
    def get_paths(x, y):
        """ Returns a list of (dist, x2, y2) which represent "direct paths" (no alternatives)
        from (x,y) to (x2,y2) in [dist] steps w
        """
        ways = []
        for dx, dy in MOVES:
            x2 = x + dx
            y2 = y + dy
            if (0 <= y2 < n and 0 <= x2 < m) and mat[y2][x2] != "#":
                ways.append((x2, y2))

        paths = []
        for x2, y2 in ways:
            dist = 0
            prev = (x, y)
            nextp = [(x2, y2)]
            while len(nextp) == 1:
                x2, y2 = nextp[0]
                dist += 1
                nextp.clear()
                for dx, dy in MOVES:
                    x3 = x2 + dx
                    y3 = y2 + dy
                    p3 = (x3, y3)
                    if not (0 <= y3 < n and 0 <= x3 < m) or mat[y3][x3] == "#" or p3 == prev:
                        continue
                    nextp.append(p3)
                if nextp:
                    prev = (x2, y2)
            paths.append((dist, x2, y2))
        return paths

    nodeid = defaultdict(lambda: len(nodeid))

    def find():
        q = deque()
        # Using bitmasks because there are < 32 "path intersection coordinates" in the whole map
        pathmask = 1 << nodeid[(sx, sy)]
        q.append((0, sx, sy, pathmask))
        ans = 0
        while q:
            cost, x, y, pathmask = q.popleft()
            if (x, y) == (endx, endy):
                ans = max(ans, cost)
                continue
            nextpaths = get_paths(x, y)
            for dist, x2, y2 in nextpaths:
                bit = 1 << nodeid[(x2, y2)]
                if not (pathmask & bit):
                    q.append((cost + dist, x2, y2, pathmask | bit))
        return ans

    sol = find()
    print("Part2:", sol)


CASES = [
    """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""",
    open("23.txt", "r").read()
]
for raw in CASES:
    solve(raw)
    solve2(raw)
