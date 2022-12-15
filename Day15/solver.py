"""--- Day 14: Regolith Reservoir ---"""
import sys
import re
from collections import defaultdict


class Sensor:
    def __init__(self, x, y, dist):
        self.x = x
        self.y = y
        self.dist = dist

    def scan_range(self):
        return self.dist

    def __repr__(self):
        return f"Sensor({self.x}, {self.y}, {self.dist})"

    def points(self):
        return (self.x, self.y)

    def distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

    def in_range(self, x, y):
        return self.distance(x, y) <= self.dist


class Area:
    def __init__(self, input):
        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0
        self.sensors = []
        self.beacons = []
        for sx, sy, bx, by in input:
            dist = self.distance(sx, sy, bx, by)
            self.min_x, self.max_x = min(self.min_x, sx - dist), max(self.max_x, sx + dist)
            self.min_y, self.max_y = min(self.min_y, sy - dist), max(self.max_y, sy + dist)
            self.sensors.append(Sensor(sx, sy, dist))
            self.beacons.append((bx, by))

    def distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def get_point(self, x, y):
        for becon in self.beacons:
            if becon == (x, y):
                return "B"
        for sensor in self.sensors:
            if sensor == (x, y):
                return "S"
        for sensor in self.sensors:
            if sensor.in_range(x, y):
                return "#"
        return "."

    def count_line(self, line):
        """ Really should be optimized to get the ranges for each sensor and then union them."""
        gridline = defaultdict(lambda: ".")
        for idx, sensor in enumerate(self.sensors):
            print(f"Sensor {idx+1}/{len(self.sensors)}", end="\r")
            if sensor.y - sensor.dist <= line <= sensor.y + sensor.dist:
                for x in range(sensor.x - sensor.dist, sensor.x + sensor.dist + 1):
                    gridline[x] = self.get_point(x, line)
        return sum(1 for x in range(self.min_x, self.max_x+1) if gridline[x] == "#")

    def find_freq(self, min_x, min_y, max_x, max_y):
        for sensor in self.sensors:
            sx, sy, dist = sensor.x, sensor.y, sensor.dist
            for y in range(sy - dist, sy + dist + 1):
                if min_y <= y <= max_y:
                    delta_x = dist - abs(sy - y)
                    for x in [sx - delta_x - 1, sx + delta_x + 1]:
                        if min_x <= x <= max_x:
                            if self.get_point(x, y) == ".":
                                return x * 4_000_000 + y

    def print_header(self):
        header = [" " * 6] * 3
        for x in range(self.min_x-1, self.max_x+2):
            x = abs(x)
            header[0] += f"{x // 100 % 10}"
            header[1] += f"{x // 10 % 10}"
            header[2] += f"{x % 10}"
        print("\n".join(header))

    def print_grid(self, min_x=None, min_y=None, max_x=None, max_y=None):
        if min_x is None:
            min_x = self.min_x
        if min_y is None:
            min_y = self.min_y
        if max_x is None:
            max_x = self.max_x
        if max_y is None:
            max_y = self.max_y

        self.print_header()
        grid = defaultdict(lambda: defaultdict(lambda: "."))
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                for sensor in self.sensors:
                    if sensor.in_range(x, y):
                        grid[x][y] = "#"
        for sensor in self.sensors:
            grid[sensor.x][sensor.y] = "S"
        for x, y in self.beacons:
            grid[x][y] = "B"

        for y in range(min_y, max_y):
            print(f"{y:4}: ", end="")
            print("".join(grid[x][y] for x in range(min_x, max_x)))
        print()


def main(test):

    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"
    input = []
    for line in open(filename):
        matches = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        input.append([int(x) for x in matches.groups()])

    sensor_array = Area(input)

    print("Part 1")
    results = sensor_array.count_line(10 if test else 2_000_000)
    print(f"Result: {results}")
    if test:
        sensor_array.print_grid()
        expected = 26
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    if test:
        results = sensor_array.find_freq(0, 0, 20, 20)
    else:
        results = sensor_array.find_freq(0, 0, 4_000_000, 4_000_000)
    print(f"Result: {results}")
    if test:
        sensor_array.print_grid(0, 0, 20, 20)
        expected = 56000011
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
