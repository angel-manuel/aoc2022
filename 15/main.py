#!/usr/bin/env python3

import sys
import re
from pprint import pprint

DEBUG = False

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

parser = re.compile('Sensor at x=(?P<sx>\\-?[0-9]+), y=(?P<sy>\\-?[0-9]+): closest beacon is at x=(?P<bx>\\-?[0-9]+), y=(?P<by>\\-?[0-9]+)')

data = [dict((k, int(v)) for k, v in parser.fullmatch(line).groupdict().items()) for line in lines]

def manhattan(a, b):
    ay, ax = a
    by, bx = b

    return abs(ay - by) + abs(ax - bx)

for bs in data:
    bpos = (bs['bx'], bs['by'])
    spos = (bs['sx'], bs['sy'])
    bs['distance'] = manhattan(bpos, spos)
    bs['bpos'] = bpos
    bs['spos'] = spos

if DEBUG:
    pprint(data)

min_sx = min(bs['sx'] for bs in data)
max_sx = max(bs['sx'] for bs in data)
max_d = max(bs['distance'] for bs in data)

bposes = set(bs['bpos'] for bs in data)

if DEBUG:
    pprint({
        'min_sx': min_sx,
        'max_sx': max_sx,
        'max_d': max_d,
    })

def imposible_at_y(y):
    global data, min_sx, max_sx, max_d

    nb_count = 0
    for x in range(min_sx - max_d, max_sx + max_d + 1):
        pos = (x, y)
        for bs in data:
            sd = manhattan(pos, bs['spos'])

            if DEBUG:
                print({
                    'pos': pos,
                    'spos': bs['spos'],
                    'sd': sd,
                    'bs_dist': bs['distance'],
                })

            if sd <= max_d and sd <= bs['distance'] and pos not in bposes:
                nb_count += 1
                break
    
    return nb_count

print(imposible_at_y(10))
print(imposible_at_y(2000000))
