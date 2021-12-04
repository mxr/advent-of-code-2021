#!/usr/bin/env python3
from argparse import ArgumentParser


def part1(filename: str) -> int:
    num_inc = 0

    with open(filename) as f:
        prev = int(next(f))

        for line in f:
            curr = int(line)
            if curr > prev:
                num_inc += 1
            prev = curr

    return num_inc


def part2(filename: str) -> int:
    num_inc = 0

    with open(filename) as f:
        ppprev, pprev, prev = int(next(f)), int(next(f)), int(next(f))
        psum = ppprev + pprev + prev

        for line in f:
            curr = int(line)
            csum = psum - ppprev + curr
            if csum > psum:
                num_inc += 1
            ppprev, pprev, prev = pprev, prev, curr

    return num_inc


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
