#!/usr/bin/env python3

import sys
from pprint import pprint

DEBUG = False

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

numbers = [int(line) for line in lines]


def mix(numbers, decryption_key=1, times=1):
    indexed_numbers = list(enumerate(numbers))

    indexed_numbers = [(i, n*decryption_key, n*decryption_key % (len(numbers) - 1)) for i, n in indexed_numbers]

    for t in range(times):
        for i, orig in enumerate(numbers):
            value = orig*decryption_key
            delta = value % (len(numbers) - 1)

            pos = next(p for p, val in enumerate(indexed_numbers) if val[0] == i)
            next_pos = (pos + len(numbers) - 1 + delta) % (len(numbers) - 1)

            indexed_numbers = indexed_numbers[:pos] + indexed_numbers[pos+1:]

            if not next_pos:
                next_pos = len(numbers) - 1

            indexed_numbers.insert(next_pos, (i, value))
    
    return [value for _, value in indexed_numbers]

mixed = mix(numbers)

if DEBUG:
    print(mixed)

index0 = mixed.index(0)

i1000 = (index0 + 1000) % len(mixed)
i2000 = (index0 + 2000) % len(mixed)
i3000 = (index0 + 3000) % len(mixed)

print(mixed[i1000] + mixed[i2000] + mixed[i3000])

mixed = mix(numbers, decryption_key=811589153, times=10)

index0 = mixed.index(0)

i1000 = (index0 + 1000) % len(mixed)
i2000 = (index0 + 2000) % len(mixed)
i3000 = (index0 + 3000) % len(mixed)

print(mixed[i1000] + mixed[i2000] + mixed[i3000])
