#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    secpairs = [line.strip() for line in f.readlines() if line.strip()]

contain_count = 0
overlap_count = 0

for secpair in secpairs:
    r1, r2 = secpair.split(',')
    a1, b1 = [int(x) for x in r1.split('-')]
    a2, b2 = [int(x) for x in r2.split('-')]

    if (b1 - a1) < (b2 - a2): # make r1 always the bigger range
        a1, b1, a2, b2 = a2, b2, a1, b1

    if a1 <= a2 and b2 <= b1:
        contain_count = contain_count + 1

    if a1 > a2: # make r1 start earlier
        a1, b1, a2, b2 = a2, b2, a1, b1

    if a2 <= b1:
        overlap_count = overlap_count + 1

print(contain_count)
print(overlap_count)

