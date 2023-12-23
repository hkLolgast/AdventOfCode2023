from copy import deepcopy

def parse_input(file = 'day20.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day20example.txt')

class Module(object):
    def __init__(self, name, mod_type, targets: list[str]):
        self.name = name
        self.mod_type = mod_type
        self.targets = targets
        self.on = False
        if self.mod_type == '%':
            self.handle = self.handle_flipflop
        elif self.mod_type == '&':
            self.handle = self.handle_conjunction
            self.inputs = {}
        else:
            raise ValueError(mod_type)

    def handle_flipflop(self, pulse, source):
        if pulse == 'high':
            return []
        assert pulse == 'low'
        if self.on:
            self.on = False
            return [(target, 'low', self.name) for target in self.targets]
        self.on = True
        return [(target, 'high', self.name) for target in self.targets]
        

    def handle_conjunction(self, pulse, source):
        self.inputs[source] = pulse
        if all(self.inputs[src] == 'high' for src in self.inputs):
            return [(target, 'low', self.name) for target in self.targets]
        return [(target, 'high', self.name) for target in self.targets]
    
    def is_in_starting_state(self):
        if self.mod_type == '%':
            return not self.on
        return all(v == 'low' for v in self.inputs.values())
        
    def state(self):
        if self.mod_type == '%':
            return self.on
        return tuple([self.inputs[k] for k in sorted(self.inputs.keys())])

def format_input(inp: list[str]):
    modules = {}
    for line in inp:
        module, targets = line.split(' -> ')
        targets = targets.split(', ')
        if module == 'broadcaster':
            broadcaster = targets
            continue
        mod_type = module[0]
        module = module[1:]
        modules[module] = Module(module, mod_type, targets)
    
    for module_id in modules:
        module = modules[module_id]
        for target in module.targets:
            if target in modules:
                target_module = modules[target]
                if target_module.mod_type == '&':
                    target_module.inputs[module_id] = 'low'
    for target in broadcaster:
        if target in modules:
            target_module = modules[target]
            if target_module.mod_type == '&':
                target_module.inputs['broadcaster'] = 'low'
    return modules, broadcaster

def press_button(modules, broadcaster, pulse_counts, to_watch = []) -> set[str]:
    pulses = [(t, 'low', 'broadcaster') for t in broadcaster]
    pulse_counts['low'] += 1        # button -> broadcaster
    checked = []
    while pulses:
        target, pulse, source = pulses.pop(0)
        if source in to_watch and pulse == 'high':
            checked.append(source)
        pulse_counts[pulse] += 1
        if target in modules:
            module = modules[target]
            pulses.extend(module.handle(pulse, source))
    return checked

def solve(inp: tuple[dict[str, Module], list[str]], part, example):
    modules, broadcaster = inp
    pulse_counts = {'low': 0, 'high': 0}
    if part == 2 and example:
        return None
    if part == 1:
        for _ in range(1000):
            press_button(modules, broadcaster, pulse_counts)
        return pulse_counts['low'] * pulse_counts['high']
    
    presses = 0
    to_check = None
    for mod in modules:
        if 'rx' in modules[mod].targets:
            assert to_check is None
            to_check = modules[mod].inputs.keys()
    periods = {}
    double_checked = set()
    while True:
        presses += 1
        checked = press_button(modules, broadcaster, pulse_counts, to_check)
        if checked:
            for k in checked:
                if k in periods:
                    assert presses % periods[k] == 0
                    double_checked.add(k)
                    if len(double_checked) == len(to_check):
                        p = 1
                        for k in to_check:
                            p *= periods[k]
                        return p
                else:
                    periods[k] = presses

        

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
