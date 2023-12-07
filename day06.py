def parse_input(file = 'day06.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day06example.txt')

def format_input(inp: list[str]):
    times = inp[0].split()[1:]
    distances = inp[1].split()[1:]
    return times, distances

def distance(charge_time, total_time):
    return charge_time * (total_time - charge_time)

def find(min_time, max_time, total_time, min_distance, depth = 0):
    if max_time - min_time == 1:
        return max_time
    avg = (max_time + min_time) // 2
    if distance(avg, total_time) > min_distance:
        return find(min_time, avg, total_time, min_distance, depth + 1)
    return find(avg, max_time, total_time, min_distance, depth + 1)

def solve(inp, part, example):
    times, distances = inp
    if part == 2:
        times = [''.join(times)]
        distances = [''.join(distances)]
    times = list(map(int, times))
    distances = list(map(int, distances))
    tot = 1
    for race in range(len(times)):
        charge = find(0, times[race], times[race], distances[race])
        tot *= times[race] - 2 * charge + 1
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
