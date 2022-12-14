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

M = []

for y in range(max_y+3):
    M.append(['.'] * ((2 * max_y) + max_x - min_x))

def get_m(pos):
    global M
    x, y = pos

    return M[y][(x - min_x + max_y) + 1]

def set_m(pos, val):
    global M
    x, y = pos

    M[y][(x - min_x + max_y) + 1] = val

# set_m((500, 0), 's')

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

for x in range(len(M[-1])):
    M[-1][x] = '#'


def sim_sand_grain(voidfall=True):
    sandpos = (500, 0)

    if get_m(sandpos) != '.':
        return 'entry_blocked'

    while True:
        if voidfall and sandpos[1] >= max_y:
            return 'voidfall'
        elif not voidfall and sandpos[1] == max_y + 1:
            set_m(sandpos, 'o')
            return 'resting'

        moved = False
        for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
            belowpos = (sandpos[0] + dx, sandpos[1] + dy)
            if get_m(belowpos) == '.':
                sandpos = belowpos
                moved = True
                break
        
        if not moved:
            set_m(sandpos, 'o')
            return 'resting'
    

sandcounter = 0
while True:
    res = sim_sand_grain()

    if res == 'resting':
        sandcounter += 1
    else:
        break

# print('\n'.join(''.join(line) for line in M))
print(sandcounter)

while True:
    res = sim_sand_grain(voidfall=False)

    if res == 'resting':
        sandcounter += 1
    else:
        break

# print('\n'.join(''.join(line) for line in M))
print(sandcounter)
