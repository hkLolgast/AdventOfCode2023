from copy import deepcopy

def parse_input(file = 'day19.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day19example.txt')

def format_input(inp: list[str]):
    workflows = {}
    parts = []
    parsing_parts = False
    for line in inp:
        if line == '':
            parsing_parts = True
            continue
        if parsing_parts:
            values = line.strip('{}').split(',')
            part = {}
            for item in values:
                k, v = item.split('=')
                part[k] = int(v)
            parts.append(part)
        else:
            name = line[:line.index('{')]
            commands = line.rstrip('}')[line.index('{') + 1:].split(',')
            workflows[name] = commands
    return workflows, parts

def follow_workflow(part, workflow):
    for command in workflow:
        if ':' not in command:
            return command
        condition, result = command.split(':')
        if condition[1] == '<':
            if part[condition[0]] < int(condition[2:]):
                return result
        elif condition[1] == '>':
            if part[condition[0]] > int(condition[2:]):
                return result
    raise ValueError('No matching result')

def solve(inp, part, example):
    workflows, parts = inp
    if part == 1:
        accepted = []
        for p in parts:
            workflow_id = 'in'
            while workflow_id not in ('A', 'R'):
                workflow_id = follow_workflow(p, workflows[workflow_id])
            if workflow_id == 'A':
                accepted.append(p)

        return sum(sum(p.values()) for p in accepted)
    
    parts_by_workflow = {((1, 4000), (1, 4000), (1, 4000), (1, 4000)): 'in'}
    accepted = []
    cycles = 0
    while parts_by_workflow:
        cycles += 1
        if cycles == 100_000:
            raise InterruptedError
        parts = list(parts_by_workflow.keys())[0]
        workflow = parts_by_workflow[parts]
        del parts_by_workflow[parts]
        if workflow == 'A':
            accepted.append(parts)
            continue
        if workflow == 'R':
            continue
        for command in workflows[workflow]:
            if ':' not in command:
                parts_by_workflow[parts] = command
                break
            condition, dest = command.split(':')
            i = 'xmas'.index(condition[0])
            treshold = int(condition[2:])
            filtered = list(parts)
            if condition[1] == '<':
                if parts[i][0] < treshold:
                    filtered[i] = (parts[i][0], min(treshold - 1, parts[i][1]))
                    parts_by_workflow[tuple(filtered)] = dest
                    if parts[i][1] >= treshold:
                        parts = list(parts)
                        parts[i] = (treshold, parts[i][1])
                        parts = tuple(parts)
            else:
                if parts[i][1] > treshold:
                    filtered[i] = (max(treshold + 1, parts[i][0]), parts[i][1])
                    parts_by_workflow[tuple(filtered)] = dest
                    if parts[i][1] >= treshold:
                        parts = list(parts)
                        parts[i] = (parts[i][0], treshold)
                        parts = tuple(parts)
    tot = 0
    for parts in accepted:
        p = 1
        for m1, m2 in parts:
            p *= m2 - m1 + 1
        tot += p
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
