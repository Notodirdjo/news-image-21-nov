#!/usr/bin/env python3
"""Hand the finished front page to the make.fun grader.

draw.py renders entry.png in advance; this script only copies that
file into the directory the grader provides through
MAKEFUN_OUTPUT_DIR. Nothing is fetched, generated or deleted here,
so the run is offline and repeats byte for byte.

The output folder is created when it is absent. It is never removed:
the grader mounts it, and deleting it would break the run. After the
copy, the file is read back and compared byte for byte with the
source, so a bad copy fails loudly instead of passing silently.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ARTWORK = os.path.join(HERE, "entry.png")


def deliver():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)

    if not os.path.isfile(ARTWORK):
        raise SystemExit("entry.png is missing; run draw.py first")

    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(ARTWORK, target)
    if os.path.getsize(target) != os.path.getsize(ARTWORK):
        raise SystemExit("copied entry.png has the wrong size")

    with open(ARTWORK, "rb") as source_handle:
        source_bytes = source_handle.read()
    with open(target, "rb") as target_handle:
        target_bytes = target_handle.read()
    if source_bytes != target_bytes:
        raise SystemExit("copied entry.png differs from the source")
    print("wrote %s (%d bytes)" % (target, len(target_bytes)))
    print("sha256 " + hashlib.sha256(target_bytes).hexdigest())
    return target


if __name__ == "__main__":
    deliver()
