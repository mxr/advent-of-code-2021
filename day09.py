#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import Tuple


class Map:
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid

        # memoize neighbors
        def neighbors(i: int, j: int) -> Generator[Tuple[int, int, int], None, None]:
            for i_delta, j_delta in (-1, 0), (+1, 0), (0, -1), (0, +1):
                ni, nj = i + i_delta, j + j_delta

                if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                    yield grid[ni][nj], ni, nj

        self.neighbors = {
            (i, j): list(neighbors(i, j))
            for i, row in enumerate(grid)
            for j, _ in enumerate(row)
        }


def parse(filename: str) -> Map:
    with open(filename) as f:
        return Map([[int(n) for n in line.strip()] for line in f])


def part1(filename: str) -> int:
    m = parse(filename)

    risk = 0
    for i, row in enumerate(m.grid):
        for j, p in enumerate(row):
            if all(p < n for n, _, _ in m.neighbors[i, j]):
                risk += p + 1

    return risk


def part2(filename: str) -> int:
    m = parse(filename)

    low_points = [
        (i, j)
        for i, row in enumerate(m.grid)
        for j, p in enumerate(row)
        if all(p < n for n, _, _ in m.neighbors[i, j])
    ]

    seen = set()

    def basin(i: int, j: int) -> int:
        if (i, j) in seen:
            return 0
        seen.add((i, j))

        p = m.grid[i][j]
        if p == 9:
            return 0

        b = 1
        for n, ni, nj in m.neighbors[i, j]:
            if p < n and (ni, nj) not in seen:
                b += basin(ni, nj)

        return b

    basins = [basin(i, j) for i, j in low_points]
    top3 = sorted(basins, reverse=True)[:3]

    prod = 1
    for b in top3:
        prod *= b

    return prod


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
