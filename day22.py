from __future__ import annotations

import re
from collections.abc import Generator
from copy import copy
from typing import NamedTuple


RE = re.compile(r"\w=(-?\d+)\.\.(-?\d+)")


class Range(NamedTuple):
    start: int
    end: int

    def __iter__(self) -> Generator[int, None, None]:
        yield from range(self.start, self.end + 1)

    def bound(self) -> int:
        return max(abs(self.start), abs(self.end))


class Cube(NamedTuple):
    xr: Range
    yr: Range
    zr: Range

    def bound(self) -> int:
        return max(self.xr.bound(), self.yr.bound(), self.zr.bound())

    def overlaps(self, o: Cube) -> bool:
        return (
            self.xr.start <= o.xr.end
            and self.xr.end >= o.xr.start
            and self.yr.start <= o.yr.end
            and self.yr.end >= o.yr.start
            and self.zr.start <= o.zr.end
            and self.zr.end >= o.zr.start
        )

    def envelopes(self, o: Cube) -> bool:
        return (
            self.xr.start <= o.xr.start <= o.xr.end <= self.xr.end
            and self.yr.start <= o.yr.start <= o.yr.end <= self.yr.end
            and self.zr.start <= o.zr.start <= o.zr.end <= self.zr.end
        )

    def without(self, o: Cube) -> Generator[Cube, None, None]:
        """returns the cubes created by removing the other cube"""

        s = copy(self)

        # split along x-axis
        if s.xr.start < o.xr.start:
            pre, post = Range(s.xr.start, o.xr.start - 1), Range(o.xr.start, s.xr.end)
            yield Cube(pre, s.yr, s.zr)
            s = Cube(post, s.yr, s.zr)
        if s.xr.end > o.xr.end:
            post, pre = Range(o.xr.end + 1, s.xr.end), Range(s.xr.start, o.xr.end)
            yield Cube(post, s.yr, s.zr)
            s = Cube(pre, s.yr, s.zr)

        # split along y-axis
        if s.yr.start < o.yr.start:
            pre, post = Range(s.yr.start, o.yr.start - 1), Range(o.yr.start, s.yr.end)
            yield Cube(s.xr, pre, s.zr)
            s = Cube(s.xr, post, s.zr)
        if s.yr.end > o.yr.end:
            post, pre = Range(o.yr.end + 1, s.yr.end), Range(s.yr.start, o.yr.end)
            yield Cube(s.xr, post, s.zr)
            s = Cube(s.xr, pre, s.zr)

        # split along z-axis
        if s.zr.start < o.zr.start:
            pre, post = Range(s.zr.start, o.zr.start - 1), Range(o.zr.start, s.zr.end)
            yield Cube(s.xr, s.yr, pre)
            s = Cube(s.xr, s.yr, post)
        if s.zr.end > o.zr.end:
            post = Range(o.zr.end + 1, s.zr.end)
            yield Cube(s.xr, s.yr, post)

    def volume(self) -> int:
        return (
            (self.xr.end - self.xr.start + 1)
            * (self.yr.end - self.yr.start + 1)
            * (self.zr.end - self.zr.start + 1)
        )


class Command(NamedTuple):
    pos: str
    cube: Cube


class Core:
    def __init__(self, half_width: int) -> None:
        width = 2 * half_width + 1

        self.hw = half_width
        self.cubes = [[[False] * width for _ in range(width)] for _ in range(width)]

    def apply(self, cmd: Command) -> None:
        enable, cube = cmd.pos == "on", cmd.cube

        for z in cube.xr:
            for x in cube.yr:
                for y in cube.zr:
                    self.cubes[z + self.hw][x + self.hw][y + self.hw] = enable

    def count_on(self) -> int:
        return sum(sum(row) for face in self.cubes for row in face)


def parse(filename: str) -> Generator[Command, None, None]:
    with open(filename) as f:
        for line in f:
            pos, _, ranges = line.partition(" ")
            xr, yr, zr = (Range(int(s), int(e)) for s, e in RE.findall(ranges))

            yield Command(pos, Cube(xr, yr, zr))


def part1(filename: str) -> int:
    c = Core(50)
    for cmd in parse(filename):
        if cmd.cube.bound() <= 50:
            c.apply(cmd)

    return c.count_on()


def part2(filename: str) -> int:
    commands = list(reversed(tuple(parse(filename))))
    distinct: set[Cube] = set()
    while commands:
        pos, cube = commands.pop()
        # TODO: sometimes cube is a dupe, not sure if this is a bug
        if pos == "on":
            for d in distinct:
                if cube.overlaps(d):
                    if not d.envelopes(cube):
                        commands.extend(Command(pos, c) for c in cube.without(d))
                    break
            else:
                distinct.add(cube)
        else:
            for d in tuple(distinct):
                if cube.overlaps(d):
                    distinct.remove(d)
                    distinct.update(d.without(cube))

    return sum(d.volume() for d in distinct)


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
