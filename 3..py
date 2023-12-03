from collections import defaultdict
import sys

RAWINPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


RAWINPUT = open('3.txt').read()


def read():
    data = []
    for line in RAWINPUT.split("\n"):
        line = line.strip()
        if not line:
            continue
        row = [int(c) if c in "0123456789" else c for c in line]
        # print(row)
        data.append(row)
    return data


def adjacent(y, x, data):
    for y2 in (y - 1, y, y + 1):
        for x2 in (x - 1, x, x + 1):
            if x2 < 0 or y2 < 0 or x2 >= len(data[0]) or y2 >= len(data) or (x, y) == (x2, y2):
                # out of bounds or same
                continue
            c = data[y2][x2]
            if not isinstance(c, int) and c != ".":
                return True
    return False


def solve():
    data = read()

    ans = 0
    for y, row in enumerate(data):
        digit = None
        nearsym = False
        for x, c in enumerate(row):
            if isinstance(c, int):
                digit = (digit or 0) * 10 + c
                if adjacent(y, x, data):
                    nearsym = True
            else:
                if digit is not None:
                    if nearsym:
                        # is adj
                        print(digit, "adj")
                        ans += digit
                    else:
                        # not adj
                        print(digit, "not adj")
                nearsym = False
                digit = None
        if nearsym:
            ans += digit
    print(f"SUM={ans}")
    # 535158 incorrect !?
    # 536576


def get_gears(y, x, data):
    gear_ids = set()
    for y2 in (y - 1, y, y + 1):
        for x2 in (x - 1, x, x + 1):
            if x2 < 0 or y2 < 0 or x2 >= len(data[0]) or y2 >= len(data) or (x, y) == (x2, y2):
                # out of bounds or same
                continue
            c = data[y2][x2]
            if c == "*":
                gear_ids.add((y2, x2))
    return gear_ids


def solve2():
    data = read()

    ans = 0
    gears_numbers = defaultdict(list)
    for y, row in enumerate(data):
        digit = None
        gear_ids = set()
        for x, c in enumerate(row):
            if isinstance(c, int):
                digit = (digit or 0) * 10 + c
                gear_ids.update((gids := get_gears(y, x, data)))
            else:
                if digit is not None:
                    for gear_id in gear_ids:
                        gears_numbers[gear_id].append(digit)
                digit = None
                gear_ids = set()
        if digit is not None:
            for gear_id in gear_ids:
                gears_numbers[gear_id].append(digit)

    ans = 0
    for gear_id, numbers in gears_numbers.items():
        print(gear_id, numbers)
        if len(numbers) == 2:
            ans += numbers[0] * numbers[1]
    print(f"SUM={ans}")


solve()
solve2()
