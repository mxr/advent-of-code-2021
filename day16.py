#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Iterable
from typing import NamedTuple
from typing import Tuple


def parse(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def part1(filename: str) -> int:
    data = parse(filename)
    packet = format(int(data, 16), "b").zfill(len(data * 4))

    p, _ = parse_packet(packet)

    return p.version


def part2(filename: str) -> int:
    data = parse(filename)
    packet = format(int(data, 16), "b").zfill(len(data * 4))

    p, _ = parse_packet(packet)

    return p.value


class Packet(NamedTuple):
    version: int
    value: int


def parse_packet(packet: str) -> Tuple[Packet, int]:
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


def parse_literal(packet: str) -> Tuple[int, int]:
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
