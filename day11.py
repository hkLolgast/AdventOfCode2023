from copy import deepcopy

def parse_input(file = 'day11.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day11example.txt')

def format_input(inp: list[str]):
    return [[c for c in line] for line in inp]

DISTANCE_CACHE: dict
def distance(direction: str, v0: int, v1: int, empty_lines: list[int], expansion: int):
    cache = DISTANCE_CACHE[direction]
    low = min((v0, v1))
    high = max((v0, v1))
    if low not in cache:
        cache[low] = {low: 0}
    if high in cache[low]:
        return cache[low][high]
    farthest = max(cache[low])
    for v in range(farthest + 1, high + 1):
        cache[low][v] = cache[low][v-1] + (expansion if v in empty_lines else 1)
    return cache[low][high]

def solve(inp, part, example):
    global DISTANCE_CACHE
    DISTANCE_CACHE = {'hor': {}, 'vert': {}}
    expansion = 2 if part == 1 else 100 if example else 1_000_000
    empty_columns = []
    empty_rows = []
    for row, line in enumerate(inp):
        if all(c == '.' for c in line):
            empty_rows.append(row)
    for c in range(len(inp[0])):
        if all(line[c] == '.' for line in inp):
            empty_columns.append(c)

    galaxies = []
    for row, line in enumerate(inp):
        for col, c in enumerate(line):
            if c == '#':
                galaxies.append((row, col))
    total_dist = 0
    for i, gal in enumerate(galaxies):
        for gal2 in galaxies[i+1:]:
            vert = distance('vert', gal[0], gal2[0], empty_rows, expansion)
            hor = distance('hor', gal[1], gal2[1], empty_columns, expansion)
            total_dist += vert + hor
    return total_dist

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
