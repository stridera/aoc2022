import sys
from enum import Enum
from functools import cache

# set recursion limit to 10000
sys.setrecursionlimit(10_000)


class DIRECTIONS(Enum):
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)
    stay = (0, 0)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


MOVE_ASCII = {
    DIRECTIONS.up: '^',
    DIRECTIONS.right: '>',
    DIRECTIONS.down: 'v',
    DIRECTIONS.left: '<',
    DIRECTIONS.stay: '.',
}

MOVE = {
    DIRECTIONS.up: lambda y, x: (y - 1, x),
    DIRECTIONS.right: lambda y, x: (y, x + 1),
    DIRECTIONS.down: lambda y, x: (y + 1, x),
    DIRECTIONS.left: lambda y, x: (y, x - 1),
    DIRECTIONS.stay: lambda y, x: (y, x),
}

MOVE_MAP = {
    '^': DIRECTIONS.up,
    '>': DIRECTIONS.right,
    'v': DIRECTIONS.down,
    '<': DIRECTIONS.left,
    '.': DIRECTIONS.stay,
}


class ColdValley:
    def __init__(self, map):
        self.size = (len(map), len(map[0]))
        self.max = 350
        stage = []
        for y, line in enumerate(map):
            for x, char in enumerate(line):
                if char in ['>', '<', '^', 'v']:
                    stage.append((y, x, MOVE_MAP[char]))
        stage = frozenset(stage)

        # Created all the possible iterations of the blizzards
        blizzards = []
        for _ in range(len(map) * len(map[0])):
            blizzards.append(stage)
            stage = self.move_blizzards(stage)
        self.blizzards = tuple(blizzards)

        self.seen = dict()

    def get_blizzard(self, step) -> frozenset[tuple[int, int, DIRECTIONS]]:
        return self.blizzards[step % len(self.blizzards)]

    def format_grid(self, location, goal, step):
        grid = [['.'] * self.size[1] for _ in range(self.size[0])]
        for y, row in enumerate(grid):
            if y == 0 or y == len(grid) - 1:
                for x, _ in enumerate(row):
                    row[x] = '#'
            else:
                row[0] = '#'
                row[-1] = '#'
        grid[location[0]][location[1]] = 'E'
        for blizzard in self.get_blizzard(step):
            by, bx, d = blizzard
            if grid[by][bx] == '.':
                grid[by][bx] = MOVE_ASCII[d]
            elif grid[by][bx].isdigit():
                grid[by][bx] = str(int(grid[by][bx]) + 1)
            else:
                grid[by][bx] = '2'
        grid[goal[0]][goal[1]] = 'G'
        output = '\n'
        for row in grid:
            output += ''.join(row) + '\n'
        return output

    @cache
    def move_blizzards(self, blizzards: frozenset[tuple[int, int, DIRECTIONS]]) -> frozenset:
        sy, sx = self.size
        new_blizzards = set()
        for blizzard in blizzards:
            by, bx, direction = blizzard
            new_y, new_x = MOVE[direction](by, bx)
            # If we hit the edge, we end up on the opposite side
            if new_y <= 0:
                new_y = sy - 2
            elif new_y >= sy - 1:
                new_y = 1
            if new_x <= 0:
                new_x = sx - 2
            elif new_x >= sx - 1:
                new_x = 1
            new_blizzards.add((new_y, new_x, direction))
        return frozenset(new_blizzards)

    @cache
    def snow_walk(self, location: tuple[int, int], goal: tuple[int, int], step: int = 0) -> tuple[str, int]:
        log = f"Step {step}: ({location} -> {goal})\n"
        grid_log = self.format_grid(location, goal, step)

        if step > self.max:
            return '', -1

        if ((location, step % len(self.blizzards)) in self.seen and
                self.seen[(location, step % len(self.blizzards))] < step):
            # log += f'Already seen this location at a lower step.  Skipping.\n'
            return '', -1

        self.seen[(location, step % len(self.blizzards))] = step

        best = self.max
        best_log = ''
        for direction in DIRECTIONS:
            new_y, new_x = MOVE[direction](*location)
            log += f'\t{direction} to: {(new_y, new_x)} '
            if (new_y, new_x) == goal:
                log += grid_log + f'Goal!  {step + 1} steps\n'
                return log, step + 1
            if direction != DIRECTIONS.stay and (new_y <= 0 or new_y >= self.size[0] - 1 or new_x <= 0 or new_x >= self.size[1] - 1):
                log += f'Out of bounds.\n'
                continue
            if any((new_y, new_x) == flurry[0: 2] for flurry in self.get_blizzard(step+1)):
                log += f'blizzed.\n'
                continue
            log += f'ok.  Walking to: {new_y}, {new_x} '
            attempt_log, attempt = self.snow_walk((new_y, new_x), goal, step + 1)
            log += f' = {attempt} steps\n'
            if attempt != -1 and attempt < best:
                best_log = attempt_log
                best = attempt

        resp = ''
        for l, r in zip(grid_log.split('\n'), log.split('\n')):
            resp += l + r + '\n'
        return resp + best_log, best


def main(test: bool = False):
    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    map = open(filename).read().splitlines()
    cv = ColdValley(map)

    start = 0, map[0].index('.')
    goal = len(map) - 1, map[-1].index('.')

    print("Part 1")
    log, r1 = cv.snow_walk(start, goal)
    print(r1)
    if test:
        print(log)
        expected = 18
        assert r1 == expected, f"Expected {expected}, got {r1}"
        print("Test passed")

    # print("Part 2")
    log2, r2 = cv.snow_walk(goal, start, r1+1)
    log3, r3 = cv.snow_walk(start, goal, r2+1)
    if test:
        print(log2)
        print(log3)
        expected = 54
        results = r3
        assert r3 == expected, f"Expected {expected}, got {results}"
        print("Test passed")
    print(r1, r2, r3)


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
