import sys
import re
from functools import cache
from dataclasses import dataclass


@dataclass
class Valve:
    pressure: int
    tunnels: list[str]


class Tunnels:
    def __init__(self, valves: dict[str, Valve]):
        self.valves = valves
        self.minutes = 0

    def run(self, minutes: int, helpers: int = 0):
        self.minutes = minutes
        return self.search(helpers, minutes, frozenset(), 'AA')

    @cache
    def search(self, helpers: int, minutes: int, opened: frozenset, current: str):
        if minutes == 0:
            if helpers > 0:
                return self.search(helpers-1, self.minutes, opened, 'AA')
            else:
                return 0

        # Branch out
        best = 0
        minutes -= 1

        # Try w/o opening any valves first
        for tunnel in self.valves[current].tunnels:
            best = max(best, self.search(helpers, minutes, opened, tunnel))

        # Now open the valve (if appropriate) and try again
        pressure = self.valves[current].pressure
        if pressure > 0 and current not in opened and minutes > 0:
            new_opened = set(opened)
            new_opened.add(current)
            pressure *= minutes
            for tunnel in self.valves[current].tunnels:
                best = max(best, pressure + self.search(helpers, minutes-1, frozenset(new_opened), tunnel))

        return best


def main(test):

    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"
    valves = {}
    for line in open(filename):
        matches = re.match(
            r"^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$", line)
        tunnel, flow, valve_list = matches.groups()
        to_valves = valve_list.split(", ")
        valves[tunnel] = Valve(int(flow), to_valves)

    tunnels = Tunnels(valves)

    print("Part 1")
    results = tunnels.run(30)
    print(f"Result: {results}")
    if test:
        expected = 1651
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    results = tunnels.run(26, 1)

    print(f"Result: {results}")
    if test:
        expected = 1707
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
