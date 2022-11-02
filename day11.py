from __future__ import annotations

from collections.abc import Generator


class Map:
    def __init__(self, grid: list[list[int]]) -> None:
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

    def _loop_coords(self) -> Generator[tuple[int, int], None, None]:
        for i in range(self.height):
            for j in range(self.width):
                yield i, j

    def _neighbors(self, i: int, j: int) -> Generator[tuple[int, int], None, None]:
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


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
