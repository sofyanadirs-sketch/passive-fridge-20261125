#!/usr/bin/env python3
"""Passive-aggressive fridge note — make.fun bounty entry.

Reads the single-line note from entry.txt (the entry's single source of
truth), validates it, and writes it to the output directory as entry.txt.

The note: a smart fridge's dry, petty message to its owner about the
water filter's replacement light, ignored for 41 days. The fridge's
second twist is that it stopped making ice in solidarity with the
filter — the appliance unionises against the owner.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_FILE = os.path.join(HERE, "entry.txt")
MAX_CHARS = 280


def load_note():
    """Read and validate the one-line note from entry.txt."""
    with open(ENTRY_FILE, encoding="utf-8") as handle:
        note = handle.read().strip()
    if not note:
        raise ValueError("note must not be empty")
    if "\n" in note or "\r" in note:
        raise ValueError("note must be a single line")
    if len(note) > MAX_CHARS:
        raise ValueError("note is %d chars, over the %d limit" % (len(note), MAX_CHARS))
    return note


def main():
    note = load_note()
    # An explicitly empty MAKEFUN_OUTPUT_DIR is treated as unset: without
    # this, os.makedirs("") raises FileNotFoundError and the run dies.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        # Terminate with a newline so the output file is byte-identical to
        # entry.txt (which ends with one); previously the file was one byte
        # short and `cmp` against entry.txt failed.
        handle.write(note + "\n")
    # Outputs are collected as another user: leave the file world-readable.
    os.chmod(path, 0o644)
    print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
