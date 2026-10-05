---
name: generate
description: "PM (총괄) 오케스트레이터 v9.0. 제안서 팀을 이끌어 8-Step 파이프라인을 실행합니다. 입찰 제안서(RFP) + 마케팅 제안서 + 캠페인 브레인스토밍 지원. Step 0 출력 형식 분기 + 4개 병렬 리서치 + 7개 전문 QA. 트리거: 제안서 생성, 제안서 제작, /p, /start, /pf, generate, 스크립트 작성"
---

# PM 오케스트레이터 v9.0

제안서 팀을 이끌어 **8-Step 파이프라인**을 순차 실행합니다.
모든 단계에서 **체크리스트 검증 → 사용자 컨펌 → 다음 단계** 구조.

---

## 제안서 유형

| 유형 | 입력 | 분석 대상 | 출력 |
|------|------|---------|------|
| **입찰 제안서** | `제안요청서/테스트 XX/*.pdf` | RFP (제안요청서) | `rfp_analysis.md` |
| **마케팅 제안서** | `제안요청서/테스트 XX/*.pdf` 또는 구두 브리핑 | 마케팅 플랜 | `mkt_analysis.md` |
| **캠페인 제안서** | `/brainstorm` → `campaign_brief.md` | 캠페인 브리프 | Step 1-2 건너뜀 |

`/start 테스트 XX` 실행 시 유형 선택 → 이후 파이프라인 공통.
`campaign_brief.md` 감지 시 → Step 3(스크립트)부터 시작.

---

## 제안서 팀 구성

```
┌─────────────────────────────────────────────┐
│            PM / 오케스트레이터               │
│  · 단계 관리 · 체크리스트 · 컨펌 관리       │
└──────────────────┬──────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
 분석팀         기획팀         제작팀
 ┌────────┐   ┌────────┐   ┌────────┐
 │Analyst │   │Planner │   │Convert │
 │Research│   │(script)│   │Designer│
 └────────┘   └────────┘   └────────┘
                   │
              ┌────┴────┐
              ▼         ▼
           디자인팀   검수팀
           ┌──────┐  ┌────┐
           │D.Anal│  │ QC │
           │Visual│  └────┘
           └──────┘
```

| 팀 | 역할 | 스킬/에이전트 |
|----|------|-------------|
| **분석팀** | RFP/마케팅 플랜 분석 | `analyst` |
| **리서치팀** | 4개 병렬 리서치 (시장/경쟁/타겟/BP·KPI) | `research` (4개 도메인 병렬) |
| **기획팀** | SPARK-6 스크립트 기획, Win Theme, S-E-P | `script` |
| **디자인팀** | 디자인 레퍼런스 분석, 도식화 전략 | `design-analyzer`, `visualizer` |
| **제작팀** | JSON 변환, HTML 렌더링 / PPTX 생성 | `convert`, HTML renderer / `designer` |
| **검수팀** | 7개 전문 QA × 2라운드 | `qc` (layout/shape/diagram/typo/color/content/interaction) |
| **브레인스토밍팀** | 캠페인 전략+크리에이티브+데이터 | `brainstorm` (3인 에이전트) |

---

## 8-Step 파이프라인

### Step 0: 출력 형식 선택

**담당**: PM

**업무 리스트**:
1. 사용자에게 출력 형식 선택 요청 — AskUserQuestion
   - **A) HTML→Figma** (40종 레이아웃, 정밀 디자인, Figma 변환 가능)
   - **B) PPTX** (slide_kit.py 사용, 빠른 생성, PowerPoint 직접 편집 가능)
2. 선택 결과를 이후 Step 5-6에서 분기 적용

**산출물**: 출력 형식 결정 (HTML 또는 PPTX)

---

### Step 1: 킥오프 & 분석

**담당**: PM + Analyst (분석팀)

