from collections import defaultdict
from copy import deepcopy
from AoCHelpers.optimization import ORTHOGONAL

def parse_input(file = 'day23.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day23example.txt')

def format_input(inp: list[str]):
    map = defaultdict(lambda: '#')
    for r, row in enumerate(inp):
        for c, char in enumerate(row):
            map[r, c] = char
    map[0, 1] = '#'
    map[len(inp) - 1, len(inp[0]) - 2] = '#'
    return map, (len(inp) - 2, len(inp[0]) - 2)

def find_paths(distances, dest, path):
    for neigh in distances[path[-1]]:
        if neigh == dest:
            yield [neigh]
        elif neigh not in path:
            for path2 in find_paths(distances, dest, path + [neigh]):
                yield [neigh] + path2

def find_length(distances, path):
    dist = 0
    for n1, n2 in zip(path, path[1:]):
        dist += distances[n1][n2]
    return dist

def solve(inp, part, example):
    chart, dest = inp
    start = (1, 1)
    def valid_neighbors(loc, ignore_slopes):
        neighs = ORTHOGONAL(loc)
        valid_neighs = []
        for neigh in neighs:
            char = chart[neigh]
            if char == '#':
                continue
            if char == '.' or ignore_slopes:
                valid_neighs.append(neigh)
            elif char == '>' and neigh[1] > loc[1]:
                valid_neighs.append(neigh)
            elif char == 'v' and neigh[0] > loc[0]:
                valid_neighs.append(neigh)
            elif char == '<' and neigh[1] < loc[1]:
                valid_neighs.append(neigh)
            elif char == '^' and neigh[0] < loc[0]:
                valid_neighs.append(neigh)
        return valid_neighs
    nodes = [start, dest]
    for r in range(1, dest[0] + 1):
        for c in range(1, dest[1] + 1):
            if chart[(r, c)] == '#':
                continue
            if len(valid_neighbors((r, c), True)) > 2:
                nodes.append((r, c))

    distances = {}
    for node in nodes:
        if node == dest:
            continue
        distances[node] = {}
        paths = [[node, neigh] for neigh in valid_neighbors(node, part == 2)]
        steps = 1
        while paths:
            steps += 1
            for path in paths[:]:
                for neigh in valid_neighbors(path[-1], part == 2):
                    if neigh == path[-2]:
                        continue
                    if neigh in nodes:
                        distances[node][neigh] = steps
                        paths.remove(path)
                        break
                    else:
                        path.append(neigh)
                        break

    paths = find_paths(distances, dest, [start])
    return max(find_length(distances, [start] + path) + 2 for path in paths)

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
