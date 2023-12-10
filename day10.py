from copy import deepcopy

def parse_input(file = 'day10.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day10example.txt')

def format_input(inp: list[str]):
    return inp

def neighbors(row, column, gridsize):
    neigh = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        r = row + dr
        c = column + dc
        if 0 < r < gridsize[0] and 0 < c < gridsize[1]:
            neigh.append((r, c))
    return neigh

def connections(prev, current, pipe_type):
    r, c = current
    if pipe_type == '-':
        return (r, c + 1) if prev == (r, c - 1) else (r, c - 1)
    if pipe_type == '|':
        return (r + 1, c) if prev == (r - 1, c) else (r - 1, c)
    if pipe_type == '7':
        return (r + 1, c) if prev == (r, c - 1) else (r, c - 1)
    if pipe_type == 'J':
        return (r, c - 1) if prev == (r - 1, c) else (r - 1, c)
    if pipe_type == 'L':
        return (r - 1, c) if prev == (r, c + 1) else (r, c + 1)
    if pipe_type == 'F':
        return (r, c + 1) if prev == (r + 1, c) else (r + 1, c)
    
def solve(inp, part, example):
    for row, line in enumerate(inp):
        if 'S' in line:
            start = (row, line.index('S'))
            break
    current = []
    if start[0] > 0:
        if inp[start[0] - 1][start[1]] in '|F7':
            current.append((start[0] - 1, start[1]))
    if start[0] < len(inp) - 1:
        if inp[start[0] + 1][start[1]] in '|LJ':
            current.append((start[0] + 1, start[1]))
    if start[1] > 0:
        if inp[start[0]][start[1] - 1] in '-FL':
            current.append((start[0], start[1] - 1))
    if start[1] < len(inp[0]) - 1:
        if inp[start[0]][start[1] + 1] in '-J7':
            current.append((start[0], start[1] + 1))
    assert len(current) == 2
    replacements = {
        ((0, 1), (0, -1)): '-',
        ((1, 0), (-1, 0)): '|',
        ((0, 1), (1, 0)): 'F',
        ((0, -1),  (-1, 0)): 'J',
        ((0, 1), (-1, 0)): 'L',
        ((0, -1), (1, 0)): '7'
    }
    for coords in replacements:
        if all((start[0] + dr, start[1] + dc) in current for (dr, dc) in coords):
            inp[start[0]] = inp[start[0]].replace('S', replacements[coords])
            break
        
    steps = 1
    prev = [start, start]
    path = [start]
    while steps < len(inp) * len(inp[0]):
        steps += 1
        new_locs = []
        for i in range(len(current)):
            loc = current[i]
            path.append(loc)
            new_locs.append(connections(prev[i], loc, inp[loc[0]][loc[1]]))
        prev = current[:]
        current = new_locs[:]
        if any(current.count(loc) == 2 for loc in current):
            path.append(current[0])
            if part == 1:
                return len(path) // 2
            break

    paths_by_row = {}
    for r, c in path:
        if inp[r][c] == '-':
            continue
        if r not in paths_by_row:
            paths_by_row[r] = []
        paths_by_row[r].append(c)
    for r in paths_by_row:
        paths_by_row[r] = sorted(paths_by_row[r])

    amount_inside = 0
    for row in paths_by_row:
        prev = ('', 0)
        inside = False
        for col in paths_by_row[row]:
            ch = inp[row][col]
            if ch in '|FL' and inside:
                amount_inside += col - prev[1] - 1
            if ch == '|' or (ch == '7' and prev[0] == 'L') or (ch == 'J' and prev[0] == 'F'):
                inside = not inside
            prev = (ch, col)
    return amount_inside


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
