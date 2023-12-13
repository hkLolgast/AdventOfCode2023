from copy import deepcopy

def parse_input(file = 'day12.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day12example.txt')

def format_input(inp: list[str]):
    data = []
    for line in inp:
        springs, contiguous = line.split()
        contiguous = list(map(int, contiguous.split(',')))
        data.append((springs, contiguous))
    return data

def memoize(func):
    cache = {}
    def wrapper(springs, contiguous, debug = False, *args):
        key = (springs, tuple(contiguous))
        if key not in cache:
            cache[key] = func(springs, contiguous, debug, *args)
        if debug:
            print(springs, contiguous, cache[key])
        return cache[key]
    return wrapper
        
@memoize
def find_ways(springs: str, contiguous: list[int], debug = False, depth = 0):
    # if debug:
    #     print(springs, contiguous)
    if len(springs) < sum(contiguous) + len(contiguous) - 1:
        return 0
    if not contiguous:
        return int('#' not in springs)
    elif not springs:
        # if debug:
        #     print('here', springs, contiguous, int(sum(contiguous) == 0))
        return int(sum(contiguous) == 0)
    # if contiguous[0] == 0:
    #     if springs[0] == '#':
    #         return 0
    #     return find_ways(springs[1:], contiguous[1:], debug, depth + 1)
    if springs.startswith('.'):
        return find_ways(springs[1:], contiguous, debug, depth + 1)
    if springs.startswith('#' * (contiguous[0] + 1)):
        return 0
    if springs[0] == '#':
        if '.' in springs[:contiguous[0]]:
            return 0
        if len(springs) == contiguous[0]:
            return int(len(contiguous) == 1)
        if springs[contiguous[0]] == '#':
            return 0
        return find_ways(springs[contiguous[0] + 1:], contiguous[1:], debug, depth + 1)
        # return find_ways(springs[1:], [contiguous[0] - 1] + contiguous[1:])
    
    v1 = find_ways('#' + springs[1:], contiguous, debug, depth + 1)
    v2 = find_ways(springs[1:], contiguous, debug, depth + 1)
    if debug:
        print('\t' * depth, contiguous, '#' + springs[1:], v1, '.' + springs[1:], v2)
    return (v1 + v2)
        
def solve(inp, part, example):
    total = 0
    for i, (springs, contiguous) in enumerate(inp):
        if part == 2:
            springs = springs + 4 * ('?' + springs)
            contiguous *= 5
        am = find_ways(springs, contiguous)
        total += am
    return total

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
