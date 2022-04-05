from __future__ import annotations

import statistics
from enum import Enum
from typing import Generator
from typing import Iterable


SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
PAIR_SCORES = {"(": 1, "[": 2, "{": 3, "<": 4}
PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}
OPEN = {"(", "[", "{", "<"}


class ScoreType(Enum):
    INCOMPLETE = "incomplete"
    ILLEGAL = "illegal"


def parse(filename: str) -> Generator[str, None, None]:
    with open(filename) as f:
        for line in f:
            yield line.strip()


def part1(filename: str) -> int:
    return sum(s for st, s in line_scores(parse(filename)) if st == ScoreType.ILLEGAL)


def part2(filename: str) -> int:
    return int(
        statistics.median(
            s for st, s in line_scores(parse(filename)) if st == ScoreType.INCOMPLETE
        )
    )


def line_scores(lines: Iterable[str]) -> Generator[tuple[ScoreType, int], None, None]:
    for line in lines:
        yield scores(line)


def scores(line: str) -> tuple[ScoreType, int]:
    s: list[str] = []
    for c in line:
        if not s or (s[-1] in OPEN and c in OPEN):
            s.append(c)
        elif PAIRS.get(s[-1]) == c:
            s.pop()
        else:
            return ScoreType.ILLEGAL, SCORES[c]

    score = 0
    for c in reversed(s):
        score = score * 5 + PAIR_SCORES[c]

    return ScoreType.INCOMPLETE, score


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
