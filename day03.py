from AoCHelpers import optimization

def parse_input(file = 'day03.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day03example.txt')

def format_input(inp: list[str]):
    numbers = []
    symbols = []
    number = ''
    number_poss = []
    for y, line in enumerate(inp):
        for x, c in enumerate(line):
            if c in '0123456789':
                number += c
                number_poss.append((x, y))
                continue
            if c != '.':
                symbols.append((c, (x, y)))
            if number:
                numbers.append((int(number), number_poss))
                number = ''
                number_poss = []
        if number:
            numbers.append((int(number), number_poss))
            number = ''
            number_poss = []
    return numbers, symbols

def is_part_number(poss, symbols):
    for pos in poss:
        for neighbor in optimization.ALL_DIRECT(pos):
            if any(symbol[1] == neighbor for symbol in symbols):
                return True
    return False

def solve(inp, part, example):
    numbers, symbols = inp
    tot = 0
    if part == 1:
        for v, poss in numbers:
            if is_part_number(poss, symbols):
                if example:
                    print(v)
                tot += v
    else:
        for symbol in symbols:
            if symbol[0] != '*':
                continue
            adjacent = []
            for v, poss in numbers:
                if any(neighbor in poss for neighbor in optimization.ALL_DIRECT(symbol[1])):
                    adjacent.append(v)
            if len(adjacent) == 2:
                tot += adjacent[0] * adjacent[1]
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
