from copy import deepcopy
from collections import defaultdict

def parse_input(file = 'day14.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day14example.txt')

def format_input(inp: list[str]):
    round = []
    solid = []
    for row, line in enumerate(inp):
        for col, c in enumerate(line):
            if c == 'O':
                round.append((row, col))
            elif c == '#':
                solid.append((row, col))
    return round, solid, len(inp), len(inp[0])

def roll_north(round, solid, max_row, max_col):
    solids = defaultdict(list)
    rounds = defaultdict(list)
    for rock in round:
        rounds[rock[1]].append(rock[0])
    for rock in solid:
        solids[rock[1]].append(rock[0])
    new_rounds = []
    for col in range(max_col):
        local_solids = sorted(solids[col])
        blocks = [0] + [rock + 1 for rock in local_solids] + [max_row]
        rocks = {k: 0 for k in blocks}
        block_ind = 0
        block = blocks[block_ind]
        for rock in sorted(rounds[col]):
            while rock >= blocks[block_ind + 1]:
                block_ind += 1
                block = blocks[block_ind]
            rocks[block] += 1
        
        for start in rocks:
            for i in range(rocks[start]):
                new_rounds.append((start + i, col))
    return new_rounds

def rotate_coords(rounds, solids, max_row):
    new_rounds = [(rock[1], max_row - rock[0] - 1) for rock in rounds]
    new_solids = [(rock[1], max_row - rock[0] - 1) for rock in solids]
    return new_rounds, new_solids

def print_rocks(rounds, solids, max_row, max_col):
    for row in range(max_row):
        s = ''
        for col in range(max_col):
            if (row, col) in rounds:
                s += 'O'
            elif (row, col) in solids:
                s += '#'
            else:
                s += '.'
        print(s)
    print()

def solve(inp, part, example):
    round, solid, max_row, max_col = inp
    if part == 1:
        round = roll_north(round, solid, max_row, max_col)
        return sum(max_row - rock[0] for rock in round)
    seen = {}
    cycle = 0
    while cycle < 1_000_000_000:
        for dir in range(4):
            round = roll_north(round, solid, max_row, max_col)
            round, solid = rotate_coords(round, solid, max_row)
        cycle += 1
        key = tuple(round)
        if key in seen:
            diff = cycle - seen[key]
            cycle += (1_000_000_000 - cycle) // diff * diff
        else:
            seen[key] = cycle
    return sum(max_row - rock[0] for rock in round)

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
