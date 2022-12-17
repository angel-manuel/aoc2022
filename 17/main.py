#!/usr/bin/env python3

import sys
from pprint import pprint

with open('rocks.in') as f:
    lines = [line.strip() for line in f.readlines()]

DEBUG=False

rock = []
rocks = []

for line in lines:
    if not line:
        if rock:
            rocks.append(rock[::-1])
            rock = []
    else:
        rock.append(list(line))

if rock:
    rocks.append(rock[::-1])

if DEBUG:
    pprint(rocks)

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]


SHAFT_WIDTH = 7

shaft = [['.'] * SHAFT_WIDTH]
jets = list(lines[0])

jet_i = 0


def check_clear(rock, rock_y, rock_x):
    global shaft

    rock_height, rock_width = len(rock), len(rock[0])

    for y in range(rock_height):
        if rock_y + y < 0:
            return False

        for x in range(rock_width):
            if rock_x + x >= SHAFT_WIDTH or rock_x + x < 0:
                return False
            
            if rock[y][x] == '#' and shaft[rock_y + y][rock_x + x] == '#':
                return False
    
    return True

def shaft_high():
    global shaft

    for i, level in enumerate(reversed(shaft)):
        if any(space == '#' for space in level):
            i = i - 1
            break

    highest_stone = len(shaft) - i - 1

    return highest_stone


for t in range(2022):
    highest_stone = shaft_high()
    
    rock = rocks[t % len(rocks)]

    rock_height, rock_width = len(rock), len(rock[0])

    # Expand shaft upwards if necessary
    for _ in range(len(shaft), highest_stone + 3 + rock_height):
        shaft.append(['.'] * SHAFT_WIDTH)

    # Place rock
    rock_y = highest_stone + 3 
    rock_x = 2

    while True:
        next_rock_x = rock_x + (1 if jets[jet_i] == '>' else -1)
        jet_i = (jet_i + 1) % len(jets)

        if check_clear(rock, rock_y, next_rock_x):
            rock_x = next_rock_x
        
        if check_clear(rock, rock_y - 1, rock_x):
            rock_y -= 1
        else:
            break
    
    for y in range(rock_height):
        for x in range(rock_width):
            if rock[y][x] == '#':
                shaft[rock_y + y][rock_x + x] = '#'
    
    if DEBUG:
        print('-' * SHAFT_WIDTH)
        print(f't = {t}')
        print('\n'.join([''.join(line) for line in reversed(shaft)]))
        print('-' * SHAFT_WIDTH)

print(shaft_high())