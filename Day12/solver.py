import sys

from typing import Self, Union


class Node:
    def __init__(self, position: tuple[int, int], parent: Self, cost: int = 0) -> None:
        self.position = position
        self.parent = parent
        self.cost = cost

    def __eq__(self, o: Union[Self, tuple]) -> bool:
        if isinstance(o, tuple):
            return self.position == o

        return self.position == o.position

    def __lt__(self, o: Self) -> bool:
        return self.cost < o.cost

    def __repr__(self) -> str:
        return f"Node({self.position}, {self.parent}, {self.cost})"


class A_STAR:
    def __init__(self, grid, visualize=False) -> None:
        h, w = len(grid), len(grid[0])
        self.grid = grid
        self.visualize = visualize

    def solve(self, start, end, cost_function):
        """Find the shortest path from start to end"""
        self.open = []
        self.closed = []
        self.open.append(Node(start, None))
        candidates = {}
        while self.open:
            current = min(self.open)
            self.open.remove(current)
            self.closed.append(current)

            if self.grid[current.position[0]][current.position[1]] == end:
                path = []
                while current.parent is not None:
                    path.append(current.position)
                    current = current.parent
                path.append(current.position)
                candidates[len(path) - 1] = path
            neighbors = self.get_neighbors(current, cost_function)
            for neighbor in neighbors:
                if neighbor in self.closed:
                    continue

                if neighbor not in self.open:
                    self.open.append(neighbor)
                else:
                    if neighbor.cost < current.cost:
                        current = neighbor

        best = sorted(candidates.items(), key=lambda x: x[1], reverse=True)[0]
        if self.visualize:
            icons = {(0, 1): '>', (0, -1): '<', (1, 0): 'v', (-1, 0): '^'}
            grid = [['.'] * len(self.grid[0]) for _ in range(len(self.grid))]
            last = None
            for i, j in best[1]:
                if last is None:
                    grid[i][j] = 'E'
                else:
                    x, y = last
                    grid[i][j] = icons[(x - i, y - j)]
                last = (i, j)

            print('\n'.join(["".join(row) for row in grid]))
        return best[0]

    def get_neighbors(self, current: Node, cost_function):
        """Get all neighbors of current"""
        neighbors = []
        from_val = self.get_value(current.position[0], current.position[1])
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = current.position[0] + i, current.position[1] + j
            if self.is_valid(x, y):
                to_val = self.get_value(x, y)
                if cost_function(from_val, to_val):
                    neighbors.append(Node((x, y), current, current.cost + 1))
        return neighbors

    def get_value(self, x, y):
        """Get the value of a position"""
        val = self.grid[x][y]
        if val == 'S':
            val = 'a'
        if val == 'E':
            val = 'z'
        return ord(val) - ord('a')

    def is_valid(self, x, y):
        """Check if a position is valid"""
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) and (x, y) not in self.closed


def main(test):

    if test:
        print("Testing\nPart 1")
        filename = "test.txt"
    else:
        print("Part 1")
        filename = "input.txt"

    grid = open(filename).read().splitlines()

    start = None
    end = None
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "S":
                start = (i, j)
            if col == "E":
                end = (i, j)

    a_star = A_STAR(grid, visualize=True)
    results = a_star.solve(start, 'E', lambda from_val, to_val:  to_val <= from_val + 1)

    print("Results:", results)
    if test:
        assert results == 31, f"Expected 31, got {results}"
        print("Tests passed")

    print("Part 2")

    results = a_star.solve(end, 'a', lambda from_val, to_val:  to_val >= from_val - 1)

    print("Results:", results)
    if test:
        assert results == 29, f"Expected 29, got {results}"
        print("Tests passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
