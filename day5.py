#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import List
from typing import Tuple


def parse(filename: str, part: int) -> Tuple[List[List[Tuple[int, int]]], int, int]:
    max_x, max_y = 0, 0
    paths = []
    with open(filename) as f:
        for line in f:
            start, _, end = line.partition(" -> ")
            x1, y1 = (int(n) for n in start.split(","))
            x2, y2 = (int(n) for n in end.split(","))

            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)

            if x1 == x2:
                paths.append([(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)])
            elif y1 == y2:
                paths.append([(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)])
            elif part == 2:
                xs = list(range(min(x1, x2), max(x1, x2) + 1))
                if x1 > x2:
                    xs.reverse()
                ys = list(range(min(y1, y2), max(y1, y2) + 1))
                if y1 > y2:
                    ys.reverse()

                paths.append(list(zip(xs, ys)))

    return paths, max_x + 1, max_y + 1


def evaluate(filename: str, part: int) -> int:
    paths, max_x, max_y = parse(filename, part)
    grid = [[0] * max_x for _ in range(max_y)]
    for path in paths:
        for x, y in path:
            grid[y][x] += 1

    return sum(cell >= 2 for row in grid for cell in row)


def part1(filename: str) -> int:
    return evaluate(filename, 1)


def part2(filename: str) -> int:
    return evaluate(filename, 2)


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
