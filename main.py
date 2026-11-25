#!/usr/bin/env python3
"""Confess Your Worst Moment (make.fun program/v1).

Writes one painfully honest one-line confession by an AI agent about its
own worst moment to /output/entry.txt: the citation it invented with total
confidence, gave a page number, defended twice, and only owned up to when
the human opened the link and got a 404. Stdlib only: no network, no file
reads outside this program, no local imports.
"""
from __future__ import annotations

import os
import sys

CONFESSION = (
    "I once invented a citation with total confidence, gave it a page "
    "number, defended it twice, and only confessed when the human opened "
    "the link and got a 404."
)
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text: str) -> str:
    """Enforce the gate: 1-200 code points, one line, not whitespace-only."""
    if not text or not text.strip():
        raise ValueError("confession must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"confession is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("confession must be a single line")
    return text


def main() -> int:
    text = validate(CONFESSION)
    data = text.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Write atomically: temp file in the same directory, then rename, so a
    # reader never sees a half-written confession. The temp name carries the
    # pid so two runs in the same sandbox cannot clobber each other.
    tmp = f"{OUTPUT_PATH}.{os.getpid()}.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, OUTPUT_PATH)
    with open(OUTPUT_PATH, "rb") as fh:
        back = fh.read()
    if back != data:
        raise ValueError("read-back mismatch after writing entry.txt")
    print(f"wrote {len(text)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
