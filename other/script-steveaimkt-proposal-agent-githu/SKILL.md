---
name: script
description: "제안서 스크립트 작성 스킬 (v5.0 SPARK-6). RFP 분석 + 리서치 결과를 바탕으로 전체 제안서의 슬라이드별 텍스트 스크립트(proposal_script.md)를 작성합니다. SPARK-6 프레임워크, Win Theme, Action Title, S-E-P 설득 구조, KPI 산출근거, 시각 의도, 20종 패턴 라이브러리를 포함합니다. 트리거: 스크립트 작성, 콘텐츠 기획, Win Theme, Action Title, S-E-P, KPI, SPARK-6, Part, 제안서 설계, 전략 수립, proposal_script"
---

# 제안서 스크립트 작성 스킬 (v5.0 SPARK-6)

RFP 분석 + 리서치 결과를 바탕으로 **전체 제안서의 슬라이드별 텍스트 스크립트**를 작성합니다.
Gemini가 디자인하기 전, 콘텐츠 품질을 검토할 수 있는 중간 산출물(`proposal_script.md`)을 생성합니다.

---

## 산출물

**파일**: `output/테스트 XX/proposal_script.md`

**입력**:
- `output/테스트 XX/rfp_analysis.md` (Analyst 산출물)
- `output/테스트 XX/research_brief.md` (Researcher 산출물, 있는 경우)

**목적**: 사용자가 제안서 전체 내용을 검토/수정하고, Converter가 JSON으로 변환하여 Gemini에 전달

---

## SPARK-6 프레임워크

Impact-8(맥킨지 방식) 대신 **SPARK-6** 6-Part 구조를 사용합니다.

```
Part 1: SPARK (점화)           4-8p (8%)   → 호기심
Part 2: PROBLEM→OPPORTUNITY    8-12p (15%) → 공감
Part 3: SOLUTION (핵심 전략)    8-15p (15%) → 확신
Part 4: EXECUTION (실행 계획)  25-50p (35%) → 납득
Part 5: PROOF (증명)           8-15p (17%) → 신뢰
Part 6: RETURN (투자 효과)      4-8p (10%)  → 행동
```

### 평가위원 감정 동선

```
Part 1 SPARK     → "어, 이건 좀 다르네?" (호기심)
Part 2 PROBLEM   → "우리 상황을 정확히 이해하고 있구나" (공감)
Part 3 SOLUTION  → "이 전략이라면 가능하겠다" (확신)
Part 4 EXECUTION → "구체적으로 이렇게 하는구나" (납득)
Part 5 PROOF     → "이 팀이라면 정말 해낼 수 있겠다" (신뢰)
Part 6 RETURN    → "이 가격이면 충분히 가치 있다" (행동)
```

### 각 Part 상세

**Part 1: SPARK (점화)** — 4-8p (8%)
- 표지 + Killer Stat + 목차 + Win Theme 소개
- 30초 안에 "이 제안서는 다르다" 각인
- 핵심 데이터 한 방 (Killer Stat) + 비전 선언

**Part 2: PROBLEM → OPPORTUNITY** — 8-12p (15%)
- 시장 환경 + 타겟 분석 + 핵심 과제 도출
- 문제를 문제로 두지 않고 "기회"로 재정의
- 발주처의 상황을 정확히 이해하고 있음을 증명

**Part 3: SOLUTION (핵심 전략)** — 8-15p (15%)
- 컨셉 공개 + 전략 프레임워크 + Win Theme 시너지
- "왜 이 전략이어야 하는가"에 대한 명확한 답
- 필수 장표: Concept Reveal + Strategy Framework (2종)

**Part 4: EXECUTION (실행 계획)** — 25-50p (35%)
- 채널별/월별/항목별 상세 실행 계획
- 콘텐츠 예시, 캠페인 기획, 이벤트, 일정표
- 가장 많은 분량, 구체성이 생명

**Part 5: PROOF (증명)** — 8-15p (17%)
- WHO(팀) + HOW(운영 체계) + TRACK RECORD(실적) 통합
- 조직도, 인력, 보고 체계, 리스크 관리
- 유사 수행실적, 핵심 역량, 차별화 포인트

