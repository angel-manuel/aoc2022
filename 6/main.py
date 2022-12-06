#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

def find_first_distinct(data, l=4):
    for i in range(len(data) - l):
        segment = data[i:i+l]

        if len(set(segment)) == l:
            return i + l
    
    return None

for line in lines:
    print(find_first_distinct(line, 4))
    print(find_first_distinct(line, 14))