def read(rawinput):
    data = []
    cmap = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            if cmap:
                data.append(cmap)
                cmap = []
            continue
        cmap.append(line)
    if cmap:
        data.append(cmap)
    return data


def transpose(mat):
    n = len(mat)
    m = len(mat[0])
    return [''.join(mat[i][j] for i in range(n)) for j in range(m)]


def check(mat, smudges):
    n = len(mat)
    for r in range(n - 1):
        i = r
        j = r + 1
        diff = 0
        while i >= 0 and j < n:
            diff += sum(a != b for a, b in zip(mat[i], mat[j]))
            if diff <= smudges:
                i -= 1
                j += 1
            else:
                break
        if diff == smudges:
            return r + 1
    return None


def solve(rawinput, smudges):
    maps = read(rawinput)
    ans = 0
    for mmap in maps:
        h = check(mmap, smudges)
        v = check(transpose(mmap), smudges)
        if h:
            ans += 100 * h
        else:
            ans += v
    print("ANS", ans)


CASES = [
    """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""",
    open("scratch.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve(raw, smudges=0)
    solve(raw, smudges=1)
