from copy import deepcopy

def parse_input(file = 'day17.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day17example.txt')

def format_input(inp: list[str]):
    map = {}
    for r in range(len(inp)):
        for c in range(len(inp[0])):
            map[(r, c)] = int(inp[r][c])
    return map, len(inp), len(inp[0])

def solve(inp, part, example):
    map, max_row, max_col = inp
    min_paths = {loc + (d * l,): 10 * max_row * max_col for loc in map.keys() for d in '^>V<' for l in (range(1, 4) if part == 1 else range(4, 11))}
    min_paths[(0, 0, '')] = 0
    to_check = set()
    to_check.add((0, 0, ''))
    seen  = set()
    while to_check:
        row, col, past = to_check.pop()
        seen.add((row, col, past))
        for dir in range(4):
            s = '^>V<'[dir]
            if '^>V<'[(dir + 2) % 4] in past:
                continue
            if past.startswith(3 * s):
                continue
            new_s = past if s in past else ''
            loc = [row, col]
            new_score = min_paths[(row, col, past)]
            for amount in range(3 if part == 1 else 10):
                new_s += s
                if len(new_s) == (4 if part == 1 else 11):
                    break
                if dir == 0:
                    loc[0] -= 1
                elif dir == 1:
                    loc[1] += 1
                elif dir == 2:
                    loc[0] += 1
                else:
                    loc[1] -= 1
                if tuple(loc) not in map:
                    break
                new_score += map[tuple(loc)]
                if part == 2 and len(new_s) < 4:
                    continue
                key = tuple(loc) + (new_s,)
                if new_score < min_paths[key]:
                    for am2 in range((4 if part == 1 else 11) - len(new_s)):
                        new_key = tuple(loc) + (new_s + s * am2,)
                        if new_score < min_paths[new_key]:
                            min_paths[new_key] = new_score
                    to_check.add(key)
    best = 10**99
    for d in '^>V<':
        for l in (range(1, 4) if part == 1 else range(4, 11)):
            best = min(best, min_paths[max_row - 1, max_col - 1, d * l])
    return best


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
