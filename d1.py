maps = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
ans = 0
part2 = True
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(int(c))
            if part2:
                for s, x in maps.items():
                    if line[i:].startswith(s):
                        digits.append(x)
        ans += int(f"{digits[0]}{digits[-1]}")
print(ans)
