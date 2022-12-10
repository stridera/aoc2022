import sys

def part1(filename: str, cycles: list[int]) -> list[int]:
    results = []
    cycle = 1
    register = 1
    for line in open(filename):
        if line.startswith('noop'):
            cycle += 1
        elif line.startswith('addx'):
            cycle += 1
            if cycle in cycles:
                results.append(cycle * register)
            register += int(line[4:])
            cycle += 1
        if cycle in cycles:
            results.append(cycle * register)
    return results

def draw(x: int, cycle: int) -> str:
    char = '.'
    pos = cycle % 40 
    if pos - 2 <= x <= pos:
        char = '#'
    if cycle > 1 and pos == 0:
        char += '\n'
    return char
        

def part2(filename: str) -> str:
    results = ""
    cycle = 1
    register = 1
    for line in open(filename):
        results += draw(register, cycle)
        if line.startswith('noop'):
            cycle += 1
        elif line.startswith('addx'):
            cycle += 1
            results += draw(register, cycle)
            register += int(line[4:])
            cycle += 1
    return results

def main(test):
    cycles = [20, 60, 100, 140, 180, 220]
    if test:
        print('Testing\nPart 1')
        filename = 'test.txt'
        results = part1(filename, cycles)
        assert results == [420, 1140, 1800, 2940, 2880, 3960]
        assert sum(results) == 13_140
        print("Test passed\n")

        print('Part 2')
        results = part2(filename)
        expects = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......###.
#######.......#######.......#######.....
"""
        assert results.strip() == expects.strip()
        print("Test passed\n")

    else:
        print('Part 1')
        filename = 'input.txt'
        results = part1(filename, cycles)
        print(sum(results))

        print('Part 2')
        results = part2(filename)
        print(results)

if __name__ == '__main__':
    main(len(sys.argv) == 2 and sys.argv[1] == 'test')

