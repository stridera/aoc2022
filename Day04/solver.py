

def part_one(file):
    psum = 0
    for line in open(file):
        line = line.strip()
        a, b = line.split(',')
        al, ar = a.split('-')
        bl, br = b.split('-')
        al, ar, bl, br = int(al), int(ar), int(bl), int(br)
        if (al <= bl <= ar or al <= br <= ar) or (bl <= al <= br or bl <= ar <= br):
            # if (al <= bl and br <= ar) or (bl <= al and ar <= br):
            print(al, ar, bl, br)
            psum += 1
    print(psum)


def part_two(file):
    psum = 0
    with open(file) as f:
        lines = f.readlines()


if __name__ == '__main__':
    filename = "input.txt"
    # filename = "test.txt"
    print("Part One")
    part_one(filename)
    # print("Part Two")
    # part_two(filename)
