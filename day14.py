#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
from itertools import tee
from typing import Dict
from typing import Tuple


def parse(filename: str) -> Tuple[str, Dict[Tuple[str, str], str]]:
    with open(filename) as f:
        start, raw_rules = f.read().split("\n\n")

    rules = {}
    for r in raw_rules.splitlines():
        s, _, e = r.partition(" -> ")
        rules[s[0], s[1]] = e

    return start, rules


def part1(filename: str) -> int:
    return execute(filename, 10)


def part2(filename: str) -> int:
    return execute(filename, 40)


def execute(filename: str, n: int) -> int:
    start, rules = parse(filename)

    c = Counter(start)

    s1, s2 = tee(start)
    next(s2)
    buckets = Counter(zip(s1, s2))
    for _ in range(n):
        for b, v in tuple(buckets.items()):  # avoid mutating while iterating
            (c1, c2), c3 = b, rules[b]

            c[c3] += v

            buckets[(c1, c3)] += v
            buckets[(c3, c2)] += v
            buckets[b] -= v

    mc = c.most_common()

    return mc[0][1] - mc[-1][1]


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
