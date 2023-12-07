from collections import Counter

RAWINPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

CRANK = {c: 13 - i for i, c in enumerate("AKQJT98765432")}
CRANK2 = {c: 13 - i for i, c in enumerate("AKQT98765432J")}


def read():
    data = []
    for line in RAWINPUT.split("\n"):
        line = line.strip()
        if not line:
            continue
        hand, bid = line.split(" ")
        yield hand, int(bid)
    return data


def getstrength(hand, withjoker=False):
    joker = CRANK2["J"]
    if withjoker:
        vals = [CRANK2[c] for c in hand]
    else:
        vals = [CRANK[c] for c in hand]

    cnt = Counter(vals)
    if withjoker and joker in cnt:
        best = max(
            (val for val in cnt.keys() if val != joker),
            key=lambda v: (cnt[v], v),
            default=(13, 0)
        )
        cnt = Counter(best if x == joker else x for x in vals)

    uniqs = sorted(cnt.values())
    if len(cnt) == 1:
        strength = 7
    elif uniqs == [1, 4]:
        strength = 6
    elif uniqs == [2, 3]:
        strength = 5
    elif uniqs == [1, 1, 3]:
        strength = 4
    elif uniqs == [1, 2, 2]:
        strength = 3
    elif len(cnt) == 4:
        strength = 2
    else:
        strength = 1
    return [strength, *vals]


def solve(withjoker=False):
    hands = list(read())
    hands.sort(key=lambda hb: getstrength(hb[0], withjoker=withjoker))
    ans = 0
    for r, (hand, bid) in enumerate(hands):
        ans += (r + 1) * bid
    print(f"part {withjoker=}", ans)


RAWINPUT = open('7.txt').read()
solve(withjoker=False)  # 248453531
solve(withjoker=True)  # 248781813
