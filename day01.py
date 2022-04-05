from __future__ import annotations

from typing import Generator


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for line in f:
            yield int(line)


def part1(filename: str) -> int:
    prev, *nums = parse(filename)

    num_inc = 0
    for n in nums:
        if n > prev:
            num_inc += 1
        prev = n

    return num_inc


def part2(filename: str) -> int:
    ppprev, pprev, prev, *nums = parse(filename)

    num_inc = 0
    for n in nums:
        psum = ppprev + pprev + prev

        csum = psum - ppprev + n
        if csum > psum:
            num_inc += 1
        ppprev, pprev, prev = pprev, prev, n

    return num_inc


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
