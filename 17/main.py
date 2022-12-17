#!/usr/bin/env python3

import sys
from pprint import pprint

with open('rocks.in') as f:
    lines = [line.strip() for line in f.readlines()]

DEBUG=False
PRINT_SHAFT=False

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

rock_i, jet_i = 0, 0


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

    highest_stone = len(shaft) - i - 2

    return highest_stone


t = 0

def simulate(tend=2022):
    global jet_i, rock_i, t

    for i in range(t, tend):
        t = i

        if DEBUG and t % 100000 == 0:
            print(f't = {t}')

        highest_stone = shaft_high()
        
        rock = rocks[rock_i]
        rock_i = (rock_i + 1) % len(rocks)

        rock_height, rock_width = len(rock), len(rock[0])

        # Expand shaft upwards if necessary
        for _ in range(len(shaft), highest_stone + 4 + rock_height):
            shaft.append(['.'] * SHAFT_WIDTH)

        # Place rock
        rock_y = highest_stone + 4
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
        
        if PRINT_SHAFT:
            print('-' * SHAFT_WIDTH)
            high = shaft_high()
            print(f't = {t}, high = {high}')
            print('\n'.join([''.join(line) for line in reversed(shaft)]))
            print('-' * SHAFT_WIDTH)
    
    t = tend

simulate(2022)
print(shaft_high() + 1)

# We simulate far ahead that the cycle has probably started
simulate(50000)

cycle_len = 0
s_floor, s_rock_i, s_jet_i = ''.join(shaft[shaft_high()]), rock_i, jet_i

while True:
    simulate(t + len(rock))
    cycle_len += len(rock)

    floor = ''.join(shaft[shaft_high()])

    if rock_i == s_rock_i and jet_i == s_jet_i and floor == s_floor:
        break

if DEBUG:
    pprint({
        'cycle_len': cycle_len,
    })

h1 = shaft_high()
t1 = t

if DEBUG:
    pprint({
        'rock_i': rock_i,
        'jet_i': jet_i,
        'floor': shaft[h1],
    })

simulate(t + cycle_len)
h2 = shaft_high()
t2 = t

if DEBUG:
    pprint({
        'rock_i': rock_i,
        'jet_i': jet_i,
        'floor': shaft[h2],
    })

cycle_h = h2 - h1

t_final = 1000000000000
h = h2 + cycle_h*((t_final - t2) // cycle_len)

t_rest = (t_final - t2) % cycle_len
t = t_final - t_rest

if DEBUG:
    pprint({
        'h1': h1,
        'h2': h2,
        't1': t1,
        't2': t2,
        'cycle_h': cycle_h,
        't_rest': t_rest,
        't_final': t_final,
        'h_full': h,
    })

simulate(t_final)

h += (shaft_high() - h2)
print(h + 1)

