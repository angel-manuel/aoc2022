#!/usr/bin/env python3

import sys
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines()]

cubes = [tuple(int(x) for x in line.split(',')) for line in lines]
scubes = set(cubes)

exposed = 0

def ncubes(cube):
    x, y, z = cube

    yield (x-1, y, z)
    yield (x+1, y, z)
    yield (x, y-1, z)
    yield (x, y+1, z)
    yield (x, y, z-1)
    yield (x, y, z+1)


for cube in cubes:
    x, y, z = cube

    for ncube in ncubes(cube):
        if ncube not in scubes:
            exposed += 1

print(exposed)

min_x = min(cube[0] for cube in cubes)
min_y = min(cube[1] for cube in cubes)
min_z = min(cube[2] for cube in cubes)

max_x = max(cube[0] for cube in cubes)
max_y = max(cube[1] for cube in cubes)
max_z = max(cube[2] for cube in cubes)

initial_water = (min_x - 1, min_y - 1, min_z - 1)

water = [initial_water]
wvisited = set()
wtouching = set()

while water:
    wcube = water.pop()

    touching = False
    for wncube in ncubes(wcube):
        nx, ny, nz = wncube

        if nx < min_x - 1 or max_x + 1 < nx or ny < min_y - 1 or max_y + 1 < ny or nz < min_z - 1 or max_z + 1 < nz:
            continue

        if wncube in scubes:
            touching = True
        elif wncube not in wvisited:
            water.append(wncube)
            wvisited.add(wncube)

    if touching:
        wtouching.add(wcube)

wet = 0

for cube in cubes:
    x, y, z = cube

    for ncube in ncubes(cube):
        if ncube in wtouching:
            wet += 1

print(wet)
