def split_in_half(t):
    l = t[:len(t)//2]
    r = t[len(t)//2:]
    return l, r


def get_priority(c):
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27


def part_one(file):
    psum = 0
    for line in open(file):
        line = line.strip()
        l, r = split_in_half(line)
        common = (set([*l]) & set([*r])).pop()
        priority = get_priority(common)
        print(l, r, common, priority)
        psum += priority
    print(psum)


def part_two(file):
    psum = 0
    with open(file) as f:
        lines = f.readlines()

    for i in range(0, len(lines), 3):
        l1 = lines[i].strip()
        l2 = lines[i+1].strip()
        l3 = lines[i+2].strip()
        common = (set([*l1]) & set([*l2]) & set([*l3])).pop()
        priority = get_priority(common)
        print(l1, l2, l3, common, priority)
        psum += priority
    print(psum)


if __name__ == '__main__':
    filename = "input.txt"
    # filename = "test.txt"
    # print("Part One")
    # part_one(filename)
    print("Part Two")
    part_two(filename)
