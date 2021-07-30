
import os
import sys

def find_substring_in_list(list, sub, start = 0):
    for i in range(start, len(list)):
        if list[i].index(sub) != -1:
            return i
    return -1

def replace_block_in_list(list, idx, size, new_block):
    diff = len(new_block) - size
    
    if diff > 0:
        for i in range(diff):
            list.insert(idx, [0])

        list[idx:idx + size] = new_block



def main():
    path = '../CMakeLists.txt'
    with open(path, 'r+') as f:
        contents = f.readlines();

        add_call_idx = find_substring_in_list(contents, 'add_library(aubio')
        end_idx = find_substring_in_list(contents, ')', add_call_idx) + 1

        size_before = end_idx - add_call_idx

        fun_call = contents[add_call_idx:end_idx]
        
        fun_call[-1] = fun_call[-1].replace(')', '')

        dir = os.listdir('../src') 

        src = [s for s in dir if '.h' in s or '.c' in s]

        src, subdirs = [], []
        for entry in dir:
            (subdirs, src)['.h' in entry or '.c' in entry].append(entry)

        fun_call.extend(src)

        for sd in subdirs:
            dir = os.listdir('../src/' + sd)
            fun_call.extend(dir)

        fun_call.sort()    
        fun_call[-1] = fun_call[-1] + ')'



if __name__ == '__main__':
    main()
