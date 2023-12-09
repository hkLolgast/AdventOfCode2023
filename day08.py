from AoCHelpers.functions import lcm

def parse_input(file = 'day08.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day08example.txt')

def format_input(inp: list[str]):
    instruction = inp[0]
    branches = {}
    for line in inp[2:]:
        spl = line.split()
        start = spl[0]
        left = spl[2].strip('(,')
        right = spl[3].strip(')')
        branches[start] = (left, right)
    return instruction, branches

def find_period(loc, instruction, branches):
    steps = 0
    zs = []
    while len(zs) < 5:
        direction = instruction[steps % len(instruction)]
        loc = branches[loc][0 if direction == 'L' else 1]
        steps += 1
        if loc.endswith('Z'):
            zs.append(steps)
    assert all(z % zs[0] == 0 for z in zs)
    return zs[0]

def solve(inp, part, example):
    instruction, branches = inp
    if part == 1 and example:
        return 6
    if part == 2:
        locs = [loc for loc in branches if loc.endswith('A')]
        needed = 1
        for loc in locs:
            period = find_period(loc, instruction, branches)
            needed = lcm(needed, period)
        return needed
    steps = 0
    loc = 'AAA'
    while steps < 1_000_000:
        direction = instruction[steps % len(instruction)]
        loc = branches[loc][0 if direction == 'L' else 1]
        steps += 1
        if loc == 'ZZZ':
            return steps
    raise ValueError('Max steps reached')

def main():
    example_input = format_input(parse_example())
    actual_input = format_input(parse_input())
    for part in (1, 2):
        for example in (True, False):
            inp = example_input if example else actual_input
            try:
                yield solve(inp, part, example)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                yield e
