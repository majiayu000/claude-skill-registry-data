---
name: proposal-ppt
description: "RFP(제안요청서) 분석 및 입찰 제안서 자동 생성 (PPTX / HTML+Figma). 사용자가 \"제안서\", \"제안요청서\", \"RFP\", \"입찰\", \"PPTX 생성\", \"slide_kit\", \"테스트 폴더\", \"제안서 만들어\", \"제안서 제작\", \"proposal\", \"HTML 제안서\", \"Figma 제안서\" 등을 언급할 때 활성화."
version: 4.1.0
---

# 입찰 제안서 자동 생성 스킬

RFP 문서를 분석하여 Impact-8 구조의 전문 입찰 제안서를 자동 생성합니다.

## 2가지 생성 모드

| 모드 | 커맨드 | 파이프라인 | 결과물 |
|------|--------|-----------|--------|
| **PPTX** (기본) | `/proposal 테스트 XX --format pptx` | `slide_kit.py` → PPTX | `.pptx` 파일 |
| **Figma** | `/proposal 테스트 XX --format figma` | `slide_kit_html.py` → HTML → Gemini → Figma | `.html` + Figma |

## 프로젝트 경로

```
프로젝트 루트:    <PROJECT_ROOT>
RFP 입력:        제안요청서/테스트 XX/  (PDF 파일들)
출력:            output/테스트 XX/      (생성 스크립트 + 결과물)
slide_kit PPTX:  src/generators/slide_kit.py
slide_kit HTML:  src/generators/slide_kit_html.py
html_enhancer:   src/generators/html_enhancer.py
figma_exporter:  src/generators/figma_exporter.py
pipeline:        src/orchestrators/pipeline.py (후처리: Gemini + Figma)
```

---

## STEP 1: 인자 파싱

- 첫 번째 인자: 테스트 폴더명
- `--format`: pptx (기본) 또는 figma
- `--theme`: default, corporate, warm, nature, creative
- 입력: `제안요청서/{폴더명}/` → 출력: `output/{폴더명}/`

## STEP 2: RFP 분석

PDF 읽기 → 추출:
- 프로젝트명, 발주처, 과업 범위, 평가 기준, 예산, 일정
- 프로젝트 유형: marketing_pr / event / it_system / public / consulting

## STEP 3: 콘텐츠 기획

- **Win Theme 3개** — 제안서 전체 반복 핵심 메시지
- **Impact-8 Phase** 콘텐츠 설계 (Phase 0~7)
- **Action Title** — 인사이트 기반 문장형 제목 (Topic Title 금지)
- **KPI + 산출근거** — 모든 KPI에 근거 데이터 포함

## STEP 4: 생성 스크립트 작성

### PPTX 모드 → `generate_제안서.py`

```python
import sys; sys.path.insert(0, "<PROJECT_ROOT>")
from src.generators.slide_kit import *

prs = new_presentation()
WIN = {"data": "...", "story": "...", "ugc": "..."}

slide_cover(prs, "프로젝트명", "발주처명")
slide_toc(prs, "목차", [("01", "HOOK", "설명"), ...], pg=2)

# Phase별 섹션 구분자 + 콘텐츠 슬라이드들
slide_section_divider(prs, "01", "SUMMARY", "부제", "스토리", "data", WIN)
s = new_slide(prs)
bg(s, C["white"])
TB(s, "Action Title — 인사이트 기반 제목", pg=3)
v = VStack()
HIGHLIGHT(s, "핵심 메시지", y=v.next(Inches(0.75)))
# ...

slide_closing(prs, "감사합니다", project_title="프로젝트명")
save_pptx(prs, "output/{폴더명}/제안서.pptx")
```

**PPTX 핵심**: 모든 함수의 첫 인자가 `prs` 또는 `s` (슬라이드 객체). Inches() 좌표계.

### Figma 모드 → `generate_제안서_html.py`

```python
import sys; sys.path.insert(0, "<PROJECT_ROOT>")
from src.generators.slide_kit_html import *

slides = []
WIN = {"data": "...", "story": "...", "ugc": "..."}

slides.append(slide_cover("프로젝트명", "발주처명"))
slides.append(slide_toc("목차", [("01", "HOOK", "설명"), ...]))

# Phase별 섹션 구분자 + 콘텐츠 슬라이드들
slides.append(slide_section_divider("01", "SUMMARY", "부제", "스토리", "data", WIN))
parts = []
parts.append(TB("Action Title — 인사이트 기반 제목"))
parts.append(HIGHLIGHT("핵심 메시지", y=Z["ct_y"]))
slides.append(new_slide("".join(parts), bg(C["white"])))
# ...

slides.append(slide_closing("감사합니다", client="발주처명"))
html = render_presentation(slides, title="프로젝트명")
save_html(html, "output/{폴더명}/proposal.html")

# 후처리
from src.orchestrators.pipeline import PostProcessor
import asyncio
post = PostProcessor()
result = asyncio.run(post.run("output/{폴더명}/proposal.html", format="figma"))
```

