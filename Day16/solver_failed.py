import sys
import re
import itertools
from collections import defaultdict
from functools import cache
from tqdm import tqdm
import math


class Tunnels:
    def __init__(self, valves):
        self.valves = valves

        self.known_paths = defaultdict(dict)
        for valve in valves:
            for tunnel in valves[valve][1]:
                self.search(valve, tunnel)
                # self.known_paths[valve][tunnel] = valve + tunnel

    def _search(self, from_valve, to_valve, path=None):
        if path is None:
            path = from_valve
        if from_valve == to_valve:
            return path
        best = None
        for tunnel in self.valves[from_valve][1]:
            if tunnel in path:
                continue

            result = self._search(tunnel, to_valve, path + tunnel)
            if result is not None:
                if best is None or len(result) < len(best):
                    best = result
        return best

    @cache
    def search(self, from_valve, to_valve):
        return self._search(from_valve, to_valve)

    @cache
    def get_pressure(self, from_valve, to_valve):
        path = self.search(from_valve, to_valve)
        if path is not None:
            return sum(self.valves[tunnel][0] for tunnel in path[2:])

    def get_path(self, from_valve, to_valve):
        path = self.search(from_valve, to_valve)
        # print(f"Path: {from_valve}, {to_valve}, {path}")
        if path is not None:
            return path

    def process(self, minutes=30):
        # Find all combinations of the list so we can find the best path
        best_pressure = 0
        best_path = None

        pvalves = [valve for valve in self.valves if self.valves[valve][0] > 0]
        print(pvalves)
        for path in tqdm(itertools.permutations(pvalves), total=math.factorial(len(pvalves))):

            pressure = 0
            path_min = minutes
            from_valve = "AA"
            current_path = from_valve
            for next_valve in path:
                if self.valves[next_valve][0] == 0:
                    continue
                route = self.get_path(from_valve, next_valve)
                current_path += route[2:] + "**"
                path_min -= (len(route) // 2)
                pressure += self.valves[next_valve][0] * path_min
                if "".join(path) == 'DDBBJJHHEECC':
                    print(f'Path: {from_valve}, {next_valve}, {route} Pressure: {pressure} Time Remaining: {path_min}')
                from_valve = next_valve
            if "".join(path) == 'DDBBJJHHEECC':
                print(f'Path: AA, {", ".join(path)}  Pressure: {pressure}')
                print(f'Path: {current_path}  Pressure: {pressure}')
                self.print_path(current_path)
            if pressure > best_pressure:
                best_pressure = pressure
                best_path = current_path
        # self.print_path(best_path)
        print("Best Pressure: ", best_pressure)
        print("Best Path: ", best_path)
        return best_pressure

    def print_path(self, path):
        open = set()
        minutes = 30
        room = path[:2]
        path = path[2:]
        max_pressure = 0
        while minutes > 0:
            minutes -= 1
            print(f"== Minute {30 - minutes} ==")

            # Info
            if len(open) == 0:
                print("No valves are open.")
            else:
                pressure = sum(self.valves[tunnel][0] for tunnel in open)
                max_pressure += pressure
                print(f'Valves {", ".join(sorted(open))} are open, releasing {pressure} pressure.')

            if len(path) == 0:
                continue

            if path[:2] == "**":
                print(f"You open valve {room}.")
                open.add(room)
            else:
                room = path[:2]
                print(f"You move to valve {room}.")
            path = path[2:]

            print()
        print(f"Max Pressure: {max_pressure}")


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
        valves[tunnel] = (int(flow), to_valves)
    print("Part 1")
    tunnels = Tunnels(valves)
    results = tunnels.process()

    print(f"Result: {results}")
    if test:
        expected = 1651
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