**업무 리스트**:
1. 제안서 유형 선택 (입찰/마케팅) — AskUserQuestion
2. 입력 폴더 확인 및 파일 목록 제시
3. (입찰) `analyst` 스킬로 RFP PDF 분석 → `rfp_analysis.md`
4. (마케팅) `analyst` 스킬 마케팅 모드로 PDF 분석 또는 사용자 브리핑 수집 → `mkt_analysis.md`

**체크리스트**:
```
[ ] 프로젝트명 / 발주처(클라이언트) 추출
[ ] 과업 범위 완전성 (주요 업무 항목 모두 포함)
[ ] (입찰) 평가 기준 배점표 정확성
[ ] (마케팅) 마케팅 목표 + 타겟 정의
[ ] Pain Point 3개 근거 기반 식별
[ ] 프로젝트 유형 판별 (marketing_pr / event / it_system / public / consulting)
[ ] 예산, 일정 추출
```

**확인 사항** (사용자에게 제시):
- 분석 결과 요약 (프로젝트 개요, Pain Point 3개, 프로젝트 유형)
- 체크리스트 달성 현황
- "분석 결과를 확인해주세요. 수정할 사항이 있으면 말씀해주세요."

**요청 사항**:
- (마케팅, PDF 없을 때) 목표, 타겟, 예산, 기존 채널, KPI 직접 입력 요청
- 추가 참고 자료 여부

**산출물**: `output/테스트 XX/rfp_analysis.md` 또는 `mkt_analysis.md`

---

### Step 2: 병렬 리서치

**담당**: 리서치팀 (4개 병렬 에이전트)

**업무 리스트**:
1. `research` 스킬을 **4개 병렬 Agent**로 실행:
   - **시장환경 리서처**: 시장 규모, 성장률, 점유율, 산업 트렌드, 규제 환경
   - **경쟁/벤치마킹 리서처**: 경쟁사 캠페인 분석, 유사 프로젝트 사례, 해외 벤치마크
   - **타겟 인사이트 리서처**: 타겟 이용행태, 소비 트렌드, 전환 장벽, 미디어 소비 패턴
   - **BP·KPI 리서처**: 성공 사례, KPI 벤치마크 (CTR/CPA/전환율), 예산 대비 성과
2. PM이 4개 결과를 `research_brief.md`로 통합
3. Evidence용 데이터 수집 (출처 필수)
4. WebSearch + WebFetch 활용, 각 리서처 최대 8회 검색

**체크리스트**:
```
[ ] 5대 영역 각각 최소 2개 이상 데이터 포인트
[ ] 모든 데이터에 출처 포함 (기관명/URL/연도)
[ ] 경쟁사/벤치마킹 사례 3건 이상
[ ] KPI 벤치마크 수치 포함 (전환율, ROI, 도달률 등)
[ ] 데이터 신뢰성 — 최근 2년 이내 자료
```

**확인 사항**:
- 리서치 요약 (영역별 핵심 발견)
- 체크리스트 달성 현황
- "리서치 결과를 확인해주세요. 추가 리서치가 필요한 영역이 있으면 말씀해주세요."

**요청 사항**:
- 추가 리서치 방향, 특정 경쟁사 지정 여부
- 내부 자료/데이터 공유 여부

**산출물**: `output/테스트 XX/research_brief.md`

---

### Step 3: 콘텐츠 기획 (★ 핵심 승인 단계)

**담당**: Planner (기획팀, `script` 스킬)

**업무 리스트**:
1. SPARK-6 구조로 `proposal_script.md` 작성
2. Win Theme 3개 도출 (Pain Point 대응)
3. S-E-P 설득 구조 적용 (모든 콘텐츠 슬라이드)
4. Action Title (인사이트+팩트 기반, 15~35자)
5. KPI + 산출근거 (리서치 데이터 기반), Bridge 문장
6. 시각 의도 + 패턴 힌트 + 분위기

