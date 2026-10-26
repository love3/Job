#!/usr/bin/env python3
"""Reject known private paths and local home paths in the Git index.

This is a narrow publication guard, not a personal-data or secret scanner.
It reads staged blobs, so deleting a sensitive working file is not sufficient.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


HOME_PATH = re.compile(rb"/(?:Users|home)/[^\s/<>\"']+|[A-Za-z]:[\\/]Users[\\/][^\s\\/<>\"']+")
CACHE_DIRS = {"__pycache__", "node_modules", ".venv", ".pytest_cache", ".ruff_cache"}


def private_path(name: str) -> bool:
    path = PurePosixPath(name)
    if name == "config/preferences.yaml" or name.startswith("Resume/private/"):
        return True
    for directory in ("JD/preparations/", "Resume/variants/"):
        if name.startswith(directory) and name != directory + "README.md":
            return True
    if len(path.parts) == 2 and path.parts[0] == "Resume" and path.suffix.lower() in {".html", ".htm", ".pdf"}:
        return True
    if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
        return True
    return bool(CACHE_DIRS.intersection(path.parts)) or path.suffix in {".pyc", ".pyo"}


def check_index(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--stage", "-z"],
        check=True, capture_output=True,
    )
    errors = []
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, sha, stage = metadata.split()
        name = raw_path.decode("utf-8", errors="replace")
        if private_path(name):
            errors.append(f"{name}: private or generated path must not be tracked")
            continue
        if mode in {b"160000", b"120000"}:
            errors.append(f"{name}: nested repositories and symlinks require a separate publication design")
            continue
        if stage != b"0":
            errors.append(f"{name}: unresolved index entry")
            continue
        blob = subprocess.run(
            ["git", "-C", str(root), "cat-file", "blob", sha.decode("ascii")],
            check=True, capture_output=True,
        ).stdout
        if HOME_PATH.search(blob):
            errors.append(f"{name}: local home path must not be published")
    return errors


def main() -> int:
    try:
        errors = check_index(Path(__file__).resolve().parents[1])
    except (OSError, subprocess.CalledProcessError):
        print("ERROR: cannot read this repository's Git index", file=sys.stderr)
        return 2
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("PASS: no known private paths or local home paths in the Git index")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
