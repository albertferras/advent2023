import sys

RAWINPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
RAWINPUT = open('4.txt').read()


def read():
    data = []
    for line in RAWINPUT.split("\n"):
        line = line.strip()
        if not line:
            continue
        card_id, nnn = line.split(":")
        winnums, mynums = nnn.split("|")
        winnums = [int(x) for x in winnums.strip().split()]
        mynums = [int(x) for x in mynums.strip().split()]
        yield card_id, winnums, mynums
    return data


def solve():
    data = read()
    ans = 0
    for card_id, winnums, mynums in data:
        hits = len(set(winnums).intersection(mynums))
        if not hits:
            continue
        ans += 2**(hits-1)
    print(f"{ans=}")


def solve2():
    data = read()
    dp = [0] * 300
    for i, (card_id, winnums, mynums) in enumerate(data):
        dp[i] += 1
        hits = len(set(winnums).intersection(mynums))
        for j in range(hits):
            dp[i+j+1] += dp[i]
    print(sum(dp))

solve()
solve2()
