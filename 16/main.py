#!/usr/bin/env python3

import sys
import re
from pprint import pprint


with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

DEBUG = False

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

def solve2(t=26, visited=[], pos1='AA', pos2='AA', going1=None, going2=None, opened=[]):
    if not t:
        return 0, []

    if DEBUG:
        pprint({
            't': t,
            'visited': visited,
            'pos1': pos1,
            'pos2': pos2,
            'going1': going1,
            'going2': going2,
        })

    if going1 and going2:
        tgt1, t1 = going1 
        tgt2, t2 = going2

        if t1 == t2:
            if t1 + 1 <= t:
                t -= t1 + 1

                extra_opened = []
                pressure_release = 0
                if tgt1 not in opened:
                    extra_opened.append(tgt1)
                    pressure_release += mapped_data[tgt1][1]*t

                if tgt2 not in opened:
                    extra_opened.append(tgt2)
                    pressure_release += mapped_data[tgt2][1]*t

                subpressure, path = solve2(t, visited, tgt1, tgt2, None, None, opened + extra_opened)

                return pressure_release + subpressure, path + extra_opened
        elif t1 < t2:
            if t1 + 1 <= t:
                t -= t1 + 1

                pressure_release = 0
                extra_opened = []
                if tgt1 not in opened:
                    pressure_release = mapped_data[tgt1][1]*t
                    extra_opened = [tgt1]

                subpressure, path = solve2(t, visited, tgt1, pos2, None, (tgt2, t2 - (t1 + 1)), opened + extra_opened)

                return pressure_release + subpressure, path + extra_opened
        elif t1 > t2:
            if t2 + 1 <= t:
                t -= t2 + 1

                pressure_release = 0
                extra_opened = []
                if tgt2 not in opened:
                    pressure_release = mapped_data[tgt2][1]*t
                    extra_opened = [tgt2]

                subpressure, path = solve2(t, visited, pos1, tgt2, (tgt1, t1 - (t2 + 1)), None, opened + extra_opened)

                return pressure_release + subpressure, path + extra_opened
        
        return 0, []
    
    valves_by_flow = [valve for _, valve in sorted([(vflow, valve) for valve, vflow, _ in data if vflow and valve not in visited], reverse=True)]

    if DEBUG and not valves_by_flow:
        pprint({
            't': t,
            'visited': visited,
            'pos1': pos1,
            'pos2': pos2,
            'going1': going1,
            'going2': going2,
        })

    max_total = 0
    best_path = []
    if not going1:
        for valve in valves_by_flow + [pos1]:
            d = D[valve_index[pos1]][valve_index[valve]]

            if not d:
                if going2:
                    d = t + 10
                else:
                    continue

            total, path = solve2(t, visited + [valve], pos1, pos2, (valve, d), going2, opened)

            if total > max_total:
                max_total = total
                best_path = path
    elif not going2:
        for valve in valves_by_flow + [pos2]:
            d = D[valve_index[pos2]][valve_index[valve]]

            if not d:
                d = t + 10

            total, path = solve2(t, visited + [valve], pos1, pos2, going1, (valve, d), opened)

            if total > max_total:
                max_total = total
                best_path = path
    
    return max_total, best_path

print(solve2())
