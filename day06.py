def parse_input(file = 'day06.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day06example.txt')

def format_input(inp: list[str]):
    times = list(map(int, inp[0].split()[1:]))
    distances = list(map(int, inp[1].split()[1:]))
    return times, distances

def solve(inp, part, example):
    times, distances = inp
    if part == 2:
        s = ''
        for t in times:
            s += str(t)
        times = [int(s)]
        s = ''
        for d in distances:
            s += str(d)
        distances = [int(s)]
    tot = 1
    for race in range(len(times)):
        t = times[race]
        d = distances[race]
        wins = 0
        for charge in range(1, t):
            dist = (t - charge) * charge
            if dist > d:
                wins += 1
        tot *= wins
    return tot

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
