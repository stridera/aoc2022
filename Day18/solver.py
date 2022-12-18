import sys


class Blocks:
    def __init__(self, cubes: list[tuple[int, int, int]]):
        self.cubes = cubes

    def nearby(self, x, y, z):
        for dx in (-1, 1):
            yield x + dx, y, z
        for dy in (-1, 1):
            yield x, y + dy, z
        for dz in (-1, 1):
            yield x, y, z + dz

    def p1(self):
        # Find surface area excluding edges of connected cubes
        surface_area = len(self.cubes) * 6
        for cube in self.cubes:
            x, y, z = cube
            if (x + 1, y, z) in self.cubes:
                surface_area -= 2
            if (x, y + 1, z) in self.cubes:
                surface_area -= 2
            if (x, y, z + 1) in self.cubes:
                surface_area -= 2
        return surface_area

    def p2(self):
        # Close in from the sides until we find the external surface area
        min_x = min(self.cubes, key=lambda x: x[0])[0] - 1
        max_x = max(self.cubes, key=lambda x: x[0])[0] + 1
        min_y = min(self.cubes, key=lambda x: x[1])[1] - 1
        max_y = max(self.cubes, key=lambda x: x[1])[1] + 1
        min_z = min(self.cubes, key=lambda x: x[2])[2] - 1
        max_z = max(self.cubes, key=lambda x: x[2])[2] + 1
        seen = set()
        external_surface_area = 0
        to_check = [(min_x, min_y, min_z)]
        while to_check:
            x, y, z = to_check.pop()
            if (x, y, z) in seen:
                continue
            seen.add((x, y, z))
            for nx, ny, nz in self.nearby(x, y, z):
                if (nx, ny, nz) in self.cubes:
                    external_surface_area += 1
                elif ((nx, ny, nz) not in seen and
                        min_x <= nx <= max_x and
                        min_y <= ny <= max_y and
                        min_z <= nz <= max_z):
                    to_check.append((nx, ny, nz))
        return external_surface_area


def main(test):
    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"
    cubes = []

    for line in open(filename):
        cubes.append(tuple(map(int, line.split(","))))
    puzzle = Blocks(cubes)

    print("Part 1")
    results = puzzle.p1()
    print(f"Result: {results}")
    if test:
        expected = 64
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    results = puzzle.p2()
    print(f"Result: {results}")
    if test:
        expected = 58
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
