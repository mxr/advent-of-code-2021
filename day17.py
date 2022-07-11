from __future__ import annotations

import functools
import re
from itertools import product


RE = re.compile(r"-?\d+")


def parse(filename: str) -> tuple[tuple[int, int], tuple[int, int]]:
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
def execute(filename: str) -> tuple[int, int]:
    (x1, x2), (y1, y2) = parse(filename)

    hits = set()
    ypm = -1

    for xv, yv in product(range(1, x2 + 1), range(y2, abs(y2) + 1)):

        @functools.lru_cache(maxsize=None)
        def x(t: int) -> int:
            if t == 0:
                return 0
            return x(t - 1) + max(0, xv - t + 1)  # noqa: B023

        def y(t: int) -> int:
            @functools.lru_cache(maxsize=None)
            def ypv(t: int) -> tuple[int, int]:
                if t == 0:
                    return 0, yv  # noqa: B023
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


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
