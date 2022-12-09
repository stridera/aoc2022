'''
Example input:
    Part One:
    bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
    nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11

    Part Two:
    mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
    bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
    nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26

'''
import sys
from typing import List


def all_different(arr: List[str]) -> bool:
    return len(set(arr)) == len(arr)


def find_start_of_packet(line: str, size: int) -> int:
    line_array = list(line)
    for i in range(size, len(line_array)):
        if all_different(line_array[i-size:i]):
            return i
    return -1


def process(file):
    with open(file) as f:
        line = f.read()
        print("Part One: ", find_start_of_packet(line, 4))
        print("Part Two: ", find_start_of_packet(line, 14))


def test():
    print("Test Part One")
    assert find_start_of_packet("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert find_start_of_packet("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert find_start_of_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert find_start_of_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11
    print("Passed")

    print("Test Part two")
    assert find_start_of_packet("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert find_start_of_packet("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert find_start_of_packet("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert find_start_of_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert find_start_of_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26
    print("Passed")


if __name__ == '__main__':
    filename = len(sys.argv) == 2 and sys.argv[1] or "input.txt"
    test()
    process(filename)
