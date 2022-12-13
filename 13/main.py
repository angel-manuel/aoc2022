#!/usr/bin/env python3

import sys
import re
from pprint import pprint
from functools import cmp_to_key

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

packet_tok_re = re.compile('\\[|\\]|[0-9]+|,')

def parse_packet_toks(toks):
    if toks[0] != '[':
        return int(toks[0]), toks[1:]
    else:
        toks = toks[1:]
        ret = []

        while toks[0] != ']':
            if toks[0] == ',':
                toks = toks[1:]
                continue

            subpacket, toks = parse_packet_toks(toks)
            ret.append(subpacket)
        
        toks = toks[1:]

        return ret, toks


def parse_packet(s):
    toks = packet_tok_re.findall(s)

    packet, toks = parse_packet_toks(toks)

    return packet

packets = [parse_packet(line) for line in lines]

packet_pairs = list(zip(packets[::2], packets[1::2]))

def packet_cmp(p1, p2):
    i1 = isinstance(p1, int)
    i2 = isinstance(p2, int)

    if i1 and i2:
        return p2 - p1
    
    if not i1 and not i2:
        for e1, e2 in zip(p1, p2):
            c = packet_cmp(e1, e2)

            if c:
                return c
        
        return len(p2) - len(p1)
    
    if i1:
        return packet_cmp([p1], p2)

    if i2:
        return packet_cmp(p1, [p2])

res = 0
for i, (p1, p2) in enumerate(packet_pairs):
    c = packet_cmp(p1, p2)

    if c >= 0:
        res += i + 1

print(res)

packets.append([[2]])
packets.append([[6]])

packets.sort(key=cmp_to_key(packet_cmp), reverse=True)

s1, s2 = None, None
for i, packet in enumerate(packets):
    sp = str(packet)
    if sp == '[[2]]':
        s1 = i + 1
    elif sp == '[[6]]':
        s2 = i + 1

print(s1*s2)
