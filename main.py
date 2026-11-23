#!/usr/bin/env python3
"""news-image-20261123 entry (Python 3.13, standard library only).

The image is drawn at build time by gen_image.py and shipped as entry.png
beside this file. This program only copies it to the output directory:
deterministic, no network, no dependencies.
"""
import os
import shutil
import sys

OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))
print("wrote entry.png", file=sys.stderr)
