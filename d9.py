def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        yield [int(x) for x in line.split()]
    return data


def solve(rawinput):
    data = read(rawinput)
    ans = ans2 = 0
    for row in data:
        dp = [row]
        while not all(x == 0 for x in dp[-1]):
            arr = dp[-1]
            dp.append([arr[i + 1] - arr[i] for i in range(len(arr) - 1)])

        # part 1
        ans += sum(arr[-1] for arr in dp)

        # part 2
        last = 0
        for i in range(len(dp) - 2, -1, -1):
            last = dp[i][0] - last
        ans2 += last
    print(f"{ans=}")
    print(f"{ans2=}")


CASES = [
    """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""",
    open("9.txt", "r").read()
]
for raw in CASES:
    solve(raw)
