def parse_input(file = 'day05.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day05example.txt')

def create_map(lines):
    m = {}
    i = 0
    while lines[i] != '':
        dest, source, length = list(map(int, lines[i].split()))
        m[source] = (dest, length)
        i += 1
        if i == len(lines):
            break
    return m

def format_input(inp: list[str]):
    seeds = list(map(int, inp[0].split()[1:]))
    i = 3
    maps = []
    for j in range(7):
        new_map = create_map(inp[i:])
        maps.append(new_map)
        i+= len(new_map) + 2
    return seeds, maps

def find(entry, map):
    for k in map.keys():
        if k <= entry < k + map[k][1]:
            offset = entry - k
            return map[k][0] + offset
    return entry

def reverse_find(dest, map):
    for k in map.keys():
        d = map[k][0]
        if d <= dest < d + map[k][1]:
            return k + dest - d, k
    return dest, None

def solve(inp, part, example):
    if part == 1:
        seeds, maps = inp
        locations = []
        for seed in seeds:
            entry = seed
            for m in maps:
                entry = find(entry, m)
            locations.append(entry)
        return min(locations)
    
    seed_inp, maps = inp
    seed_ranges = []
    for i in range(0, len(seed_inp), 2):
        seed_ranges.append((seed_inp[i], seed_inp[i] + seed_inp[i + 1]))
    start_dest = 0
    min_jump = 10**99
    iters = 0
    while True:
        iters += 1
        if iters == 10_000:
            raise ValueError('Could not find solution')
        source = start_dest
        for m in maps[::-1]:
            dest = source
            source, k = reverse_find(dest, m)
            if k is not None:
                dest_start, length = m[k]
                offset = dest - dest_start
                min_jump = min(min_jump, length - offset)

        for r in seed_ranges:
            if r[0] <= source < r[1]:
                return start_dest
        if min_jump == 10**99:
            raise ValueError('Could not find solution')
        start_dest += min_jump

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