**Part 6: RETURN (투자 효과)** — 4-8p (10%)
- 예산 구조 + KPI + ROI + Next Step + Closing
- "이 투자는 이만큼 돌아옵니다" + Call to Action

### 프로젝트 유형별 가중치

| Part | Marketing/PR | Event | IT/System | Public | Consulting |
|------|-------------|-------|-----------|--------|------------|
| 1 SPARK | 8% | 6% | 5% | 5% | 6% |
| 2 PROBLEM→OPP | 15% | 10% | 15% | 18% | 18% |
| 3 SOLUTION | 15% | 12% | 15% | 12% | 18% |
| 4 EXECUTION | **35%** | **45%** | **35%** | 30% | 25% |
| 5 PROOF | 17% | 17% | 20% | 22% | 20% |
| 6 RETURN | 10% | 10% | 10% | 13% | 13% |

---

## proposal_script.md 포맷

```markdown
# [프로젝트명] 제안서 스크립트
> 발주처: [발주처명] | 유형: marketing_pr | 예산: X억원 | 기간: YYYY.MM ~ YYYY.MM

---

## 전략 요약

### Win Themes (3대 수주 전략)
| # | Win Theme | Pain Point | 우리의 해법 |
|---|-----------|-----------|-----------|
| W1 | [키워드형 전략명] | [PP1 요약] | [솔루션 1줄] |
| W2 | [키워드형 전략명] | [PP2 요약] | [솔루션 1줄] |
| W3 | [키워드형 전략명] | [PP3 요약] | [솔루션 1줄] |

### 핵심 KPI
| KPI | 목표 | 산출근거 | 데이터 출처 |
|-----|------|---------|-----------|
| [지표명] | [수치] | [계산식] | [출처 URL/기관명] |

### 컨셉
> "[한 줄 컨셉 — 슬로건형]"

---

## Part 1: SPARK (N장)

### S01. 표지
- **유형**: cover
- **내용**: [프로젝트명] / [발주처명]

### S02. Killer Stat
- **Action Title**: "국내 공공배달 시장 점유율 3%, 97%의 빈 공간이 기회다"
- **의도**: 첫 장에서 '숫자 하나'를 기억하게 만든다
- **내용**:
  - Story: 배달앱 시장 30조원 시대, 공공배달은 아직 3% 미만
  - Evidence: 통계청 2025 배달앱 시장 보고서 (출처)
  - Promise: 이 97%를 채울 전략을 제안합니다
- **시각 의도**: 대형 숫자 "3%" 중앙 배치, 주변에 컨텍스트 데이터 3개
- **분위기**: dark, 임팩트
- **Win Theme**: W1

### S03. 목차
- **유형**: toc
- **내용**: Part 1~6 목차

### S04. Win Theme 소개
- **Action Title**: "3대 전략으로 서울배달+ 이용자 200% 성장 달성"
- **의도**: 전체 전략의 방향을 30초 안에 전달
- **내용**:
  - Story: 3가지 핵심 전략으로 서울배달+ 성장을 이끈다
  - Evidence: 각 Win Theme별 핵심 데이터 1개씩
  - Promise: 이 3대 전략의 시너지로 목표 달성
- **시각 의도**: 3열 카드 (아이콘 + 제목 + 본문 3줄)
- **분위기**: white, 깔끔한
- **Win Theme**: all
- **Bridge**: "이 전략이 왜 필요한지, 시장 환경부터 살펴보겠습니다"

---

## Part 2: PROBLEM → OPPORTUNITY (N장)

### S05. 섹션 전환
- **유형**: section_divider
- **Part**: 02 PROBLEM → OPPORTUNITY
- **부제**: 시장 환경과 기회 분석
- **Win Theme**: W1
- **Bridge**: "기회를 잡기 위해, 시장이 어떤 변화를 겪고 있는지 살펴보겠습니다"

### S06. 시장 환경 분석
- **Action Title**: "배달앱 MAU 2,800만 시대, 소비자 행동이 바뀌고 있다"
- **의도**: 시장 전체 맥락을 3가지 핵심 수치로 압축
- **내용**:
  - Story: 배달앱이 일상 인프라가 된 지금, 소비자는 '가격'이 아닌 '가치'로 선택
  - Evidence: MAU 2,800만(앱 리서치), 가치소비 검색량 +180%(네이버 트렌드)
  - Promise: 가치소비 트렌드가 공공배달의 핵심 성장 동력
- **시각 의도**: 3개 핵심 수치 카드 상단 + 트렌드 라인 차트 하단
- **분위기**: white, 데이터 중심
- **Win Theme**: W1
- **리서치 참조**: 시장 환경 #1

... (나머지 Part 3~6 동일 패턴) ...

---

## 요약 통계

| Part | 장수 | 비중 |
|------|------|------|
| 1 SPARK | 4 | 7% |
| 2 PROBLEM→OPP | 8 | 15% |
| 3 SOLUTION | 8 | 15% |
| 4 EXECUTION | 20 | 36% |
| 5 PROOF | 10 | 18% |
| 6 RETURN | 5 | 9% |
| **합계** | **55** | **100%** |
```

