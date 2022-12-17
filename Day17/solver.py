import sys
import re
from collections import defaultdict
from functools import cache
from dataclasses import dataclass
import math

SHAPES = [
    ['####'],
    [' # ',
     '###',
     ' # ',],
    ['  #',
     '  #',
     '###'],
    ['#',
     '#',
     '#',
     '#',],
    ['##',
     '##',]
]


def overlaps(cur, grid, x, y):
    for row in SHAPES[cur]:
        for idx, pos in enumerate(row):
            if pos == '#':
                if grid[x+idx][y] != '.':
                    return True
        y -= 1
    return False


def draw(grid, cur, x, y):
    print("+-------+")
    for row in range(y, -1, -1):
        line = ['.'] * 7
        for col in range(7):
            if grid[col][row] == '#':
                line[col] = '#'
            if cur is not None:
                sx, sy = col - x, y - row
                if 0 <= sx < len(SHAPES[cur][0]) and 0 <= sy < len(SHAPES[cur]):
                    pos = SHAPES[cur][sy][sx]
                    if pos == '#':
                        line[col] = '@'
        print(f'|{"".join(line)}|')
    print("+-------+")


def run(jets: str, rocks: int = 10, debug: bool = False):
    grid = defaultdict(lambda: defaultdict(lambda: "."))
    rock = 0
    cur = None
    top = 0
    x, y = 0, 0
    step = 0
    height_changes = []
    while True:
        # Move Phase
        if cur is None:
            if rock >= rocks:
                return top, height_changes
            cur = rock % len(SHAPES)
            x, y = 2, top + len(SHAPES[cur]) + 2
            if debug:
                print("New rock", rock+1, "at", x, y)
        else:
            if y == 0 or overlaps(cur, grid, x, y-1):
                # print("Stop")
                ot = top
                if y + 1 > top:
                    top = y + 1
                height_changes.append(top - ot)

                for row in SHAPES[cur]:
                    for idx, pos in enumerate(row):
                        if pos == '#':
                            grid[x+idx][y] = '#'
                    y -= 1
                cur = None
                rock += 1
                if debug:
                    draw(grid, None, 0, top)

            else:
                y -= 1
                if debug:
                    print("Move Down")
                    draw(grid, cur, x, y)

        # Jets Phase
        if cur is not None:
            direction = jets[step]
            step = step + 1 if step < len(jets) - 1 else 0
            if direction == '<' and x > 0 and not overlaps(cur, grid, x-1, y):
                if debug:
                    print("Move Left")
                x -= 1
            elif direction == '>' and x + len(SHAPES[cur][0]) < 7 and not overlaps(cur, grid, x+1, y):
                if debug:
                    print("Move Right")
                x += 1
            else:
                if debug:
                    print("No move", direction)

        if debug:
            draw(grid, cur, x, y)

    print("ERROR!")


def find_cycles(changes):
    best = 0
    results = None
    for m in range(0, len(changes), len(SHAPES)):
        print(f"Searching for cycle starting at {m} (len: {len(changes)})", end="\r")
        heights = changes[m:]
        for n in range(len(SHAPES), len(changes), len(SHAPES)):
            step = n
            test = heights[:step]
            cycle = 0
            while test == heights[step:step+n]:
                if step >= len(heights):
                    break
                else:
                    cycle += 1
                    step += n
                    if cycle > best:
                        best = cycle
                        results = m, n
                        print(f"Found cycle: {m} {n} {cycle} {best}", ' ' * 50)
                    if cycle > 5:
                        # Just count it...
                        return m, n

    return results


def main(test):

    if test:
        # print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    line = open(filename).readline()

    print("Part 1")
    # results = run(line, 11, True)
    results, height_changes = run(line, 2022)
    print(f"Result: {results}")
    if test:
        expected = 3068
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    results, height_changes = run(line, 15000)
    f, t = find_cycles(height_changes)
    cycles = 1_000_000_000_000
    results = sum(height_changes[:f])

    cycles -= f
    cycle_sum = sum(height_changes[f:f+t])
    results += cycle_sum * (cycles // t)
    results += sum(height_changes[f:f+cycles % t])
    print(f"Result: {results}")
    if test:
        expected = 1_514_285_714_288
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
