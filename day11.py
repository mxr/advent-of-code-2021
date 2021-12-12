#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import Tuple


class Map:
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.height, self.width = len(self.grid), len(self.grid[0])
        self.steps = 0

    def step(self) -> int:
        self.steps += 1

        for i, j in self._loop_coords():
            self.grid[i][j] += 1

        q = [(i, j) for i, j in self._loop_coords() if self.grid[i][j] > 9]
        flashed = set(q)
        while q:
            i, j = q.pop()
            for ni, nj in self._neighbors(i, j):
                self.grid[ni][nj] += 1
                if self.grid[ni][nj] > 9 and (ni, nj) not in flashed:
                    q.append((ni, nj))
                    flashed.add((ni, nj))

        for i, j in flashed:
            self.grid[i][j] = 0

        return len(flashed)

    def all_flashed(self) -> bool:
        return all(self.grid[i][j] == 0 for i, j in self._loop_coords())

    def _loop_coords(self) -> Generator[Tuple[int, int], None, None]:
        for i in range(self.height):
            for j in range(self.width):
                yield i, j

    def _neighbors(self, i: int, j: int) -> Generator[Tuple[int, int], None, None]:
        for di in (-1, 0, +1):
            for dj in (-1, 0, +1):
                if di == dj == 0:
                    continue

                ni, nj = i + di, j + dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    yield ni, nj


def parse(filename: str) -> Map:
    with open(filename) as f:
        grid = [[int(n) for n in line.strip()] for line in f]

    return Map(grid)


def part1(filename: str) -> int:
    m = parse(filename)

    return sum(m.step() for _ in range(100))


def part2(filename: str) -> int:
    m = parse(filename)

    while not m.all_flashed():
        m.step()

    return m.steps


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
