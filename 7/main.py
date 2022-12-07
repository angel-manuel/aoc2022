#!/usr/bin/env python3

import sys
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

def build_ls(session):
    cwd = []

    folder_ls = {}

    i = 0
    while i < len(session):
        line = session[i]

        if not line.startswith('$'):
            print('ERROR: Expected command')
            return None
        
        _dollar, command, *args = line.split()

        if command == 'cd':
            target = args[0]
            if target == '..':
                cwd.pop()
            elif target == '/':
                cwd = []
            else:
                cwd.append(target)
            i = i + 1
        elif command == 'ls':
            ls_contents = []
            i = i + 1

            while i < len(session):
                line = session[i]

                if line.startswith('$'):
                    break

                size, name = line.split()

                size = 0 if size == 'dir' else int(size)

                ls_contents.append((size, name))
                i = i + 1
            
            path = '/' + '/'.join(cwd)
            folder_ls[path] = ls_contents
 
    return folder_ls

folder_ls = build_ls(lines)

dir_size_cache = {}
def dir_size(folder_ls, dir):
    global dir_size_cache

    if dir in dir_size_cache:
        return dir_size_cache[dir]

    if dir not in folder_ls:
        print(f'Unknown {dir}')
        return None
    
    ret = 0
    ls = folder_ls[dir]

    for entry in ls:
        size, name = entry

        ret = ret + size

        if size == 0: # dir
            next_dir = dir + '/' + name

            if dir == '/':
                next_dir = '/' + name

            ret = ret + dir_size(folder_ls, next_dir)
    
    dir_size_cache[dir] = ret
    return ret

pprint(folder_ls)

answer = 0
for path in folder_ls.keys():
    size = dir_size(folder_ls, path)

    if size <= 100000:
        answer = answer + size

print(answer)

free_space = 70000000 - dir_size(folder_ls, '/')
needed_space = 30000000 - free_space

if needed_space <= 0:
    print(0)
else:
    possible = [item for item in dir_size_cache.items() if item[1] >= needed_space]
    smallest = min(possible, key=lambda item: item[1])

    print(smallest)
