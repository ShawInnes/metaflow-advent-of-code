from metaflow import FlowSpec, step, card, IncludeFile, Parameter
import itertools


def batch(iterable, size):
    it = iter(iterable)
    while item := list(itertools.islice(it, size)):
        yield item


def script_path(filename):
    import os

    filepath = os.path.join(os.path.dirname(__file__))
    return os.path.join(filepath, filename)


def get_duplicate(rucksack):
    half_length = len(rucksack) // 2
    part1 = rucksack[:half_length]
    part2 = rucksack[half_length:]
    duplicate = list(set(part1) & set(part2))[0]
    return duplicate


def get_group_badge(group):
    duplicate = list(set(group[0]) & set(group[1]) & set(group[2]))[0]
    return duplicate


priority = "-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def lookup_priority(item):
    return priority.rindex(item)


class PlayListFlow(FlowSpec):

    input_data = IncludeFile(
        "input_data",
        default=script_path("day03.txt"),
    )

    @card
    @step
    def start(self):
        self.rucksacks = list(self.input_data.split("\n"))

        self.next(self.part1_start, self.part2_start)

    @card
    @step
    def part1_start(self):

        self.next(self.part1, foreach="rucksacks")

    @card
    @step
    def part2_start(self):
        self.groups = list(batch(self.rucksacks, 3))

        self.next(self.part2, foreach="groups")

    @card
    @step
    def part1(self):
        self.rucksack = self.input

        print("Computing statistics for %s" % self.rucksack)

        self.duplicate = get_duplicate(self.rucksack)
        self.priority = lookup_priority(self.duplicate)

        self.next(self.join1)

    @card
    @step
    def part2(self):
        self.group = self.input

        print("Computing statistics for %s" % self.group)

        self.badge = get_group_badge(self.group)
        self.priority = lookup_priority(self.badge)

        self.next(self.join2)

    @card
    @step
    def join1(self, inputs):

        self.sum = sum(inp.priority for inp in inputs)

        self.next(self.join_final)

    @card
    @step
    def join2(self, inputs):
        self.sum = sum(inp.priority for inp in inputs)

        self.next(self.join_final)

    @card
    @step
    def join_final(self, inputs):
        self.part1_sum = inputs.join1.sum
        self.part2_sum = inputs.join2.sum
        self.next(self.end)

    @card
    @step
    def end(self):
        print("The Part 1 answer is %d" % self.part1_sum)
        print("The Part 2 answer is %d" % self.part2_sum)


if __name__ == "__main__":
    PlayListFlow()
