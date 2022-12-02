#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

conversion = {
  'A': 1,
  'X': 1,
  'B': 2,
  'Y': 2,
  'C': 3,
  'Z': 3,
}

matches = [[conversion[x] for x in line.split()] for line in lines]

def match_score(m):
    p1, p2 = m

    win = 0
    if p2 == 3: # Scissors
        if p1 == 2: # vs Paper
            win = 6
        elif p1 == 3: # vs Scissors
            win = 3
    elif p2 == 2: # Paper
        if p1 == 2: # vs Paper
            win = 3
        elif p1 == 1: # vs Rock
            win = 6
    elif p2 == 1: # Rock
        if p1 == 3: # vs Scissors
            win = 6
        elif p1 == 1: # vs Rock
            win = 3

    return win + p2

def match_score2(m):
    p1, res = m

    p2 = p1 # Tie
    if res == 1: # Lose
        p2 = ((p1 - 1) + 2) % 3 + 1
    elif res == 3: # Win
        p2 = ((p1 - 1) + 1) % 3 + 1

    return match_score((p1, p2))

print(sum(match_score(m) for m in matches))
print(sum(match_score2(m) for m in matches))

