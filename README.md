# 온라인 전용몰 vs 온·오프라인 병행몰 — 의류 거래 비교

데이터 분석 입문 수업(대학 비전공자) 발표용 HTML 슬라이드 덱입니다.
**전체 18장(S00–S17)** 과 **하이라이트 샘플 6장(H00–H05)** 이 구현되어 있습니다.
전체 덱은 `slides/index.html`, 샘플은 `slides/highlight.html`입니다.

## 배포
- 전체 덱: https://ckzi-su.github.io/online-clothing-channel-deck/
- PPT 테마: https://ckzi-su.github.io/online-clothing-channel-deck/?theme=ppt
- 하이라이트 샘플: https://ckzi-su.github.io/online-clothing-channel-deck/highlight.html
- 저장소: https://github.com/ckzi-su/online-clothing-channel-deck

## 한눈에 보는 구조

```
.
├── README.md                 # 프로젝트 허브 (여기)
├── AGENTS.md                 # 작업·소통 규칙
├── DESIGN.md                 # Figma 디자인 시스템 명세
├── requirements.txt          # manim / seaborn / matplotlib / pandas
├── docs/
│   ├── 01-brief.md           # 주제, 질문, 범위, 청중, 산출물
│   ├── 02-outline.md         # 전체 18장 슬라이드 + 근거 계약
│   ├── 03-decisions.md       # 확정된 결정 로그
│   ├── 04-open-questions.md  # 답변 대기 / 결정됨
│   └── 05-motion.md          # 모션·차트 설계와 재생성 방법
├── references/
│   ├── README.md             # 레퍼런스 수집·인용 규칙
│   ├── sources.json          # 인용의 단일 원본
│   ├── notes/                # 출처별 요약 노트 (R01-....md)
│   └── files/                # 원문·디자인 레퍼런스
├── data/
│   ├── raw/                  # 원본 KOSIS xlsx
│   ├── processed/            # 스크립트 산출 CSV (덱에 쓰는 수치)
│   └── README.md             # 출처, 단위, 변환, 한계
├── scripts/
│   ├── xlsx_to_csv.py        # xlsx → tidy CSV
│   ├── check_refs.py         # [R{NN}] 등록 검증
│   ├── render_motion.sh      # seaborn + Manim 자산 재생성
│   ├── charts/               # seaborn 차트
│   └── manim/                # Manim 장면
└── slides/
    ├── index.html            # 전체 18장 (16:9, FIGMA/PPT 토글)
    ├── highlight.html        # 하이라이트 6장 샘플 (H00–H05)
    ├── assets/css/deck.css   # 두 테마 + 차트 스타일
    ├── assets/js/deck.js     # 샘플 모션
    ├── assets/js/deck-full.js# 전체 덱 모션
    ├── assets/vendor/        # anime.js v3.2.1 (오프라인)
    ├── assets/charts/        # seaborn SVG (테마별)
    ├── assets/video/         # Manim MP4 + 포스터 (테마별)
    └── README.md             # 조작법·테마·검수
```

## 디자인 컨셉 두 가지
- **FIGMA**: `DESIGN.md`의 흑백 + 파스텔 블록 + 마젠타 포인트.
- **PPT**: 종이 질감 + 검정 아웃라인 + 러스트 포인트. (프로젝트 7의 `section.ppt` 레퍼런스)
- 덱 우하단 `FIGMA / PPT` 버튼 또는 키보드 `T`로 전환합니다.
- `references/files/ppt-persona-reference.jpg`는 퍼플 페르소나/저니맵 참고 이미지입니다.
  현재 PPT 테마에는 미적용을 유지합니다(D014).

## 모션 그래프
| 슬라이드 | 방식 | 파일 |
|---|---|---|
| S01 상위 7개 | anime.js 가로 막대 성장 | `deck-full.js` |
| S03 규모 추이 | anime.js 선·면·점·카운터 | `deck-full.js` |
| S04 채널 비교 | anime.js 두 선 그리기 | `deck-full.js` |
| S05 점유율 | anime.js 100% 누적 막대 성장 | `deck-full.js` |
| S06 8월 역전 | Manim 막대 성장 | `assets/video/phase_reversal*.mp4` |
| S07 기여도 | anime.js 기여 막대 | `deck-full.js` |
| S08 패션 카테고리 | seaborn SVG + 와이프 리빌 | `assets/charts/category_omni_*.svg` |
| S09 포지션 맵 | anime.js 산점도 팝 | `deck-full.js` |
| S10–S16 | 카드·여정·신뢰 경로·결론 스태거 | `deck-full.js` |

## 재현 명령
```bash
# 데이터
python3 scripts/xlsx_to_csv.py
python3 scripts/check_refs.py

# 모션 자산 (최초 1회 환경 설치)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
./scripts/render_motion.sh

# 미리보기
python3 -m http.server 8000
# 전체:   http://localhost:8000/slides/
# 샘플:   http://localhost:8000/slides/highlight.html
# PPT:    http://localhost:8000/slides/?theme=ppt
```
Manim은 macOS에서 `brew install pkg-config cairo pango ffmpeg`가 필요합니다.

## 주제를 한 문장으로
> 2026년 3~8월 온라인 의류 거래에서, 온라인 전용몰과 온·오프라인 병행몰의
> 규모·점유율 추이는 어떻게 다르며 그 차이는 무엇을 시사하는가?

핵심 데이터는 KOSIS 「온라인쇼핑동향조사」 `DT_1KE10051`입니다.
**이 통계는 온라인 거래만 집계하므로, '병행몰'은 오프라인 매출이 아니라
오프라인 매장을 가진 사업자의 온라인 매출입니다.** 덱에서 반드시 명시합니다.

## 레퍼런스를 넣는 방식 (요약)
1. 원문을 `references/files/`에 저장하고, `references/notes/R{NN}-{slug}.md` 노트를 만든다.
2. `references/sources.json`에 `R{NN}`을 등록한다. (등록 없는 인용 금지)
3. `docs/02-outline.md`의 해당 슬라이드에 `[R{NN}]`로 연결한다.
4. 덱 하단 출처에도 같은 ID를 쓴다.

자세한 규칙: `references/README.md`

## 현재 상태
- [x] 폴더 구조·규칙 수립
- [x] KOSIS 원본 데이터 확보 및 CSV 변환
- [x] 전체 18장 아웃라인 + 수치 메모
- [x] 디자인 컨셉 2종(FIGMA/PPT)
- [x] 전체 18장(S00–S17) + 하이라이트 샘플(H00–H05)
- [x] 데이터 모션 8종(anime.js 6, Manim 1, seaborn 1)
- [ ] 추가 레퍼런스 수집 (R02–R06)
- [ ] 15분 리허설 후 분량·문구 조정
- [ ] 인쇄/PDF·오탈자 최종 검수
