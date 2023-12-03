def parse_input(file = 'day02.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day02example.txt')

def format_input(inp: list[str]):
    games = []
    for line in inp:
        spl = line.split()
        id = int(spl[1].rstrip(':'))
        rounds = []
        round = []
        for ind in range(2, len(spl), 2):
            am = int(spl[ind])
            color = spl[ind+1]
            round.append((color.rstrip(',;'), am))
            if color.endswith(';'):
                rounds.append(round)
                round = []
        rounds.append(round)
        games.append((id, rounds))
    return games

def is_valid(rounds, limits):
    for round in rounds:
        for color, am in round:
            if am > limits[color]:
                return False
    return True

def solve(games, part, example):
    lims = {
        'blue': 14,
        'green': 13,
        'red': 12
    }
    poss = []
    tot = 0
    for id, rounds in games:
        if part == 1:
            if is_valid(rounds, lims):
                if example:
                    print(id)
                poss.append(id)
        else:
            colors = {'red': 0, 'green': 0, 'blue': 0}
            for round in rounds:
                for color, am in round:
                    colors[color] = max(colors[color], am)
            tot += colors['red'] * colors['green'] * colors['blue']
    if part == 1:
        return sum(poss)
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
