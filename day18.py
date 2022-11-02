from __future__ import annotations

import ast
import math
import re
from collections.abc import Generator
from collections.abc import Iterable
from itertools import permutations
from typing import Any
from typing import TypeVar

T = TypeVar("T")

RE = re.compile(r"(\d+),(\d+)\]")
RE_D = re.compile(r"\d+")
RE_T = re.compile(r"\d{2,}")


def parse(filename: str) -> Generator[str, None, None]:
    with open(filename) as f:
        for line in f:
            yield line.strip()


def part1(filename: str) -> int:
    sns = parse(filename)

    t = next(sns)
    for sn in sns:
        t = sreduce(add(t, sn))

    return mag(t)


def part2(filename: str) -> int:
    sns = tuple(parse(filename))

    m = -1
    for sn1, sn2 in permutations(sns, 2):
        m = max(m, mag(sreduce(add(sn1, sn2))), mag(sreduce(add(sn2, sn1))))

    return m


def add(sn1: str, sn2: str) -> str:
    return f"[{sn1},{sn2}]"


def sreduce(sn: str) -> str:
    while True:
        ce, s, e, nl, nr = can_explode(sn)
        if ce:
            b = sn[: s - 1]
            m = last(RE_D.finditer(b))
            if m:
                b = f"{b[: m.start()]}{int(m.group()) + nl}{b[m.end() :]}"

            a = sn[e:]
            m = RE_D.search(a)
            if m:
                a = f"{a[: m.start()]}{int(m.group()) + nr}{a[m.end() :]}"

            sn = f"{b}0{a}"
            continue

        m = RE_T.search(sn)
        if m:
            n = int(m.group())
            sn = f"{sn[: m.start()]}[{n // 2},{math.ceil(n / 2)}]{sn[m.end() :]}"
            continue

        break

    return sn


def can_explode(sn: str) -> tuple[bool, int, int, int, int]:
    b = 0
    for i, c in enumerate(sn):
        if c == "[":
            b += 1
        elif c == "]":
            b -= 1
        elif "0" <= c <= "9" and b >= 5:
            m = RE.match(sn[i:])
            if m:
                return True, i, i + len(m.group()), int(m.group(1)), int(m.group(2))

    return False, -1, -1, -1, -1


def last(ms: Iterable[T]) -> T | None:
    lm = None
    for m in ms:
        lm = m

    return lm


def mag(sn: str) -> int:
    def mag_pair(snl: list[Any]) -> int:
        left, right = snl

        ml = 3 * (left if isinstance(left, int) else mag_pair(left))
        mr = 2 * (right if isinstance(right, int) else mag_pair(right))

        return ml + mr

    return mag_pair(ast.literal_eval(sn))


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
