def parse_input(file = 'day01.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day01example.txt')

def format_input(inp: list[str]):
    return inp

def solve(inp: list[str], part, example):
    s = 0
    if part == 2:
        for line in inp:
            first = None
            for i in range(len(line)):
                try:
                    v = int(line[i])
                    first = line[i]
                    break
                except ValueError:
                    pass
                for j, num in enumerate(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']):
                    if line[i:].startswith(num):
                        first = str(j)
                        break
                if first:
                    break
            for i in range(len(line)-1, -1, -1):
                try:
                    v = int(line[i])
                    s += int(first + str(v))
                    break
                except ValueError:
                    pass
                for j, num in enumerate(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']):
                    if line[i:].startswith(num):
                        s += int(first + str(j))
                        break
                else:
                    continue
                break

        return s
    for line in inp:
        for c in line:
            try:
                v = int(c)
                first = c
                break
            except ValueError:
                continue
        for c in line[::-1]:
            try:
                v = int(c)
                s += int(first + c)
                break
            except ValueError:
                continue
    return s

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
