#!/usr/bin/env python3

import sys
from pprint import pprint
from functools import reduce
from operator import mul
from copy import deepcopy

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

monkey_rules = {}

def parse_monkey(lines):
    if not lines[0].startswith('Monkey'):
        return None, lines

    monkey = {}
    monkey['index'] = int(lines[0].split()[-1][:-1])

    starting_commas = ''.join(lines[1].split()[2:])
    monkey['starting'] = [int(x) for x in starting_commas.split(',')]

    op_tokens = lines[2].split()
    op_tokens = op_tokens[op_tokens.index('=')+1:]

    if op_tokens[1] == '+':
        if op_tokens[0] == op_tokens[2] and op_tokens[0] == 'old':
            op = lambda x: x + x
        else:
            n = int(op_tokens[2])
            op = lambda x: x + n
    elif op_tokens[1] == '*':
        if op_tokens[0] == op_tokens[2] and op_tokens[0] == 'old':
            op = lambda x: x * x
        else:
            n = int(op_tokens[2])
            op = lambda x: x * n
    
    monkey['op'] = op
    monkey['op_str'] = ' '.join(op_tokens)

    monkey['test_div'] = int(lines[3].split()[-1])

    monkey['true_dst'] = int(lines[4].split()[-1])
    monkey['false_dst'] = int(lines[5].split()[-1])

    monkey['inspected'] = 0

    return monkey, lines[6:]

while lines:
    monkey, lines = parse_monkey(lines)
    monkey_rules[monkey['index']] = monkey

orig_monkey_rules = deepcopy(monkey_rules)

def round(monkey_state, div3=True):
    test_div_cap = reduce(mul, [monkey['test_div'] for monkey in monkey_state.values()], 1)

    for mi in sorted(monkey_state.keys()):
        turn(monkey_state, mi, test_div_cap, div3)

def turn(monkey_state, mi, test_div_cap, div3):
    monkey = monkey_state[mi]

    items = monkey['starting'][:]
    monkey['starting'] = []

    while items:
        item = items.pop()

        inspected_item = monkey['op'](item)
        monkey['inspected'] += 1
        
        if div3:
            inspected_item = inspected_item // 3
        
        inspected_item = inspected_item % test_div_cap

        if inspected_item % monkey['test_div'] == 0:
            monkey_state[monkey['true_dst']]['starting'].append(inspected_item)
        else:
            monkey_state[monkey['false_dst']]['starting'].append(inspected_item)

for t in range(20):
    round(monkey_rules)

minspected = [monkey['inspected'] for monkey in monkey_rules.values()]
minspected.sort(reverse=True)

monkey_business = minspected[0] * minspected[1]
print(monkey_business)

monkey_rules = deepcopy(orig_monkey_rules)

for t in range(10000):
    round(monkey_rules, div3=False)

minspected = [monkey['inspected'] for monkey in monkey_rules.values()]
minspected.sort(reverse=True)

monkey_business = minspected[0] * minspected[1]
print(monkey_business)

