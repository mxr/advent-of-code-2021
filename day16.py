#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import List
from typing import NamedTuple
from typing import Tuple


def parse(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def part1(filename: str) -> int:
    data = parse(filename)
    packet = format(int(data, 16), "b").zfill(len(data * 4))

    out = parse_packet(packet)

    return out.version


def part2(filename: str) -> int:
    data = parse(filename)
    packet = format(int(data, 16), "b").zfill(len(data * 4))

    out = parse_packet(packet)

    return out.value


class Out(NamedTuple):
    version: int
    value: int
    i: int


def parse_packet(packet: str) -> Out:
    version, type_id = int(packet[:3], 2), int(packet[3 : 3 + 3], 2)

    if type_id == 4:
        n, di = parse_literal(packet[6:])
        return Out(version, n, di + 6)
    else:
        lt_id = packet[6]
        if lt_id == "0":
            i, t = 0, int(packet[7 : 7 + 15], 2)
            outs = []
            while i < t:
                out = parse_packet(packet[i + 7 + 15 :])
                outs.append(out)

                version += out.version
                i += out.i

            return Out(version, value(type_id, [o.value for o in outs]), i + 6 + 1 + 15)

        else:
            i, c, n = 0, 0, int(packet[7 : 7 + 11], 2)
            outs = []
            while c < n:
                out = parse_packet(packet[i + 7 + 11 :])
                outs.append(out)

                version += out.version
                i += out.i
                c += 1

            return Out(version, value(type_id, [o.value for o in outs]), i + 6 + 1 + 11)


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


def value(type_id: int, values: List[int]) -> int:
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
    elif type_id == 5:
        return int(values[0] > values[1])
    elif type_id == 6:
        return int(values[0] < values[1])
    else:
        assert type_id == 7
        return int(values[0] == values[1])


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
