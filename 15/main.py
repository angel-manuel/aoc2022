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

def merge_segments(s1, s2):
    s1a, s1b = s1
    s2a, s2b = s2

    if s1a > s2a:
        s1a, s1b, s2a, s2b = s2a, s2b, s1a, s1b
    
    if s2a <= s1b:
        return (s1a, max(s2b, s1b))
    
    return None

def imp_seg_at_y(y):
    segments = []

    for bs in data:
        spos = bs['spos']
        dist = bs['distance']

        xdist = dist - abs(spos[1] - y)

        if xdist >= 0:
            xpos = spos[0]
            segments.append((xpos - xdist, xpos + xdist))
    
    segments.sort()

    if not segments:
        return segments

    msegments = []
    accseg = segments[0]
    for i in range(1, len(segments)):
        newaccseg = merge_segments(accseg, segments[i])

        if newaccseg:
            accseg = newaccseg
        else:
            msegments.append(accseg)
            accseg = segments[i]
    
    if accseg:
        msegments.append(accseg)
    
    return msegments

def count_from_imp_seg(y, segments):
    bxs = set(bs['bpos'][0] for bs in data if bs['bpos'][1] == y)

    ret = 0
    for segment in segments:
        sa, sb = segment

        ret += sb - sa + 1

        for bx in bxs:
            if sa <= bx and bx <= sb:
                ret -= 1
    
    return ret


# pprint(imp_seg_at_y(10))
# pprint(imp_seg_at_y(2000000))

print(count_from_imp_seg(10, imp_seg_at_y(10)))
print(count_from_imp_seg(2000000, imp_seg_at_y(2000000)))

def subtract_segments(s1, s2):
    s1a, s1b = s1
    s2a, s2b = s2

    ret = []

    if s1a < s2a:
        ret.append((s1a, min(s2a - 1, s1b)))
    
    if s2b < s1b:
        ret.append((max(s1a, s2b + 1), s1b))
    
    return ret


def possible_in_area(mins, maxs):
    min_x, min_y = mins
    max_x, max_y = maxs

    ret = []

    for y in range(min_y, max_y + 1):
        possible = [(min_x, max_x)]

        for imp_seg in imp_seg_at_y(y):
            if not possible:
                break

            new_possible = []

            for possible_seg in possible:
                new_possible.extend(subtract_segments(possible_seg, imp_seg))

            possible = new_possible
        
        if possible:
            ret.append((y, possible))
    
    return ret

area_pos = possible_in_area((0, 0), (20, 20))

if DEBUG:
    pprint(area_pos)

if len(lines) == 32:
    area_pos = possible_in_area((0, 0), (4000000 , 4000000))

    if DEBUG:
        pprint(area_pos)

pos = (area_pos[0][1][0][0], area_pos[0][0])

if DEBUG:
    print(pos)

tuning_freq = pos[0]*4000000 + pos[1]

print(tuning_freq)
