from __future__ import annotations

import functools
from collections.abc import Iterable
from typing import NamedTuple


def parse(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def part1(filename: str) -> int:
    return execute(filename).version


def part2(filename: str) -> int:
    return execute(filename).value


class Packet(NamedTuple):
    version: int
    value: int


@functools.lru_cache(maxsize=1)
def execute(filename: str) -> Packet:
    data = parse(filename)
    packet = format(int(data, 16), "b").zfill(len(data * 4))

    p, _ = parse_packet(packet)
    return p


def parse_packet(packet: str) -> tuple[Packet, int]:
    version, type_id = int(packet[:3], 2), int(packet[3 : 3 + 3], 2)

    if type_id == 4:
        n, di = parse_literal(packet[6:])
        return Packet(version, n), di + 6

    ps = []
    lt_id = packet[6]
    offset = 7 + (15 if lt_id == "0" else 11)

    if lt_id == "0":
        i, t = 0, int(packet[7:offset], 2)
        while i < t:
            p, di = parse_packet(packet[i + offset :])

            ps.append(p)
            i += di

    else:
        i, n = 0, int(packet[7:offset], 2)
        for _ in range(n):
            p, di = parse_packet(packet[i + offset :])

            ps.append(p)
            i += di

    version += sum(p.version for p in ps)
    val = value(type_id, (p.value for p in ps))
    i += offset

    return Packet(version, val), i


def parse_literal(packet: str) -> tuple[int, int]:
    ds = []
    i = 0
    while packet[i] != "0":
        ds.append(packet[i + 1 : i + 1 + 4])
        i += 5
    ds.append(packet[i + 1 : i + 1 + 4])
    i += 5

    n = int("".join(ds), 2)

    return n, i


def value(type_id: int, values: Iterable[int]) -> int:
    if type_id == 0:
        return sum(values)
    elif type_id == 1:
        p = 1
        for v in values:
            p *= v
        return p
    elif type_id == 2:
        return min(values)
    elif type_id == 3:
        return max(values)

    v1, v2 = values
    if type_id == 5:
        return v1 > v2
    elif type_id == 6:
        return v1 < v2
    else:
        assert type_id == 7
        return v1 == v2


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
