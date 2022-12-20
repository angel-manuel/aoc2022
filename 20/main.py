#!/usr/bin/env python3

import sys
from pprint import pprint

DEBUG = True

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

numbers = [int(line) for line in lines]

def mix(numbers):
    indexed_numbers = list(enumerate(numbers))

    if DEBUG:
        print(indexed_numbers)

    for i, value in enumerate(numbers):
        pos = indexed_numbers.index((i, value))
        next_pos = (pos + len(numbers) - 1 + value) % (len(numbers) - 1)

        indexed_numbers = indexed_numbers[:pos] + indexed_numbers[pos+1:]

        if not next_pos:
            next_pos = len(numbers) - 1

        indexed_numbers.insert(next_pos, (i, value))
        
        if DEBUG and False:
            print(indexed_numbers)
    
    return [value for _, value in indexed_numbers]

mixed = mix(numbers)

if DEBUG:
    print(mixed)

index0 = mixed.index(0)

i1000 = (index0 + 1000) % len(mixed)
i2000 = (index0 + 2000) % len(mixed)
i3000 = (index0 + 3000) % len(mixed)

print(mixed[i1000] + mixed[i2000] + mixed[i3000])
