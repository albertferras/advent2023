from pprint import pprint

MOVES = {
    # c: [(dx, dy)]
    "|": [(0, 1), (0, -1)],
    "-": [(1, 0), (-1, 0)],
    "L": [(1, 0), (0, 1)],
    "J": [(-1, 0), (0, 1)],
    "7": [(-1, 0), (0, -1)],
    "F": [(1, 0), (0, -1)],
    ".": [],
    "S": [(0, 1), (0, -1), (1, 0), (-1, 0)],
}


def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        data.append(list(line))
    return data[::-1]


def solve(rawinput):
    data = read(rawinput)
    n = len(data)
    m = len(data[0])

    # Find S
    sx = sy = None
    for y in range(n):
        for x in range(m):
            if data[y][x] == "S":
                sx = x
                sy = y
        if sx or sy:
            break

    for startC in MOVES.keys():
        if startC in ".S":
            continue
        data[sy][sx] = startC
        valid = True
        for dx, dy in MOVES[startC]:
            x2 = sx + dx
            y2 = sy + dy
            if not (0 <= x2 < m and 0 <= y2 < n):
                valid = False
                break
            if not any((x2 + m2[0], y2 + m2[1]) == (sx, sy) for m2 in MOVES[data[y2][x2]]):
                valid = False
                break
        if not valid:
            continue

        mnext = MOVES[startC][0]
        last = (sx, sy)
        x = sx + mnext[0]
        y = sy + mnext[1]
        valid = True
        nodes = [(sx, sy), (x, y)]
        while (x, y) != (sx, sy):
            if not (0 <= x < m and 0 <= y < n) or data[y][x] == ".":
                valid = False
                break
            dx, dy = next(m for m in MOVES[data[y][x]] if (x + m[0], y + m[1]) != last)
            last = (x, y)
            x += dx
            y += dy
            nodes.append((x, y))

        if valid:
            print("LOOP SIZE = ", len(nodes))
            ans = len(nodes) // 2
            print("PART 1 = ", ans)

            # swap line
            nodes = set(nodes)
            ans = 0
            for y in range(n):
                inside = False
                wallstart = None
                for x in range(m):
                    if (x, y) in nodes:
                        c = data[y][x]
                        if c in "-S":
                            pass
                        elif c == "|":
                            inside = not inside
                        else:
                            if wallstart:
                                if wallstart+c in ("L7", "FJ"):
                                    inside = not inside
                                wallstart = None
                            else:
                                wallstart = c
                    else:
                        ans += int(inside)
            print("PART 2 = ", ans)


CASES = [
    """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...""",
    """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""", """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""",
    """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""",
    open("10.txt", "r").read()  # 6806
]
for raw in CASES:
    print("=" * 100)
    solve(raw)
