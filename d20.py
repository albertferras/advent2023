import math
from pprint import pprint
import operator
import re
from collections import deque, defaultdict
from functools import cache, reduce
from typing import Literal

PARTS = ['x', 'm', 'a', 's']


def read(rawinput):
    flows = {}
    ftypes = {}
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue

        src, dests = line.split(" -> ")
        if src[0] in '%&':
            ftype = src[0]
            label = src[1:]
        else:
            ftype = 'start'
            label = src
        flows[label] = [x.strip() for x in dests.split(',')]
        ftypes[label] = ftype

    ends = set()
    for label, dests in flows.items():
        for dest in dests:
            if dest not in flows:
                ends.add(dest)
    for label in ends:
        flows[label] = []
        ftypes[label] = 'end'
    return flows, ftypes


def solve1(rawinput):
    flows, ftypes = read(rawinput)

    states = defaultdict(lambda: ['low', {}])
    for label, dests in flows.items():
        states[label]
        for dest in dests:
            states[dest][1][label] = 'low'
    states = dict(states)

    def flip(pulse):
        return 'high' if pulse == 'low' else 'low'

    tjflips = defaultdict(list)
    tjlastflip = defaultdict(lambda: "low")

    def pushbutton(k):
        lows = highs = 0
        q = deque([('button', 'broadcaster', 'low')])
        lows += 1

        qmflips = []
        while q:
            source, label, pulse = q.popleft()
            if label == "tj":
                if tjlastflip[source] != pulse:
                    tjlastflip[source] = pulse
                    tjflips[source].append(k)

            newpulse = pulse
            if ftypes[label] == '%':  # FLIP FLOP
                if pulse == 'high':
                    continue
                newpulse = states[label][0] = flip(states[label][0])
            elif ftypes[label] == '&':  # CONJUNCTION
                mem = states[label][1]
                mem[source] = pulse
                newpulse = "low" if all(p == "high" for p in mem.values()) else "high"
            for target in flows[label]:
                q.append((label, target, newpulse))
                if newpulse == 'low':
                    lows += 1
                else:
                    highs += 1
        return lows, highs, qmflips

    # cycle detection?
    tlows = thighs = 0
    k = 0
    CYCLES = 100000
    while k < CYCLES:
        k += 1
        lows, highs, qmflips = pushbutton(k)
        tlows += lows
        thighs += highs

    def get_pattern(nums):
        delta = nums[0]
        if all(i * k for i, k in enumerate(nums, start=1)):
            return delta
        return "?"

    print(tlows, thighs)
    print('sol', tlows * thighs)

    patterns = []
    for label, xs in tjflips.items():
        pattern = get_pattern(xs)
        patterns.append(pattern)
        print(f"{label}: pattern={get_pattern(xs)},  {', '.join(map(str, xs))}")
    print(math.lcm(*patterns))

CASES = [
 """broadcaster -> a, b, c
    %a -> b
    %b -> c
    %c -> inv
    &inv -> a""",
        """
    broadcaster -> a
    %a -> inv, con
    &inv -> b
    %b -> con
    &con -> output
    """,
    open("scratch.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve1(raw)
    # 121534 = bad
    # solve2(raw)
