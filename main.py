#!/usr/bin/env python3
"""Entry point for the 24 November 2026 news image.

The front page is drawn at build time by render.py and kept in this
repository as entry.png. When the harness runs this script, the only
thing it does is copy that finished image into the output directory
the harness provides, byte for byte. There is no drawing code here,
no font handling, no network and no randomness, so repeated runs
always write the same bytes.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"


def output_path() -> Path:
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = Path(directory) / "entry.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    target = output_path()
    shutil.copyfile(IMAGE, target)
    print(f"copied {IMAGE.name} -> {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
