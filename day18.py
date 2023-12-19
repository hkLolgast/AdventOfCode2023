from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day18.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day18example.txt')

def format_input(inp: list[str]):
    insts = []
    for line in inp:
        dir, amount, color = line.split()
        insts.append((dir, int(amount), color))
    return insts

def move(loc, dir, amount = 1):
    if dir == 'U':
        return (loc[0] - amount, loc[1])
    if dir == 'R':
        return (loc[0], loc[1] + amount)
    if dir == 'D':
        return (loc[0] + amount, loc[1])
    if dir == 'L':
        return (loc[0], loc[1] - amount)
    raise ValueError(f'Unexpected dir: {dir}')

def solve(inp, part, example):
    if part == 1:
        instructions = [(dir, amount) for dir, amount, color in inp]
    else:
        instructions = []
        for _, _, color in inp:
            amount = int(color[2:7], 16)
            dir = 'RDLU'[int(color[-2])]
            instructions.append((dir, amount))
    corners = set()
    corners.add((0, 0))
    loc = (0, 0)
    for dir, amount in instructions:
        loc = move(loc, dir, amount)
        corners.add(loc)
    corners = sorted(corners)
    insides = [corners[0][1], corners[1][1]]
    current_row = corners[0][0]
    total = corners[1][1] - corners[0][1] + 1
    for c1, c2 in zip(corners[2::2], corners[3::2]):
        if c1[0] != current_row:
            new_row = c1[0]
            for r1, r2 in zip(insides[::2], insides[1::2]):
                total += (r2 - r1 + 1) * (new_row - current_row)
            current_row = new_row
        for i, v in enumerate(insides):
            if v == c1[1]:
                if i + 1 < len(insides) and insides[i + 1] == c2[1]:
                    insides.remove(v)
                    insides.remove(c2[1])
                    if i % 2 == 1:
                        total += c2[1] - c1[1] - 1
                    break
                insides.insert(i, c2[1])
                insides.remove(v)
                if i % 2 == 1:
                    total += c2[1] - v
                break
            elif v == c2[1]:
                insides.insert(i, c1[1])
                insides.remove(v)
                if i % 2 == 0:
                    total += v - c1[1]
                break
        else:
            for i in range(len(insides) - 1):
                if insides[i] < c1[1] < insides[i + 1]:
                    if i % 2 == 1:
                        total += c2[1] - c1[1] + 1
                    break
            else:
                total += c2[1] - c1[1] + 1
            insides.append(c1[1])
            insides.append(c2[1])
            insides = sorted(insides)
    return total

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
