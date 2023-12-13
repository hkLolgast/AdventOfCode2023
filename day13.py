from copy import deepcopy

def parse_input(file = 'day13.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day13example.txt')

def format_input(inp: list[str]):
    patterns = []
    pattern = []
    for line in inp:
        if line == '':
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    return patterns

def find_mirror(pattern, smudged, flipped = False):
    matches = {}
    near_matches = {}
    for i, row in enumerate(pattern[:-1]):
        matches[i] = []
        near_matches[i] = []
        for j in range(i + 1, len(pattern)):
            if pattern[j] == pattern[i]:
                matches[i].append(j)
            if smudged:
                diffs = 0
                for k in range(len(row)):
                    if pattern[i][k] != pattern[j][k]:
                        diffs += 1
                        if diffs == 2:
                            break
                else:
                    near_matches[i].append(j)

    for mirror in range(1, len(pattern)):
        near = 0
        for i in range(0, mirror):
            opposite = mirror + (mirror - i - 1)
            if opposite >= len(pattern):
                continue
            if opposite not in matches[i]:
                if not smudged:
                    break
                if opposite not in near_matches[i]:
                    break
                near += 1
                if near == 2:
                    break
        else:
            if not smudged or near == 1:
                return mirror * 100
    if flipped:
        raise ValueError
    cols = [''.join(line[i] for line in pattern) for i in range(len(pattern[0]))]
    return find_mirror(cols, smudged) // 100

def solve(inp, part, example):
    return sum(find_mirror(pattern, part == 2) for pattern in inp)

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
