#!/usr/bin/env python3
"""Copy entry.png to the output directory and verify its SHA-256.

Standard library only, no network. The output directory comes from the
MAKEFUN_OUTPUT_DIR environment variable and defaults to "out". Running
the program twice writes byte-identical output.
"""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if sha256_of(source) != sha256_of(target):
        print("error: entry.png copy failed the SHA-256 check",
              file=sys.stderr)
        return 1
    print("wrote {}".format(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
