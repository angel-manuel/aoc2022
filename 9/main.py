#!/usr/bin/env python3

import sys
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

tail_pos = set()

def move_tail(head, tail):
    delta = (head[0] - tail[0], head[1] - tail[1])

    if abs(delta[0]) + abs(delta[1]) <= 2 and abs(delta[0]) <= 1 and abs(delta[1]) <= 1:
        return tail
    
    if abs(delta[0]) == 2 and delta[1] == 0:
        tail = (tail[0] + delta[0] // 2, tail[1])

    if abs(delta[1]) == 2 and delta[0] == 0:
        tail = (tail[0], tail[1] + delta[1] // 2)
    
    if abs(delta[0]) == 2 and abs(delta[1]) == 1:
        tail = (tail[0] + delta[0] // 2, tail[1] + delta[1])

    if abs(delta[1]) == 2 and abs(delta[0]) == 1:
        tail = (tail[0] + delta[0], tail[1] + delta[1] // 2)

    if abs(delta[0]) == 2 and abs(delta[1]) == 2:
        tail = (tail[0] + delta[0] // 2, tail[1] + delta[1] // 2)
    
    return tail

def move_string(slist, commands):
    tail_pos = set()

    tail_pos.add(slist[-1])

    for command in commands:
        dir, l = command.split()

        for t in range(int(l)):
            head = slist[0]

            if dir == 'R':
                head = (head[0], head[1] + 1)
            elif dir == 'U':
                head = (head[0] - 1, head[1])
            elif dir == 'L':
                head = (head[0], head[1] - 1)
            elif dir == 'D':
                head = (head[0] + 1, head[1])
            
            slist[0] = head

            for i in range(1, len(slist)):
                slist[i] = move_tail(slist[i-1], slist[i])
            
            tail = slist[-1]
            tail_pos.add(tail)
    
    return tail_pos

tail_pos = move_string([(0, 0)] * 2, lines)

print(len(tail_pos))

tail_pos_10 = move_string([(0, 0)] * 10, lines)

print(len(tail_pos_10))
