def parse_input(file = 'day07.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day07example.txt')

def format_input(inp: list[str]):
    return [(line.split()[0], int(line.split()[1])) for line in inp]

def score(hand: str):
    cards = [c for c in set(hand)]
    cards = sorted(cards, key = lambda c: hand.count(c), reverse=True)
    if hand.count(cards[0]) == 5:
        return 6
    if hand.count(cards[0]) == 4:
        return 5
    if hand.count(cards[0]) == 3:
        if hand.count(cards[1]) == 2:
            return 4
        return 3
    if hand.count(cards[0]) == 2:
        if hand.count(cards[1]) == 2:
            return 2
        return 1
    return 0

def solve(inp: list[str, int], part, example):
    def sort_key(hand):
        label_score = []
        for card in hand:
            if part == 1:
                label_score.append('23456789TJQKA'.index(card))
            else:
                label_score.append('J23456789TQKA'.index(card))
        if part == 1:
            sc = score(hand)
        else:
            scores = [score(hand.replace('J', c)) for c in '23456789TQKA']
            sc = sorted(scores)[-1]
        return (sc, tuple(label_score))
    
    sorted_hands = sorted([hand for hand, bid in inp], key = sort_key)
    return sum((sorted_hands.index(hand) + 1) * bid for hand, bid in inp)

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
