from copy import deepcopy

def parse_input(file = 'day15.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day15example.txt')

def format_input(inp: list[str]):
    return inp[0].split(',')

def hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h

def solve(inp, part, example):
    if part == 1:
        return sum(hash(p) for p in inp)
    boxes = [[] for _ in range(256)]
    for inst in inp:
        if '=' in inst:
            label, focal = inst.split('=')
            box = hash(label)
            for i, lens in enumerate(boxes[box][:]):
                if lens[0] == label:
                    boxes[box].remove(lens)
                    boxes[box].insert(i, (label, focal))
                    break
            else:
                boxes[box].append((label, focal))
        else:
            label = inst.rstrip('-')
            box = hash(label)
            for lens in boxes[box]:
                if lens[0] == label:
                    boxes[box].remove(lens)
                    break
    tot = 0
    for i, box in enumerate(boxes):
        for j, (label, focal_length) in enumerate(box):
            tot += (1 + i) * (1 + j) * int(focal_length)
    return tot

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
