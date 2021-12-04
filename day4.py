#!/usr/bin/env python3
from argparse import ArgumentParser
from dataclasses import dataclass
from itertools import zip_longest
from typing import Dict
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import TypeVar

T = TypeVar("T")


def grouper(iterable: Iterable[T], n: int) -> Iterable[Tuple[T, ...]]:
    args = [iter(iterable)] * n
    return zip_longest(*args)


@dataclass
class Cell:
    value: int
    marked: bool = False

    def mark(self) -> None:
        self.marked = True


class CellWithLoc(NamedTuple):
    row: int
    col: int
    cell: Cell


class Board:
    def __init__(self, grid: List[List[Cell]]) -> None:
        self._cell_index: Dict[int, CellWithLoc] = {}
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                self._cell_index[cell.value] = CellWithLoc(i, j, cell)

        self.grid = grid
        self._last_marked = (-1, -1)
        self._won = False

    def maybe_mark(self, value: int) -> bool:
        if self._won:
            return False

        cwl = self._cell_index.get(value)
        if not cwl:
            return False

        cwl.cell.mark()
        self._last_marked = (cwl.row, cwl.col)
        return True

    def score(self, last_called: int) -> int:
        # fmt: off
        unmarked_sum = sum(
            c.value for r in self.grid for c in r if not c.marked
        )
        # fmt: on

        return last_called * unmarked_sum

    def won(self) -> bool:
        if not self._won:
            row, col = self._last_marked

            # fmt: off
            self._won = (
                all(c.marked for c in self.grid[row]) or
                all(r[col].marked for r in self.grid)
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

            boards.append(Board(grid))

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

    boards_left = len(boards)
    for num in drawing:
        for board in boards:
            if board.maybe_mark(num) and board.won():
                boards_left -= 1
                if not boards_left:
                    return board.score(num)

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
