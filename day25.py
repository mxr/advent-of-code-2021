#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import Tuple


class Map:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.height, self.width = len(self.grid), len(self.grid[0])

    def move(self) -> bool:
        moved = False

        for i in range(self.height):
            can_move = [
                (j, nj)
                for j, nj in self.jnj()
                if self.grid[i][j] == ">" and self.grid[i][nj] == "."
            ]
            for j, nj in can_move:
                self.grid[i][j], self.grid[i][nj] = ".", ">"

            moved |= bool(can_move)

        for j in range(self.width):
            can_move = [
                (i, ni)
                for i, ni in self.ini()
                if self.grid[i][j] == "v" and self.grid[ni][j] == "."
            ]
            for i, ni in can_move:
                self.grid[i][j], self.grid[ni][j] = ".", "v"

            moved |= bool(can_move)

        return moved

    def ini(self) -> Generator[Tuple[int, int], None, None]:
        for i in range(self.height):
            yield i, (i + 1) % self.height

    def jnj(self) -> Generator[Tuple[int, int], None, None]:
        for j in range(self.width):
            yield j, (j + 1) % self.width


def parse(filename: str) -> Map:
    with open(filename) as f:
        return Map([list(line.strip()) for line in f])


def part1(filename: str) -> int:
    m = parse(filename)

    c = 1
    while m.move():
        c += 1

    return c


def part2(filename: str) -> int:
    return -1


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
