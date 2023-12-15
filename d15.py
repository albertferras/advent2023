def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        yield list(line)
    return data


def solve1(rawinput):
    ans = 0
    for s in rawinput.strip().split(","):
        h = 0
        for c in s:
            h = (h+ord(c))*17 % 256
        ans += h
    print("SOL", ans)


def solve2(rawinput):
    boxes = [[] for _ in range(256)]
    for s in rawinput.strip().split(","):
        if s.endswith("-"):
            op = "-"
            label = s[:-1]
            f = None
        else:
            op = "="
            label, f = s.split("=")
            f = int(f)

        h = 0
        for c in label:
            h = (h+ord(c))*17 % 256

        if op == "=":
            box = boxes[h]
            if label in [lab for lab, foc in box]:
                box[:] = [(label2, foc if label2!=label else f) for label2, foc in box]
            else:
                boxes[h].append((label, f))
        elif op == "-":
            for box in boxes:
                box[:] = [(label2, foc) for label2, foc in box if label2 != label]

    ans = 0
    for i, box in enumerate(boxes, start=1):
        for slot, (lab, f) in enumerate(box, start=1):
            ans += i * slot * f
    print("SOL", ans)


CASES = [
    # """HASH""",
    "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7",
    open("scratch.txt", "r").read()
]
for raw in CASES:
    print("=" * 100)
    solve1(raw)
    solve2(raw)
