#!/usr/bin/env python3

import sys
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

paths = [[tuple(int(coord) for coord in pos.split(',')) for pos in line.split(' -> ')] for line in lines]

# pprint(paths)

min_x = min(min(pos[0] for pos in path) for path in paths)
max_x = max(max(pos[0] for pos in path) for path in paths)
max_y = max(max(pos[1] for pos in path) for path in paths)

# print(min_x)
# print(max_x)
# print(max_y)

M = []

for y in range(max_y+1):
    M.append(['.'] * (3 + max_x - min_x))

def get_m(pos):
    global M
    x, y = pos

    return M[y][(x - min_x) + 1]

def set_m(pos, val):
    global M
    x, y = pos

    M[y][(x - min_x) + 1] = val

for path in paths:
    for i in range(1, len(path)):
        start, end = path[i-1], path[i]
        delta = (end[0] - start[0], end[1] - start[1])
        deltalen = abs(delta[0]) + abs(delta[1])
        ndelta = (delta[0] // deltalen, delta[1] // deltalen)

        cur = start
        while cur != end:
            set_m(cur, '#')
            cur = (cur[0] + ndelta[0], cur[1] + ndelta[1])
        
        set_m(end, '#')

sandcounter = 0

voidfall = False
while not voidfall:
    sandpos = (500, 0)

    if get_m(sandpos) != '.':
        break

    resting = False
    while not resting:
        if sandpos[1] >= max_y:
            voidfall = True
            break

        moved = False
        for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
            belowpos = (sandpos[0] + dx, sandpos[1] + dy)
            if get_m(belowpos) == '.':
                sandpos = belowpos
                moved = True
                break
        
        if not moved:
            set_m(sandpos, 'o')
            resting = True
            sandcounter += 1

print('\n'.join(''.join(line) for line in M))
print(sandcounter)
