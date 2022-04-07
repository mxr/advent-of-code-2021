from __future__ import annotations

import sys
from argparse import ArgumentParser
from typing import Callable


def main(part1: Callable[[str], int], part2: Callable[[str], int]) -> int:
    parser = ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=0)
    parser.add_argument(
        "-f", "--filename", type=str, default=sys.argv[0].replace(".py", ".txt")
    )

    args = parser.parse_args()

    part: int = args.part
    filename: str = args.filename

    if (part or 1) == 1:
        print("part1: ", end="")
        print(part1(filename))
    if (part or 2) == 2:
        print("part2: ", end="")
        print(part2(filename))

    return 0
