from __future__ import annotations

from typing import Generator


class Map:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid

        # memoize neighbors
        def neighbors(i: int, j: int) -> Generator[tuple[int, int, int], None, None]:
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

    return sum(p + 1 for p, _, _ in low_points(m))


def low_points(m: Map) -> Generator[tuple[int, int, int], None, None]:
    return (
        (p, i, j)
        for i, row in enumerate(m.grid)
        for j, p in enumerate(row)
        if all(p < n for n, _, _ in m.neighbors[i, j])
    )


def part2(filename: str) -> int:
    m = parse(filename)

    low_coords = [(i, j) for _, i, j in low_points(m)]

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

    basins = [basin(i, j) for i, j in low_coords]

    prod = 1
    for b in sorted(basins, reverse=True)[:3]:
        prod *= b

    return prod


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
