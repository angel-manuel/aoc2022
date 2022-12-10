#!/usr/bin/env python3

import sys
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

cycle = 1
regx = 1

state_history = [(cycle, regx)]

for instr in lines:
    op, *args = instr.split()

    if op == 'noop':
        cycle = cycle + 1
    elif op == 'addx':
        addarg = int(args[0])

        cycle = cycle + 1
        state_history.append((cycle, regx))
        cycle = cycle + 1
        regx = regx + addarg

    state_history.append((cycle, regx))

# pprint(state_history)

sum_state_val = 0
for c in range(19, len(state_history), 40):
    state_val = state_history[c][0] * state_history[c][1]
    sum_state_val += state_val

print(sum_state_val)

# Screen
if len(state_history) >= 40*6:
    for y in range(6):
        line = ''
        for x in range(40):
            c = y*40 + x + 1
            regx = state_history[c-1][1]

            if c != state_history[c-1][0]:
                print('ERROR')

            if abs(regx - x) <= 1:
                line += '#'
            else:
                line += '.'

        print(line)
            
