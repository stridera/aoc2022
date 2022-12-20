import sys


def format_data(data: list[int], indexes: list[int]):
    return [data[idx] for idx in indexes]


def solve(data: list[int], aug: int = 1, test: bool = False):
    data = [d * aug for d in data]
    indexes = [i for i in range(len(data))]
    if test:
        print(format_data(data, indexes))
    for _ in range(10 if aug > 1 else 1):
        for idx, val in enumerate(data):
            sidx = indexes.index(idx)
            indexes.pop(sidx)
            indexes.insert((sidx + val) % (len(data) - 1), idx)
            if test:
                print(format_data(data, indexes))

    mixed = format_data(data, indexes)
    idx = mixed.index(0)
    return sum(mixed[(v + idx) % len(mixed)] for v in [1_000, 2_000, 3_000])


def main(test):
    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    data = list(map(int, open(filename).read().splitlines()))

    print("Part 1")
    results = solve(data, 1, test)
    print(results)
    if test:
        expected = 3
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    key = 811_589_153
    results = solve(data, key, test)
    print(results)
    if test:
        expected = 1_623_178_306
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
