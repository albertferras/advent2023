import copy
import math
from dataclasses import dataclass
from pprint import pprint
import operator
import re
from collections import deque, defaultdict
from functools import cache, reduce
from typing import Literal


@dataclass
class Coord:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    a: Coord
    b: Coord

    @property
    def lowerZ(self) -> int:
        return min(self.a.z, self.b.z)

    @property
    def bottom_coords(self):
        for x in range(self.a.x, self.b.x + 1):
            for y in range(self.a.y, self.b.y + 1):
                yield (x, y)


def read(rawinput):
    bricks = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue

        a, b = line.split("~")
        brick = Brick(
            Coord(*tuple(int(v) for v in a.split(','))),
            Coord(*tuple(int(v) for v in b.split(',')))
        )
        bricks.append(brick)
    return bricks


def drawX(bmap):
    xmax = len(bmap)
    ymax = len(bmap[0])
    zmax = len(bmap[0][0])
    print(' x ')
    for z in range(zmax - 1, -1, -1):
        line = []
        for x in range(xmax):
            yvals = set()
            for y in range(ymax):
                v = bmap[x][y][z]
                if v != -1:
                    yvals.add(v)
            if not yvals:
                c = "."
            elif len(yvals) == 1:
                c = str(list(yvals)[0])
            else:
                c = "?"
            line.append(c)
        print(''.join(line), z)
    print()


def drawY(bmap):
    xmax = len(bmap)
    ymax = len(bmap[0])
    zmax = len(bmap[0][0])
    print(' y ')
    for z in range(zmax - 1, -1, -1):
        line = []
        for y in range(ymax):
            xvals = set()
            for x in range(xmax):
                v = bmap[x][y][z]
                if v != -1:
                    xvals.add(v)
            if not xvals:
                c = "."
            elif len(xvals) == 1:
                c = str(list(xvals)[0])
            else:
                c = "?"
            line.append(c)
        print(''.join(line), z)
    print()


def solve1(rawinput):
    bricks = read(rawinput)
    xmax = max(max(br.a.x, br.b.x) for br in bricks) + 1
    ymax = max(max(br.a.y, br.b.y) for br in bricks) + 1
    zmax = max(max(br.a.z, br.b.z) for br in bricks) + 2
    print(xmax, ymax, zmax)

    # sort by lower Z position
    bricks.sort(key=lambda br: br.lowerZ)

    bmap = [
        [[-1] * zmax for _ in range(ymax)]
        for _ in range(xmax)
    ]
    # bmap[x][y][z]
    for i, brick in enumerate(bricks):
        zstart = z = brick.lowerZ
        suppcoords = list(brick.bottom_coords)
        while z - 1 >= 0 and all(bmap[x][y][z - 1] == -1 for (x, y) in suppcoords):
            z -= 1
        fall = zstart - z
        brick.a.z -= fall
        brick.b.z -= fall
        for (x, y) in suppcoords:
            for zi in range(brick.a.z, brick.b.z + 1):
                if bmap[x][y][zi] != -1:
                    raise ValueError("Already occupied")
                bmap[x][y][zi] = i
    if len(bricks) < 10:
        drawX(bmap)
        drawY(bmap)

    # Part 1
    # Check supporting if removed
    supportedby = defaultdict(set)
    supporting = defaultdict(set)
    for i, brick in enumerate(bricks):
        upperz = max(brick.a.z, brick.b.z)
        supportedby[i]
        for (x, y) in brick.bottom_coords:
            above = bmap[x][y][upperz+1]
            if above != -1:
                supporting[i].add(above)
                supportedby[above].add(i)

    ans = 0
    for i in range(len(bricks)):
        if any(supportedby[b] == {i} for b in supporting[i]):
            # can't be disintegrated
            # print(f"Brick {i} cannot be disintegrated")
            pass
        else:
            # print(f"Brick {i} can be disintegrated")
            ans += 1
    print(f"Answer: {ans}")

    # Part 2
    def fallchain(i, supby, suping):
        fallen = set()
        q = deque()
        q.append(i)
        while q:
            b = q.popleft()
            if b in fallen:  # already checked
                continue
            fallen.add(b)

            for b2 in suping[b]:
                # b2 is supported by b
                supby[b2].remove(b)
                if not supby[b2]:
                    # removing 'b' would make 'b2' fall!
                    q.append(b2)
            suping[b].clear()

        return len(fallen) - 1

    ans2 = 0
    for i in range(len(bricks)):
        size = fallchain(i, copy.deepcopy(supportedby), copy.deepcopy(supporting))
        print(f"Disintegrating brick {i} would cause {size} bricks to fall")
        ans2 += size
    print(f"Answer 2: {ans2}")

CASES = [
    """1,0,1~1,2,1
   0,0,2~2,0,2
   0,2,3~2,2,3
   0,0,4~0,2,4
   2,0,5~2,2,5
   0,1,6~2,1,6
   1,1,8~1,1,9
       """,
    open("scratch.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve1(raw)
