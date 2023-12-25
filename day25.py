from collections import defaultdict
from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx

def parse_input(file = 'day25.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day25example.txt')

def format_input(inp: list[str]):
    modules = defaultdict(list)
    for line in inp:
        mods = line.split(' ')
        m0 = mods[0].rstrip(':')
        modules[m0].extend(mods[1:])
        for mod in mods[1:]:
            modules[mod].append(m0)
    return modules

def solve(links, part, example):
    modules = list(links.keys())
    G = nx.Graph()
    for mod in modules:
        G.add_node(mod)
    for mod in modules:
        for link in links[mod]:
            G.add_edge(mod, link, capacity = 1)
          
    for mod in modules[1:]:
        joins, (set_a, set_b) = nx.minimum_cut(G, modules[0], mod)
        if joins == 3:
            return len(set_a) * len(set_b)

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
