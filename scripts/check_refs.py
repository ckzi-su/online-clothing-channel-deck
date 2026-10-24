#!/usr/bin/env python3
"""Validate that every [R{NN}] citation is registered in references/sources.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "references" / "sources.json"
SCAN_DIRS = [ROOT / "docs", ROOT / "slides", ROOT / "references" / "notes"]
PATTERN = re.compile(r"\[R(\d{2})\]")


def main() -> int:
    registry = json.loads(SOURCES.read_text(encoding="utf-8"))
    known = set(registry.get("sources", {}))
    missing: list[tuple[Path, int, str]] = []
    used: dict[str, set[str]] = {}

    for directory in SCAN_DIRS:
        for path in sorted(directory.rglob("*")):
            if path.suffix not in {".md", ".html"}:
                continue
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for ref in PATTERN.findall(line):
                    key = f"R{ref}"
                    used.setdefault(key, set()).add(str(path.relative_to(ROOT)))
                    if key not in known:
                        missing.append((path.relative_to(ROOT), lineno, key))

    if missing:
        print("미등록 인용이 있습니다:")
        for path, lineno, key in missing:
            print(f"  {path}:{lineno} -> {key}")
        print("\nreferences/sources.json에 등록하거나 인용을 제거하세요.")
        return 1

    print(f"등록된 출처: {len(known)}개 / 문서에서 사용된 출처: {len(used)}개")
    for key in sorted(used):
        print(f"  {key}: {', '.join(sorted(used[key]))}")

    unused = sorted(known - set(used))
    if unused:
        print(f"\n아직 사용되지 않은 출처: {', '.join(unused)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
