#!/usr/bin/env python3
"""KOSIS xlsx -> tidy CSV for the clothing-channel deck.

Only uses the Python standard library (no openpyxl required).

Usage:
    python3 scripts/xlsx_to_csv.py
    python3 scripts/xlsx_to_csv.py --input data/raw/foo.xlsx

Outputs:
    data/processed/clothing_monthly.csv      (long format: month/channel/value)
    data/processed/clothing_wide.csv         (one row per month + shares)
    data/processed/category_latest.csv       (all categories, latest month)
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "data" / "raw" / "온라인쇼핑몰_운영형태별_상품군별거래액_20261025005845.xlsx"
OUT_DIR = ROOT / "data" / "processed"

ONLINE = "온라인 전용몰"
OMNI = "온·오프라인 병행몰"


def col_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch) - 64)
    return idx - 1


def read_sheet(path: Path, sheet: str = "sheet1") -> list[dict[int, str]]:
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root:
                shared.append("".join(t.text or "" for t in si.iter(NS + "t")))

        root = ET.fromstring(zf.read(f"xl/worksheets/{sheet}.xml"))
        rows: list[dict[int, str]] = []
        for row in root.iter(NS + "row"):
            cells: dict[int, str] = {}
            for c in row.iter(NS + "c"):
                value = c.find(NS + "v")
                if value is None:
                    inline = c.find(NS + "is")
                    text = "".join(t.text or "" for t in inline.iter(NS + "t")) if inline is not None else ""
                else:
                    text = shared[int(value.text)] if c.get("t") == "s" else value.text
                cells[col_index(c.get("r"))] = (text or "").strip()
            if cells:
                rows.append(cells)
        return rows


def normalize_month(label: str) -> tuple[str, bool]:
    provisional = "p)" in label
    match = re.search(r"(\d{4})\.(\d{2})", label)
    if not match:
        raise ValueError(f"unrecognized month label: {label!r}")
    return f"{match.group(1)}-{match.group(2)}", provisional


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()

    if not args.input.exists():
        print(f"input not found: {args.input}", file=sys.stderr)
        return 1

    rows = read_sheet(args.input)
    header = rows[0]
    months = {idx: normalize_month(text) for idx, text in header.items() if idx >= 3}

    records: list[dict[str, object]] = []
    current_group = ""
    current_sub = ""
    for row in rows[1:]:
        group = row.get(0) or current_group
        sub = row.get(1) or current_sub
        channel = row.get(2, "")
        current_group, current_sub = group, sub
        if group != "의복" or channel not in ("계", ONLINE, OMNI):
            continue
        for idx, (month, provisional) in months.items():
            raw = row.get(idx, "")
            if raw == "":
                continue
            records.append(
                {
                    "month": month,
                    "provisional": provisional,
                    "category": "의복",
                    "channel": channel,
                    "value_million_krw": int(float(raw)),
                }
            )

    if not records:
        print("no 의복 rows found", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with (OUT_DIR / "clothing_monthly.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["month", "provisional", "category", "channel", "value_million_krw"])
        writer.writeheader()
        writer.writerows(records)

    wide: dict[str, dict[str, object]] = {}
    for record in records:
        month = str(record["month"])
        bucket = wide.setdefault(
            month,
            {"month": month, "provisional": record["provisional"], "total": 0, ONLINE: 0, OMNI: 0},
        )
        channel = str(record["channel"])
        bucket["total" if channel == "계" else channel] = record["value_million_krw"]

    with (OUT_DIR / "clothing_wide.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = ["month", "provisional", "online_only", "omnichannel", "total", "online_share_pct", "omni_share_pct"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for month in sorted(wide):
            row = wide[month]
            total = int(row["total"])
            online = int(row[ONLINE])
            omni = int(row[OMNI])
            writer.writerow(
                {
                    "month": month,
                    "provisional": row["provisional"],
                    "online_only": online,
                    "omnichannel": omni,
                    "total": total,
                    "online_share_pct": round(online / total * 100, 2) if total else "",
                    "omni_share_pct": round(omni / total * 100, 2) if total else "",
                }
            )

    latest = sorted(months.values())[-1][0]
    latest_idx = next(idx for idx, (month, _) in months.items() if month == latest)
    category_rows: list[dict[str, object]] = []
    current_group = ""
    current_sub = ""
    for row in rows[1:]:
        group = row.get(0) or current_group
        sub = row.get(1) or current_sub
        channel = row.get(2, "")
        current_group, current_sub = group, sub
        if sub != "소계" or channel not in ("계", ONLINE, OMNI):
            continue
        raw = row.get(latest_idx, "")
        if raw == "":
            continue
        category_rows.append(
            {
                "category": group,
                "subcategory": sub,
                "channel": channel,
                "value_million_krw": int(float(raw)),
            }
        )

    by_category: dict[tuple[str, str], dict[str, int]] = {}
    for record in category_rows:
        key = (str(record["category"]), str(record["subcategory"]))
        by_category.setdefault(key, {})[str(record["channel"])] = int(record["value_million_krw"])

    with (OUT_DIR / "category_latest.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = ["category", "subcategory", "online_only", "omnichannel", "total", "omni_share_pct"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for (category, subcategory), values in by_category.items():
            total = values.get("계", 0)
            omni = values.get(OMNI, 0)
            writer.writerow(
                {
                    "category": category,
                    "subcategory": subcategory,
                    "online_only": values.get(ONLINE, 0),
                    "omnichannel": omni,
                    "total": total,
                    "omni_share_pct": round(omni / total * 100, 2) if total else "",
                }
            )

    print(f"wrote {len(records)} monthly rows, {len(wide)} months, {len(by_category)} categories")
    print(f"latest month: {latest} (provisional={sorted(months.values())[-1][1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
