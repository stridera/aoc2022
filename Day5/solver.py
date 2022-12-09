'''
Example input:
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
import sys


def process(file):
    rows = []
    num_stacks = 0
    f = open(file)
    for line in f:
        if line.strip().startswith('1'):
            lines = [line[i:i+4].strip() for i in range(0, len(line), 4)]
            num_stacks = len(lines)
            break
        rows.append(line.rstrip())

    stacks = [[] for _ in range(num_stacks)]
    for line in rows:
        stack = [line[i:i+4].strip(' ][') for i in range(0, len(line), 4)]
        for i, s in enumerate(stack):
            if s:
                stacks[i].insert(0, s)

    print(stacks)
    for line in f:
        if not line.strip():
            continue
        print('next', line.strip())
        verb, count, _, from_stack, _, to_stack = line.split()
        count = int(count)
        from_stack = int(from_stack) - 1
        to_stack = int(to_stack) - 1
        if verb == 'move':
            # Part One
            # for i in range(count):
            #     stacks[to_stack].append(stacks[from_stack].pop())
            # Part Two
            stacks[to_stack].extend(stacks[from_stack][-count:])
            stacks[from_stack] = stacks[from_stack][:-count]
            print(stacks)

    print("Final code: ", end=' ')
    for s in stacks:
        print(s.pop(), end='')

    f.close()


def part_two(file):
    psum = 0
    with open(file) as f:
        lines = f.readlines()


if __name__ == '__main__':
    filename = len(sys.argv) == 2 and sys.argv[1] or "input.txt"
    print("Part One")
    process(filename)
