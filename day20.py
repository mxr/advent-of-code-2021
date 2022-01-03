#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict
from typing import DefaultDict
from typing import List
from typing import Tuple


class Image:
    def __init__(self, enh: str, inp: List[List[str]]):
        self.enh = enh

        self.width, self.height, self.border = len(inp[0]), len(inp), 50

        self.grid = self._new_grid()
        self.grid.update(
            {(i, j): c for i, row in enumerate(inp) for j, c in enumerate(row)}
        )

    def _new_grid(self) -> DefaultDict[Tuple[int, int], str]:
        return defaultdict(lambda: ".")

    def apply(self, n: int) -> None:
        for k in range(n):
            ng = self._new_grid()

            # hack since real input flip-flops, doesn't work for the sample though
            self.grid.default_factory = lambda: self.enh[0 if k % 2 else 511]

            for i in range(-self.border, self.height + self.border):
                for j in range(-self.border, self.width + self.border):
                    pos = int(
                        "".join(
                            "1" if self.grid[i + di, j + dj] == "#" else "0"
                            for di in (-1, 0, 1)
                            for dj in (-1, 0, 1)
                        ),
                        2,
                    )
                    ng[i, j] = self.enh[pos]

            self.grid = ng

    def count(self) -> int:
        return sum(v == "#" for v in self.grid.values())


def parse(filename: str) -> Image:
    with open(filename) as f:
        e, i = f.read().split("\n\n")

    return Image(e, [list(s) for s in i.splitlines()])


def part1(filename: str) -> int:
    return execute(filename, 2)


def part2(filename: str) -> int:
    return execute(filename, 50)


def execute(filename: str, n: int) -> int:
    i = parse(filename)
    i.apply(n)

    return i.count()


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
