#!/usr/bin/env python3
"""fn_md5.py -- tell me exactly which functions changed between two builds.

IN PLAIN WORDS
--------------
You edited one thing in a 4,800-line file. Did you also change something else by accident?

A normal text diff answers "which lines are different", which is not the same question. Lines move
when you insert something above them. Reformatting shows up as a change. A diff of a big file is
noisy enough that you stop reading it, and that is when a real change slips through.

This gives each function its own fingerprint and compares the fingerprints. A function either has
the same fingerprint as before -- in which case it behaves identically, guaranteed -- or it does
not, in which case it is named and you have to justify it before shipping.

The output is a sentence like "91 functions, 90 unchanged, 1 changed: <name>". That is a claim a
reviewer can check in ten seconds instead of reading 4,800 lines.

Everything before the first function -- globals, inputs, type declarations -- is hashed together as
__preamble__, so an edit at declaration level cannot hide by not being inside a function.

USAGE
-----
    python fn_md5.py parent.pine child.pine

Exits 0 if nothing changed, 1 if anything did, so it can gate a build script.
"""

from __future__ import annotations

import hashlib
import re
import sys

# A function declaration: `name(args) =>` starting at column 0.
DECL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(.*\)\s*=>\s*$")


def digest_functions(path: str) -> dict[str, tuple[str, int]]:
    """Split a file into functions and return {name: (md5, line_count)}."""
    blocks: dict[str, list[str]] = {}
    current, buffer = "__preamble__", []

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            match = DECL.match(line.rstrip("\n"))
            if match:
                blocks[current] = buffer
                current, buffer = match.group(1), [line]
            else:
                buffer.append(line)
    blocks[current] = buffer

    return {
        name: (hashlib.md5("".join(body).encode()).hexdigest(), len(body))
        for name, body in blocks.items()
    }


def compare(parent: str, child: str) -> list[tuple[str, str, str, str]]:
    a, b = digest_functions(parent), digest_functions(child)
    changes = []
    for name in sorted(set(a) | set(b)):
        x, y = a.get(name), b.get(name)
        if x is None:
            changes.append((name, "ADDED", "", y[0]))
        elif y is None:
            changes.append((name, "REMOVED", x[0], ""))
        elif x[0] != y[0]:
            changes.append((name, f"{x[1]} -> {y[1]} lines", x[0], y[0]))
    return changes


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2

    parent, child = argv[1], argv[2]
    a, b = digest_functions(parent), digest_functions(child)
    changes = compare(parent, child)
    total = len(set(a) | set(b))

    print(f"functions: {len(a)} -> {len(b)}")
    print(f"unchanged: {total - len(changes)}")
    print(f"changed:   {len(changes)}")
    for name, kind, before, after in changes:
        print(f"\n  {name}  [{kind}]")
        print(f"    parent  {before}")
        print(f"    child   {after}")

    return 1 if changes else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
