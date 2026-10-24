#!/usr/bin/env python3
"""Bundle a slide deck into one self-contained HTML file.

Inlines CSS, JS, anime.js, theme-specific SVG charts, and Manim MP4/PNG assets
as data URIs so the result can be submitted/uploaded as a single file.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def data_uri(path: Path, mime: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def inline_script(content: str) -> str:
    return content.replace("</script>", "<\\/script>")


def bundle(input_path: Path, output_path: Path) -> None:
    source_dir = input_path.parent
    html = input_path.read_text(encoding="utf-8")

    css_path = source_dir / "assets/css/deck.css"
    html = html.replace(
        '<link rel="stylesheet" href="assets/css/deck.css" />',
        f"<style>\n{css_path.read_text(encoding='utf-8')}\n</style>",
    )

    anime_path = source_dir / "assets/vendor/anime.min.js"
    html = html.replace(
        '<script src="assets/vendor/anime.min.js"></script>',
        f"<script>\n{inline_script(anime_path.read_text(encoding='utf-8'))}\n</script>",
    )

    chart = {
        "figma": data_uri(source_dir / "assets/charts/category_omni_figma.svg", "image/svg+xml"),
        "ppt": data_uri(source_dir / "assets/charts/category_omni_ppt.svg", "image/svg+xml"),
    }
    video = {
        "figma": data_uri(source_dir / "assets/video/phase_reversal.mp4", "video/mp4"),
        "ppt": data_uri(source_dir / "assets/video/phase_reversal_ppt.mp4", "video/mp4"),
    }
    poster = {
        "figma": data_uri(source_dir / "assets/video/phase_poster.png", "image/png"),
        "ppt": data_uri(source_dir / "assets/video/phase_poster_ppt.png", "image/png"),
    }
    embedded = json.dumps(
        {"chart": chart, "video": video, "poster": poster},
        ensure_ascii=False,
        separators=(",", ":"),
    )

    deck_script = re.search(r'<script src="(assets/js/[^"]+)"></script>', html)
    if not deck_script:
        raise SystemExit(f"deck script not found in {input_path}")
    script_path = source_dir / deck_script.group(1)
    script_content = inline_script(script_path.read_text(encoding="utf-8"))
    html = html.replace(
        deck_script.group(0),
        f"<script>window.__DECK_EMBEDDED__ = {embedded};</script>\n<script>\n{script_content}\n</script>",
    )

    html = html.replace(
        'src="assets/charts/category_omni_figma.svg"',
        f'src="{chart["figma"]}"',
    )
    html = html.replace(
        'src="assets/video/phase_reversal.mp4"',
        f'src="{video["figma"]}"',
    )
    html = html.replace(
        'poster="assets/video/phase_poster.png"',
        f'poster="{poster["figma"]}"',
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"wrote {output_path} ({size_mb:.2f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="slides/index.html")
    parser.add_argument("--output", default="dist/online-clothing-channel-deck.html")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    bundle(input_path, output_path)


if __name__ == "__main__":
    main()
