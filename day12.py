from __future__ import annotations

from collections import Counter
from collections import defaultdict


def parse(filename: str) -> dict[str, set[str]]:
    paths = []
    with open(filename) as f:
        for line in f:
            s, _, e = line.strip().partition("-")
            if s != "end" and e != "start":
                paths.append((s, e))
            if s != "start" and e != "end":
                paths.append((e, s))

    caves = defaultdict(set)
    for s, e in paths:
        caves[s].add(e)

    return caves


def part1(filename: str) -> int:
    caves = parse(filename)

    def count_paths(start: str, seen: set[str]) -> int:
        if start == "end":
            return 1

        n = 0
        for c in caves[start]:
            if c not in seen:
                new_seen = {start, *seen} if start == start.lower() else set(seen)
                n += count_paths(c, new_seen)

        return n

    return count_paths("start", set())


def part2(filename: str) -> int:
    caves = parse(filename)

    # TODO - very slow :)
    def paths(start: str, seen: Counter[str]) -> list[list[str]]:
        if start == "end":
            return [["end"]]

        ps = []
        for c in caves[start]:
            if seen[c] <= 1:
                new_seen = Counter(seen)
                if start == start.lower():
                    new_seen[start] += 1
                for p in paths(c, new_seen):
                    new_p = [start, *p]
                    count = Counter(new_p)
                    if (
                        count["start"] <= 1
                        and count["end"] <= 1
                        and (
                            sum(cv == cv.lower() and v == 2 for cv, v in count.items())
                            <= 1
                        )
                    ):
                        ps.append(new_p)

        return ps

    return len(paths("start", Counter()))


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
