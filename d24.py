import math

import dataclasses
import numpy as np
import z3


@dataclasses.dataclass
class XYZ:
    x: float
    y: float
    z: float

    @property
    def norm2(self):
        mag = math.sqrt(self.x ** 2 + self.y ** 2)
        return XYZ(
            self.x / mag,
            self.y / mag,
            0
        )


@dataclasses.dataclass
class Ray:
    p: XYZ
    v: XYZ

    def position_at(self, t: float) -> XYZ:
        return XYZ(self.p.x + t * self.v.x,
                   self.p.y + t * self.v.y,
                   self.p.z + t * self.v.z)


def read(rawinput):
    data = []
    for line in rawinput.split("\n"):
        line = line.strip()
        if not line:
            continue
        p, v = line.split(" @ ")

        p = XYZ(*(int(x.strip()) for x in p.split(",")))
        v = XYZ(*(int(x.strip()) for x in v.split(",")))
        yield Ray(p, v)
    return data


def solve(rawinput, b1, b2):
    data = list(read(rawinput))
    n = len(data)
    ta = XYZ(b1, b1, 0)
    tb = XYZ(b2, b2, 0)

    ans = 0
    for i in range(n):
        ray1 = data[i]
        for j in range(i + 1, n):
            ray2 = data[j]
            pin = intersection_point(ray1, ray2)
            if pin:
                futurea = intime(ray1, pin) > 0
                futureb = intime(ray2, pin) > 0
                if futurea and futureb and ta.x <= pin.x <= tb.x and ta.y <= pin.y <= tb.y:
                    ans += 1
    print("Part 1" ,ans)


def intime(ray: Ray, pin: XYZ):
    # At what time will `ray` reach `ip` (guaranteed intersection)
    # ray1.p + t*ray1.v == pin
    k = (pin.x - ray.p.x) / ray.v.x
    return k


def solve2_numpy(rawinput):
    data = list(read(rawinput))
    r0, r1, r2 = data[:3]

    (x0, y0, z0), (vx0, vy0, vz0) = (r0.p.x, r0.p.y, r0.p.z), (r0.v.x, r0.v.y, r0.v.z)
    (x1, y1, z1), (vx1, vy1, vz1) = (r1.p.x, r1.p.y, r1.p.z), (r1.v.x, r1.v.y, r1.v.z)
    (x2, y2, z2), (vx2, vy2, vz2) = (r2.p.x, r2.p.y, r2.p.z), (r2.v.x, r2.v.y, r2.v.z)

    equation_matrix = np.zeros((6, 6), dtype=np.float64)
    vector = np.zeros(6, dtype=np.float64)

    equation_matrix[0, 1] = vz0 - vz1
    equation_matrix[0, 2] = vy1 - vy0
    equation_matrix[0, 4] = z1 - z0
    equation_matrix[0, 5] = y0 - y1

    equation_matrix[1, 0] = vz1 - vz0
    equation_matrix[1, 2] = vx0 - vx1
    equation_matrix[1, 3] = z0 - z1
    equation_matrix[1, 5] = x1 - x0

    equation_matrix[2, 0] = vy0 - vy1
    equation_matrix[2, 1] = vx1 - vx0
    equation_matrix[2, 3] = y1 - y0
    equation_matrix[2, 4] = x0 - x1

    equation_matrix[3, 1] = vz0 - vz2
    equation_matrix[3, 2] = vy2 - vy0
    equation_matrix[3, 4] = z2 - z0
    equation_matrix[3, 5] = y0 - y2

    equation_matrix[4, 0] = vz2 - vz0
    equation_matrix[4, 2] = vx0 - vx2
    equation_matrix[4, 3] = z0 - z2
    equation_matrix[4, 5] = x2 - x0

    equation_matrix[5, 0] = vy0 - vy2
    equation_matrix[5, 1] = vx2 - vx0
    equation_matrix[5, 3] = y2 - y0
    equation_matrix[5, 4] = x0 - x2

    indepx0 = y0 * vz0 - vy0 * z0
    indepx1 = y1 * vz1 - vy1 * z1
    indepx2 = y2 * vz2 - vy2 * z2

    indepy0 = z0 * vx0 - vz0 * x0
    indepy1 = z1 * vx1 - vz1 * x1
    indepy2 = z2 * vx2 - vz2 * x2

    indepz0 = x0 * vy0 - vx0 * y0
    indepz1 = x1 * vy1 - vx1 * y1
    indepz2 = x2 * vy2 - vx2 * y2

    vector[0] = indepx0 - indepx1
    vector[1] = indepy0 - indepy1
    vector[2] = indepz0 - indepz1
    vector[3] = indepx0 - indepx2
    vector[4] = indepy0 - indepy2
    vector[5] = indepz0 - indepz2

    result = np.linalg.solve(equation_matrix, vector)
    print(result[:3])
    k = int(np.round(np.sum(result[:3])))
    print(k)


def solve2_z3(rawinput):
    data = list(read(rawinput))
    h1, h2, h3 = data[:3]

    # rock throw from (rx, ry, rz)
    rx, ry, rz = z3.Reals("rx ry rz")
    # rock throw vector
    dx, dy, dz = z3.Reals("dx dy dz")
    # times when rock intersect with h0 h1 h2
    t1, t2, t3 = z3.Reals("t1 t2 t3")

    solver = z3.Solver()
    equations = [
        rx + t1 * dx == h1.p.x + t1 * h1.v.x,
        ry + t1 * dy == h1.p.y + t1 * h1.v.y,
        rz + t1 * dz == h1.p.z + t1 * h1.v.z,
        rx + t2 * dx == h2.p.x + t2 * h2.v.x,
        ry + t2 * dy == h2.p.y + t2 * h2.v.y,
        rz + t2 * dz == h2.p.z + t2 * h2.v.z,
        rx + t3 * dx == h3.p.x + t3 * h3.v.x,
        ry + t3 * dy == h3.p.y + t3 * h3.v.y,
        rz + t3 * dz == h3.p.z + t3 * h3.v.z,
    ]
    solver.add(*equations)
    assert solver.check() == z3.sat
    model = solver.model()
    print("Vars solution: ", model)
    print("Part2:", model[rx].as_long() + model[ry].as_long() + model[rz].as_long())


def intersection_point(ray1: Ray, ray2: Ray) -> XYZ | None:
    p = ray1.p
    q = ray2.p
    r = ray1.v.norm2
    s = ray2.v.norm2

    pqx = q.x - p.x
    pqy = q.y - p.y
    rx = r.x
    ry = r.y
    rxt = -ry
    ryt = rx
    qx = pqx * rx + pqy * ry
    qy = pqx * rxt + pqy * ryt
    sx = s.x * rx + s.y * ry
    sy = s.x * rxt + s.y * ryt
    if sy == 0:
        # Same line
        return None
    a = qx - qy * sx / sy
    return XYZ(p.x + a * rx, p.y + a * ry, 0)


CASES = [
    ("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""", 7, 27),
    (open("24.txt", "r").read(), 200000000000000, 400000000000000)
]
for raw, b1, b2 in CASES:
    solve(raw, b1, b2)
    solve2_numpy(raw)
    solve2_z3(raw)
    print("---------------")
