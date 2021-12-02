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
