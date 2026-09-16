#!/usr/bin/env python3
"""pineflight.py -- catch the five mistakes that have actually cost me a round trip.

IN PLAIN WORDS
--------------
The chart platform is the only place this code can be compiled. There is no compiler on my machine.
So every mistake costs a full round trip: paste the file in, wait, read the error, come back, fix,
paste again.

This is not a compiler and it does not try to be. It looks for exactly five things, and every one of
them is on the list because it happened, wasted a cycle, and was worth never repeating.

It cannot prove the file compiles. It can prove these five are absent, which is the useful half.

WHAT IT CHECKS
--------------
1. Writing to a script-level variable from inside a function.
   The language forbids it. It is an easy mistake because the variable is visible from in there,
   it just cannot be assigned to.

2. Declaring a variable as one type and assigning it a field of a different type.
   `bool flag = someObject.someField` where that field is actually an int. Reads perfectly, fails
   on paste. The tool reads the type declarations, learns what each field really is, and checks.

3. Comma-separated declarations or assignments on one line.
   Legal in most languages, not here.

4. Continuation lines indented differently from the statement they continue.
   A run of related assignments has to share one indentation level. Break that and the parser
   reads the tail as a new statement.

5. Numbers in log output without explicit formatting.
   This one is not a compiler error and it is the nastiest of the five, because the file compiles
   and runs. The platform helpfully inserts thousand separators into numbers -- so a logged price
   of 1457.75 comes out as "1,457.75", the comma lands in the middle of a comma-separated log line,
   and every downstream parser silently reads the wrong fields. You do not find out until the data
   is wrong.

USAGE
-----
    python pineflight.py source.pine                     # whole file
    python pineflight.py source.pine ranges.txt          # only inserted line ranges
    python pineflight.py source.pine --strings a,b,c     # names that are string log args

Exits 1 if any hard error is found. Formatting warnings alone exit 0.
"""

from __future__ import annotations

import re
import sys

DECL_FN = re.compile(r"^[A-Za-z_]\w*\s*\(.*\)\s*=>\s*$")
DECL_TYPE = re.compile(r"^type\s+(\w+)")
FIELD = re.compile(r"^\s+(int|float|bool|string|line|label|box|table|array<[^>]+>)\s+(\w+)")
SCOPE_VAR = re.compile(r"^var\s+(int|float|bool|string)\s+(\w+)\s*=")
TYPED_VAR = re.compile(r"^var\s+(\w+)\s+(\w+)\s*=")
ASSIGN = re.compile(r"^(\w+)\s*:=")
TYPED_FROM_FIELD = re.compile(r"^(int|float|bool|string)\s+(\w+)\s*=\s*(\w+)\.(\w+)\s*(//.*)?$")
COMMA_ASSIGN = re.compile(r":=[^,]*,\s*\w+\s*:=")
COMMA_DECL = re.compile(r"^(int|float|bool|string)\s+\w+\s*=[^,]*,\s*\w+\s*=")
PLACEHOLDER = re.compile(r"(\w+)=\{(\d+)\}")
CONTINUATION = re.compile(r"^([A-Za-z_]\w*?)([A-Z])\s*:=")


def field_types(src: list[str]) -> dict[tuple[str, str], str]:
    """Map (type_name, field_name) -> declared type, by reading the type declarations."""
    types: dict[tuple[str, str], str] = {}
    current = None
    for line in src:
        m = DECL_TYPE.match(line)
        if m:
            current = m.group(1)
            continue
        if current and line.strip() and not line[0].isspace():
            current = None
        if current:
            m = FIELD.match(line)
            if m:
                types[(current, m.group(2))] = m.group(1).split("<")[0]
    return types


def var_types(src: list[str]) -> dict[str, str]:
    """Map variable name -> declared type, for script-level variables."""
    out: dict[str, str] = {}
    for line in src:
        for pattern in (TYPED_VAR, SCOPE_VAR):
            m = pattern.match(line)
            if m:
                out[m.group(2)] = m.group(1)
    return out


def check(path: str, ranges=None, string_args: set[str] | None = None):
    src = open(path, encoding="utf-8").readlines()
    ftypes, vtypes = field_types(src), var_types(src)
    string_args = string_args or set()

    scope_names = {
        m.group(2) for m in (SCOPE_VAR.match(line) for line in src) if m
    }
    in_range = lambda i: ranges is None or any(a <= i <= b for a, b in ranges)

    problems: list[tuple[int, str, str]] = []
    inside_function = False

    for i, raw in enumerate(src, 1):
        line = raw.rstrip("\n")
        stripped = line.strip()

        if DECL_FN.match(stripped):
            inside_function = True
            continue
        if stripped and not line[0].isspace() and not stripped.startswith("//"):
            inside_function = False
        if not in_range(i) or not stripped or stripped.startswith("//"):
            continue

        # 1. script-scope write from inside a function
        if inside_function:
            m = ASSIGN.match(stripped)
            if m and m.group(1) in scope_names:
                problems.append((i, "SCOPE",
                                 f'writes script-scope variable "{m.group(1)}" inside a function'))

        # 2. declared type vs the field actually being read
        m = TYPED_FROM_FIELD.match(stripped)
        if m:
            declared, _, obj, field = m.group(1), m.group(2), m.group(3), m.group(4)
            actual = ftypes.get((vtypes.get(obj), field))
            if actual and actual != declared:
                problems.append((i, "TYPE",
                                 f"declared {declared} but {obj}.{field} is {actual}"))

        # 3. comma-separated declaration or assignment
        code = stripped.split("//")[0]
        if COMMA_ASSIGN.search(code) or COMMA_DECL.match(code):
            problems.append((i, "COMMA", "comma-separated declaration or assignment"))

        # 5. numeric log placeholders without explicit formatting
        if ("log.info(" in stripped or "str.format(" in stripped) and re.search(r"=\{\d+\}", stripped):
            for name, idx in PLACEHOLDER.findall(stripped):
                if name in string_args:
                    continue
                problems.append((i, "FORMAT",
                                 f"{name}={{{idx}}} has no ',number,#' -> thousand separators "
                                 f"will be inserted and will break the log's field layout"))

    # 4. continuation-line indentation within a run of related assignments
    group_indent = None
    previous_stem = None
    for i, raw in enumerate(src, 1):
        if not in_range(i):
            continue
        stripped, col = raw.strip(), len(raw) - len(raw.lstrip())
        m = CONTINUATION.match(stripped)
        if not m:
            previous_stem = None
            continue
        stem = m.group(1)
        if stem != previous_stem:
            group_indent, previous_stem = col, stem
        elif group_indent is not None and col != group_indent:
            problems.append((i, "INDENT",
                             f"continuation indented {col}, its group starts at {group_indent}"))

    return problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2

    path = argv[1]
    ranges, strings = None, set()

    rest = argv[2:]
    while rest:
        token = rest.pop(0)
        if token == "--strings":
            strings = set(rest.pop(0).split(","))
        else:
            ranges = [tuple(int(n) for n in x.split("-")) for x in open(token) if x.strip()]

    problems = check(path, ranges, strings)

    print(f"pineflight {path}" + ("  (inserted ranges only)" if ranges else "  (whole file)"))
    if not problems:
        print("  clean on all five checks")
    for i, kind, message in problems:
        print(f"  L{i:<6}{kind:<9}{message}")

    return 1 if any(kind != "FORMAT" for _, kind, _ in problems) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
