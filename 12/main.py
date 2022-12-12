#!/usr/bin/env python3

import sys
import heapq
from itertools import product
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = [list(line.strip()) for line in f.readlines() if line.strip()]

H = lines

width = len(H[0])
height = len(H)

start, end = None, None

for y, line in enumerate(H):
    for x, c in enumerate(line):
        if c == 'S':
            start = (y, x)
        elif c == 'E':
            end = (y, x)

H[start[0]][start[1]] = 'a'
H[end[0]][end[1]] = 'z'

def manhatthan(a, b):
    ay, ax = a
    by, bx = b

    return abs(ay - by) + abs(ax - bx)

def dijkstra(start):
    global H, width, height

    G = [[None] * width for _ in H]

    G[start[0]][start[1]] = 0

    O = []
    C = set()

    heapq.heappush(O, (0, start))

    while O:
        g_current, current = heapq.heappop(O)
        C.add(current)

        # if current == end:
        #     break

        y, x = current
        for ny, nx in [(y+1, x), (y,x+1), (y-1, x), (y,x-1)]:
            if ny < 0 or ny >= height or nx < 0 or nx >= width:
                continue

            if ord(H[y][x]) - ord(H[ny][nx]) > 1:
                continue
            
            new_g = g_current + 1
            g_near = G[ny][nx]
            n = (ny, nx)

            if not g_near or new_g < g_near:
                G[ny][nx] = new_g

                found = False
                for i, o in enumerate(O):
                    if o == n:
                        O[i] = (new_g, o) 
                        heapq.heapify(O)
                        found = True
                        break

                if not found:
                    heapq.heappush(O, (new_g, n))
            
    return G

G = dijkstra(end)
# print('\n'.join([''.join(chr(ord('a') + h % 26) if h else '.' for h in line) for line in G]))

print(G[start[0]][start[1]])

ming = None
for gline, hline in zip(G, H):
    for g, h in zip(gline, hline):
        if not g:
            continue

        if h == 'a':
            if not ming or g < ming:
                ming = g

print(ming)