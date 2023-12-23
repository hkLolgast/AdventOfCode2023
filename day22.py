from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day22.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day22example.txt')

def format_input(inp: list[str]):
    grid = defaultdict(int)
    blocks = []
    for line in inp:
        start, end = line.split('~')
        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))
        block = []
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    block.append((x, y, z))
                    grid[x, y, z] = 1
        blocks.append(tuple(sorted(block, key = lambda b: b[2])))
    return blocks, grid

def fall_blocks(grid, blocks, example):
    moving = True
    while moving:
        moving = False
        new_blocks = []
        for block in blocks:
            if all (z > 1 and ((not grid[x, y, z - 1]) or (x, y, z - 1) in block) for x, y, z in block):
                new_block = []
                for x, y, z in block:
                    grid[x, y, z] = 0
                    grid [x, y, z - 1] = 1
                    new_block.append((x, y, z - 1))
                new_blocks.append(tuple(new_block))
                moving = True
            else:
                new_blocks.append(block)
        blocks = new_blocks
    return grid, blocks

def supports(block, blocks_by_z):
    supportees = set()
    for x, y, z in block:
        try:
            for block2 in blocks_by_z[z + 1]:
                if block != block2 and any(loc[0] == x and loc[1] == y for loc in block2):
                    supportees.add(block2)
                    break
        except:
            pass
    return supportees

def total_falls(start_block, supporters, supportees):
    falling = set()
    to_check = set()
    falling.add(start_block)
    to_check.add(start_block)
    while to_check:
        block = to_check.pop()
        for block2 in supportees[block]:
            if all(block3 in falling.union(to_check) for block3 in supporters[block2]):
                falling.add(block2)
                to_check.add(block2)
    return len(falling)

def solve(inp, part, example):
    blocks, grid = inp
    blocks = sorted(blocks, key = lambda b: b[0][2])
    grid, blocks = fall_blocks(grid, blocks, example)
    blocks = sorted(blocks, key = lambda b: b[0][2])
    max_z = max(block[-1][2] for block in blocks)
    blocks_by_z = {z: [block for block in blocks if any(loc[2] == z for loc in block)] for z in range(1, max_z + 1)}
    unsafe = set()
    supporters = defaultdict(list)
    supportees = defaultdict(list)
    for block in blocks:
        for block2 in supports(block, blocks_by_z):
            supporters[block2].append(block)
            supportees[block].append(block2)

    if part == 1:
        for block in supporters:
            if len(supporters[block]) == 1:
                unsafe.add(supporters[block][0])
        return len(blocks) - len(unsafe)
    
    return sum(total_falls(block, supporters = supporters, supportees = supportees) - 1 for block in blocks)



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
