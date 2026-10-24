#!/usr/bin/env python3
"""Manim hero: the August reversal in month-over-month clothing sales."""

from __future__ import annotations

import csv
import os
from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    GrowFromEdge,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
    config,
)

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "processed" / "clothing_wide.csv"
FONT = "Apple SD Gothic Neo"

INK = "#14110D"
MAGENTA = os.environ.get("MANIM_ACCENT", "#FF3D8B")
MUTED = "#6B6258"

config.background_color = "#FFFFFF"
config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 30


def monthly_change(previous: int, current: int) -> float:
    return (current - previous) / previous * 100


def load_changes() -> tuple[float, float, float, float]:
    rows = {row["month"]: row for row in csv.DictReader(INPUT.open(encoding="utf-8-sig"))}
    july = rows["2026-07"]
    august = rows["2026-08"]
    june = rows["2026-06"]
    return (
        monthly_change(int(june["online_only"]), int(july["online_only"])),
        monthly_change(int(june["omnichannel"]), int(july["omnichannel"])),
        monthly_change(int(july["online_only"]), int(august["online_only"])),
        monthly_change(int(july["omnichannel"]), int(august["omnichannel"])),
    )


class PhaseReversal(Scene):
    def construct(self) -> None:
        jul_online, jul_omni, aug_online, aug_omni = load_changes()

        title = Text("8월의 역전", font=FONT, font_size=46, weight="BOLD", color=INK)
        title.to_edge(UP, buff=0.55)
        subtitle = Text(
            "전월 대비 의류 온라인 거래액 감소율 (%)",
            font=FONT,
            font_size=22,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(title, shift=UP * 0.15), FadeIn(subtitle), run_time=0.8)

        baseline = Line(LEFT * 5.7 + DOWN * 2.0, RIGHT * 5.7 + DOWN * 2.0, color=INK, stroke_width=2)
        self.play(Create(baseline), run_time=0.5)

        scale = 0.145
        base_y = -2.0
        width = 0.95
        centers = {"jul": -2.25, "aug": 2.25}

        def make_bar(x: float, value: float, color: str) -> tuple[Rectangle, Text]:
            magnitude = abs(value)
            height = magnitude * scale
            bar = Rectangle(
                width=width,
                height=height,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            bar.move_to([x, base_y + height / 2, 0])
            label = Text(f"-{magnitude:.1f}%", font=FONT, font_size=22, color=color, weight="BOLD")
            label.next_to(bar, UP, buff=0.12)
            return bar, label

        legend_online = VGroup(
            Rectangle(width=0.22, height=0.22, fill_color=INK, fill_opacity=1, stroke_width=0),
            Text("온라인 전용몰", font=FONT, font_size=18, color=INK),
        ).arrange(RIGHT, buff=0.12)
        legend_online.to_corner(UP + RIGHT, buff=0.55)
        legend_online.shift(DOWN * 0.55)
        legend_omni = VGroup(
            Rectangle(width=0.22, height=0.22, fill_color=MAGENTA, fill_opacity=1, stroke_width=0),
            Text("온·오프라인 병행몰", font=FONT, font_size=18, color=INK),
        ).arrange(RIGHT, buff=0.12)
        legend_omni.next_to(legend_online, DOWN, buff=0.12, aligned_edge=RIGHT)
        self.play(FadeIn(legend_online), FadeIn(legend_omni), run_time=0.5)

        july_label = Text("7월", font=FONT, font_size=24, color=INK)
        july_label.move_to([centers["jul"], base_y - 0.38, 0])
        august_label = Text("8월", font=FONT, font_size=24, color=INK)
        august_label.move_to([centers["aug"], base_y - 0.38, 0])
        self.play(FadeIn(july_label), FadeIn(august_label), run_time=0.3)

        j_online_bar, j_online_label = make_bar(centers["jul"] - 0.58, jul_online, INK)
        j_omni_bar, j_omni_label = make_bar(centers["jul"] + 0.58, jul_omni, MAGENTA)
        self.play(
            GrowFromEdge(j_online_bar, DOWN),
            GrowFromEdge(j_omni_bar, DOWN),
            FadeIn(j_online_label),
            FadeIn(j_omni_label),
            run_time=1.1,
        )
        self.wait(0.5)

        a_online_bar, a_online_label = make_bar(centers["aug"] - 0.58, aug_online, INK)
        a_omni_bar, a_omni_label = make_bar(centers["aug"] + 0.58, aug_omni, MAGENTA)
        self.play(
            GrowFromEdge(a_online_bar, DOWN),
            GrowFromEdge(a_omni_bar, DOWN),
            FadeIn(a_online_label),
            FadeIn(a_omni_label),
            run_time=1.1,
        )
        self.wait(0.35)

        reversal = Text("병행몰이 더 크게 감소", font=FONT, font_size=21, color=MAGENTA, weight="BOLD")
        reversal.next_to(a_omni_bar, UP, buff=0.7)
        underline = Line(
            reversal.get_left() + DOWN * 0.06,
            reversal.get_right() + DOWN * 0.06,
            color=MAGENTA,
            stroke_width=2,
        )
        self.play(FadeIn(reversal, shift=UP * 0.1), Create(underline), run_time=0.6)

        note = Text(
            "7·8월은 잠정치(p) · 단위: 백만 원",
            font=FONT,
            font_size=16,
            color=MUTED,
        )
        note.to_edge(DOWN, buff=0.35)
        source = Text(
            "출처: 국가데이터처, 온라인쇼핑동향조사 (2026.08 잠정) [R01]",
            font=FONT,
            font_size=14,
            color=MUTED,
        )
        source.next_to(note, DOWN, buff=0.08)
        self.play(FadeIn(note), FadeIn(source), run_time=0.5)
        self.wait(2.0)