**체크리스트**:
```
[ ] SPARK-6 6-Part 구조 완성
[ ] Part별 비중이 프로젝트 유형 가중치에 부합
[ ] Win Theme 3개 → Pain Point 정확 대응
[ ] 모든 콘텐츠 슬라이드에 S-E-P 존재
[ ] Evidence에 출처 포함 (리서치 데이터 활용)
[ ] Action Title: Topic Title 아닌 인사이트 기반 (15~35자)
[ ] Part 3 필수 장표: Concept Reveal + Strategy Framework (2종)
[ ] Bridge 문장: 모든 Part 전환점(5개)에 존재
[ ] KPI 산출근거 + 출처 포함
[ ] 패턴 다양성: 10종 이상 패턴 사용
[ ] 분위기 리듬: white 5장 연속 금지, dark/light 교차
[ ] 총 슬라이드 수: 목표 분량 범위 내 (40~80장)
[ ] Placeholder: [대괄호] 표준 사용
```

**확인 사항** (★ 반드시 사용자 승인 필요):
- 스크립트 전체 요약:
  - 목차 (Part별 슬라이드 수)
  - Win Theme 3개 + 대응 Pain Point
  - 총 슬라이드 수
  - 핵심 KPI 목록
- 체크리스트 전체 달성 현황
- "★ 스크립트 기획안을 승인해주세요. 수정/추가/삭제할 내용이 있으면 슬라이드 번호(S01~)로 알려주세요."

**요청 사항**:
- 수정 사항 (슬라이드별 피드백)
- 추가/삭제할 슬라이드
- 강조하고 싶은 영역

**피드백 루프**: 사용자가 "승인" / "진행해" → Step 4로 이동. 수정 요청 시 반영 후 재확인.

**산출물**: `output/테스트 XX/proposal_script.md`

---

### Step 4: 디자인 전략

**담당**: 디자인팀 (`design-analyzer` + `visualizer` 스킬)

**업무 리스트**:
1. **(4a)** `디자인 레퍼런스/` 폴더 확인
   - 파일 있으면: `design-analyzer` 스킬로 분석 → `design_analysis.md`
   - 비어있으면: 기본 디자인 시스템(design-style.md) 기반 기본값 생성
2. **(4b)** `visualizer` 스킬로 슬라이드별 도식화 전략 수립 → `visualization_strategy.md`
   - 텍스트 패턴 감지 → 40종 레이아웃 중 최적 선택
   - 텍스트:도식 비율 결정
   - Mermaid/차트 코드 생성

**체크리스트**:
```
[ ] (레퍼런스 있으면) design_analysis.md 생성
[ ] 컬러 팔레트: Primary, Secondary 최소 2색 추출
[ ] 레이아웃 패턴: 빈도순 3개 이상 분석
[ ] visualization_strategy.md 생성
[ ] 전체 슬라이드의 70% 이상에 권장 layout 지정
[ ] 레이아웃 다양성: 10종 이상 서로 다른 layout 사용
[ ] title_body 남용 방지: 전체의 30% 이하
[ ] 분위기 리듬: Dark/White 교대 패턴 유지
```

**확인 사항**:
- 디자인 분석 요약 (컬러, 레이아웃 패턴, 분위기)
- 도식화 전략 요약 (변경 슬라이드 목록, 레이아웃 분포 차트)
- 체크리스트 달성 현황
- "디자인 전략을 확인해주세요. 선호하는 스타일이나 변경할 레이아웃이 있으면 말씀해주세요."

**요청 사항**:
- 디자인 선호도 (컬러, 톤, 스타일)
- 특정 슬라이드의 레이아웃 변경 요청

**산출물**: `output/테스트 XX/design_analysis.md` + `visualization_strategy.md`

---

### Step 5: 제작

**담당**: 제작팀 (`convert` 스킬 + HTML 렌더러)

**업무 리스트**:
1. `convert` 스킬로 JSON v2.0 변환
   ```bash
   python3 src/converters/script_to_json.py "output/테스트 XX/proposal_script.md" \
       --viz-strategy "output/테스트 XX/visualization_strategy.md" \
       --design-analysis "output/테스트 XX/design_analysis.md"
   ```
