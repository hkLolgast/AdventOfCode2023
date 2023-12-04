def parse_input(file = 'day04.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day04example.txt')

def format_input(inp: list[str]):
    cards = []
    for line in inp:
        numbers = line.split(':')[1]
        winning, mine = numbers.split('|')
        cards.append(([int(v) for v in winning.split()], [int(v) for v in mine.split()]))
    return cards

def points(winning, numbers):
    amount = len([n for n in numbers if n in winning])
    if amount:
        return 2**(amount - 1)
    else:
        return 0

def solve(cards, part, example):
    total = 0
    if part == 1:
        for card in cards:
            total += points(card[0], card[1])
    else:
        prizes = {}
        for id, (winning, numbers) in enumerate(cards):
            prizes[id + 1] = len([n for n in numbers if n in winning])
        owned = {i + 1: 1 for i in range(len(cards))}
        for i in range(len(cards)):
            if owned[i + 1] > 0:
                total += owned[i + 1]
                for prize in range(prizes[i + 1]):
                    owned[i + 2 + prize] += owned[i + 1]
                owned[i + 1] = 0

    return total

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
