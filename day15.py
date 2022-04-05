from __future__ import annotations

import sys
from collections import defaultdict
from typing import Dict
from typing import NewType
from typing import Tuple


Graph = NewType("Graph", Dict[Tuple[int, int], Dict[Tuple[int, int], int]])


class Map:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.height, self.width = len(self.grid), len(self.grid[0])

    def expand(self) -> None:
        new_grid = [[0] * self.height * 5 for _ in range(self.width * 5)]
        for i in range(self.height * 5):
            for j in range(self.width * 5):
                (qi, ri), (qj, rj) = divmod(i, self.height), divmod(j, self.width)
                new_grid[i][j] = 1 + (self.grid[ri][rj] + qi + qj - 1) % 9

        self.grid = new_grid
        self.height, self.width = len(self.grid), len(self.grid[0])

    def risk(self) -> int:
        # mypy has weak support for defaultdict with lambda
        # potentially related:
        # https://github.com/python/mypy/issues/1205
        # https://github.com/python/mypy/issues/7217
        graph = Graph(defaultdict(lambda: defaultdict(dict)))  # type: ignore

        for i in range(self.height):
            for j in range(self.width):
                for di, dj in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        graph[i, j][ni, nj] = self.grid[ni][nj]
                        graph[ni, nj][i, j] = self.grid[i][j]

        min_dists = {k: sys.maxsize for k in graph}
        min_dists[0, 0] = 0

        # TODO - very slow :)
        q = set(graph)
        while q:
            closest = min(q, key=lambda ij: min_dists[ij])

            for nbr, dist in graph[closest].items():
                min_dists[nbr] = min(min_dists[nbr], min_dists[closest] + dist)

            q.remove(closest)

        return min_dists[self.height - 1, self.width - 1]


def parse(filename: str) -> Map:
    with open(filename) as f:
        grid = [[int(n) for n in line.strip()] for line in f]

    return Map(grid)


def part1(filename: str) -> int:
    m = parse(filename)

    return m.risk()


def part2(filename: str) -> int:
    m = parse(filename)
    m.expand()

    return m.risk()


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
