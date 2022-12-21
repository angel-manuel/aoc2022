#!/usr/bin/env python3

import sys
from pprint import pprint

DEBUG = False

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

monkeys = {}

for line in lines:
    monkey, op = line.split(':') 
    op = op.strip().split()

    if len(op) == 1:
        n = int(op[0])

        monkeys[monkey] = {'val': n, 'op': None}
    else:
        monkeys[monkey] = {'val': None, 'op': op}

def eval_monkey(name, cache=True):
    if name not in monkeys:
        return None

    monkey = monkeys[name]

    if monkey['val']:
        return monkey['val']
    
    if not monkey['op']:
        return None
    
    op = monkey['op']

    val1 = eval_monkey(op[0], cache)
    val2 = eval_monkey(op[2], cache)

    if not val1 or not val2:
        return None

    ret = None
    if op[1] == '+':
        ret = val1 + val2
    elif op[1] == '-':
        ret = val1 - val2
    elif op[1] == '*':
        ret = val1 * val2
    elif op[1] == '/':
        ret = val1 // val2
    elif op[1] == '=':
        ret = 1 if val1 == val2 else 0

    if cache: 
        monkey['val'] = ret

    return ret

def reverse_solve(name='root', target=1):
    if name == 'humn':
        return target

    monkey = monkeys[name]

    if monkey['val']:
        val = monkey['val']
        print(f'Monkey {name} has val={val}!')
        return 'any' if val == target else None
    
    op = monkey['op']

    val1 = eval_monkey(op[0], cache=True)
    val2 = eval_monkey(op[2], cache=True)

    if not val2:
        known_val = val1
        free_monkey = op[2]
    else:
        known_val = val2
        free_monkey = op[0]
    
    if op[1] == '=':
        return reverse_solve(free_monkey, known_val)
    elif op[1] == '+':
        return reverse_solve(free_monkey, target - known_val)
    elif op[1] == '-':
        if val1: # target = known_val - x => x = known_val - target
            return reverse_solve(free_monkey, known_val - target)
        else: # target = x - known_val => x = known_val + target
            return reverse_solve(free_monkey, target + known_val)
    elif op[1] == "*":
        return reverse_solve(free_monkey, target // known_val)
    elif op[1] == "/":
        if val1: # target = known_val / x => x = known_val / target
            return reverse_solve(free_monkey, known_val // target)
        else: # target = x / known_val => x = target * known_val
            return reverse_solve(free_monkey, known_val * target)


print(eval_monkey('root', cache=False))

monkeys['humn']['val'] = None
monkeys['root']['op'][1] = '='
print(reverse_solve())
