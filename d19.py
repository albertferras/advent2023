import operator
import re
from functools import cache, reduce

PARTS = ['x', 'm', 'a', 's']


def read(rawinput):
    workflows = {}
    parts = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue

        if not line.startswith("{"):
            wid, rawrules = line.split("{")
            rules = []
            for r in rawrules.rstrip("}").split(","):
                if ":" not in r:
                    rules.append([r])
                else:
                    x = r.split(":")
                    action = x[1]
                    wid2, op, n = re.findall(r"^(\w+)([><=])(\d+)$", x[0])[0]
                    rules.append((wid2, op, int(n), action))
            workflows[wid] = rules
        else:
            x = line.strip("{").strip("}").split(",")
            part = {}
            for piece in x:
                label, val = re.findall(r"^(\w+)=(\d+)$", piece)[0]
                part[label] = int(val)
            parts.append(part)

    return workflows, parts


def solve1(rawinput):
    workflows, parts = read(rawinput)
    def evalu(part, label, op, val):
        if op == "<":
            return part[label] < val
        elif op == ">":
            return part[label] > val
        raise Exception("UNKNOWN OP", op)

    ans = 0
    for part in parts:
        current = "in"
        while current not in ("A", "R"):
            for rule in workflows[current]:
                if len(rule) > 1:
                    label, op, val, dest = rule
                    if evalu(part, label, op, val):
                        current = dest
                        break
                else:
                    current = rule[0]
                    break
        if current == "A":
            ans += sum(part.values())

    print(ans)

    idx = {rating: i for i, rating in enumerate(PARTS)}

    def count_combs(intervals):
        if any(a > b for a, b in intervals):
            return 0
        return reduce(operator.mul, (max(0, (b - a + 1)) for a, b in intervals), 1)

    @cache
    def combs(wid, intervals):
        ans = 0
        for rule in workflows[wid]:
            if len(rule) == 1:
                dest = rule[0]
                if dest == "A":
                    ans += count_combs(intervals)
                elif dest == "R":
                    pass
                else:
                    ans += combs(dest, intervals)
            else:
                label, op, val, dest = rule
                r = idx[label]
                intervals_match = [(a, b) for a, b in intervals]
                intervals_nomatch = [(a, b) for a, b in intervals]

                a, b = intervals[r]
                if op == ">":
                    intervals_match[r] = (val + 1, b)
                    intervals_nomatch[r] = (a, val)
                elif op == "<":
                    intervals_match[r] = (a, val - 1)
                    intervals_nomatch[r] = (val, b)
                else:
                    raise Exception("WHAT")

                if dest == "A":
                    ans += count_combs(intervals_match)
                elif dest == "R":
                    pass
                else:
                    ans += combs(dest, tuple(intervals_match))
                intervals = tuple(intervals_nomatch)
        return ans

    start_intervals = tuple((1, 4000) for _ in PARTS)
    ans = combs("in", start_intervals)
    print("SOLUTION", ans)


CASES = [
    """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""",
    open("scratch.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve1(raw)