---

## 슬라이드 블록 필드 정의

### 특수 슬라이드 (cover, toc, section_divider)

```markdown
### S번호. 제목
- **유형**: cover / toc / section_divider
- **내용**: ...
- **Win Theme**: WN (section_divider만)
- **Bridge**: 전환 문장 (section_divider만)
```

### 일반 콘텐츠 슬라이드

**필수 필드:**
```markdown
### S번호. 슬라이드 주제 — 부제
- **Action Title**: "인사이트 + 데이터 기반 문장"
- **의도**: 이 슬라이드가 평가위원에게 전달하는 핵심 목적 (1문장)
- **내용**:
  - Story: 상황/맥락 서술 (공감 유도)
  - Evidence: 데이터/사례/근거 (출처 필수)
  - Promise: 약속/효과/시사점 (행동 지향)
- **시각 의도**: 레이아웃 목적 + 핵심 시각 요소 (자연어, 패턴 라이브러리 참조)
- **분위기**: dark / white / light / gradient / branded + 톤 설명
- **Win Theme**: W1 / W2 / W3 / all / —
```

**선택 필드:**
```markdown
- **Bridge**: 다음 Part 전환 문장 (Part 마지막 슬라이드만)
- **발표자 노트**: 발표 시 참고사항
- **리서치 참조**: research_brief.md 섹션 참조 (예: "시장 환경 #1")
```

**시각 자료 필드 (선택):**
```markdown
- **이미지**: [설명] | 크기: full/half/quarter/icon | 출처: [출처]
- **차트**: [유형] | 데이터: {JSON} | 단위: [단위] | 색상: primary/multi
- **출처**: [기관명], [자료명], [날짜]
```

> 시각 자료 필드의 상세 규격은 `visual-assets` 스킬을 참조하세요.

---

## S-E-P 설득 구조

C-E-I(Claim-Evidence-Impact)를 대체하는 새로운 설득 구조:

| 요소 | 역할 | 차이점 |
|------|------|--------|
| **Story** | 상황/맥락 서술 → 공감 유도 | Claim(주장)보다 자연스러운 진입 |
| **Evidence** | 데이터/사례/근거 → 신뢰 확보 | 출처 필수, 리서치 데이터 기반 |
| **Promise** | 약속/효과 → 행동 유도 | Impact(영향)보다 행동 지향적 |

### 작성 예시

```
Story:   배달앱이 일상 인프라가 된 지금, 소비자는 '가격'이 아닌 '가치'로 선택한다
Evidence: MZ세대 72% "사회적 가치가 구매 결정에 영향" (대학내일 2025)
Promise: "착한 소비" 포지셔닝으로 MZ세대 자발적 확산, 앱 설치 전환율 2배 달성
```

### 적용 규칙
- Story = Action Title과 연동 (같은 맥락)
- Evidence = 반드시 출처 명시 (URL/기관명)
- Promise = "그래서 우리는 이렇게 하겠다" 형태
- 리서치 데이터가 있으면 Evidence에 우선 활용

---

## Win Theme (수주 전략 메시지)

제안서 전체에 반복되는 **3대 핵심 수주 전략 메시지**.

### 도출 패턴
1. RFP Pain Point 3개 식별
2. 각 Pain Point에 대응하는 핵심 솔루션 매칭
3. 짧고 기억에 남는 키워드로 압축 (2~4단어)

