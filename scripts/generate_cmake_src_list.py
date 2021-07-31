
import os
import sys

def find_substring_in_list(list, sub, start = 0):
    for i in range(start, len(list)):
        if list[i].find(sub) != -1:
            return i
    return -1

def replace_block_in_list(list, idx, size_before, new_block):
    diff = len(new_block) - size_before
    
    if diff > 0:
        for i in range(diff):
            list.insert(idx, 0)

        list[idx:idx + len(new_block)] = new_block

def recurse(dir):
    contents = os.listdir(dir)
    
    files = []
    for entry in contents:
        entry = os.path.join(dir, entry)
        if os.path.isdir(os.path.join(dir, entry)):
            files.extend(recurse(entry))
        else:
            if '.h' in entry or '.c' in entry:
                files.append(entry)

    return files
            

def main():
    path = '../CMakeLists.txt'
    with open(path, 'r+') as f:
        contents = f.readlines();

        add_call_idx = find_substring_in_list(contents, 'add_library(aubio')
        end_idx = find_substring_in_list(contents, ')', add_call_idx) + 1

        size_before = end_idx - add_call_idx

        fun_call = ['add_library(aubio\n']
        
        files = recurse('..\src')
        def sort_key(file):
            return (file.count('\\'), file)
        files.sort(key=sort_key)

        spaces = (' ' * len('add_library('))
        for i in range(len(files)):
            files[i] = spaces + files[i].replace('..\\', '') + '\n'

        files += ')\n'

        fun_call.extend(files)

        replace_block_in_list(contents, add_call_idx, size_before, fun_call)
        
        f.seek(0)
        f.writelines(contents)

if __name__ == '__main__':
    main()
