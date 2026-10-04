---
name: deck-factory
description: >-
  발표급 다크 에디토리얼 HTML 덱을 손으로 짓는 디자인 시스템. 브리프/원고를 받아
  Apple·Linear·Stripe 키노트급으로 보이는 프레젠테이션을 프론트엔드(HTML/CSS,
  1920×1080 슬라이드)로 만들고 헤드리스 크로미움으로 PNG/PDF까지 렌더한 뒤 공유용 PDF는 기본 경량화한다. PPTX 생성기가
  아니라 "슬라이드처럼 보이는 웹 페이지"를 짓는 방법론 + 재사용 CSS 토큰/컴포넌트.
  기본은 다크 에디토리얼이고, 문서형·보고서형·출력형 브리프는 paper-light 프로파일로 전환한다.
  트리거 — "발표자료/슬라이드/덱을 예쁘게", "IR·보고 덱을 발표급으로", "HTML로 프레젠테이션",
  "다크 에디토리얼 슬라이드", "키노트 톤 덱", "거대숫자 스탯 슬라이드", "deck-factory 디자인",
  기존 밋밋한 덱을 "상용 발표자료처럼" 다시 짜달라는 요청. 핵심 규칙 — dark는 near-black
  #08090A 캔버스(순흑 금지), light는 paper #F7F4EC 캔버스, 채운 박스 금지(surface 래더 + hairline),
  슬라이드당 accent 1곳, 거대숫자 value>label>context 3단 위계, 4모서리 헤더/푸터,
  eyebrow→마침표 액션타이틀→지배 오브젝트 1개→tail 골격, CJK word-break:keep-all,
  크기·트래킹으로 위계(굵기 남발 금지). 상세 토큰표·컴포넌트별 CSS·13-슬롯 레이아웃 어휘·
  라이트 프로파일 전환·WSL 렌더 팁은 reference.md 참조.
when_to_use: >-
  사용자가 발표자료·슬라이드·덱을 "발표급/상용 키노트처럼" 보이게 만들어 달라 하고,
  PPTX 편집이 아니라 HTML/CSS로 디자인해도 되는 경우. 밋밋하거나 아마추어 같은 기존 덱을
  다시 짜는 요청, 다크 에디토리얼 톤 프레젠테이션, 거대숫자 스탯 슬라이드에 특히 적합.
---

# deck-factory — 발표급 다크 에디토리얼 HTML 덱

브리프/원고를 받아 **상용 발표자료처럼 보이는 HTML 슬라이드**를 짓는 디자인 시스템이다.
슬라이드 = 1920×1080 `<section class="slide">` 하나. 손으로 짜되 검증된 토큰/컴포넌트를 쓴다.

이건 실제로 검증한 방법이다(12장 프리미엄 덱을 렌더까지 뽑음). 자동 파이프라인이 아니라,
**Claude가 이 디자인 계약을 따라 슬라이드를 직접 조립**하는 것까지가 이 스킬의 약속이다.
storyline→copy→compose→grade→export 6단계 자동 파이프라인은 지향하는 로드맵으로 reference.md에서만 다룬다.

## 이 8가지 규칙이 발표급과 아마추어를 가른다

1. **프로파일 먼저 결정** — 기본은 dark `#08090A` near-black. 문서·보고서·제안서·출력·핸드아웃·화이트페이퍼·이사회·공공·학술, 또는 report/proposal/document/print/handout/whitepaper/board memo/academic/government 브리프는 light `#F7F4EC` paper. 명시 `theme/profile: light|dark`가 자동 감지보다 우선한다.
2. **no_box** — 채운 회색 카드 금지. 배경은 surface 래더, 구분은 hairline(dark `rgba(255,255,255,.07)`, light `rgba(26,26,26,.10)`). 그림자·스포트라이트·대기그라디언트 금지.
3. **슬라이드당 accent 1곳** — 시그널 색을 eyebrow·metric·rule 중 딱 한 곳에만. 다색 칩 남발이 제일 촌스럽다.
4. **거대숫자 3단 위계** — Label(11px mute) > Value(140~172px, weight 600, tnum) > context(한 문장). 스탯 슬라이드 숫자 렌더높이 ≥120px. **출처각주 금지**.
5. **4모서리 헤더/푸터** — 좌상 브랜드칩, 우상 파트/날짜, 좌하 저자, 우하 페이지(`05 / 12`). 전 슬라이드 공통.
6. **에디토리얼 골격** — eyebrow(대문자, accent) → **마침표로 끝나는 액션타이틀**("두 달 만에 1억 명.") → 지배 오브젝트 1개 → tail(hairline 위 단서 1줄). 명사 나열 제목 금지.
7. **CJK 안전** — `word-break: keep-all; overflow-wrap: normal; line-break: strict;` 없으면 한글이 음절로 깨진다.
8. **크기·트래킹으로 위계** — 굵기 남발 금지. 한 슬라이드 폰트 크기 종류 ≤3. display 음수 트래킹 `-0.03em`.