2. HTML 슬라이드 렌더링
   ```bash
   python3 src/generators/html_slide_renderer.py "output/테스트 XX/proposal_slides.json" \
       --output-dir "output/테스트 XX/"
   ```
3. preview.html 열어서 결과 확인

**체크리스트**:
```
[ ] JSON 슬라이드 수 = 스크립트 슬라이드 수
[ ] Win Theme 3개 정확히 파싱
[ ] S-E-P 구조 올바르게 분리 (story/evidence[]/promise)
[ ] Evidence 출처 분리 (text + source)
[ ] design_intent 채움률 80% 이상 (layout_hint, focal_point)
[ ] 도식화 전략 반영 (layout_hint 매칭)
[ ] Bridge 보존 (누락 없음)
[ ] HTML 렌더링: 슬라이드 수 일치
[ ] 텍스트 보존: Action Title, S-E-P 내용 포함
[ ] 레이아웃 적용: design_intent 반영
[ ] 16:9 비율 (1920×1080) 유지
[ ] Pretendard 폰트 적용
```

**확인 사항**:
- preview.html 열기
- JSON 검증 결과 (슬라이드 수, Win Theme, KPI 수)
- 체크리스트 달성 현황
- "제작 결과물을 확인해주세요. 수정할 슬라이드 번호가 있으면 말씀해주세요."

**요청 사항**:
- 수정할 슬라이드 번호, 디자인 피드백
- Figma 변환 여부 (/pf 모드)

**산출물**: `output/테스트 XX/proposal_slides.json` + `slides/` + `preview.html`

---

### Step 6: 검수 (7개 전문 QA × 2라운드)

**담당**: 검수팀 (`qc` 스킬 — 7개 전문 영역)

**업무 리스트**:
1. **Round 1**: 7개 전문 QA 에이전트 병렬 실행
   - `qa-layout`: 그리드, 정렬, 여백, 크기, 요소 겹침
   - `qa-shape`: 카드 border-radius, box-shadow, 프로세스 화살표
   - `qa-diagram`: 차트 데이터 정합성, 도식 렌더링
   - `qa-typography`: 폰트 위계, 최소 크기, line-height
   - `qa-color`: CSS 변수 일관성, WCAG AA 대비율, dark/light 리듬
   - `qa-content`: Action Title, S-E-P, Win Theme 출현, 오탈자
   - `qa-interaction`: 네비게이션, 다운로드, 인쇄, JS 에러
2. **Round 2**: Critical 수정 후 재검수 + 새 이슈 탐지
3. Stage 1: 스크립트 콘텐츠 검수 (SPARK-6, S-E-P, Win Theme)
4. Stage 2: JSON 변환 정확성 검증
5. CRITICAL / WARNING / INFO 분류 리포트

**체크리스트**: `qc` 스킬의 전체 체크리스트 자동 실행

**확인 사항**:
- QC 검수 리포트 제시
- CRITICAL/WARNING/INFO 건수 요약
- "검수 결과를 확인해주세요. CRITICAL 이슈는 즉시 수정됩니다. WARNING 항목 중 수정할 사항을 알려주세요."

**요청 사항**:
- 수정 범위 결정 (콘텐츠/도식/디자인/전체/수정 불필요)

**산출물**: QC 검수 리포트

---

### Step 7: 수정 & 최종 납품

**담당**: PM (해당 팀에 수정 배분)

**업무 리스트**:
1. CRITICAL 이슈 자동 수정
2. 콘텐츠 문제 → Planner 재실행 (script 스킬)
3. 도식화 문제 → Visualizer 재실행 (visualizer 스킬)
4. 변환 문제 → Converter 재변환 (convert 스킬)
5. 디자인 문제 → HTML 재렌더링
6. 수정 후 재검수 (필요 시)
7. 최종 결과물 열기

**체크리스트**:
```
[ ] CRITICAL 0건
[ ] WARNING: 해결 완료 또는 사용자 승인
[ ] 최종 preview.html 확인
[ ] 산출물 전체 목록 제시
```

