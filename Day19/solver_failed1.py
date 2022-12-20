import sys
import re
from collections import defaultdict, namedtuple
from functools import cache
from dataclasses import dataclass
import math
from enum import Enum


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


class MaterialTuple(namedtuple('MaterialTuple', ['geode', 'obsidian', 'clay', 'ore'])):
    def __hash__(self):
        return hash(self.geode) * hash(self.obsidian) * hash(self.clay) * hash(self.ore)


class Minecraft:

    def __init__(self, blueprint: Blueprint, verbose: bool = False):
        self.blueprint = blueprint
        self.verbose = verbose
        self.materials = ['geode', 'obsidian', 'clay', 'ore', 'none']
        self.max_costs = max(cost for material in self.blueprint.costs.values() for cost in material.values())

    def log(self, message, end='\n'):
        if self.verbose:
            print(message, end=end)

    def index_of(self, mat):
        return self.materials.index(mat)

    @cache
    def should_build(self, currency, robots):
        materials = []
        for material in ['geode', 'obsidian', 'clay', 'ore']:
            if currency[self.index_of(material)] > self.max_costs:
                continue
            for required, cost in self.blueprint.costs[material].items():
                if material in ['geode', 'obsidian'] and required == 'ore':
                    continue
                if getattr(currency, required) + getattr(robots, required)*2 >= cost:
                    materials.append(material)
        return materials

    @cache
    def can_build(self, currency, material):
        if material == 'none':
            return True
        return all(currency[self.index_of(required)] >= cost
                   for required, cost in self.blueprint.costs[material].items())

    @cache
    def build(self, robots, currency, material):
        currency = [*currency]
        robots = [*robots]
        for required, cost in self.blueprint.costs[material].items():
            currency[self.index_of(required)] -= cost
        robots[self.index_of(material)] += 1

        return MaterialTuple(*robots), MaterialTuple(*currency)

    @cache
    def search(self, turn, currency: MaterialTuple, robots: MaterialTuple):
        if turn == 0:
            return currency.geode

        # print(f"Turn {turn}: {currency} {robots}")

        best = 0
        currency = MaterialTuple(*[currency[i] + robots[i] for i in range(4)])
        for material in self.should_build(currency, robots):
            if material and self.can_build(currency, material):
                best = max(best, self.search(turn - 1, *self.build(robots, currency, material)))
        else:
            best = max(best, self.search(turn - 1, currency, robots))
        return best

    def run(self, turn):
        return self.search(turn, MaterialTuple(0, 0, 0, 0), MaterialTuple(0, 0, 0, 1))


def main(test):
    if test:
        # print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    blueprints = []
    lines = open(filename).read().splitlines()
    for line in ' '.join(lines).split("Blueprint"):
        if line:
            id, data = line.split(":")
            blueprints.append(Blueprint.parse(int(id), data))

    # results = []
    # for idx, blueprint in enumerate(blueprints):
    #     results.append(Minecraft(blueprint, test).run(24) * (idx + 1))
    # print(f"Result: {results} sum: {sum(results)}")
    print([Minecraft(blueprint, test).run(24) * (idx + 1) for idx, blueprint in enumerate(blueprints)])
    results = sum([Minecraft(blueprint, test).run(24) * (idx + 1) for idx, blueprint in enumerate(blueprints)])
    if test:
        expected = 33
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    results = sum([Minecraft(blueprint, test).run(32) * (idx + 1) for idx, blueprint in enumerate(blueprints[:3])])
    print("Part 2")
    if test:
        expected = 1_514_285_714_288
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
