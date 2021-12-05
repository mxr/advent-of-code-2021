#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Generator
from typing import NamedTuple

DIRECTION_FORWARD = "forward"
DIRECTION_DOWN = "down"
DIRECTION_UP = "up"


class Vector(NamedTuple):
    direction: str
    value: int


def parse(filename: str) -> Generator[Vector, None, None]:
    with open(filename) as f:
        for line in f:
            p1, _, p2 = line.partition(" ")
            yield Vector(p1, int(p2))


def part1(filename: str) -> int:
    hor, ver = 0, 0

    for v in parse(filename):
        if v.direction == DIRECTION_FORWARD:
            hor += v.value
        elif v.direction == DIRECTION_DOWN:
            ver += v.value
        else:
            ver -= v.value

    return hor * ver


def part2(filename: str) -> int:
    hor, ver, aim = 0, 0, 0

    for v in parse(filename):
        if v.direction == DIRECTION_FORWARD:
            hor += v.value
            ver += aim * v.value
        elif v.direction == DIRECTION_DOWN:
            aim += v.value
        else:
            aim -= v.value

    return hor * ver


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
