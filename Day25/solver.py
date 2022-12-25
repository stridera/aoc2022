import sys
from enum import Enum
from functools import cache

SNAFU = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

DEC = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',
}


def snafu_to_dec(input):
    res = 0
    chars = [*input]
    for i, char in enumerate(reversed(chars)):
        dec = SNAFU[char]
        res += dec * 5 ** i
    return res


def dec_to_snafu(input):
    # Convert to base5
    res = []
    while input > 0:
        input, rem = divmod(input + 2, 5)
        res.append(rem-2)
    # Convert to snafu
    for i, char in enumerate(res):
        res[i] = DEC[char]
    return ''.join(res[::-1])


def main(test: bool = False):
    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    data = open(filename).read().splitlines()
    results = 0
    for line in data:
        results += snafu_to_dec(line)
    results = dec_to_snafu(results)

    print("Part 1")
    print(results)

    if test:
        expected = '2=-1=0'
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    print("Done!!!!!!!!!!!")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "unit":
            test()
        else:
            main(True)
    else:
        main(False)
