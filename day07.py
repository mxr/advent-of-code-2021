#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Callable
from typing import List


def parse(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(f) for f in f.read().split(",")]


def part1(filename: str) -> int:
    return execute(filename, fuel_part1)


def part2(filename: str) -> int:
    return execute(filename, fuel_part2)


def execute(filename: str, fuel_func: Callable[[int, int], int]) -> int:
    crabs = parse(filename)
    min_fuel = sum(fuel_func(c, 0) for c in crabs)
    for i in range(1, max(crabs)):
        m = 0
        for c in crabs:
            m += fuel_func(c, i)
            if m > min_fuel:
                break
        else:
            min_fuel = m

    return min_fuel


def fuel_part1(crab: int, i: int) -> int:
    return abs(crab - i)


def fuel_part2(crab: int, i: int) -> int:
    n = abs(crab - i)
    return n * (n + 1) // 2


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
