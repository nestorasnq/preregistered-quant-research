#!/usr/bin/env python3
"""blockcheck.py -- did my inserted block land where I meant it to?

IN PLAIN WORDS
--------------
This tool exists because of one specific bug, and the bug is worth understanding before the code.

A fourteen-line block was inserted into a large file at a line number copied from a
differently-numbered version of that file. It landed a few lines off -- inside the body of a type
declaration, between two of its fields.

The declaration ended early. Its last two fields stopped being fields and became loose statements.

Nothing about that looks wrong when you read it. The file is still valid text, the block is still
there, the indentation looks plausible. It happened to produce a compiler error that time, which was
luck: a block landing at the wrong depth can just as easily produce a declaration that is quietly
missing fields, or a function whose body silently ends early. In an engine that carries state
forward from the first bar, that changes results rather than failing.

So the fix was not "be more careful next time". The fix was a tool that makes the failure detectable.

THE INVARIANT
-------------
A block inserted at top level must not be followed by a line that is MORE indented than the block
itself. If the next line is deeper, the block has landed inside a body and split it in half.

Second check: a top-level line must never appear inside a type body. Adding a field to an existing
type legitimately produces a "mixed" body -- some lines from the parent, some inserted -- and that
is fine. What is not fine is a line at column 0 inside the body, because that terminates the
declaration and orphans everything after it.

USAGE
-----
    python blockcheck.py source.pine manifest.txt

The manifest is whitespace-separated inclusive line ranges of the inserted blocks, e.g.

    120-134  501-503  892-910

Exits 0 if clean, 1 if any block failed.
"""

from __future__ import annotations

import re
import sys

TYPE_DECL = re.compile(r"^type\s+\w+")


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def parse_manifest(path: str) -> list[tuple[int, int]]:
    text = open(path, encoding="utf-8").read().split()
    return [tuple(int(n) for n in token.split("-")) for token in text]


def check(source_path: str, manifest_path: str) -> list[tuple[str, str, str]]:
    lines = open(source_path, encoding="utf-8").readlines()
    blocks = parse_manifest(manifest_path)
    inserted = {i for start, end in blocks for i in range(start, end + 1)}
    problems: list[tuple[str, str, str]] = []

    # 1. A top-level block must not be followed by a more-indented line.
    for start, end in blocks:
        body = [lines[i - 1] for i in range(start, end + 1) if lines[i - 1].strip()]
        if not body:
            continue
        level = indent_of(body[0])
        following = lines[end] if end < len(lines) else ""
        if following.strip() and indent_of(following) > level:
            problems.append((
                "SPLIT-BODY",
                f"L{start}-{end}",
                f"block at column {level}, next line at column {indent_of(following)}: "
                f"{following.strip()[:60]}",
            ))

    # 2. No inserted top-level line may sit inside a type body.
    decl_start = None
    for i, line in enumerate(lines, 1):
        if TYPE_DECL.match(line):
            decl_start = i
        elif decl_start and line.strip() and not line.startswith((" ", "\t")):
            for j in range(decl_start + 1, i):
                body_line = lines[j - 1]
                if j in inserted and body_line.strip() and not body_line.startswith((" ", "\t")):
                    problems.append((
                        "TOP-LEVEL-IN-TYPE",
                        f"L{j}",
                        f"{lines[decl_start - 1].rstrip()} <- {body_line.rstrip()[:50]}",
                    ))
                    break
            decl_start = None

    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2

    source, manifest = argv[1], argv[2]
    problems = check(source, manifest)

    label = source.split("/")[-1]
    print(f"  {label:<34} {'CLEAN' if not problems else f'*** {len(problems)} PROBLEM(S)'}")
    for kind, where, detail in problems[:8]:
        print(f"     !! {kind:<20} {where:<12} {detail}")

    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
