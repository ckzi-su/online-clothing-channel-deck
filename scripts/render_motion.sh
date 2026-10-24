#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

PY=".venv/bin/python"
MANIM=".venv/bin/manim"

if [ ! -x "$PY" ]; then
  echo "먼저 .venv를 만들고 requirements.txt를 설치하세요." >&2
  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

"$PY" scripts/charts/category_omni.py

"$MANIM" -qm --media_dir media \
  scripts/manim/phase_reversal.py PhaseReversal
cp media/videos/phase_reversal/720p30/PhaseReversal.mp4 slides/assets/video/phase_reversal.mp4
ffmpeg -y -ss 7.2 -i slides/assets/video/phase_reversal.mp4 \
  -frames:v 1 -update 1 slides/assets/video/phase_poster.png >/dev/null 2>&1

MANIM_ACCENT="#B23A1F" "$MANIM" -qm --media_dir media \
  --output_file phase_reversal_ppt \
  scripts/manim/phase_reversal.py PhaseReversal
cp media/videos/phase_reversal/720p30/phase_reversal_ppt.mp4 slides/assets/video/phase_reversal_ppt.mp4
ffmpeg -y -ss 7.2 -i slides/assets/video/phase_reversal_ppt.mp4 \
  -frames:v 1 -update 1 slides/assets/video/phase_poster_ppt.png >/dev/null 2>&1

echo "모션 자산 생성 완료: slides/assets/charts/, slides/assets/video/"
