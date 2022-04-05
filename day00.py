from __future__ import annotations


def parse(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def part1(filename: str) -> int:
    return -1


def part2(filename: str) -> int:
    return -1


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
