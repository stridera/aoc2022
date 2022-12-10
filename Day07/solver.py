'''
Example input:
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
import sys
from collections import defaultdict

cwd = ""
filesystem = defaultdict(int)

def process_file(file):
    global cwd
    size, _ = file.split()
    if size == "dir":
        filesystem[cwd + '/' + file[4:]] = 0
    else:
        filesystem[cwd] += int(size)

def process_command(command):
    global cwd
    if command.startswith("cd "):
        cdir = command[3:]
        if cdir == "..":
            cwd = cwd.rpartition("/")[0]
        elif cdir == "/":
            cwd = ""
        else:
            cwd = cwd + '/' + cdir
    elif command.startswith("ls"):
        pass
    else:
        print("Unknown command:", command)

def process(file):
    for line in open(file):
        line = line.strip()
        if line:
            if line[0] == '$':
                process_command(line[2:])
            else:
                process_file(line)

    final_size = 0
    final_dir_size = {}
    for path in sorted(filesystem.keys()):
        dir_size = 0
        for test in sorted(filesystem.keys()):
            if test.startswith(path):
                dir_size += filesystem[test]
        final_dir_size[path] = dir_size
        if dir_size < 100_000:
            final_size += dir_size
    print("Part 1:", final_size)

    size_free = 70_000_000 - final_dir_size[""]
    for path in sorted(final_dir_size, key=lambda x: final_dir_size[x], reverse=True):
        print(path, final_dir_size[path])
        if path == "":
            continue
        if size_free + final_dir_size[path] >= 30_000_000:
            print("Part 2:", size_free + final_dir_size[path])
            break
    

if __name__ == '__main__':
    filename = len(sys.argv) == 2 and sys.argv[1] or "input.txt"
    process(filename)