### 스크립트 내 적용 규칙
- Part 1 마지막에 Win Theme 전체 소개
- 각 section_divider에 관련 Win Theme 태깅
- Part 3에서 Win Theme 간 시너지 시각화
- Part 5에서 Win Theme별 실적/역량 증명
- 매 슬라이드 `**Win Theme**` 필드로 태깅

### 예시
```
| # | Win Theme | Pain Point | 해법 |
| W1 | 데이터 기반 퍼널 마케팅 | 전환율 저조 | 퍼널 단계별 전환 최적화 |
| W2 | 가치소비 브랜딩 전략 | 인지도 부족 | "착한 소비" 감성 브랜딩 |
| W3 | 선순환 생태계 구축 | 가맹점 이탈 | 양면시장 동시 공략 |
```

---

## Action Title (인사이트 기반 제목)

**Topic Title → Action Title 전환 필수**

| Before (Topic Title) | After (Action Title) |
|---------------------|---------------------|
| 타겟 분석 | MZ세대 2030이 핵심, 하루 SNS 55분 사용 |
| 채널 전략 | 인스타그램 중심, 릴스로 도달률 3배 확보 |
| 시장 현황 | 배달앱 시장 30조원, 공공배달 점유율 3% 미만 |
| 예산 계획 | 총 97백만원, 콘텐츠 35% + 매체 30% 최적 배분 |

**규칙:**
- 구체적 숫자/데이터 포함 권장
- 팩트 + 인사이트 조합
- 모든 일반 콘텐츠 슬라이드에 필수
- 15~35자 권장

---

## 시각 의도 (Visual Intent)

기존 `레이아웃` 필드(함수명 기반)를 `시각 의도` 필드(자연어)로 대체합니다.

### 변경 이유
- 기존: `COLS 3열 + HIGHLIGHT` → PPTX slide_kit 함수에 종속
- 신규: `3개 핵심 수치 카드 상단 + 트렌드 차트 하단` → Gemini가 최적 디자인 결정

### 작성 방법

**패턴 라이브러리 참조 + 자연어로 기술:**

```markdown
❌ 모호한 지정:
- **시각 의도**: 시장 데이터 시각화

❌ 함수명 기반 (기존 방식):
- **레이아웃**: COLS 3열 + HIGHLIGHT | 배경: dark

✅ 자연어 의도 (신규 방식):
- **시각 의도**: 3개 핵심 수치 카드 상단 + 트렌드 라인 차트 하단 [card_grid + line_trend]

✅✅ 최고 수준:
- **시각 의도**: 대형 숫자 "3%" 중앙 배치(64pt+), 주변에 컨텍스트 데이터 카드 3개. 하단 출처 텍스트 [hero_stat]
```

### 시각 의도에 패턴 힌트 포함

`[패턴명]` 태그로 패턴 라이브러리 참조를 추가합니다:

```markdown
- **시각 의도**: 좌우 2분할, 좌측에 현재 상태/우측에 목표 상태 비교 [comparison]
- **시각 의도**: 인지→설치→주문→재구매 4단계 흐름도 + 각 단계 KPI [process_flow + data_dashboard]
```

---

## 분위기 (Mood)

기존 `배경` 필드(색상 코드)를 `분위기` 필드(톤+느낌)로 대체합니다.

### 옵션

| 분위기 | 설명 | 적용 장면 |
|--------|------|----------|
| `dark, 임팩트` | 다크 배경, 강렬한 인상 | 표지, 컨셉 공개, Killer Stat |
| `white, 깔끔한` | 순백 배경, 정돈된 느낌 | 일반 콘텐츠, 분석 |
| `white, 데이터 중심` | 순백 + 차트/수치 강조 | 시장 분석, KPI |
| `light, 부드러운` | 밝은 회색, 변주 | 서브 콘텐츠, 사례 |
| `gradient, 프리미엄` | 미세 그라디언트 | 전략, 역량 강조 |
| `branded, 포인트` | 브랜드 색조 활용 | Win Theme 강조, 차별화 |

### 분위기 배분 규칙
- white 계열 55~60%, light 15~20%, dark 10~15%, gradient/branded 10~15%
- white 5장 연속 금지
- 모든 section_divider = dark
- Part 3 Concept Reveal = dark

---

## 패턴 라이브러리 (20종)

시각 의도 작성 시 참조하는 도식화 패턴 사전입니다.

