def parse_input(file = 'day09.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day09example.txt')

def format_input(inp: list[str]):
    return [list(map(int, line.split())) for line in inp]

def calculate_next(series):
    diffs = [series]
    while not all(v == 0 for v in diffs[-1]):
        diffs.append([diffs[-1][i] - diffs[-1][i - 1] for i in range(1, len(diffs[-1]))])
    for i in range(len(diffs) - 2, -1, -1):
        diffs[i].append(diffs[i][-1] + diffs[i + 1][-1])
    return diffs[0][-1]

def calculate_first(series):
    diffs: list[list] = [series]
    while not all(v == 0 for v in diffs[-1]):
        diffs.append([diffs[-1][i] - diffs[-1][i - 1] for i in range(1, len(diffs[-1]))])
    for i in range(len(diffs) - 2, -1, -1):
        diffs[i].insert(0, diffs[i][0] - diffs[i + 1][0])
    return diffs[0][0]

def solve(inp, part, example):
    tot = 0
    for line in inp:
        tot += calculate_next(line) if part == 1 else calculate_first(line)
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
