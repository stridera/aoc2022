import sys
import re
from collections import defaultdict, namedtuple
from functools import cache
from dataclasses import dataclass
import math
from enum import Enum, auto


@dataclass
class Blueprint:
    id: int
    costs: defaultdict[str, defaultdict[str, int]]

    @staticmethod
    def parse(id: int, line: str):
        id = int(id)
        costs = defaultdict(dict)
        for part in line.split(". "):
            part = part.strip()
            matches = re.match(r"Each (\w+) robot costs (\d+) (\w+)(?: and (\d+) (\w+))?", part)
            if matches:
                costs[matches[1]][matches[3]] = int(matches[2])
                if matches[4]:
                    costs[matches[1]][matches[5]] = int(matches[4])

        return Blueprint(id, costs)


class Materials(Enum):
    geode = "geode"
    obsidian = "obsidian"
    clay = "clay"
    ore = "ore"


class Minecraft:
    def __init__(self, blueprint: Blueprint, verbose: bool = False):
        self.blueprint = blueprint
        self.verbose = verbose
        self.materials = [material.value for material in Materials]

        # Get the maximum cost of any robot
        self.max_cost = [0, 0, 0, 0]
        for material in self.blueprint.costs.values():
            for mat, cost in material.items():
                self.max_cost[self.materials.index(mat)] = max(self.max_cost[self.materials.index(mat)], cost)

    def can_build(self, material: str, currency: tuple[int, int, int, int]):
        return all(currency[self.materials.index(required)] >= cost
                   for required, cost in self.blueprint.costs[material].items())

    def still_need(self, material: str, currency:  tuple[int, int, int, int],
                   robots:  tuple[int, int, int, int], days_remaining: int):
        """ Do we have more of this material than we need? """
        max_required = self.max_cost[self.materials.index(
            material)] * days_remaining - self.get_item(currency, material)
        return max_required / days_remaining > self.get_item(robots, material)

    def get_item(self, data: tuple[int, int, int, int] | dict, item: str):
        if isinstance(data, dict):
            if item in data:
                return data[item]
            else:
                return 0
        return data[self.materials.index(item)]

    @cache
    def _run(self, days_remaining: int, currency: tuple[int, int, int, int], robots: tuple[int, int, int, int]) -> int:
        # print(f"Days remaining: {days_remaining}, currency: {currency}, robots: {robots}")
        if days_remaining == 0:
            return self.get_item(currency, Materials.geode.value)

        # Can we build a geode?  If so, do it.
        attempts = []
        if self.can_build(Materials.geode.value, currency):
            attempts.append((self.blueprint.costs[Materials.geode.value], (1, 0, 0, 0)))

        # Can we build an obsidian?  Do we have more obsidian than we need?
        elif (self.can_build(Materials.obsidian.value, currency)
              and self.still_need(Materials.obsidian.value, currency, robots, days_remaining)):
            attempts.append((self.blueprint.costs[Materials.obsidian.value], (0, 1, 0, 0)))

        else:
            # Now that we prioritized the higher order robots, we can check for the lower order robots for the best value
            if (self.can_build(Materials.clay.value, currency)
                    and self.still_need(Materials.clay.value, currency, robots, days_remaining)
                    and self.still_need(Materials.obsidian.value, currency, robots, days_remaining)):
                attempts.append((self.blueprint.costs[Materials.clay.value], (0, 0, 1, 0)))

            if (self.can_build(Materials.ore.value, currency)
                    and self.still_need(Materials.ore.value, currency, robots, days_remaining)):
                attempts.append((self.blueprint.costs[Materials.ore.value], (0, 0, 0, 1)))
            else:
                # Don't build anything (Save up for the next day)
                attempts.append(((0, 0, 0, 0), (0, 0, 0, 0)))

        best = 0
        for costs, new_robots in attempts:
            best = max(best,
                       self._run(days_remaining - 1,
                                 tuple(self.get_item(currency, item) + self.get_item(robots, item) - self.get_item(costs, item)
                                       for item in self.materials),
                                 tuple(self.get_item(robots, item) + self.get_item(new_robots, item) for item in self.materials)))
        return best

    def run(self, days_remaining: int):
        return self._run(days_remaining, (0, 0, 0, 0), (0, 0, 0, 1))


def main(test):
    if test:
        # print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    blueprints: list[Blueprint] = []
    lines = open(filename).read().splitlines()
    for line in ' '.join(lines).split("Blueprint"):
        if line:
            id, data = line.split(":")
            blueprints.append(Blueprint.parse(int(id), data))

    print("Part 1")
    results = sum([Minecraft(blueprint, test).run(24) * (idx + 1) for idx, blueprint in enumerate(blueprints)])
    print(results)
    if test:
        expected = 33
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    print("Part 2")
    results = math.prod([Minecraft(blueprint, test).run(32) for blueprint in blueprints[:3]])
    print(results)
    if test:
        expected = 3348
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
