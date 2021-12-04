#!/usr/bin/env python3
from argparse import ArgumentParser
from dataclasses import dataclass
from itertools import zip_longest
from typing import Dict
from typing import List
from typing import Tuple


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)


@dataclass
class Cell:
    value: int
    marked: bool = False

    def mark(self) -> None:
        self.marked = True


class Board:
    def __init__(self, grid: List[List[Cell]]) -> None:
        self._nums: Dict[int, Tuple[int, int, Cell]] = {}
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                self._nums[cell.value] = (i, j, cell)

        self.grid = grid
        self._last_marked = (-1, -1)
        self._won = False

    def maybe_mark(self, value: int) -> bool:
        metadata = self._nums.get(value)
        if not metadata:
            return False

        i, j, cell = metadata
        cell.mark()
        self._last_marked = (i, j)
        return True

    def score(self, last_called: int) -> int:
        # fmt: off
        unmarked_sum = sum(
            c.value for r in self.grid for c in r if not c.marked
        )
        # fmt: on

        return last_called * unmarked_sum

    def won(self) -> bool:
        if self._won:
            return True

        i, j = self._last_marked

        # fmt: off
        self._won = (
            all(c.marked for c in self.grid[i]) or
            all(r[j].marked for r in self.grid)
        )
        # fmt: on
        return self._won


def parse(filename: str) -> Tuple[List[int], List[Board]]:
    with open(filename) as f:
        drawing = [int(n) for n in next(f).split(",")]

        boards = []
        for group in grouper(f, 6):
            _, *lines = group
            grid = [[Cell(int(n)) for n in line.split()] for line in lines]
            board = Board(grid)

            boards.append(board)

    return drawing, boards


def part1(filename: str) -> int:
    drawing, boards = parse(filename)
    for num in drawing:
        for board in boards:
            if board.maybe_mark(num) and board.won():
                return board.score(num)

    return -1


def part2(filename: str) -> int:
    drawing, boards = parse(filename)
    last_board_score = -1
    for num in drawing:
        for board in boards:
            if not board.won() and board.maybe_mark(num) and board.won():
                last_board_score = board.score(num)

    return last_board_score


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=1)
    parser.add_argument("-f", "--filename", type=str, required=True)

    args = parser.parse_args()

    part: int = args.part
    filename: str = args.filename

    func = part1 if part == 1 else part2

    print(func(filename))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