## 슬라이드 짓는 절차

1. **셋업** — `assets/styles.css`를 복사해 쓴다. 슬라이드마다 `<link rel="stylesheet" href="styles.css">` + 폰트(fonts.css). light면 `<body data-theme="light">`, 혼합 테스트면 `<section class="slide" data-theme="light">`. `<section class="slide">` 안에 `.bg`(배경/이미지) → `.deck-brand/.deck-meta/.deck-author/.deck-page`(4모서리) → `.frame`(콘텐츠) 순서.
2. **마스터 크롬** — 4모서리 헤더/푸터를 먼저 박는다. 이게 매 슬라이드 뼈대다. slide-01(커버)·slide-05(스탯) 예시가 `work/premium/slides/`에 있다.
3. **레이아웃 고르기** — 13-슬롯 어휘 중 하나로만: cover · chapter · statement · bullets · two-col · cards-3 · data-split · image-full · image-split · flow · chart-bar · kpi-3 · closing. 새 레이아웃 발명 금지.
4. **골격 채우기** — `.eyebrow` → `.action-title`(마침표) → `.subhead`(선택) → 지배 오브젝트 → `.tail`(선택). 슬라이드 1장 = 지배 오브젝트 1개(한 문장/한 비교/한 스탯/한 다이어그램).
5. **거대숫자** — 스탯이면 `.stat-row > .stat`(`.k` 라벨 / `.v` 숫자 + `<small>`단위/`.mult`배수 / `.c` 캡션). 3열 `repeat(3,1fr)`.
6. **이미지 깊이** — 커버·챕터는 풀블리드 히어로 + 텍스트측 스크림(dark는 near-black, light는 paper tint). 데이터 슬라이드는 히어로를 우측 세로 슬롯에 격리 + 저조도 글로우. **생성 이미지 위 코드로 글자 합성 금지**(프롬프트로만).
7. **렌더/경량화** — 헤드리스 크로미움으로 각 slide-NN.html을 1920×1080 PNG로 캡처하고 PDF를 만든다. 공유용 PDF는 기본으로 `scripts/compact-pdf.sh input.pdf`를 실행해 `*-lite.pdf`를 낸다. 원본 PDF는 보관용이다. WSL/폰트 임베드 팁은 reference.md.

## 합격 체크리스트 (전부 YES여야 발표급)

- [ ] 프로파일이 브리프와 맞음(dark `#08090A` 또는 light `#F7F4EC`), 채운 회색 박스 0개
- [ ] 스탯 슬라이드 ≥120px 거대숫자 + value>label>context 3단 (출처각주 없음)
- [ ] 4모서리 헤더/푸터 전 슬라이드 존재
- [ ] eyebrow(accent) → 액션타이틀(마침표) → 지배 오브젝트 → tail 골격
- [ ] accent 슬라이드당 1곳, 다색 칩 0개
- [ ] 깨진 텍스트(`출처:조회` 같은 바인딩 잔재) 0개
- [ ] 커버/데이터에 히어로 이미지 + 스크림/글로우 깊이
- [ ] 공유용 PDF는 `*-lite.pdf` 경량본으로 제공됨(원본 PDF만 전달 금지)
- [ ] 한글 줄바꿈 깨짐 0개(keep-all)

한 항목이라도 NO면 발표급 아님 — 고쳐서 다시.

## 더 볼 곳 (reference.md)

- 전체 색 토큰표 · 타이포 스케일(11~172px) · 폰트 스택
- 컴포넌트별 CSS와 언제 쓰는지: 빅넘버 · flow · bento · 타임라인 · 코드블록 · 번호 스텝 · before/after 목업 · 반원 게이지
- 13-슬롯 레이아웃 어휘 상세
- 다크 → 라이트/문서 프로파일 전환법
- WSL/헤드리스 크로미움 렌더 팁(폰트 base64 임베드 이슈)
- 이미지 생성 프롬프트 원칙(글자 합성 금지)
- 지향 파이프라인(storyline→export) 로드맵
