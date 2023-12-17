from copy import deepcopy

def parse_input(file = 'day16.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day16example.txt')

def format_input(inp: list[str]):
    return inp

def energize_grid(starting_laser, grid):
    lasers = [starting_laser]
    energized = set()
    seen = set()
    while lasers:
        for laser in lasers:
            if tuple(laser) in seen:
                lasers.remove(laser)
                continue
            seen.add(tuple(laser))
            if laser[2] == 0:
                laser[0] -= 1
            elif laser[2] == 1:
                laser[1] += 1
            elif laser[2] == 2:
                laser[0] += 1
            else:
                laser[1] -= 1
            if -1 in laser:
                lasers.remove(laser)
                continue
            try:
                c = grid[laser[0]][laser[1]]
            except IndexError:
                lasers.remove(laser)
                continue
            energized.add((laser[0], laser[1]))
            if c == '/':
                if laser[2] in (1, 3):
                    laser[2] -= 1
                else:
                    laser[2] += 1
            elif c == '\\':
                if laser[2] in (1, 3):
                    laser[2] += 1
                else:
                    laser[2] -= 1
            elif c == '|':
                if laser[2] in (1, 3):
                    lasers.append([laser[0], laser[1], 0])
                    lasers.append([laser[0], laser[1], 2])
                    lasers.remove(laser)
            elif c == '-':
                if laser[2] in (0, 2):
                    lasers.append([laser[0], laser[1], 1])
                    lasers.append([laser[0], laser[1], 3])
                    lasers.remove(laser)
            laser[2] %= 4
    return len(energized)

def solve(grid, part, example):
    if part == 1:
        return energize_grid([0, -1, 1], grid)
    max_energized = 0
    for row in range(len(grid)):
        max_energized = max(max_energized, energize_grid([row, -1, 1], grid))
        max_energized = max(max_energized, energize_grid([row, len(grid[0]), 3], grid))
    for col in range(len(grid)):
        max_energized = max(max_energized, energize_grid([-1, col, 2], grid))
        max_energized = max(max_energized, energize_grid([len(grid), col, 0], grid))
    return max_energized

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
