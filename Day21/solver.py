import sys
OPS = {
    '+': int.__add__,
    '*': int.__mul__,
    '-': int.__sub__,
    # '/': int.__truediv__,
    '/': int.__floordiv__
}


def solve(data, part):
    monkeys = {}
    for line in data:
        monkey, value = line.split(":")
        monkeys[monkey] = value.strip()

    def calculate(monkey):
        value = monkeys[monkey]
        if value.isnumeric():
            return int(value)
        else:
            val1, op, val2 = value.split()
            return OPS[op](calculate(val1), calculate(val2))

    if part == 1:
        return calculate("root")
    else:
        first, _, second = monkeys["root"].split()
        # Second doesn't change, so we only need to work with the first
        # Also the first number is inversely proportional supplied number
        monkeys['humn'] = "THIS WILL THROW AN ERROR IF PART2 CHECKS HUMAN", True
        wanted = calculate(second)

        # Need to figure out if the numbers rise or lower
        monkeys['humn'] = str(1)
        test1 = calculate(first)
        monkeys['humn'] = str(100)
        test2 = calculate(first)

        increasing = False
        if test1 > test2:
            increasing = True

        # Lets expand wildly until we find the range
        low = 0
        high = 100
        # Rapid growth phase
        while True:
            monkeys['humn'] = str(high)
            test = calculate(first)

            if test == wanted:
                return low
            if (increasing and test < wanted) or (not increasing and test > wanted):
                break
            else:
                low = high
                high = high * 2

        print("Found range", low, high)
        # Binary search phase
        i = 0
        while True:
            i += 1
            if i > 50:
                break
            middle = (low + high) // 2
            monkeys['humn'] = str(middle)
            test = calculate(first)
            if test == wanted:
                return middle
            if (increasing and test < wanted) or (not increasing and test > wanted):
                high = middle
            else:
                low = middle


def main(test):
    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    data = open(filename).read().splitlines()

    print("Part 1")
    results = solve(data, 1)
    print(results)
    if test:
        expected = 152
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    results = solve(data, 2)
    print(results)
    if test:
        expected = 301
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