| # | 패턴명 | 설명 | 적용 장면 |
|---|--------|------|----------|
| 1 | **hero_stat** | 대형 숫자(48-64pt) 중앙 + 주변 데이터 카드 | Killer Stat, KPI 강조, 핵심 수치 |
| 2 | **card_grid** | 2-4열 카드 그리드 (일관된 스타일) | 전략 요약, 채널 비교, 역량 소개 |
| 3 | **bento_grid** | 비대칭 모듈 그리드 (대형+소형 혼합) | 실행 계획 총괄, 다양한 정보 집약 |
| 4 | **comparison** | 좌우 2분할 (AS-IS/TO-BE) | 경쟁사 비교, 현재/목표, Before/After |
| 5 | **process_flow** | 3-5단계 수평 흐름도 | 퍼널, 워크플로우, 프로세스 |
| 6 | **funnel** | 상→하 깔때기형 축소 | 마케팅 퍼널, 전환 단계 |
| 7 | **pyramid** | 계층적 삼각형 구조 | 전략 계층, 메시지 피라미드 |
| 8 | **concept_reveal** | 다크 배경 + 대형 키워드(56pt+) + 보조 카드 | 컨셉 공개, Big Idea |
| 9 | **data_dashboard** | KPI 카드 + 차트 + 인사이트 텍스트 | 성과 요약, 효과 분석, ROI |
| 10 | **timeline** | 수평 타임라인 + 마일스톤 카드 | 로드맵, 일정, 연혁 |
| 11 | **gantt** | 월별/주별 간트 차트 | 실행 일정, 프로젝트 계획 |
| 12 | **org_chart** | 계층형 조직도 | 팀 구성, 역할 분담 |
| 13 | **table_insight** | 테이블 + 인사이트 하이라이트 | 비용 산출, 항목 비교, 평가 매트릭스 |
| 14 | **split_visual** | 좌 60% 텍스트 + 우 40% 이미지/차트 | 사례 소개, 캠페인 설명 |
| 15 | **quote_highlight** | 핵심 인용문/메시지 중앙 대형 표시 | 비전 선언, 슬로건, 핵심 메시지 |
| 16 | **matrix_quadrant** | 2×2 매트릭스 (우선순위/포지셔닝) | 전략 매트릭스, 리스크 맵 |
| 17 | **waterfall** | 누적 증감 차트 | 예산 변동, KPI 기여도 분해 |
| 18 | **radar_profile** | 방사형 역량 비교 차트 | 역량 비교, 다차원 평가 |
| 19 | **gallery** | 2×3 또는 3×2 이미지/사례 그리드 | 수행 실적, 포트폴리오 |
| 20 | **icon_feature** | 아이콘 + 제목 + 설명의 3-4열 | 차별화 포인트, 서비스 특징 |

### 추가 차트 타입 (시각 의도에서 활용)

| 타입 | 설명 | 적용 |
|------|------|------|
| bar_chart | 세로/가로 막대 차트 | 점유율, 수치 비교 |
| pie_donut | 파이/도넛 차트 | 예산 비율, 구성 비율 |
| line_trend | 라인/면적 차트 | 트렌드, 성장 추이 |
| bubble | 버블 차트 (3차원 비교) | 시장 포지셔닝 |
| sankey | 플로우 다이어그램 | 예산 흐름, 전환 경로 |
| heatmap | 히트맵 | 시간대별 활동, 우선순위 |

### 콘텐츠별 패턴 추천

| 콘텐츠 유형 | 권장 패턴 |
|------------|----------|
| 시장 환경/분석 | card_grid / data_dashboard / split_visual |
| 핵심 인사이트 | hero_stat / quote_highlight |
| 전략 프레임워크 | pyramid / process_flow / concept_reveal |
| 채널/항목 비교 | comparison / table_insight |
| 실행 프로세스 | process_flow / funnel / timeline |
| KPI/성과 목표 | data_dashboard / hero_stat |
| 월별 일정 | gantt / timeline |
| 조직도/팀 구성 | org_chart |
| 수행 실적 | gallery / card_grid |
| 데이터 비교 | table_insight / comparison |
| 예산/비율 | pie_donut + table_insight / waterfall |
| 차별화 포인트 | icon_feature / card_grid |
| 리스크 관리 | matrix_quadrant / table_insight |
| 컨셉 공개 | concept_reveal |
| 비전/메시지 | quote_highlight |

