# 05. 모션·차트 설계

## 도구 분담
| 도구 | 역할 | 산출물 |
|---|---|---|
| seaborn / matplotlib | 인쇄·백업용 정적 차트, 테마별 색 | `slides/assets/charts/*.svg` |
| Manim | 발표용 히어로 애니메이션(막대 성장) | `slides/assets/video/*.mp4` |
| anime.js | 슬라이드 안 SVG 선·점·카운터·이미지 리빌 | `slides/assets/js/deck.js`, `deck-full.js` |
| SVG / CSS | 16:9 레이아웃, 테마 토큰 | `slides/index.html`, `assets/css/deck.css` |

> CDN은 쓰지 않는다. anime.js는 `slides/assets/vendor/anime.min.js`(v3.2.1)에 로컬 보관.

## 전체 덱 모션 매핑 (S00–S17)
| 슬라이드 | 내용 | 모션 | 데이터 |
|---|---|---|---|
| S00 | 표지 | 제목·메타 순차 등장 | – |
| S01 | 상위 7개 상품군 | 가로 막대 성장 | `category_latest.csv` |
| S03 | 6개월 규모 추이 | 선·면·점·카운터 | `clothing_wide.csv` |
| S04 | 누적 채널 비교 | 두 선 그리기 + 점유율 바 | `clothing_wide.csv` |
| S05 | 병행몰 비중 | 100% 누적 막대 성장 | `clothing_wide.csv` |
| S06 | 8월의 역전 | Manim 막대 성장 + 역전 강조 | `clothing_wide.csv` |
| S07 | 감소액 기여도 | 기여 막대 성장 | `clothing_wide.csv` |
| S08 | 패션 4군 병행몰 비중 | seaborn SVG + 와이프 리빌 | `category_latest.csv` |
| S09 | 규모 × 비중 포지션 | 산점도 팝 + 라벨 | `category_latest.csv` |
| S10–S16 | 프레임·가설·반론·결론 | 카드·여정·신뢰 경로 스태거 | – |

## 하이라이트 샘플 (H00–H05)
`slides/highlight.html`에 보존. H01–H05는 전체 덱의 S03·S04·S06·S08·S15에 대응합니다.

## 재생성
```bash
# 1) 정적 차트 2종(피그마/PPT)
.venv/bin/python scripts/charts/category_omni.py

# 2) Manim 2종(피그마/PPT) + 포스터
./scripts/render_motion.sh
```

## 테마
- **Figma**: `DESIGN.md`의 흑백 + 파스텔 블록 + 마젠타 포인트.
- **PPT**: 종이 질감 + 검정 아웃라인 + 러스트 포인트.
- 테마 전환은 우하단 `FIGMA / PPT` 버튼 또는 키보드 `T`.
- 테마에 따라 seaborn SVG와 Manim MP4를 교체한다.

## 접근성·안전장치
- `prefers-reduced-motion: reduce`이면 애니메이션을 건너뛰고 최종 상태를 보여 준다.
- JS가 실패해도 HTML의 최종 수치·차트가 읽히도록 기본값을 최종 상태로 둔다.
- 색만으로 구분하지 않는다: 범례 라벨·수치 라벨·패턴을 함께 쓴다.
- 발표장 오프라인 동작을 위해 영상·SVG·anime.js를 모두 로컬에 둔다.

## 비전공자 배려
- 별도 설명 박스 대신 차트의 축·단위·기간을 카드 안에서 바로 읽히게 둔다.
- 단위(백만 원), 기간, 잠정치(p) 표기를 차트와 하단 출처에 반복한다.
- 누적(3→8월)과 월별(7→8월)을 구분해 “한 달만 보고 단정하지 않기”를 명시한다.
- 가설 문구는 작은 라벨 대신 “~할 수 있다” 가능형으로 완화한다.

## 확인할 것
- [x] PPT 테마는 `section.ppt`(종이 질감) 유지 확정. 퍼플 이미지는 참고용 보관 (D014)
- [x] 전체 18장(S00–S17) 구현 완료 (D018)
- [ ] 추가 문헌(R02–R06) 확보 후 S10–S13 가설 문구 보강
