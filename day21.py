from copy import deepcopy
from functools import reduce
from AoCHelpers.optimization import ORTHOGONAL

def parse_input(file = 'day21.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day21example.txt')

class Map(dict):
    def __missing__(self, key):
        if self.part == 1:
            return 0
        r, c = key
        return self[r % self.max_row, c % self.max_col]

def format_input(inp: list[str]):
    map = Map()
    for r, row in enumerate(inp):
        for c, char in enumerate(row):
            map[r, c] = 0 if char == '#' else 1
            if char == 'S':
                start = (r, c)
    map.max_row = len(inp)
    map.max_col = len(inp[0])
    return map, start

def solve(inp, part, example):
    map, start = inp
    map.part = part
    if part == 1:
        max_steps = 6 if example else 64
    else:
        max_steps = max(4 * map.max_row, 100)
        target = 26501365
    visited = [set(), set()]
    visited[0].add(start)
    last = set()
    last.add(start)
    total = []
    for step in range(1, max_steps + 1):
        new = set()
        for loc in last:
            for neigh in ORTHOGONAL(loc):
                if neigh not in visited[step % 2] and map[neigh]:
                    new.add(neigh)
        visited[step % 2].update(new)
        last = new
        if part == 2 and step % map.max_row == target % map.max_row:
            total.append(len(visited[step % 2]))
    if part == 1:
        return len(visited[max_steps % 2])
    diffs = [x - y for x, y in zip(total[1:], total)]
    diff2s = [x - y for x, y in zip(diffs[1:], diffs)]
    assert diff2s[-1] == diff2s[-2]
    amount = total[-1]
    diff = diffs[-1]
    beginning = len(total) * map.max_row + target % map.max_row
    for step in range(beginning, target + 1, map.max_row):
        diff += diff2s[-1]
        amount += diff
    return amount

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
