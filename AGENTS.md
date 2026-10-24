# AGENTS.md — 이 프로젝트에서 일하는 규칙

## 언어와 태도
- 사용자와의 소통, 문서, 슬라이드 카피는 **한국어**를 기본으로 한다.
- 모르는 것은 추측해서 채우지 않고 `docs/04-open-questions.md`에 질문으로 남긴다.
- 사용자의 결정을 대신 확정하지 않는다. 제안과 확정을 구분한다.

## 근거와 인용 (가장 중요)
- 모든 사실 주장에는 `[R{NN}]` 인용을 붙인다. `references/sources.json`에 없는 ID는 쓰지 않는다.
- 데이터 수치는 `data/processed/`의 CSV 또는 `data/raw/` 원본에서만 가져온다.
  기억이나 어림값으로 숫자를 만들지 않는다.
- 새 출처를 추가할 때는 3단계를 모두 수행한다:
  1. `references/files/`에 원문 저장 (가능한 경우)
  2. `references/notes/R{NN}-{slug}.md` 요약 노트 작성
  3. `references/sources.json` 등록 + `docs/02-outline.md`의 사용 슬라이드 표시
- 인터넷 출처는 제목, 발행기관, 발행일, 접속일, URL을 모두 기록한다. URL을 추측하지 않는다.
- 1차 자료(공식 통계·원논문)를 2차 자료(뉴스·블로그)보다 우선한다. 2차 자료는 보조로만 쓴다.
- 인용은 주장 단위로 한다. "연구에 따르면" 같은 모호한 표현 금지.

## 데이터 규칙
- 원본 `data/raw/`는 수정하지 않는다. 가공은 `scripts/`로만 하고 `data/processed/`에 쓴다.
- 단위는 **백만 원**. 월 표기의 `p)`는 잠정치이므로 슬라이드/각주에 표시한다.
- 파생 수치(증감률, 점유율)는 반올림 기준을 문서에 남긴다. (현재: 소수 둘째 자리)
- `온·오프라인 병행몰`을 "오프라인 매출"로 해석하지 않는다. 이 통계는 온라인 거래만 포함한다.
- 상관을 인과로 쓰지 않는다. 원인 설명은 별도 근거가 있을 때만 "가설"로 표시한다.

## 슬라이드 규칙
- 16:9, 단일 발표 흐름. 슬라이드마다 **하나의 메시지**만 둔다.
- 각 슬라이드 하단에 출처 표기: `출처: 국가데이터처, 온라인쇼핑동향조사 (2026.08 잠정) [R01]`
- 차트는 `data/processed/` 수치를 직접 사용하고, 축 단위·기간·잠정치 여부를 표시한다.
- 텍스트는 발표용으로 짧게. 상세 설명은 발표자 노트나 `docs/`로 뺀다.
- 색만으로 정보를 구분하지 않는다(색약 접근성). 온라인 전용/병행은 색 + 라벨/패턴 병행.

## 소통 규칙
- 작업 전 `docs/02-outline.md`와 `docs/04-open-questions.md`를 확인한다.
- 방향이 바뀌면 `docs/03-decisions.md`에 날짜·결정·이유·대안을 기록한다.
- 사용자에게 물을 것이 생기면 채팅에만 두지 말고 `docs/04-open-questions.md`에도 남긴다.
- 사용자가 답하면 해당 질문을 `결정됨`으로 옮기고 결정 로그에 연결한다.
- 파일을 크게 갈아엎기 전에는 무엇을 왜 바꾸는지 먼저 한 줄로 알린다.

## 검증
- 데이터 변경 후: `python3 scripts/xlsx_to_csv.py` 재실행, CSV 수치 확인.
- 슬라이드 변경 후: `python3 -m http.server 8000`으로 열어 16:9 깨짐/오탈자/출처 누락 확인.
- 마무리 전: 모든 `[R{NN}]`가 `sources.json`에 존재하는지, 모든 수치가 CSV에 있는지 대조.

## 모션·차트 규칙 (2026-10-25 추가)
- 정적 차트: `.venv/bin/python scripts/charts/*.py` → `slides/assets/charts/` (테마별 SVG).
- Manim: `scripts/manim/*.py` → `slides/assets/video/` (Figma/PPT 색상 2종).
  - 전체 재생성: `./scripts/render_motion.sh`
  - 환경: `brew install pkg-config cairo pango ffmpeg` + `pip install -r requirements.txt`
- 브라우저 모션: anime.js v3.2.1. `slides/assets/vendor/anime.min.js`만 사용하고 CDN은 쓰지 않는다.
- 애니메이션은 슬라이드 진입 시 재생하고, `prefers-reduced-motion`에서는 끈다.
  JS가 실패해도 최종 수치·차트가 보이도록 HTML 기본값을 최종 상태로 둔다.
- 차트 색은 CSS 변수(`--chart-a`, `--chart-b`)로 테마에 맞춘다. 색만으로 구분하지 않는다.
- 샘플 ID `H00–H05`와 전체 덱 ID `S00–S17`을 섞지 않는다.
