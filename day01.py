def parse_input(file = 'day01.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day01example.txt')

def format_input(inp: list[str]):
    return inp

def find_first(line, include_written):
    subs = list(map(str, range(10)))
    if include_written:
        subs += ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']        
    for i in range(len(line)):
        for v, s in enumerate(subs):
            if line[i:].startswith(s):
                return v % 10
            
def find_last(line, include_written):
    subs = list(map(str, range(10)))
    if include_written:
        subs += ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']        
    for i in range(len(line) - 1, -1, -1):
        for v, s in enumerate(subs):
            if line[i:].startswith(s):
                return v % 10

def solve(inp: list[str], part, example):
    s = 0
    for line in inp:
        first = str(find_first(line, part == 2))
        last = str(find_last(line, part == 2))
        try:
            s += int(first + last)
        except:
            if not example:     # Example for part 2 has invalid input for 1
                print(line)
                raise
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
