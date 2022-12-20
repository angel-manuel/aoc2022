#!/usr/bin/env python3

import sys
from pprint import pprint
import re
from multiprocessing import Pool

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines()]

parser = re.compile('Blueprint (?P<id>[0-9]+): Each ore robot costs (?P<ore_robot_cost>[0-9]+) ore. Each clay robot costs (?P<clay_robot_cost>[0-9]+) ore. Each obsidian robot costs (?P<obsidian_robot_ore_cost>[0-9]+) ore and (?P<obsidian_robot_clay_cost>[0-9]+) clay. Each geode robot costs (?P<geode_robot_ore_cost>[0-9]+) ore and (?P<geode_robot_obsidian_cost>[0-9]+) obsidian.')

blueprints = [
    {k: int(v) for k, v in parser.fullmatch(line).groupdict().items()} for line in lines
]

pprint(blueprints)

def ore_combos(blueprint, resources):
    combos = []

    ore_robots = -1

    while resources[0] >= 0:
        ore_robots += 1
        combos.append((resources[:], [ore_robots, 0, 0, 0]))

        resources[0] -= blueprint['ore_robot_cost']
    
    return combos

claymem = {}    

def clay_combos(blueprint, resources):
    global claymem

    claymem_key = (blueprint['id'], resources[0])

    if claymem_key in claymem:
        return claymem[claymem_key]

    combos = []

    clay_robots = -1

    while resources[0] >= 0:
        clay_robots += 1

        subcombos = ore_combos(blueprint, resources[:])

        for subcombo in subcombos:
            combo = (subcombo[0], subcombo[1][:])
            combo[1][1] = clay_robots
            combos.append(combo)

        resources[0] -= blueprint['clay_robot_cost']

    claymem[claymem_key] = combos
    return combos

obsidianmem = {}

def obsidian_combos(blueprint, resources):
    global obsidianmem

    obsidianmem_key = (blueprint['id'], tuple(resources[:2]))

    if obsidianmem_key in geodemem:
        return obsidianmem[obsidianmem_key]

    combos = []

    obsidian_robots = -1

    while resources[0] >= 0 and resources[1] >= 0:
        obsidian_robots += 1

        subcombos = clay_combos(blueprint, resources[:])
        
        for subcombo in subcombos:
            combo = (subcombo[0], subcombo[1][:])
            combo[1][2] = obsidian_robots
            combos.append(combo)

        resources[0] -= blueprint['obsidian_robot_ore_cost']
        resources[1] -= blueprint['obsidian_robot_clay_cost']

    obsidianmem[obsidianmem_key] = combos
    return combos

geodemem = {}

def geode_combos(blueprint, resources):
    global geodemem

    geodemem_key = (blueprint['id'], tuple(resources))

    if geodemem_key in geodemem:
        return geodemem[geodemem_key]

    combos = []

    geode_robots = -1
    while resources[0] >= 0 and resources[2] >= 0:
        geode_robots += 1

        subcombos = obsidian_combos(blueprint, resources[:])

        for subcombo in subcombos:
            combo = (subcombo[0], subcombo[1][:])
            combo[1][3] = geode_robots
            combos.append(combo)

        resources[0] -= blueprint['geode_robot_ore_cost']
        resources[2] -= blueprint['geode_robot_obsidian_cost']

    geodemem[geodemem_key] = combos
    return combos

def solve(blueprint, t=24, resources=[0,0,0,0], robots=[1,0,0,0], solvemem={}):
    ore, clay, obsidian, geodes = resources

    if not t:
        return geodes
    
    solvemem_key = (t, tuple(resources[:3]), tuple(robots))

    if solvemem_key in solvemem:
        return solvemem[solvemem_key] + geodes
    
    combos = geode_combos(blueprint, resources[:3])

    combos = [(list(a + b for a, b in zip(res + [geodes], robots)), list(a + b for a, b in zip(rob, robots))) for res, rob in combos]

    scores = [solve(blueprint, t-1, res, rob, solvemem) for res, rob in combos]

    ret = max(scores)
    solvemem[solvemem_key] = ret - geodes
    return ret


print(solve(blueprints[0], t=20))
print(solve(blueprints[0]))

# with Pool(15) as p:
#     blueprint_scores = p.map(solve, blueprints)

# pprint(blueprint_scores)

# res = sum([(i+1)*score for i, score in enumerate(blueprint_scores)])
# print(res)
