limits = {
    "red": 12,
    "green": 13,
    "blue": 14
}


def play(iterable):
    ans = 0
    ans2 = 0
    for line in iterable:
        if not line.strip():
            continue
        game, sets = line.strip().split(":")
        game_id = int(game.split(" ")[1])
        valid = True
        mins = {"red": 0, "green": 0, "blue": 0}
        for s in sets.split(";"):
            for cubesraw in s.split(","):
                x, color = cubesraw.strip().split(" ")
                x = int(x)
                color = color.strip()
                if x > limits.get(color, 0):
                    valid = False
                mins[color] = max(mins[color], x)
        if valid:
            ans += game_id
        # Calculate power (part2)
        p = 1
        for k in mins.values():
            p *= k
        ans2 += p
    print(f"{ans=}")
    print(f"{ans2=}")


play("""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split("\n"))

play("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split("\n"))

with open("input.txt", "r") as f:
    play(f)
