import sys
from dataclasses import dataclass, field
import math
import time

OPS = {
    '+': int.__add__,
    '*': int.__mul__,
    '-': int.__sub__,
    '/': int.__truediv__,
}


@dataclass
class Monkey:
    items: list = field(default_factory=list)
    operation: str = ""
    divisor: int = 1
    true_target: str = ""
    false_target: str = ""
    inspections: int = 0

    def inspect(self, item):
        self.inspections += 1
        _, _, val1, op, val2 = self.operation.split()
        return OPS[op](val1 == "old" and item or int(val1), val2 == "old" and item or int(val2))


def process(filename: str, rounds, worry_relief=None):
    with open(filename) as f:
        lines = f.readlines()

    monkeys = {}
    while lines:
        line = lines.pop(0).strip()
        if not line:
            continue
        if line.startswith("Monkey"):
            monkey = Monkey()
            monkey_id = line.split(" ")[1].rstrip(':')
            monkey.items = [int(x) for x in lines.pop(0).strip().split(":")[1].strip().split(',')]
            monkey.operation = lines.pop(0).strip().split(":")[1].strip()
            monkey.divisor = int(lines.pop(0).strip().split(" ")[-1].strip())
            monkey.true_target = lines.pop(0).strip().split(" ")[-1].strip()
            monkey.false_target = lines.pop(0).strip().split(" ")[-1].strip()
            monkeys[monkey_id] = monkey

    lcm = math.prod([m.divisor for m in monkeys.values()])
    for _ in range(rounds):
        for monkey_id, monkey in monkeys.items():
            while monkey.items:
                item = monkey.items.pop(0)
                item = monkey.inspect(item)

                if worry_relief:
                    item = item // worry_relief

                item = item % lcm

                to = monkey.true_target if item % monkey.divisor == 0 else monkey.false_target
                monkeys[to].items.append(item)

    return math.prod(sorted([m.inspections for m in monkeys.values()], reverse=True)[:2])


def main(test):
    if test:
        print("Testing\nPart 1")
        filename = "test.txt"
        results = process(filename, 20, 3)
        assert results == 10605, f"Expected 10605, got {results}"
        print("Tests passed")

        print("Part 2")
        results = process(filename, 10_000)
        assert results == 2713310158, f"Expected 2713310158, got {results}"
        print("Tests passed")
    else:
        print("Part 1")
        filename = "input.txt"
        results = process(filename, 20)
        print(f"Result: {results}")

        print("\nPart 2")
        results = process(filename, 10_000)
        print(f"Result: {results}")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