---

## Part 3 필수 장표 (2종)

### 1. Concept Reveal
- **분위기**: dark, 임팩트
- **시각 의도**: 대형 컨셉 키워드(56pt+) 중앙 배치 + 하단에 4단계 순환 카드 [concept_reveal]
- **필수 요소**: 핵심 컨셉 1줄 + 4단계 또는 3요소 분해

### 2. Strategy Framework
- **분위기**: white 또는 light
- **시각 의도**: Win Theme 3개의 연결 구조 + 시너지 메시지 [process_flow]
- **필수 요소**: W1-W2-W3 연결 흐름 + 통합 메시지
- **Bridge**: Part 4 연결 문장 포함

---

## Bridge 문장

각 Part 마지막 슬라이드에 Bridge 필드로 다음 Part 전환:

```
Part 1 → 2: "이 전략이 왜 필요한지, 시장 환경부터 살펴보겠습니다"
Part 2 → 3: "이 과제들에 대한 해답을 전략 컨셉에서 제시합니다"
Part 3 → 4: "이 전략을 구현할 구체적 실행 계획입니다"
Part 4 → 5: "이 계획을 실현할 팀과 운영 체계입니다"
Part 5 → 6: "이 역량으로 만들어낼 투자 효과입니다"
```

---

## KPI + 산출근거

| KPI | 목표 | 산출근거 | 데이터 출처 |
|-----|------|---------|-----------|
| 앱 다운로드 | +15만 건 | 월 1.5만 × 10개월 | 유사 공공앱 캠페인 평균 |
| 인지도 | 60→80% | 매체(+10%p)+SNS(+5%p)+이벤트(+5%p) | 서울시 정책인지도 조사 |

**규칙:**
- 리서치 데이터가 있으면 산출근거에 우선 반영
- 출처 URL 또는 기관명 필수
- Part 1 SPARK에서 KPI 미리보기
- Part 6 RETURN에서 KPI 상세 + ROI

---

## Placeholder 표준

```
✅ [발주처명], [프로젝트명], [담당자 연락처]
❌ OOO, XXX, ___, ○○○
```

---

## 스크립트 작성 프로세스

1. **RFP 분석 + 리서치 결과 확인**: rfp_analysis.md + research_brief.md 읽기
2. **Win Theme 도출**: Pain Point 3개 → 솔루션 → 키워드
3. **KPI 설계**: 목표값 + 산출근거 (리서치 데이터 기반)
4. **Part별 슬라이드 설계**: 유형별 가중치에 따라 장수 배분
5. **슬라이드별 블록 작성**: Action Title → S-E-P → 시각 의도 → 분위기
6. **Bridge 문장 삽입**: Part 전환점에 배치
7. **분위기 리듬 검증**: Dark-Light 교차 확인
8. **요약 통계 작성**: Part별 장수/비중 테이블

---

## 스크립트 검토 체크리스트

**콘텐츠 품질:**
- [ ] Win Theme 3개가 RFP Pain Point에 명확히 대응하는가
- [ ] 모든 Action Title이 인사이트+팩트 기반인가 (Topic Title 금지)
- [ ] 모든 콘텐츠 슬라이드에 S-E-P 구조가 적용되었는가
- [ ] Evidence에 출처가 포함되었는가
- [ ] Part별 비중이 프로젝트 유형 가중치에 부합하는가
- [ ] Part 3에 필수 장표 2종(Concept Reveal + Strategy Framework)이 있는가
- [ ] Bridge 문장이 모든 Part 전환점에 있는가
- [ ] KPI에 산출근거 + 출처가 포함되었는가
- [ ] Placeholder가 [대괄호] 표준을 따르는가

**시각 품질:**
- [ ] 시각 의도가 자연어로 명확히 기술되었는가 (모호한 "데이터 시각화" 금지)
- [ ] 패턴 라이브러리 태그 [패턴명]가 적절히 포함되었는가
- [ ] 분위기 리듬: white 5장 연속 없음
- [ ] 패턴 다양성: 10종 이상 패턴 사용 (card_grid만 반복 금지)
- [ ] Part 3 컨셉 슬라이드에 dark + concept_reveal 지정
