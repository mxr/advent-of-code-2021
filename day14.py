from __future__ import annotations

from collections import Counter
from itertools import tee


def parse(filename: str) -> tuple[str, dict[tuple[str, str], str]]:
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

            buckets[c1, c3] += v
            buckets[c3, c2] += v
            buckets[b] -= v

    mc = c.most_common()

    return mc[0][1] - mc[-1][1]


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
