def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        yield list(line)
    return data


def solve(rawinput):
    mat = list(read(rawinput))
    n = len(mat)
    tiltnorth(mat)
    ans = 0
    for i, line in enumerate(mat):
        print(''.join(line))
        ans += (n - i) * sum(c == "O" for c in line)
    print("ANS", ans)


def tiltnorth(mat):
    n = len(mat)
    m = len(mat[0])
    for y in range(n):
        for x in range(m):
            if mat[y][x] == 'O':
                j = y
                while j > 0 and mat[j - 1][x] == '.':
                    mat[j - 1][x] = 'O'
                    mat[j][x] = '.'
                    j -= 1


def tiltsouth(mat):
    n = len(mat)
    m = len(mat[0])
    for y in range(n - 1, -1, -1):
        for x in range(m):
            if mat[y][x] == 'O':
                j = y
                while j < n - 1 and mat[j + 1][x] == '.':
                    mat[j + 1][x] = 'O'
                    mat[j][x] = '.'
                    j += 1


def tiltwest(mat):
    n = len(mat)
    m = len(mat[0])
    for y in range(n - 1, -1, -1):
        for x in range(m):
            if mat[y][x] == 'O':
                j = x
                while j > 0 and mat[y][j - 1] == '.':
                    mat[y][j - 1] = 'O'
                    mat[y][j] = '.'
                    j -= 1


def tilteast(mat):
    n = len(mat)
    m = len(mat[0])
    for y in range(n - 1, -1, -1):
        for x in range(m - 1, -1, -1):
            if mat[y][x] == 'O':
                j = x
                while j < m - 1 and mat[y][j + 1] == '.':
                    mat[y][j + 1] = 'O'
                    mat[y][j] = '.'
                    j += 1


def build_snapshot_id(mat):
    return ''.join(''.join(row) for row in mat)


CYCLES = 1000000000


def solve2(rawinput):
    mat = list(read(rawinput))
    n = len(mat)

    visited = {}
    i = 1
    jumped = False
    while i < CYCLES:
        tiltnorth(mat)
        tiltwest(mat)
        tiltsouth(mat)
        tilteast(mat)
        if not jumped:
            snapshot_id = build_snapshot_id(mat)
            if snapshot_id in visited:
                start = visited[snapshot_id]
                end = i
                dist = (end - start)

                # start + dist*K < 10000000
                k = (CYCLES - start) // dist
                i = start + dist * k
                jumped = True
                continue
            visited[snapshot_id] = i
        i += 1

    ans = 0
    for i, line in enumerate(mat):
        # print(''.join(line))
        ans += (n - i) * sum(c == "O" for c in line)
    print("ANS", ans)


CASES = [
    """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""",
    open("scratch.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve(raw)
    solve2(raw)
