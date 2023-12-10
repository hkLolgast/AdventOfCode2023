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
    steps = 1
    prev = [start, start]
    path = [start]
    frontloop = []
    backloop = []
    while steps < len(inp) * len(inp[0]):
        steps += 1
        new_path = []
        frontloop.append(current[0])
        backloop.append(current[1])
        for i in range(len(current)):
            loc = current[i]
            new_path.append(connections(prev[i], loc, inp[loc[0]][loc[1]]))
        prev = current[:]
        current = new_path[:]
        if any(current.count(loc) == 2 for loc in current):
            if part == 1:
                return len(frontloop) + 1
            path = [start] + frontloop + [current[0]] + backloop[::-1]
            break
    
    amount_inside = 0
    for row in range(len(inp)):
        opener = ''
        inside = False
        for col in range(len(inp[0])):
            loc = (row, col)
            ch = inp[row][col]
            if loc in path:
                if not opener:
                    if ch == '|':
                        inside = not inside
                    else:
                        opener = ch
                elif ch != '-':
                    if (opener == 'F' and ch == 'J') or (opener == 'L' and ch == '7'):
                        inside = not inside
                    opener = ''
            elif inside:
                amount_inside += 1
    return amount_inside


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
