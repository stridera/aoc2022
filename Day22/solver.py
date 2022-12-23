import sys
from enum import Enum


class DIRECTIONS(Enum):
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)


MOVE_ASCII = {
    DIRECTIONS.up: '^',
    DIRECTIONS.right: '>',
    DIRECTIONS.down: 'v',
    DIRECTIONS.left: '<',
}

MOVE_NAME = {
    DIRECTIONS.up: 'Up',
    DIRECTIONS.right: 'Right',
    DIRECTIONS.down: 'Down',
    DIRECTIONS.left: 'Left',
}


def p(data):
    x, y, d = data
    return f"({x}, {y}, {MOVE_NAME[d]})"


class Dance:
    def __init__(self, map, verbose: bool = False):
        self.map = map
        self.verbose = verbose

        self.start = (0, 0)
        for i in range(len(self.map[0])):
            if self.map[0][i] == ".":
                self.start = (0, i)
                break

        self.max_x = max([len(line) for line in self.map])

        self.position = self.start
        self.map[0][self.start[1]] = 'S'
        self.direction = DIRECTIONS.right

    def turn_left(self):
        if self.verbose:
            print(f"Turn Left")
        if self.direction == DIRECTIONS.up:
            self.direction = DIRECTIONS.left
        elif self.direction == DIRECTIONS.right:
            self.direction = DIRECTIONS.up
        elif self.direction == DIRECTIONS.down:
            self.direction = DIRECTIONS.right
        elif self.direction == DIRECTIONS.left:
            self.direction = DIRECTIONS.down

    def turn_right(self):
        if self.verbose:
            print("Turn Right")
        if self.direction == DIRECTIONS.up:
            self.direction = DIRECTIONS.right
        elif self.direction == DIRECTIONS.right:
            self.direction = DIRECTIONS.down
        elif self.direction == DIRECTIONS.down:
            self.direction = DIRECTIONS.left
        elif self.direction == DIRECTIONS.left:
            self.direction = DIRECTIONS.up

    @staticmethod
    def cube_face(x, y, divisor=50):
        """Get the face of the cube that the given position is on.  Each face is 50x50. """
        if x < 0 or x >= 150 or y < 0 or y >= 200:
            return 0
        return (
            (0, 1, 2),
            (0, 3, 0),
            (4, 5, 0),
            (6, 0, 0),
        )[y//divisor][x//divisor]

    @staticmethod
    def cube_move(x, y, dir, divisor=50):
        face = Dance.cube_face(x, y, divisor)
        ty, tx = (y + dir.value[0], x + dir.value[1])
        to_face = Dance.cube_face(tx, ty, divisor)
        if face == to_face:
            return tx, ty, dir
        elif face == 1:
            if dir == DIRECTIONS.up:
                return 0, 100+x, DIRECTIONS.right
            elif dir == DIRECTIONS.left:
                return 0, 149-y, DIRECTIONS.right
            elif dir == DIRECTIONS.right:
                return tx, ty, DIRECTIONS.right
            elif dir == DIRECTIONS.down:
                return tx, ty, DIRECTIONS.down
        elif face == 2:
            if dir == DIRECTIONS.up:
                return x-100, 199, DIRECTIONS.up
            elif dir == DIRECTIONS.left:
                return tx, ty, DIRECTIONS.left
            elif dir == DIRECTIONS.right:
                return 99, 149-y, DIRECTIONS.left
            elif dir == DIRECTIONS.down:
                return 99, x-50, DIRECTIONS.left
        elif face == 3:
            if dir == DIRECTIONS.up:
                return tx, ty, DIRECTIONS.up
            elif dir == DIRECTIONS.left:
                return y-50, 100, DIRECTIONS.down
            elif dir == DIRECTIONS.right:
                return y+50, 49, DIRECTIONS.up
            elif dir == DIRECTIONS.down:
                return tx, ty, DIRECTIONS.down
        elif face == 4:
            if dir == DIRECTIONS.up:
                return 50, 50+x, DIRECTIONS.right
            elif dir == DIRECTIONS.left:
                return 50, 149-y, DIRECTIONS.right
            elif dir == DIRECTIONS.right:
                return tx, ty, DIRECTIONS.right
            elif dir == DIRECTIONS.down:
                return tx, ty, DIRECTIONS.down
        elif face == 5:
            if dir == DIRECTIONS.up:
                return tx, ty, DIRECTIONS.up
            elif dir == DIRECTIONS.left:
                return tx, ty, DIRECTIONS.left
            elif dir == DIRECTIONS.right:
                return 149, 149-y, DIRECTIONS.left
            elif dir == DIRECTIONS.down:
                return 49, 100+x, DIRECTIONS.left
        elif face == 6:
            if dir == DIRECTIONS.up:
                return tx, ty, DIRECTIONS.up
            elif dir == DIRECTIONS.left:
                return y-100, 0, DIRECTIONS.down
            elif dir == DIRECTIONS.right:
                return y-100, 149, DIRECTIONS.up
            elif dir == DIRECTIONS.down:
                return x+100, 0, DIRECTIONS.down

        print("INVALID MOVE", tx, ty)

    def move(self, steps, part2: bool = False):
        if self.verbose:
            print("Moving", steps, "steps", self.direction)
        y, x = self.position
        dir = self.direction
        while steps > 0:
            if not part2:
                y, x = (y + dir.value[0], x + dir.value[1])
                if y < 0 and dir == DIRECTIONS.up:
                    y = len(self.map) - 1
                elif y >= len(self.map) and dir == DIRECTIONS.down:
                    y = 0
                elif x < 0 and dir == DIRECTIONS.left:
                    x = len(self.map[y]) - 1
                elif x >= len(self.map[y]) and dir == DIRECTIONS.right:
                    x = 0
                if y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y]) or self.map[y][x] == " ":
                    continue
            else:
                # Oh god why...
                if self.verbose:
                    print("Cube Move", p((x, y, dir)), end=" ")
                x, y, dir = self.cube_move(x, y, dir, len(self.map)//4)
                if self.verbose:
                    print("->", p((x, y, dir)))

            if self.map[y][x] == "#":
                return
            print((y+1, x+1), MOVE_NAME[self.direction])

            self.map[y][x] = MOVE_ASCII[self.direction]
            self.position = (y, x)
            self.direction = dir
            steps -= 1

    def print_map(self):
        for line in self.map:
            print("".join(line))

    def solve(self, path, part2: bool = False):
        idx = 0
        while idx < len(path):
            if self.verbose:
                self.print_map()
            if path[idx] == "L":
                self.turn_left()
                idx += 1
            elif path[idx] == "R":
                self.turn_right()
                idx += 1
            elif path[idx].isnumeric():
                start = idx
                while idx < len(path) and path[idx].isnumeric():
                    idx += 1
                self.move(int(path[start:idx]), part2)

        facing = 0
        if self.direction == DIRECTIONS.right:
            facing = 0
        elif self.direction == DIRECTIONS.down:
            facing = 1
        elif self.direction == DIRECTIONS.left:
            facing = 2
        elif self.direction == DIRECTIONS.up:
            facing = 3

        if self.verbose:
            self.print_map()
        print(p((*self.position, self.direction)), facing)
        return (self.position[0]+1) * 1000 + (self.position[1]+1) * 4 + facing


def _test(a, expected):
    mv = Dance.cube_move(*a)
    assert mv == expected, f"Q: {p(a)} Exp {p(expected)}, got {p(mv)}"


def test():
    print("1 => 6 (Up)")
    _test((50, 0, DIRECTIONS.up), (0, 150, DIRECTIONS.right))
    _test((99, 0, DIRECTIONS.up), (0, 199, DIRECTIONS.right))
    print("1 => 4 (Left)")
    _test((50, 0, DIRECTIONS.left), (0, 149, DIRECTIONS.right))
    _test((50, 49, DIRECTIONS.left), (0, 100, DIRECTIONS.right))
    print("1 => 2 (Right)")
    _test((99, 0, DIRECTIONS.right), (100, 0, DIRECTIONS.right))
    _test((99, 49, DIRECTIONS.right), (100, 49, DIRECTIONS.right))
    print("1 => 3 (Down)")
    _test((50, 49, DIRECTIONS.down), (50, 50, DIRECTIONS.down))
    _test((99, 49, DIRECTIONS.down), (99, 50, DIRECTIONS.down))

    print("2 => 6 (Up)")
    _test((100, 0, DIRECTIONS.up), (0, 199, DIRECTIONS.up))
    _test((149, 0, DIRECTIONS.up), (49, 199, DIRECTIONS.up))
    print("2 => 1 (Left)")
    _test((100, 0, DIRECTIONS.left), (99, 0, DIRECTIONS.left))
    _test((100, 49, DIRECTIONS.left), (99, 49, DIRECTIONS.left))
    print("2 => 5 (Right)")
    _test((149, 0, DIRECTIONS.right), (99, 149, DIRECTIONS.left))
    _test((149, 49, DIRECTIONS.right), (99, 100, DIRECTIONS.left))
    print("2 => 3 (Down)")
    _test((100, 49, DIRECTIONS.down), (99, 50, DIRECTIONS.left))
    _test((149, 49, DIRECTIONS.down), (99, 99, DIRECTIONS.left))

    print("3 => 1 (Up)")
    _test((50, 50, DIRECTIONS.up), (50, 49, DIRECTIONS.up))
    _test((99, 50, DIRECTIONS.up), (99, 49, DIRECTIONS.up))
    print("3 => 4 (Left)")
    _test((50, 50, DIRECTIONS.left), (0, 100, DIRECTIONS.down))
    _test((50, 99, DIRECTIONS.left), (49, 100, DIRECTIONS.down))
    print("3 => 2 (Right)")
    _test((99, 50, DIRECTIONS.right), (100, 49, DIRECTIONS.up))
    _test((99, 99, DIRECTIONS.right), (149, 49, DIRECTIONS.up))
    print("3 => 5 (Down)")
    _test((50, 99, DIRECTIONS.down), (50, 100, DIRECTIONS.down))
    _test((99, 99, DIRECTIONS.down), (99, 100, DIRECTIONS.down))

    print("4 => 3 (Up)")
    _test((0, 100, DIRECTIONS.up), (50, 50, DIRECTIONS.right))
    _test((49, 100, DIRECTIONS.up), (50, 99, DIRECTIONS.right))
    print("4 => 1 (Left)")
    _test((0, 100, DIRECTIONS.left), (50, 49, DIRECTIONS.right))
    _test((0, 149, DIRECTIONS.left), (50, 0, DIRECTIONS.right))
    print("4 => 5 (Right)")
    _test((49, 100, DIRECTIONS.right), (50, 100, DIRECTIONS.right))
    _test((49, 149, DIRECTIONS.right), (50, 149, DIRECTIONS.right))
    print("4 => 6 (Down)")
    _test((0, 149, DIRECTIONS.down), (0, 150, DIRECTIONS.down))
    _test((49, 149, DIRECTIONS.down), (49, 150, DIRECTIONS.down))

    print("5 => 3 (Up)")
    _test((50, 100, DIRECTIONS.up), (50, 99, DIRECTIONS.up))
    _test((99, 100, DIRECTIONS.up), (99, 99, DIRECTIONS.up))
    print("5 => 4 (Left)")
    _test((50, 100, DIRECTIONS.left), (49, 100, DIRECTIONS.left))
    _test((50, 149, DIRECTIONS.left), (49, 149, DIRECTIONS.left))
    print("5 => 2 (Right)")
    _test((99, 100, DIRECTIONS.right), (149, 49, DIRECTIONS.left))
    _test((99, 149, DIRECTIONS.right), (149, 0, DIRECTIONS.left))
    print("5 => 6 (Down)")
    _test((50, 149, DIRECTIONS.down), (49, 150, DIRECTIONS.left))
    _test((99, 149, DIRECTIONS.down), (49, 199, DIRECTIONS.left))

    print("6 => 4 (Up)")
    _test((0, 150, DIRECTIONS.up), (0, 149, DIRECTIONS.up))
    _test((49, 150, DIRECTIONS.up), (49, 149, DIRECTIONS.up))
    print("6 => 1 (Left)")
    _test((0, 150, DIRECTIONS.left), (50, 0, DIRECTIONS.down))
    _test((0, 199, DIRECTIONS.left), (99, 0, DIRECTIONS.down))
    print("6 => 5 (Right)")
    _test((49, 150, DIRECTIONS.right), (50, 149, DIRECTIONS.up))
    _test((49, 199, DIRECTIONS.right), (99, 149, DIRECTIONS.up))
    print("6 => 2 (Down)")
    _test((0, 199, DIRECTIONS.down), (100, 0, DIRECTIONS.down))
    _test((49, 199, DIRECTIONS.down), (149, 0, DIRECTIONS.down))

    print("All tests passed")


def main(test: bool = False):
    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    data = open(filename).read().splitlines()

    map = []
    for line in data:
        if line == "":
            break
        map.append(list(line))
    directions = data[-1]

    dance = Dance(map, test)

    # print("Part 1")
    # results = dance.solve(directions)
    # print(results)
    # if test:
    #     expected = 6032
    #     assert results == expected, f"Expected {expected}, got {results}"
    #     print("Test passed")

    # print("Part 2")
    results = dance.solve(directions, True)
    print(results)
    if test:
        print("Don't bother... won't run with the test data.  Wrong format.")
        expected = 5031
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "unit":
            test()
        else:
            main(True)
    else:
        main(False)
