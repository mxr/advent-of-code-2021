from __future__ import annotations

from collections import Counter


def parse(filename: str) -> list[int]:
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


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