**HTML 핵심**: `prs`/`s` 인자 없음 (HTML 문자열 반환). px 좌표계. `new_slide(parts, bg_color)`.

## STEP 5: 실행 및 검증

```bash
cd "<PROJECT_ROOT>"
python3 "output/{폴더명}/generate_제안서.py"        # PPTX
python3 "output/{폴더명}/generate_제안서_html.py"    # Figma
```

오류 시 수정 반복. 완료 시 `open` 명령으로 파일 열기.

---

## PPTX vs HTML API 차이 요약

| 항목 | PPTX (slide_kit.py) | HTML (slide_kit_html.py) |
|------|---------------------|--------------------------|
| 첫 인자 | `prs` 또는 `s` (객체) | 없음 (문자열 반환) |
| 좌표 | Inches (예: `Inches(1.1)`) | px (예: `158`) |
| 변환 | — | `px = inches × 144` |
| 색상 | `C["primary"]` (RGBColor) | `C["primary"]` (HEX `"#002C5F"`) |
| 새 슬라이드 | `s = new_slide(prs)` | `new_slide(parts, bg_color)` |
| 저장 | `save_pptx(prs, path)` | `render_presentation()` + `save_html()` |
| VStack gap | `0.2` (inches) | `29` (px) |
| 기본 폰트 크기 | `sz=13` (pt) | `sz=17` (px) |

## HTML 좌표 상수 (px)

```
SW=1920  SH=1080  ML=115  MR=115  CW=1690
Z["ct_y"]=158  Z["ct_b"]=936  GAP=29  CGAP=22
```

---

## Impact-8 Phase 구성

| Phase | 이름 | 비중 | 장수 |
|-------|------|------|------|
| 0 | HOOK (표지+목차+티저) | 5% | 3-10p |
| 1 | SUMMARY (Executive Summary) | 5% | 3-5p |
| 2 | INSIGHT (시장+문제) | 10% | 8-15p |
| 3 | CONCEPT & STRATEGY | 12% | 8-15p |
| 4 | **ACTION PLAN** (핵심) | **40%** | 30-60p |
| 5 | MANAGEMENT (조직+운영) | 10% | 6-12p |
| 6 | WHY US (역량+실적) | 12% | 8-15p |
| 7 | INVESTMENT & ROI | 6% | 4-8p |

**총 40~80장**

## 레이아웃 선택 가이드

| 콘텐츠 유형 | 권장 함수 |
|------------|----------|
| 시장 환경/배경 분석 | `COLS()` |
| 핵심 인사이트/메시지 | `HIGHLIGHT()` |
| 전략 프레임워크 | `PYRAMID()` |
| 채널/항목 비교 | `COMPARE()` |
| 실행 프로세스 | `FLOW()` |
| KPI/성과 목표 | `KPIS()` |
| 월별 일정 | `GANTT_CHART()` |
| 조직도 | `ORG()` |
| 수행 실적 | `GRID()` |
| 데이터 비교 | `TABLE()` |
| 통계/수치 강조 | `STAT_ROW()` |
| 타임라인 | `TIMELINE()` |
| 차별화 포인트 | `ICON_CARDS()` |
| 매트릭스 | `MATRIX()` |
| 인용문 | `QUOTE()` |
| 예산/비율 | `PIE_CHART()` / `BAR_CHART()` |
| 추세/성장 | `LINE_CHART()` |
| 고급 카드 | `CARD()` |

## PPTX 겹침/공백 방지

- HIGHLIGHT→0.75", COLS→0.30", MT→0.20" 간격
- MT 높이: 3줄=1.1", 4줄=1.4", 5줄=1.7", 6줄=2.0"
- 44pt 제목: 최대 18자, 초과 시 2줄 분리
- 하단 공백 > 0.5" → IMG_PH 또는 HIGHLIGHT
- 배경색 ≠ 카드 색상

## Phase 3 필수 컨셉 장표 (3종)

1. **Concept Reveal** — 다크 배경, 60pt 대형 컨셉 키워드, 4단계 순환 카드
2. **Strategy Synergy Map** — 3대 Win Theme 연결 구조
3. **Big Idea Reveal** — 36pt 중앙 컨셉 + 3-Step 카드

## 금지 사항

- ❌ RGBColor/HEX 하드코딩 → `C["primary"]` 사용
- ❌ 폰트명 직접 입력 → `FONT` 상수 사용
- ❌ 맑은 고딕 등 다른 폰트 → Pretendard만
- ❌ 헬퍼 함수 재정의
- ❌ Topic Title → Action Title
- ❌ OOO/XXX 플레이스홀더 → `[대괄호]` 형식
