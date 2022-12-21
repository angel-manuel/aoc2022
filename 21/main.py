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

def eval_monkey(name):
    monkey = monkeys[name]

    if monkey['val']:
        return monkey['val']
    
    op = monkey['op']

    val1 = eval_monkey(op[0])
    val2 = eval_monkey(op[2])

    ret = None
    if op[1] == '+':
        ret = val1 + val2
    elif op[1] == '-':
        ret = val1 - val2
    elif op[1] == '*':
        ret = val1 * val2
    elif op[1] == '/':
        ret = val1 // val2
    
    monkey['val'] = ret
    return ret

print(eval_monkey('root'))
