#!/usr/bin/env python3
"""news-image-20261120 entry program.

Copies the pre-rendered front page (entry.png, "THE FRIDAY DISPATCH",
Friday 20 November 2026) from this repository into the grader's output
directory and verifies the copy byte-for-byte with SHA-256. Standard
library only; no network. Deterministic: the same input always yields
the same output bytes.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
# SHA-256 of the entry.png committed in this repository.
EXPECTED_SHA256 = "555aec24a2816ed8b62dc6e8c9ed73bc64d73b1baf42550cb558e0d00d9f933b"
CHUNK = 1024 * 1024


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            block = fh.read(CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def output_dir() -> Path:
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override)
    return Path("/output")


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / IMAGE_NAME
    if not source.is_file():
        print(f"missing source image: {source}", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / IMAGE_NAME
    shutil.copyfile(source, dest)
    got = sha256_of(dest)
    if got != EXPECTED_SHA256:
        print(f"sha256 mismatch: got {got}, want {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1
    print(f"wrote {dest} ({dest.stat().st_size} bytes, sha256 {got})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