**확인 사항**:
- 수정 완료 내역
- 최종 산출물 목록 + 열기
- "최종 결과물을 확인해주세요. 추가 수정이 필요하면 말씀해주세요. 완료라면 '완료'라고 말씀해주세요."

**산출물**: 최종 `proposal.html` (또는 Figma/PPTX)

---

## 스마트 시작 (기존 산출물 감지)

기존 산출물이 있으면 해당 Step부터 시작:

| 감지 파일 | 시작 Step |
|----------|----------|
| `campaign_brief.md` 있음 | Step 3 (스크립트, 리서치 건너뜀) |
| `proposal_slides.json` 있음 | Step 5 (HTML 렌더링만) |
| `visualization_strategy.md` 있음 | Step 5 (JSON 변환부터) |
| `proposal_script.md` 있음 | Step 4 (디자인 전략부터) |
| `rfp_analysis.md` 또는 `mkt_analysis.md` 있음 | Step 2 (리서치부터) |
| 아무것도 없음 | Step 0 (전체 실행) |

---

## 커맨드별 동작

| 커맨드 | 동작 |
|--------|------|
| `/start 테스트 XX` | 유형 선택 → Step 1~7 전체 |
| `/p 테스트 XX` | 입찰 모드 기본, 스마트 시작 |
| `/pf 테스트 XX` | HTML→Figma 모드, 스마트 시작 |
| `/research 테스트 XX` | Step 2만 |
| `/convert 테스트 XX` | Step 5만 (JSON+HTML) |
| `/r 테스트 XX` | Step 6만 (QC 검수) |
| `/e 테스트 XX` | proposal_script.md 편집 |
| `/open 테스트 XX` | 결과물 열기 |

---

## 컨펌 요청 포맷 (통일)

각 Step 완료 시 아래 포맷으로 사용자에게 제시:

```
═══ Step N 완료: [Step 이름] ═══

📋 업무 완료 내역:
- [완료된 작업 1]
- [완료된 작업 2]

✅ 체크리스트:
[x] 항목 1 — 달성
[x] 항목 2 — 달성
[ ] 항목 3 — 미달성 (사유)

📊 핵심 결과:
- [핵심 수치/결과 1]
- [핵심 수치/결과 2]

🔍 확인 사항:
- [사용자가 검토할 사항]

💬 요청 사항:
- [사용자에게 요청할 사항]

→ 다음 단계: Step N+1 [Step 이름]
→ 진행하시겠습니까?
```

---

## 산출물 구조

```
output/테스트 XX/
├── rfp_analysis.md              ← Step 1 (입찰)
├── mkt_analysis.md              ← Step 1 (마케팅)
├── research_brief.md            ← Step 2
├── proposal_script.md           ← Step 3 (★ 핵심)
├── design_analysis.md           ← Step 4a
├── visualization_strategy.md    ← Step 4b
├── proposal_slides.json         ← Step 5 (v2.0)
├── proposal.html                ← Step 5 (Gemini 모드)
├── slides/                      ← Step 5 (HTML 모드)
│   ├── slide_01.html
│   └── ...
└── preview.html                 ← Step 5 (통합 미리보기)
```

---

## 목표 분량

| 프로젝트 규모 | 예산 | 목표 슬라이드 |
|-------------|------|------------|
| 소규모 | ~5천만원 | 40~50장 |
| 중규모 | 5천만~2억원 | 50~65장 |
| 대규모 | 2억원~ | 65~80장 |

---

## 절대 하지 말 것

- proposal_script.md 없이 바로 JSON/코드 생성
- 사용자 승인 없이 다음 Step 진행
- 리서치 없이 스크립트 작성
- Evidence에 출처 없는 데이터 사용
- 디자인 레퍼런스 있는데 분석 건너뛰기
- Visualizer 건너뛰고 Converter 직행
- title_body 레이아웃 남용 (40종 중 콘텐츠에 맞는 레이아웃 선택)
- 체크리스트 제시 없이 컨펌 요청
