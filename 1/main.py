#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines()]

lines.append('')

elf_lists = []
elf_list = []

for line in lines:
    if not line:
        if elf_list:
            elf_lists.append(elf_list)
        elf_list = []
    else:
        elf_list.append(int(line))

elf_cals = list(sum(elf_list) for elf_list in elf_lists)

print(max(elf_cals))

elf_cals.sort()

print(sum(elf_cals[-3:]))

