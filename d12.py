from functools import cache


def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        s, values = line.split()
        yield s, [int(x) for x in values.split(',')]
    return data


def solve(rawinput, fold=1):
    solution = 0
    for s, values in read(rawinput):
        s = '?'.join(s for _ in range(fold))
        values *= fold
        n = len(s)
        m = len(values)

        @cache
        def dp(i, j, x):
            if j == m:
                return int(i == n or all(c in ".?" for c in s[i:]))
            elif i == n:
                return int(values[j] == x and j == m - 1)

            ans = 0
            if s[i] in '.?':
                if x == 0:
                    ans += dp(i + 1, j, x)
                elif x == values[j]:
                    ans += dp(i + 1, j + 1, 0)
            if s[i] in "#?" and x < values[j]:
                ans += dp(i + 1, j, x + 1)
            return ans

        res = dp(0, 0, 0)
        print(s[:16] + ("..." if len(s) > 16 else ''), values, 'WAYS===', res)
        solution += res
    print(f"RESULT {fold=} -> {solution}")


CASES = [
    """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""",
    open("12.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve(raw)
    solve(raw, fold=5)
