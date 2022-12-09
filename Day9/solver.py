""" 
Consider a rope with a knot at each end; these knots mark the head and the tail of the rope. 
If the head moves far enough away from the tail, the tail is pulled toward the head.
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
import sys
from collections import defaultdict
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __and__(self, other):
        return Point(self.x & other.x, self.y & other.y)    

    def __or__(self, other):
        return Point(self.x | other.x, self.y | other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return f"({self.x}, {self.y})"



UP = Point(0, 1)
DOWN = Point(0, -1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
    

class Grid:
    def __init__(self, knots: int = 1):
        self.grid = defaultdict(lambda: defaultdict(int))
        self.head = Point(0, 0)
        self.tails = [Point(0, 0) for _ in range(knots)]

    def _determine_move(self, head, tail) -> Point:
        move = Point(0, 0)
        hx, hy = head
        tx, ty = tail
        if hx > tx + 1 or hx < tx - 1 or hy > ty + 1 or hy < ty - 1:
            if hx > tx: move |= RIGHT
            if hx < tx: move |= LEFT
            if hy > ty: move |= UP
            if hy < ty: move |= DOWN
        return move

    def move(self, direction):
        # Move Head
        if direction == 'R':
            self.head += RIGHT
        elif direction == 'U':
            self.head += UP
        elif direction == 'L':
            self.head += LEFT
        elif direction == 'D':
            self.head += DOWN

        # Tail(s) Follows
        head = self.head
        for tail in self.tails:
            tail += self._determine_move(head, tail)
            head = tail

        self.grid[head.x][head.y] = 1

    def touched(self):
        return sum([sum(self.grid[x].values()) for x in self.grid])

def main(filename):
    grid1 = Grid(1)
    grid2 = Grid(9)
    for line in open(filename):
        dir, dist = line.strip().split()
        for _ in range(int(dist)):
            grid1.move(dir)
            grid2.move(dir)
    
    print("Part 1:", grid1.touched())
    print("Part 2:", grid2.touched())

if __name__ == '__main__': 
    main(len(sys.argv) == 2 and sys.argv[1] or "input.txt")