def check(times, distances):
    ans = 1  # assuming there's atleast always 1 way
    for t, dist in zip(times, distances):
        ans *= sum(
            ((t - hold_down_time) * hold_down_time) > dist
            for hold_down_time in range(1, t)
        )
    return ans


def solve(rawinput):
    lines = rawinput.split("\n")

    times = list(map(int, lines[0].replace("Time:", "").strip().split()))
    distances = list(map(int, lines[1].replace("Distance:", "").strip().split()))
    print("part1: ", check(times, distances))

    times2 = [int(''.join(str(x) for x in times))]
    distances2 = [int(''.join(str(x) for x in distances))]
    print("part2: ", check(times2, distances2))


solve("""Time:      7  15   30
Distance:  9  40  200""")
solve(open('6.txt').read())
