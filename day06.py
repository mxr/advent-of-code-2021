#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
from typing import List


def parse(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(f) for f in f.read().split(",")]


def execute(filename: str, days: int) -> int:
    fish = parse(filename)
    ages = Counter(fish)

    for _ in range(days):
        new_ages: Counter[int] = Counter()
        for age, count in ages.items():
            if age == 0:
                new_ages[6] += count
                new_ages[8] += count
            else:
                new_ages[age - 1] += count
        ages = new_ages

    return sum(ages.values())


def part1(filename: str) -> int:
    return execute(filename, 80)


def part2(filename: str) -> int:
    return execute(filename, 256)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=0)
    parser.add_argument("-f", "--filename", type=str, required=True)

    args = parser.parse_args()

    part: int = args.part
    filename: str = args.filename

    if (part or 1) == 1:
        print(f"part1: {part1(filename)}")
    if (part or 2) == 2:
        print(f"part2: {part2(filename)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
