#!/usr/bin/env python3

import sys
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

tail_pos = set()

head = (0, 0)
tail = (0, 0)
for line in lines:
    dir, l = line.split()

    print(line)

    for i in range(int(l)):
        if dir == 'R':
            head = (head[0], head[1] + 1)
        elif dir == 'U':
            head = (head[0] - 1, head[1])
        elif dir == 'L':
            head = (head[0], head[1] - 1)
        elif dir == 'D':
            head = (head[0] + 1, head[1])
        
        delta = (head[0] - tail[0], head[1] - tail[1])

        if abs(delta[0]) + abs(delta[1]) <= 2 and abs(delta[0]) <= 1 and abs(delta[1]) <= 1:
            pprint({
                'head': head,
                'tail': tail
            })
            tail_pos.add(tail)
            continue

        if abs(delta[0]) == 2 and delta[1] == 0:
            tail = (tail[0] + delta[0] // 2, tail[1])

        if abs(delta[1]) == 2 and delta[0] == 0:
            tail = (tail[0], tail[1] + delta[1] // 2)
        
        if abs(delta[0]) == 2 and abs(delta[1]) == 1:
            tail = (tail[0] + delta[0] // 2, tail[1] + delta[1])

        if abs(delta[1]) == 2 and abs(delta[0]) == 1:
            tail = (tail[0] + delta[0], tail[1] + delta[1] // 2)
        
        pprint({
            'head': head,
            'tail': tail
        })
        tail_pos.add(tail)

print(len(tail_pos))
