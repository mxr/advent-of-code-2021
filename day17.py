#!/usr/bin/env python3
import functools
import re
from argparse import ArgumentParser
from itertools import product
from typing import Tuple

RE = re.compile(r"-?\d+")


def parse(filename: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    with open(filename) as f:
        line = f.read()

    # target area: x=20..30, y=-10..-5
    # order is: left right bottom top
    x1r, x2r, y2r, y1r = RE.findall(line)

    return (int(x1r), int(x2r)), (int(y1r), int(y2r))


def part1(filename: str) -> int:
    m, _ = execute(filename)

    return m


def part2(filename: str) -> int:
    _, n = execute(filename)

    return n


@functools.lru_cache(maxsize=1)
def execute(filename: str) -> Tuple[int, int]:
    (x1, x2), (y1, y2) = parse(filename)

    hits = set()
    ypm = -1

    for xv, yv in product(range(1, x2 + 1), range(y2, abs(y2) + 1)):

        @functools.lru_cache(maxsize=None)
        def x(t: int) -> int:
            if t == 0:
                return 0
            return x(t - 1) + max(0, xv - t + 1)

        def y(t: int) -> int:
            @functools.lru_cache(maxsize=None)
            def ypv(t: int) -> Tuple[int, int]:
                if t == 0:
                    return 0, yv
                py, pv = ypv(t - 1)
                return py + pv, pv - 1

            return ypv(t)[0]

        m = -1
        for t in range(1000):
            xp, yp = x(t), y(t)
            m = max(m, yp)
            if xp > x2 or yp < y2:
                break
            if x1 <= xp <= x2 and y1 >= yp >= y2:
                ypm = max(ypm, m)
                hits.add((xv, yv))

    return ypm, len(hits)


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
