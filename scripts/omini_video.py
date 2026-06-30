#!/usr/bin/env python3
"""Backward-compatible wrapper for omini / Gemini Omni video jobs."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import kie_media  # noqa: E402


def main() -> int:
    if "--provider" not in sys.argv:
        sys.argv[1:1] = ["--provider", "omini"]
    return kie_media.main()


if __name__ == "__main__":
    raise SystemExit(main())
