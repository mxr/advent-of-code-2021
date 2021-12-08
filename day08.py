#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict
from itertools import chain
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Set


class Mapping(NamedTuple):
    ins: List[Set[str]]
    outs: List[Set[str]]


def parse(filename: str) -> Generator[Mapping, None, None]:
    with open(filename) as f:
        for line in f:
            ins, _, outs = line.partition(" | ")
            yield Mapping([set(i) for i in ins.split()], [set(j) for j in outs.split()])


LENS = {
    2,  # one
    4,  # four,
    3,  # seven
    7,  # eight
}


def part1(filename: str) -> int:
    return sum(len(out) in LENS for m in parse(filename) for out in m.outs)


def part2(filename: str) -> int:
    return sum(decode(m) for m in parse(filename))


def decode(m: Mapping) -> int:
    by_len = group_by_len(chain(m.ins, m.outs))

    one = by_len[2][0]
    four = by_len[4][0]
    seven = by_len[3][0]
    eight = by_len[7][0]

    nine = next(s for s in by_len[6] if s >= (four | seven))
    six = next(s for s in by_len[6] if (s | seven) == eight)
    zero = next(s for s in by_len[6] if s != nine and s != six)

    five = next(s for s in by_len[5] if (s | one) == nine)
    three = next(s for s in by_len[5] if (s | one) == s)
    two = next(s for s in by_len[5] if s != five and s != three)

    segments = {
        tuple(sorted(zero)): "0",
        tuple(sorted(one)): "1",
        tuple(sorted(two)): "2",
        tuple(sorted(three)): "3",
        tuple(sorted(four)): "4",
        tuple(sorted(five)): "5",
        tuple(sorted(six)): "6",
        tuple(sorted(seven)): "7",
        tuple(sorted(eight)): "8",
        tuple(sorted(nine)): "9",
    }

    return int("".join(segments[tuple(sorted(o))] for o in m.outs))


def group_by_len(sets: Iterable[Set[str]]) -> Dict[int, List[Set[str]]]:
    deduped = defaultdict(set)
    for s in sets:
        deduped[len(s)].add(tuple(sorted(s)))

    retyped = {}
    for k, vs in deduped.items():
        retyped[k] = [set(v) for v in vs]

    return retyped


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
