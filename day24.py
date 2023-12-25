from copy import deepcopy
from AoCHelpers.functions import lcm

def parse_input(file = 'day24.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day24example.txt')

def format_input(inp: list[str]):
    points = []
    for line in inp:
        s = line.split('@')
        p = tuple(map(int, s[0].split(', ')))
        v = tuple(map(int, s[1].split(', ')))
        points.append((p, v))
    return points

def sign(v):
    return 0 if v == 0 else 1 if v > 0 else - 1

def intersect(p1, v1, p2, v2, ignore_z):
    dydx1 = v1[1] / v1[0] if v1[0] else 10**99
    dydx2 = v2[1] / v2[0] if v2[0] else 10**99
    dydx = dydx2 - dydx1
    if dydx == 0:
        return None
    dy = p2[1] - p1[1]
    dx = p2[0] - p1[0]
    dx_intersect1 = -(dy + dydx2 * -dx) / dydx
    x_intersect = p1[0] + dx_intersect1
    dx_intersect2 = x_intersect - p2[0]
    if sign(dx_intersect1) != sign(v1[0]) or sign(dx_intersect2) != sign(v2[0]):
        return None
    y_intersect = p1[1] + dx_intersect1 * dydx1
    if ignore_z:
        return (x_intersect, y_intersect)
    else:
        dzdx1 = v1[2] / v1[0]
        z_intersect1 = p1[2] + dx_intersect1 * dzdx1
        dzdx2 = v2[2] / v2[0]
        z_intersect2 = p2[2] + dx_intersect2 * dzdx2
        if abs(z_intersect1 - z_intersect2) > 0.1:
            return None
    return (x_intersect, y_intersect, z_intersect1)

def solve(inp, part, example):
    if part == 1:
        lims = (7, 27) if example else (200000000000000, 400000000000000)
        in_area = 0
        for i, (p1, v1) in enumerate(inp):
            for (p2, v2) in inp[i+1:]:
                intersection = intersect(p1, v1, p2, v2, True)
                if intersection and all(lims[0] <= intersection[i] <= lims[1] for i in range(2)):
                    in_area += 1
        return in_area
    
    '''
    ps(t1) = p1 + v1 * t1
    ps(t1 + dt) = p2 + v2 * t1 + v2 * dt
    ps(t1) + vs * dt = p2* + v2 * dt
    ps(t1) - p2*  = (vs - v2) * dt
    p1* - p2* = 0 mod dt
    '''
    vs = [None, None, None]
    ps = [None, None, None]
    for i, (p1, v1) in enumerate(inp):
        for p2, v2 in inp[i + 1:]:
            for j in range(3):
                if p1[j] == p2[j] and v1[j] == v2[j]:
                    ps[j] = p1[j]
                    vs[j] = v1[j]
                    to_check = j

    # ps + vs * t = p + v * t
    # ps - p = (v - vs) * t
    if example:
        return None
    ts = []
    p0 = None
    for p, v in inp:
        if v[to_check] == vs[to_check]:
            continue
        t_intercept = (ps[to_check] - p[to_check]) // (v[to_check] - vs[to_check])
        if p0 is None:
            t0 = t_intercept
            p0 = [p[j] + v[j] * t_intercept for j in range(3)]
        else:
            p1 = [p[j] + v[j] * t_intercept for j in range(3)]
            d = [p1[j] - p0[j] for j in range(3)]
            vs = [d[j] // (t_intercept - t0) for j in range(3)]
            ps = [p1[j] - vs[j] * t_intercept for j in range(3)]
            return sum(ps)
    

    # for t1 in range(1, 50):
    #     for p1, v1 in inp:
    #         int1 = tuple(p1[i] + v1[i] * t1 for i in range(3))
    #         for p2, v2 in inp:
    #             if p1 == p2 and v1 == v2:
    #                 continue
    #             int2 = tuple(p2[i] + v2[i] * (t1 + dt) for i in range(3))
    #             dp = tuple(int2[i] - int1[i] for i in range(3))
    #             if any(dp[i] % dt != 0 for i in range(3)):
    #                 continue
    #             v_stone = tuple(dp[i] / dt for i in range(3))
    #             p_stone = tuple(int1[i] - v_stone[i] for i in range(3))
    #             for p3, v3 in inp:
    #                 inter = intersect(p_stone, v_stone, p3, v3, False)
    #                 if not inter:
    #                     break
    #             else:
    #                 return int(sum(p_stone))

def main():
    example_input = format_input(parse_example())
    actual_input = format_input(parse_input())
    for part in (1, 2):
        for example in (True, False):
            inp = deepcopy(example_input if example else actual_input)
            try:
                yield solve(inp, part, example)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                yield e
