# References — 수집·인용 규칙

## 원칙
1. **등록 없는 인용 금지.** 슬라이드의 모든 `[R{NN}]`는 `sources.json`에 있어야 한다.
2. **1차 자료 우선.** 공식 통계·원논문 > 정부/산업 보고서 > 뉴스 > 블로그.
3. **주장 단위 인용.** "연구에 따르면" 금지. 어떤 문장의 어떤 수치/주장에 붙는지 명시.
4. **URL 추측 금지.** 실제로 연 URL만 기록하고, 접속일을 남긴다.
5. **원문 보관.** PDF·HTML 스크린샷을 `files/`에 저장한다. 저작권상 공유 불가하면 경로만 기록.

## ID 규칙
- `R01`, `R02`, … 두 자리. **재사용 금지** (삭제해도 번호를 다시 쓰지 않음).
- 파일명: `notes/R{NN}-{slug}.md` (예: `R01-kosis-DT_1KE10051.md`).
- `sources.json`의 `used_in`에 슬라이드 ID를 적는다.

## 새 출처 추가 3단계
1. `references/files/`에 원문 저장 → 파일명에 연도·기관 포함.
2. `references/notes/`에 요약 노트 작성 (`_TEMPLATE.md` 복사).
3. `references/sources.json` 등록 → `docs/02-outline.md`의 슬라이드 행에 `[R{NN}]` 표시.

## sources.json 필드
| 필드 | 설명 |
|---|---|
| `id` | `R01` 형식 |
| `type` | `official_statistics`, `paper`, `report`, `news`, `case`, `methodology` |
| `title` | 원제 |
| `collection` | 통계/조사/저널명 |
| `publisher` | 발행기관 |
| `authors` | 저자 (없으면 빈 배열) |
| `published` | 발행일 `YYYY-MM-DD` (모르면 빈 문자열) |
| `accessed` | 접속일 `YYYY-MM-DD` |
| `period` | 자료가 다루는 기간 |
| `url` | 실제 URL |
| `local_file` | `references/files/` 또는 `data/raw/` 상대 경로 |
| `note_file` | 요약 노트 경로 |
| `reliability` | 신뢰 등급 설명 |
| `key_facts` | 이 출처로만 주장할 수 있는 핵심 사실 |
| `caveats` | 해석 금지/한계 |
| `used_in` | 사용 슬라이드 ID 배열 |

## 신뢰 등급
- **A (1차):** 공식 통계, 원논문, 법령.
- **B (준1차):** 정부·공공기관 보고서, 산업협회 통계.
- **C (2차):** 주요 언론, 컨설팅 리포트.
- **D (보조):** 블로그, 기업 마케팅 자료 — 사실 근거로 단독 사용 금지.

## 현재 등록 대장
| ID | 유형 | 제목 | 발행/접속 | 사용 슬라이드 |
|---|---|---|---|---|
| R01 | 공식 통계 | 온라인쇼핑몰 운영형태별/상품군별거래액 (DT_1KE10051) | 접속 2026-10-25 | S00–S17 (샘플 H00–H05) |

## 디자인 레퍼런스 (인용 대상 아님)
- `DESIGN.md` — FIGMA 디자인 시스템(토큰 원본, 현재 적용).
- `files/design-apple-reference.md` — 이전 Apple 계열 명세(보관용, 미적용).
- `../7/assets/theme.css`의 `section.ppt` — PPT 양식(종이 질감/흑백) 참고.
- `files/ppt-persona-reference.jpg` — 사용자 제공 퍼플 페르소나/저니맵 이미지. 현재 테마에는 미적용 유지(D014). 메모: `notes/design-ppt-persona.md`

## 이 주제에서 더 찾아야 할 자료 (TODO)
- [ ] **R02** 온라인쇼핑동향조사 조사개요/지침 — '운영형태' 정의 확인 (A/B)
- [ ] **R03** 옴니채널 소비자 행태 학술논문 (예: 쇼루밍/웹루밍, 반품·교환) (A)
- [ ] **R04** 의류 온라인 반품률·사이즈 관련 공식/산업 자료 (B/C)
- [ ] **R05** 국내 패션 리테일러의 온·오프라인 연계 사례 (C, 보조)
- [ ] **R06** 2026년 7~8월 의류 소비 둔화 관련 공식 자료 (있다면) (B)

> 자료를 찾으면 URL을 먼저 확인하고, 이 목록의 ID를 실제 등록 ID로 바꾼다.
> 찾지 못한 항목은 삭제하지 말고 `docs/04-open-questions.md`에 이유와 함께 남긴다.
