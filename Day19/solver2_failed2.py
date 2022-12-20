import sys
import re
from collections import defaultdict
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


@dataclass
class Materials:
    geode: int
    obsidian: int
    clay: int
    ore: int

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __hash__(self):
        return hash(self.geode) * hash(self.obsidian) * hash(self.clay) * hash(self.ore)

    def __str__(self):
        return f"Materials(geode={self.geode}, obsidian={self.obsidian}, clay={self.clay}, ore={self.ore})"

    def __repr__(self):
        return self.__str__()

    def items(self):
        return [('geode', self.geode), ('obsidian', self.obsidian), ('clay', self.clay), ('ore', self.ore)]


class Minecraft:
    def __init__(self, blueprint: Blueprint, verbose: bool = False):
        self.blueprint = blueprint
        self.currency: Materials = Materials(0, 0, 0, 0)
        self.robots: Materials = Materials(0, 0, 0, ore=1)
        self.verbose = verbose
        self.materials = ['geode', 'obsidian', 'clay', 'ore']

        # Get the maximum cost of any robot
        self.max_cost = Materials(0, 0, 0, 0)
        for material in self.blueprint.costs.values():
            for mat, cost in material.items():
                self.max_cost[mat] = max(self.max_cost[mat], cost)

    def log(self, message, end='\n'):
        if self.verbose:
            print(message, end=end)

    def mine(self):
        for produces, amount in self.robots.items():
            if amount == 0:
                continue
            self.log(f"{amount} {produces}-collecting robot collects {amount} {produces}; ", end='')
            self.currency[produces] += amount
            self.log(f"you now have {self.currency[produces]} {produces}.")

    def should_build2(self, days_remaining):
        """ If we were to build robots today, how many geodes would we have when we run out of days?"""
        materials = ['geode', 'obsidian', 'clay', 'ore']

        best = 0
        best_robot = 'clay'

        for new_robot in materials:
            final_cur = Materials(*[self.currency[material] + self.robots[material]
                                  * days_remaining for material in materials])
            final_cur[materials.index(new_robot)] += days_remaining
            print(new_robot, final_cur)
            for _ in range(days_remaining):
                building = None
                if self.can_build(materials.index('geode'), final_cur):
                    building = 'geode'
                elif self.can_build(materials.index('obsidian'), final_cur):
                    building = 'obsidian'
                elif self.can_build(materials.index('clay'), final_cur):
                    building = 'clay'
                elif self.can_build(materials.index('ore'), final_cur):
                    building = 'ore'
                if building:
                    for material, cost in self.blueprint.costs[building].items():
                        final_cur[materials.index(material)] -= cost
            if final_cur[0] > best:
                best = final_cur[0]
                best_robot = new_robot
        return best_robot

    def should_build(self, days_remaining: int):
        """ If we were to build robots today, how many geodes would we have when we run out of days?"""
        # Can we build a geode?  If so, do it.
        if self.can_build('geode'):
            return 'geode'

        # Can we build an obsidian?  Do we have more obsidian than we need?
        if (self.can_build('obsidian') and self.still_need('obsidian', days_remaining)):
            return 'obsidian'

        # Now that we prioritized the higher order robots, we can decide if we need more clay.
        if (self.still_need('clay', days_remaining)
                and self.still_need('clay', days_remaining)
                and self.still_need('obsidian', days_remaining)):
            return 'clay'

        if self.still_need('ore', days_remaining):
            return 'ore'

        return None

    def still_need(self, material: str, days_remaining: int):
        """ Do we have more of this material than we need? """
        max_required = self.max_cost[material] * days_remaining - self.currency[material]
        return max_required / days_remaining > self.robots[material]

    def can_build(self, material: str):
        return all(self.currency[required] >= cost for required, cost in self.blueprint.costs[material].items())

    def build(self, days):
        new_robot = None
        material = self.should_build(days)
        print("Want to build", material)
        if material is not None and self.can_build(material):
            new_robot = material
            cost_str = ', '.join(f"{cost} {material}" for material, cost in self.blueprint.costs[material].items())
            self.log(f"Spend {cost_str} to start building a {material}-collecting robot.")
            robot_cost = self.blueprint.costs[material]
            for material, cost in robot_cost.items():
                self.currency[material] -= cost
        return new_robot

    def run(self, days):
        self.robots['ore'] = 1
        for day in range(days):
            self.log(f"== Minute {day + 1} ==")
            new_robot = self.build(days)
            self.mine()
            if new_robot:
                self.robots[new_robot] += 1
                self.log(
                    f"The new {new_robot}-collecting robot is ready you now have {self.robots[new_robot]} of them.")
            self.log("")
        return self.currency['geode']


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

    results = []
    for idx, blueprint in enumerate(blueprints):
        results.append(Minecraft(blueprint, test).run(24) * (idx + 1))
    print(f"Result: {results} sum: {sum(results)}")
    results = sum(results)
    if test:
        expected = 33
        assert results == expected, f"Expected {expected}, got {results}"
        print("Test passed")

    # print("Part 2")
    # if test:
    #     expected = 1_514_285_714_288
    #     assert results == expected, f"Expected {expected}, got {results}"
    #     print("Test passed")


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
