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
