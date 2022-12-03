#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    rucksacks = [line.strip() for line in f.readlines() if line.strip()]

elems = []

for rucksack in rucksacks:
    comp1, comp2 = rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]
    both = set(comp1).intersection(set(comp2))
    elems.append(both.pop())

def elem_to_val(elem):
    if elem.islower():
        return ord(elem) - ord('a') + 1
    else:
        return ord(elem) - ord('A') + 27

print(sum(elem_to_val(elem) for elem in elems))

group_badges = []

for group_num in range(len(rucksacks)//3):
    group = rucksacks[group_num*3:group_num*3+3]
    
    group_badge = set(group[0]).intersection(set(group[1])).intersection(set(group[2])).pop()
    group_badges.append(group_badge)

print(sum(elem_to_val(elem) for elem in group_badges))

