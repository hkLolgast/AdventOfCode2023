from copy import deepcopy

def parse_input(file = 'day11.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day11example.txt')

def format_input(inp: list[str]):
    return [[c for c in line] for line in inp]

def solve(inp, part, example):
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
            dist = 0
            for row in range(gal[0], gal2[0]):
                dist += expansion if row in empty_rows else 1
            c0 = min((gal[1], gal2[1]))
            c1 = max((gal[1], gal2[1]))
            for col in range(c0, c1):
                dist += expansion if col in empty_columns else 1
            total_dist += dist
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
