#!/usr/bin/env python3
"""Render the 2026-08 omnichannel-share bar chart in two deck themes."""

from __future__ import annotations

import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "processed" / "category_latest.csv"
OUT = ROOT / "slides" / "assets" / "charts"

THEMES = {
    "figma": {
        "background": "#ffffff",
        "text": "#000000",
        "bar": "#1f1d3d",
        "highlight": "#ff3d8b",
        "grid": "#e6e6e6",
    },
    "ppt": {
        "background": "#f4f1ea",
        "text": "#14110d",
        "bar": "#14110d",
        "highlight": "#b23a1f",
        "grid": "#c9c2b4",
    },
}

LABELS = {
    "가방": "가방",
    "패션용품 및 액세서리": "패션용품",
    "의복": "의복",
    "신발": "신발",
    "전체": "전체 평균",
}


def load_rows() -> tuple[list[tuple[str, float]], float]:
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8-sig")))
    picked: list[tuple[str, float]] = []
    total = 0.0
    for row in rows:
        if row["category"] == "합계":
            total = float(row["omni_share_pct"])
        elif row["category"] in LABELS and row["category"] != "전체":
            picked.append((LABELS[row["category"]], float(row["omni_share_pct"])))
    picked.sort(key=lambda item: item[1])
    return picked, total


def render(theme: str, rows: list[tuple[str, float]], total: float) -> None:
    palette = THEMES[theme]
    sns.set_theme(style="white")
    plt.rcParams.update(
        {
            "font.family": "Apple SD Gothic Neo",
            "axes.unicode_minus": False,
            "svg.fonttype": "path",
            "text.color": palette["text"],
            "axes.labelcolor": palette["text"],
            "xtick.color": palette["text"],
            "ytick.color": palette["text"],
        }
    )

    fig, ax = plt.subplots(figsize=(10.2, 4.4), dpi=160)
    fig.patch.set_facecolor(palette["background"])
    ax.set_facecolor(palette["background"])

    names = ["전체 평균"] + [name for name, _ in rows]
    values = [total] + [value for _, value in rows]
    color_lookup = {
        "전체 평균": palette["grid"],
        "가방": palette["bar"],
        "패션용품": palette["bar"],
        "신발": palette["bar"],
        "의복": palette["highlight"],
    }
    order = ["전체 평균", "가방", "패션용품", "신발", "의복"]
    lookup = dict(zip(names, values))
    names = order
    values = [lookup[name] for name in names]
    colors = [color_lookup[name] for name in names]

    sns.barplot(
        x=values,
        y=names,
        hue=names,
        palette=colors,
        dodge=False,
        legend=False,
        ax=ax,
        edgecolor=palette["background"],
        linewidth=1.5,
    )

    for patch, value in zip(ax.patches, values):
        label_value = Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        ax.text(
            value + 1.2,
            patch.get_y() + patch.get_height() / 2,
            f"{label_value}%",
            va="center",
            ha="left",
            fontsize=15,
            fontweight="bold",
            color=palette["text"],
        )

    ax.axvline(total, color=palette["text"], linestyle=(0, (4, 4)), linewidth=1.1, alpha=0.55)
    ax.set_xlim(0, 64)
    ax.set_xlabel("병행몰 비중 (%)", fontsize=14, labelpad=10)
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=16, length=0, pad=10)
    ax.tick_params(axis="x", labelsize=12, colors=palette["text"])
    for label in ax.get_yticklabels():
        if label.get_text() == "의복":
            label.set_fontweight("bold")
            label.set_color(palette["highlight"])

    ax.grid(axis="x", color=palette["grid"], linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(palette["grid"])

    fig.tight_layout(pad=0.6)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"category_omni_{theme}.svg", facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    rows, total = load_rows()
    for theme in THEMES:
        render(theme, rows, total)
        print(f"wrote {OUT / f'category_omni_{theme}.svg'}")


if __name__ == "__main__":
    main()
