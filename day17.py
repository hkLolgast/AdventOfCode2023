from copy import deepcopy
from AoCHelpers.optimization import Pathfinder, ORTHOGONAL

def parse_input(file = 'day17.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day17example.txt')

def format_input(inp: list[str]):
    map = {}
    for r in range(len(inp)):
        for c in range(len(inp[0])):
            map[(r, c)] = int(inp[r][c])
    return map, len(inp), len(inp[0])

class CrucibleFinder(Pathfinder):
    def __init__(self, *args, example = False, **kwargs):
        self.example = example
        super().__init__(*args, **kwargs)

    def apply_move(self, state, move):
        return state + [move]
    
    def is_valid_location(self, loc):
        return loc in self.map

    def is_valid_move(self, state, move):
        if not self.is_valid_location(move):
            return False
        last = state[-4:]
        if len(last) > 1:
            if last[-2] == move:
                return False
        if len(last) == 4:
            if all(loc[0] == move[0] for loc in last) or all(loc[1] == move[1] for loc in last):
                return False
        if state.count(move) == 2:
            return False
        return True
        
    def get_valid_moves(self, state):
        return [move for move in self.neighbors(state[-1]) if self.is_valid_move(state, move)]

    def score_state(self, state):
        score = 10 * sum(state[-1])
        for loc in state[1:]:
            score -= self.map[loc]
        return score

    def get_state_hash(self, state):
        return tuple(state)

    def is_finished(self, state):
        # if self.example:
        #     print(state)
        return state[-1] == self.solved_state_hash

def solve(inp, part, example):
    map, max_row, max_col = inp
    p = CrucibleFinder(map, [(0, 0)], (max_row - 1, max_col - 1), states_to_keep = 1000, find_all_solutions = True, max_steps = 2 * (max_row + max_col), example = example)
    p.neighbors = ORTHOGONAL
    sols = p.get_minimal_path()
    min_loss = 966
    best_path = None
    for score, path in sols:
        loss = 0
        for loc in path[1:]:
            loss += map[loc]
        if loss < min_loss:
            min_loss = loss
            best_path = path
    if example:
        print(best_path)
    return min_loss

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
