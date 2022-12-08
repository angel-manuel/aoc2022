#!/usr/bin/env python3

import sys
from pprint import pprint
from operator import mul
from functools import reduce

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

H = [[int(x) for x in line] for line in lines]
# pprint(H)
width = len(H[0])
height = len(H)

visibility = [[0] * width for _ in H]

for y in range(height):
    tallest = -1
    for x in range(width):
        h = H[y][x]
        if h > tallest:
            tallest = h
            visibility[y][x] = visibility[y][x] + 1
    
    tallest = -1
    for x in range(width-1, -1, -1):
        h = H[y][x]
        if h > tallest:
            tallest = h
            visibility[y][x] = visibility[y][x] + 1

for x in range(width):
    tallest = -1
    for y in range(height):
        h = H[y][x]
        if h > tallest:
            tallest = h
            visibility[y][x] = visibility[y][x] + 1
    
    tallest = -1
    for y in range(height-1, -1, -1):
        h = H[y][x]
        if h > tallest:
            tallest = h
            visibility[y][x] = visibility[y][x] + 1

print(sum(sum(v > 0 for v in vline) for vline in visibility))

#           Left, Up, Right, Down
scenic = [[[None, None, None, None] for _ in H[0]] for _ in H]

for y in range(height):
    for x in range(width):
        h = H[y][x]

        # Up
        if y == 0:
            scenic[y][x][1] = 0
        else:
            h_up = H[y-1][x]
            scenic[y][x][1] = 1 + (scenic[y-1][x][1] if h_up < h else 0)
        
        # Left
        if x == 0:
            scenic[y][x][0] = 0
        else:
            h_left = H[y][x-1]
            scenic[y][x][0] = 1 + (scenic[y][x-1][0] if h_left < h else 0)


for y in range(height-1, -1, -1):
    for x in range(width-1, -1, -1):
        h = H[y][x]

        # Down
        if y == height-1:
            scenic[y][x][3] = 0
        else:
            h_down = H[y+1][x]
            scenic[y][x][3] = 1 + (scenic[y+1][x][3] if h_down < h else 0)
        
        # Right
        if x == width-1:
            scenic[y][x][2] = 0
        else:
            h_right = H[y][x+1]
            scenic[y][x][2] = 1 + (scenic[y][x+1][2] if h_right < h else 0)

pprint(H)
pprint(scenic)
scenic_scores = [[reduce(mul, scenic_views, 1) for scenic_views in scenic_line] for scenic_line in scenic]
pprint(scenic_scores)
print(max(max(ssline) for ssline in scenic_scores))
    
