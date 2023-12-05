import math
SAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def parse(raw):
    lines = raw.strip().split("\n")
    seeds = [int(x) for x in lines[0].replace("seeds: ", "").split()]
    maps = {}
    current_map_id = None
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        if line.endswith("map:"):
            current_map_id = line.replace(" map:", "")
            maps[current_map_id] = []
        else:
            dest, src, rlen = [int(x) for x in line.split()]
            maps[current_map_id].append((dest, src, rlen))
    # fill range gaps to simplify get_mapped_range implementation
    for mapid, mapranges in maps.items():
        mapranges.sort(key=lambda x: x[1])
        newranges = []
        current = 0
        for dest, src, rlen in mapranges:
            if current < src:
                newranges.append((current, current, src-current))
            newranges.append((dest, src, rlen))
            current = src+rlen
        newranges.append((current, current, 99999))
        mapranges[:] = newranges
    return seeds, maps


def get_mapped_value(mapranges, value):
    for dest, src, rlen in mapranges:
        if value in range(src, src+rlen):
            delta = value-src
            return dest+delta
    raise ValueError(f"Parsing incorrect. Mapped range missing: {mapranges} {value=}")


def get_mapped_range(mapranges, value_start, value_end):
    ranges = []
    current = value_start
    for dest, src, rlen in mapranges:
        if current in range(src, src + rlen):
            delta = current - src
            rstart = dest + delta

            current = min(src+rlen-1, value_end)
            ranges.append((rstart, dest + current - src))
            if current < value_end:
                current += 1
    return ranges


def solve(raw):
    seeds, maps = parse(raw)
    ans = math.inf
    for seed in seeds:
        value = seed
        for mapid, mapranges in maps.items():
            value = get_mapped_value(mapranges, value)
        location = value
        ans = min(ans, location)
    print("Min", ans)

    # part 2
    print("part2=============")
    currentranges = []
    for i in range(0, len(seeds), 2):
        currentranges.append((seeds[i], seeds[i]+seeds[i+1]))
    for mapid, mapranges in maps.items():
        newranges = []
        for srange in currentranges:
            newranges.extend(get_mapped_range(mapranges, srange[0], srange[1]))
        currentranges = newranges
    print("Min", min(r[0] for r in currentranges))


solve(SAMPLE)
with open("input.txt", "r") as f:
    solve(f.read())
