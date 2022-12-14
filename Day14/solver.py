"""--- Day 14: Regolith Reservoir ---"""
import sys
from collections import defaultdict


class Sandfall:
    def __init__(self, input, orgin=(500, 0), has_floor=False):
        self.grid = defaultdict(lambda: defaultdict(lambda: "."))
        self.orgin = orgin
        self.has_floor = has_floor

        x, y = orgin
        self.grid[x][y] = "+"
        self.min_x = self.max_x = x
        self.min_y = self.max_y = y
        self.parse_input(input)

    def parse_input(self, input):
        for line in input:
            line = line.strip()
            if not line:
                continue
            path = line.split(" -> ")
            start = None
            for point in path:
                if start:
                    self.add_path(start, point)
                start = point

    def add_path(self, start, end):
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))
        if start_x == end_x:
            if start_y > end_y:
                start_y, end_y = end_y, start_y
            for y in range(start_y, end_y+1):
                self.grid[start_x][y] = "#"
        elif start_y == end_y:
            if start_x > end_x:
                start_x, end_x = end_x, start_x
            for x in range(start_x, end_x+1):
                self.grid[x][start_y] = "#"
        else:
            raise ValueError(f"Invalid path: {start} -> {end}")
        self.min_x = min(self.min_x, start_x, end_x)
        self.max_x = max(self.max_x, start_x, end_x)
        self.max_y = max(self.max_y, start_y, end_y)

    def print_header(self):
        header = [" " * 6] * 3
        for x in range(self.min_x-1, self.max_x+2):
            header[0] += f"{x // 100 % 10}"
            header[1] += f"{x // 10 % 10}"
            header[2] += f"{x % 10}"
        print("\n".join(header))

    def print_grid(self):
        self.print_header()
        for y in range(self.min_y, self.max_y+3):
            print(f"{y:4}: ", end="")
            print("".join(self.grid[x][y] for x in range(self.min_x-1, self.max_x+2)))
        print()

    def fill(self):
        x, y = self.orgin
        i = 0
        if self.grid[x][y] == "o":
            return False
        while True:
            i += 1
            if i > 1000:
                print("Too many iterations")
                return False

            if y >= self.max_y + 1:
                if self.has_floor:
                    self.grid[x-1][y+1] = "#"
                    self.grid[x][y+1] = "#"
                    self.grid[x+1][y+1] = "#"
                else:
                    return False
            if self.grid[x][y+1] == ".":
                y += 1
            elif self.grid[x-1][y+1] == ".":
                x -= 1
                y += 1
            elif self.grid[x+1][y+1] == ".":
                x += 1
                y += 1
            else:
                break
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.grid[x][y] = "o"
        return True


def run(input, part, expected):
    sandfall = Sandfall(input, has_floor=(part == 2))
    round = 0
    while sandfall.fill():
        round += 1

    sandfall.print_grid()

    if expected is not None:
        assert round == expected, f"Expected expected, got {round}"
        print("Tests passed")
    print("Final:", round)


def main(test):

    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"
    input = open(filename).read().split("\n")

    print("Part 1")
    run(input, 1, 24 if test else None)

    print("Part 2")
    run(input, 2, 93 if test else None)


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
