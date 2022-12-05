#!/usr/bin/env python3

import sys
import re

with open(sys.argv[1]) as f:
    lines = [line for line in f.readlines() if line.strip()]

allnum = re.compile('[0-9\s]+')

stack_index, stack_line = next((i, line) for i, line in enumerate(lines) if allnum.fullmatch(line))
stack_count = max(int(x) for x in stack_line.split())

stacks = []
for i in range(stack_count):
    stacks.append([])

elemre = re.compile('\\[([A-Z]+)\\]')
for line in lines[:stack_index]:
    for elem_match in elemre.finditer(line):
        pos = elem_match.span()[0]
        elem = elem_match.groups()[0]

        stack = pos // 4

        stacks[stack].append(elem)

for stack in stacks:
    stack.reverse()

# Copy original stacks
stacks2 = [[x for x in stack] for stack in stacks]

for command in lines[stack_index+1:]:
    command = command.strip()
    if not command:
        continue

    toks = command.split()
    _move, amount, _from, src, _to, dst = toks
    amount, src, dst = int(amount), int(src) - 1, int(dst) - 1

    for i in range(amount):
        elem = stacks[src].pop()
        stacks[dst].append(elem)

print(''.join(stack[-1] for stack in stacks))

stacks = stacks2

for command in lines[stack_index+1:]:
    command = command.strip()
    if not command:
        continue

    toks = command.split()
    _move, amount, _from, src, _to, dst = toks
    amount, src, dst = int(amount), int(src) - 1, int(dst) - 1

    elems = stacks[src][-amount:]

    for i in range(amount):
        stacks[src].pop()
    
    stacks[dst].extend(elems)

print(''.join(stack[-1] for stack in stacks))