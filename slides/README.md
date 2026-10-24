# Slides — HTML 덱

## 구조
```
slides/
├── index.html              # 전체 18장 S00–S17 (16:9)
├── highlight.html          # 하이라이트 6장 H00–H05
├── assets/css/deck.css     # FIGMA/PPT 테마 + 차트 스타일
├── assets/js/deck-full.js  # 전체 덱 이동·테마·anime.js 타임라인
├── assets/js/deck.js       # 하이라이트 샘플 모션
├── assets/vendor/          # anime.js v3.2.1 (로컬, CDN 미사용)
├── assets/charts/          # seaborn SVG (Figma/PPT)
├── assets/video/           # Manim MP4 + 포스터 (Figma/PPT)
└── assets/img/             # 필요 시 로고·아이콘
```

## 두 디자인 컨셉
| 모드 | 기준 | 특징 |
|---|---|---|
| FIGMA | 루트 `DESIGN.md` | 흑백 + 파스텔 블록(라일락/민트/크림) + 마젠타 포인트 |
| PPT | 프로젝트 7의 `section.ppt` | 오프화이트 종이 질감 + 검정 아웃라인 + 러스트 포인트 |

- 우하단 `FIGMA / PPT` 버튼, 키보드 `T`로 전환.
- URL 파라미터 `?theme=figma` / `?theme=ppt`로 고정 가능.
- 테마에 따라 seaborn SVG와 Manim MP4가 교체됨.

## 조작
| 키 | 동작 |
|---|---|
| `→` `Space` `PageDown` | 다음 |
| `←` `PageUp` | 이전 |
| `Home` / `End` | 처음 / 끝 |
| `T` | 테마 전환 |
| `R` | 현재 슬라이드 애니메이션 다시 재생 |

## 규칙
- 16:9 고정. JS가 `min(뷰포트/1280, 뷰포트/720)`로 스케일.
- 전체 덱 ID는 `S00–S17`, 샘플 ID는 `H00–H05`.
- 모든 사실 주장 하단에 `출처: … [R{NN}]`.
- 차트 수치는 `data/processed/` CSV에서만. 축 단위·기간·잠정치 표기.
- 색만으로 구분하지 않는다: 색 + 라벨 + 수치 라벨.
- `prefers-reduced-motion`이면 모션을 끄고 최종 상태를 보여 준다.
- JS가 실패해도 HTML 기본값(최종 수치)이 읽히도록 유지한다.

## 모션 그래프
| 슬라이드 | 방식 |
|---|---|
| S01 | anime.js 상위 7개 가로 막대 |
| S03 | anime.js 선·면·점·카운터 |
| S04 | anime.js 두 선 그리기 |
| S05 | anime.js 100% 누적 막대 |
| S06 | Manim 8월 역전 영상 |
| S07 | anime.js 기여도 막대 |
| S08 | seaborn SVG + 와이프 리빌 |
| S09 | anime.js 산점도 |
| S10–S16 | 카드·여정·신뢰 경로·결론 스태거 |

## 미리보기
```bash
python3 -m http.server 8000
# 전체: http://localhost:8000/slides/
# 샘플: http://localhost:8000/slides/highlight.html
# PPT:  http://localhost:8000/slides/?theme=ppt
```
`index.html`을 직접 열어도 동작하도록 외부 CDN에 의존하지 않는다.

## 모션 자산 재생성
```bash
.venv/bin/python scripts/charts/category_omni.py
./scripts/render_motion.sh
```
자세한 설계: `docs/05-motion.md`

## 상태
- [x] 전체 S00–S17 18장
- [x] 하이라이트 H00–H05 6장
- [x] FIGMA/PPT 테마 토글
- [x] 데이터 모션 8종(anime.js 6, Manim 1, seaborn 1)
- [ ] R02–R06 문헌 보강
- [ ] 15분 리허설 후 문구·분량 조정
- [ ] 인쇄/PDF·오탈자 최종 검수
