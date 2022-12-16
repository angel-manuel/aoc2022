#!/usr/bin/env python3

import sys
import re
from pprint import pprint


with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]


parser = re.compile('Valve ([A-Z]+) has flow rate=([0-9]+); [a-z\s]* ((?:[A-Z]+,?\s*)*)')

parsed = [parser.match(line).groups() for line in lines]
parsed = [(valve, int(flow), conns.split(', ')) for valve, flow, conns in parsed]

data = parsed
mapped_data = {valve: (valve, flow, conns) for valve, flow, conns in data}

valve_index = {valve[0]: index for index, valve in enumerate(data)}

working_valves = [valve for valve, flow, _ in data if flow]

def floyd_warshall():
    global data, valve_index

    dist = []

    for _ in range(len(data)):
        dist.append([None] * len(data))
    
    for i in range(len(data)):
        dist[i][i] = 0
    
    for i, valve in enumerate(data):
        for conn in valve[2]:
            j = valve_index[conn]
            dist[i][j] = 1
    
    for k in range(len(data)):
        for i in range(len(data)):
            for j in range(len(data)):
                dist_ik = dist[i][k]
                dist_kj = dist[k][j]

                if dist_ik and dist_kj:
                    alt_dist = dist[i][k] + dist[k][j]
                    if dist[i][j] is None or dist[i][j] > alt_dist:
                        dist[i][j] = alt_dist

    return dist

D = floyd_warshall()
# pprint(D)

# sw_valves = sorted([(flow - D[valve_index['AA']][valve_index[valve]], valve) for valve, flow, _ in data if flow], reverse=True)

def simulate_order(valve_order):
    t=30
    pos='AA'
    
    tot=0
    flow=0

    print(valve_order)

    for valve in valve_order:
        d = D[valve_index[pos]][valve_index[valve]]

        eff_t = min(t, d)
        t -= eff_t

        tot += flow*eff_t
        pos = valve

        if t > 0:
            t -= 1
            tot += flow
            flow += mapped_data[valve][1]
        else:
            break
    
    tot += t*flow
    
    return tot

def solve(t=30, visited=[], pos='AA'):
    if not t:
        return 0, []

    valves_by_flow = [valve for _, valve in sorted([(vflow, valve) for valve, vflow, _ in data if vflow], reverse=True)]

    max_total = 0
    best_valve = None
    best_valves = []
    for valve in valves_by_flow:
        d = D[valve_index[pos]][valve_index[valve]]

        if d + 1 > t or valve in visited:
            continue

        t -= d + 1
        visited.append(valve)

        subtotal, m_best_valves = solve(t, visited, valve)

        total = t*mapped_data[valve][1] + subtotal

        if total > max_total:
            best_valve = valve
            best_valves = m_best_valves
            max_total = total

        visited.remove(valve)
        t += d + 1

    if best_valve:
        best_valves.insert(0, best_valve)

    return max_total, best_valves

print(solve())
