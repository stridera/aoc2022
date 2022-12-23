import sys
from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, field


class Dir(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)


@dataclass
class Elf:
    name: str
    x: int
    y: int
    f: None | tuple[int, int] = None

    def __str__(self):
        return f'Elf {self.name.upper()} ({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        yield self.x
        yield self.y


def print_area(elves: list[Elf], buffer=2):
    min_x = min([e.x for e in elves]) - buffer
    max_x = max([e.x for e in elves]) + buffer
    min_y = min([e.y for e in elves]) - buffer
    max_y = max([e.y for e in elves]) + buffer

    names = {}
    for elf in elves:
        names[(elf.x, elf.y)] = elf.name.upper()
        if elf.f is not None:
            names[elf.f] = elf.name.lower()

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) in names:
                print(names[(x, y)], end="")
            else:
                print(".", end="")
        print()


def planter(elves: list[Elf], verbose=False):
    if verbose:
        print_area(elves)

    directions = [Dir.NORTH, Dir.SOUTH, Dir.WEST, Dir.EAST]
    p1 = 0
    r = 0
    while True:
        r += 1
        if verbose:
            print("Round", r+1)

        proposals = defaultdict(list)
        current_points = [(x, y) for x, y in elves]
        for elf in elves:
            x, y = elf
            nearby_elves = []
            for other_elf in elves:
                if elf == other_elf:
                    continue
                if elf.x + 1 >= other_elf.x >= elf.x - 1 and elf.y + 1 >= other_elf.y >= elf.y - 1:
                    nearby_elves.append(other_elf)

            for dir in directions:
                prop = None
                if len(nearby_elves) == 0:
                    elf.f = None
                    break
                elif dir == Dir.NORTH and sum([1 for e in nearby_elves if e.y < elf.y]) == 0 and (x, y-1) not in current_points:
                    prop = (x, y-1), elf
                elif dir == Dir.SOUTH and sum([1 for e in nearby_elves if e.y > elf.y]) == 0 and (x, y+1) not in current_points:
                    prop = (x, y+1), elf
                elif dir == Dir.WEST and sum([1 for e in nearby_elves if e.x < elf.x]) == 0 and (x-1, y) not in current_points:
                    prop = (x-1, y), elf
                elif dir == Dir.EAST and sum([1 for e in nearby_elves if e.x > elf.x]) == 0 and (x+1, y) not in current_points:
                    prop = (x+1, y), elf

                if prop is not None:
                    proposals[prop[0]].append(prop[1])
                    break

        directions.append(directions.pop(0))

        if not proposals:
            break

        for k, v in proposals.items():
            if len(v) == 1:
                elf = v[0]
                if verbose:
                    print(f'Elf ({elf.x}, {elf.y}) moved to {k}')
                elf.f = (elf.x, elf.y)
                elf.x, elf.y = k

        if verbose:
            print_area(elves)

        if r == 10:
            min_x = min([x for x, _ in elves])
            max_x = max([x for x, _ in elves])
            min_y = min([y for _, y in elves])
            max_y = max([y for _, y in elves])
            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            p1 = area - len(elves)
            if verbose:
                print("Final.")
                print(min_x, max_x, min_y, max_y, elves)
                print_area(elves, 0)

    return p1, r


def main(test: bool = False):
    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    data = open(filename).read().splitlines()
    elves = []
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                elves.append(Elf(chr(len(elves)+ord('a')), x, y))

    p1, p2 = planter(elves, test)

    print("Part 1")
    print(p1)
    if test:
        expected = 110
        assert p1 == expected, f"Expected {expected}, got {p1}"
        print("Test passed")

    print("Part 2")
    print(p2)
    if test:
        expected = 20
        assert p2 == expected, f"Expected {expected}, got {p2}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")

# part 1: 4000
# part 2: 1040
