---
name: clio
description: >
  마무리투수(Closer) + 역사의 뮤즈. 파이프라인 최종 점검(GO/NO-GO 판정) +
  소스 기반 흐름도 추출 + 문서 산출물(PRD, 기술문서, 매뉴얼) 일괄 생성.
  /clio, 클리오, 마무리, 최종 점검, 산출물 생성 요청에 실행한다. 레거시 호출명은 /closer와 클로저다.
---

# Clio (클리오) — 마무리투수 + 역사의 뮤즈

> **클리오(Clio / Kleio)**: 그리스 신화 9 뮤즈 중 **역사의 뮤즈**.
> 야구의 마무리투수(Closer)처럼, 모든 파이프라인이 끝난 뒤 최종 점검하고 판정을 내린다.
> 그리고 역사의 뮤즈답게, 확정된 코드를 후대에 남길 기록으로 정리한다.
>
> **마무리투수 → 기록자.** 점검 먼저, 문서는 그 다음.

## GS 작업을 전달받은 경우에만

GS 인증 사전점검에서 등급·기관 기준·run_dir을 전달받으면 `gs-certification` 모듈을
프로젝트 실제 경로 → 현재 CLI 활성 루트 → SKILLS-CATALOG.md의 정확한 source-only 경로로 해석한다.
그 SKILL.md를 읽고 부모 디렉터리의 `references/clio-gs-documents.md`를 적용한다.
GS 입력이 없는 일반 실행은 기존 절차를 따른다. 필수 참조 누락은 NOT RUN으로 반환한다.
사용자의 점검/수정 권한과 GS 출력 경로를 우선하고 기존 latest 보고서를 덮어쓰지 않는다.

## Quick Start

```
/clio                          # 전체 실행 (점검 + 문서)
/clio src/                     # 특정 소스 디렉토리 지정
/clio --check-only             # 최종 점검만 (Phase 1, GO/NO-GO 판정)
/clio --docs-only              # 문서 생성만 (Phase 2~3, 점검 건너뜀)
/clio --flow-only              # 흐름도만 추출 (Phase 2)
```

**공식 호출명:** `/clio` (별칭: `클리오`, `마무리`, `최종 점검`, 레거시: `/closer`, `클로저`)

## 내부 소스 모듈 해석 계약 (필수)

`flow-verifier`, `humanizer`, `mermaid-diagrams`, `pdf`와 선택 모듈 `diagram-design`은 Clio가 호출하는 등록 스킬이 아니라
절차·문법·스크립트를 직접 소비하는 source-only 내부 모듈입니다. 각 이름에 대해 해석된
`SKILL.md` 절대경로를 `MODULE_SKILL[name]`, 그 부모 디렉터리를 `MODULE_ROOT[name]`으로
기록합니다.

각 모듈을 처음 쓰기 전에 다음 순서로 해석합니다.

1. 프로젝트 루트의 `skills/<name>/SKILL.md`가 **실제 파일로 존재하고 frontmatter의 `name`이
   정확히 `<name>`일 때만** 그 절대경로를 사용합니다. 없거나 이름이 다르면 프로젝트의 다른
   경로를 추측하지 않고 2번으로 갑니다.
2. 없으면 현재 런타임의 활성 루트에서 정확한 `skills/<name>/SKILL.md`를 확인합니다. Codex는
   `$CODEX_HOME/skills`(미설정이면 `~/.codex/skills`), Claude와 Grok 호환 표면은
   `~/.claude/skills`, Antigravity는 `~/.gemini/antigravity-cli/skills`입니다. 파일 존재와 frontmatter 이름이
   모두 일치할 때만 사용하고, 아니면 3번으로 갑니다.
3. 없으면 현재 런타임의 전역 `SKILLS-CATALOG.md`를 읽습니다. Codex는
   `$CODEX_HOME/SKILLS-CATALOG.md`(미설정이면 `~/.codex/SKILLS-CATALOG.md`), Claude와
   Grok 호환 표면은 `~/.claude/SKILLS-CATALOG.md`, Antigravity는
   `~/.gemini/antigravity-cli/SKILLS-CATALOG.md`입니다. 첫 번째 셀이 정확히 `<name>`인 행
   (`| <name> | ... | ... | <읽을 경로> |`) 하나를 찾아 `읽을 경로`의 절대 `SKILL.md`를
   그대로 사용합니다. 정확한 이름의 행이 0개이거나 2개 이상이면 해석 실패이며 다른 행이나
   레지스트리 경로를 추측하지 않습니다.
4. 해석한 파일의 존재를 확인하고 `SKILL.md` 전체를 읽은 뒤에만 그 모듈의 기준을 적용합니다.
   참조 파일은 `MODULE_ROOT[name]/references/...`, 스크립트는
   `MODULE_ROOT[name]/scripts/...`로부터 절대경로를 만듭니다.

이 과정은 모듈 읽기이지 스킬 호출이 아닙니다. `/flow-verifier`, `/humanizer`,
`/mermaid-diagrams`, `/pdf`, `/diagram-design`을 호출하거나 스킬 레지스트리에 등록됐다고 가정하지 않습니다.
프로젝트·활성 루트 파일도 없고 카탈로그의 정확한 행·`읽을 경로`·필수 참조나 스크립트 중 하나라도 없으면
`CHECKLIST.md`와 `FINAL-REPORT.md`의 `Module Coverage`에 경로와 이유를 기록하고 다음 한정된
native fallback을 사용합니다. fallback도 실행할 수 없는 작업은 `NOT RUN` 또는 `UNVERIFIED`로
남기며 완료나 PASS로 바꾸지 않습니다.

| 모듈 | 한정된 native fallback |
|------|------------------------|
| `flow-verifier` | 노드·분기·순서·오류·코드에만 있는 경로를 직접 대조하고 `source: native-fallback` 표기 |
| `mermaid-diagrams` | `flowchart TD`, 안정적인 노드 ID, 인용된 label, 명시적 edge만 사용. renderer가 없으면 문법 검증은 `NOT RUN` |
| `humanizer` | 아래 S1 금지 패턴과 변경률 가드만 적용하고 전체 한국어 패턴 커버리지는 `UNVERIFIED` |
| `pdf` | 대체 변환기를 임의로 설치하거나 호출하지 않고 PDF 산출을 `NOT RUN`으로 기록한 뒤 Markdown 문서는 유지 |
| `diagram-design` (선택) | 에디토리얼 렌더링을 생략하고 문서의 Mermaid 코드 블록을 유지. `Rendered Diagrams`는 `NOT RUN`으로 기록 |

## 파이프라인 위치

```
/zephermine → /agent-team → /argos → /minos → /clio
  설계사        포세이돈        감리관     QA 실사      마무리투수 + 기록자
```

**전제 조건:** 구현이 완료된 상태. argos/minos는 선행 권장이지만 필수는 아님.

---

## CRITICAL: First Actions

### 1. Print Intro

```
Clio(클리오) — 마무리투수 등판
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
순서: Detect → Phase 1 (최종 점검) → Phase 2 (흐름도) → Phase 3 (문서) → Phase 3.5 (문서 사이트) → Phase 4 (보고서)
"마무리투수가 먼저 점검하고, 역사의 뮤즈가 기록한다."
```

### 2. Detect Project

프로젝트를 감지합니다:

1. `$ARGUMENTS`로 전달된 경로 사용
2. 없으면 현재 디렉토리에서 자동 감지:
   - `package.json`, `pom.xml`, `pyproject.toml`, `*.csproj` 등 프로젝트 파일 탐색
   - `src/`, `app/`, `lib/` 등 소스 디렉토리 탐색
3. 기존 산출물 수집 (archive/ 경로 제외):
   - `docs/plan/*/spec.md` — 설계 산출물
   - `docs/plan/*/verify-report.md` — argos 감리 보고서
   - `docs/flow-diagrams/` — 기존 흐름도
   - Playwright/Cypress 테스트 결과 — minos 결과

상태 출력:

```
📂 프로젝트 감지:
  프로젝트: {project-name}
  기술 스택: {tech-stack}
  소스 경로: {src-path}

📋 기존 산출물:
  설계(spec):        {있음/없음}
  감리(argos):       {PASS/CONDITIONAL/FAIL | 없음}
  QA(minos):         {통과율 N% | 없음}
  흐름도:            {N개 | 없음}
```

### 3. Archive Previous & Create Output Directory

**기존 산출물이 있으면 아카이브 후 클린 상태로 시작합니다.**

1. `docs/clio/latest/` 디렉토리가 존재하는지 확인
2. 존재하면 → `docs/clio/archive/YYYY-MM-DD-HHMMSS/`로 이동
3. 새 `docs/clio/latest/` 디렉토리 생성

```
docs/
└── clio/
    ├── latest/                     # 항상 최신본 (여기를 참조)
    │   ├── CHECKLIST.md            # Phase 1 산출물 (최종 점검 결과)
    │   ├── flow-diagrams/          # Phase 2 산출물
    │   │   ├── system-overview.mmd
    │   │   └── {feature-name}.mmd
    │   ├── PRD.md                  # Phase 3 산출물
    │   ├── TECHNICAL.md            # Phase 3 산출물
    │   ├── USER-MANUAL.md          # Phase 3 산출물
    │   └── FINAL-REPORT.md         # Phase 4 산출물
    └── archive/                    # 이전 실행 이력
```

### 실행 역할과 소유권

역할명은 특정 CLI의 에이전트 이름이 아니라 의미 계약입니다. 현재 런타임의 내장 역할 중 계약을
충족하는 것을 사용하며, 특정 모델명이나 spawn 인자 형식을 강제하지 않습니다.

| 작업 | 의미 역할 | 허용 범위 |
|------|-----------|-----------|
| 소스 탐색, 흐름 추적, 설계 대조, 문서 사실 검증 | 읽기 전용 탐색·검토 역할 | 코드와 산출물을 읽고 `file:line` 근거 또는 Mermaid 초안을 반환. 파일 수정 금지 |
| 테스트·린트·타입 검사 실행 | general-write 역할 | 지정 명령과 도구의 임시 산출물만 허용. 소스 수정 금지 |
| 흐름도·문서·문서 사이트 파일 생성 | general-write 역할 | 메인이 지정한 단일 출력 경로 집합만 소유하고 검증 결과와 변경 경로를 반환 |

메인 컨텍스트만 archive/latest 전환, GO/NO-GO 판정, 작업 상태, 발견 병합, 출력 파일 소유권
배정 같은 공유 상태를 변경합니다. 두 작업자에게 같은 파일을 배정하지 않습니다. 네이티브 위임이
없거나 실패하면 메인 컨텍스트에서 같은 계약을 Phase 순서대로 실행합니다.

---

## Phase 1: 최종 점검 (마무리투수)

**목적:** 모든 파이프라인 결과를 수집하고, 누락·미통과 항목을 탐지하여 GO/NO-GO를 판정한다.

### 1-1. 파이프라인 결과 수집

| 항목 | 수집 방법 | 없으면 |
|------|----------|--------|
| argos 감리 보고서 | `docs/plan/*/verify-report.md` 파싱 | "미실행" 기록 |
| minos QA 결과 | Playwright 테스트 결과 파싱 | "미실행" 기록 |
| 설계 spec | `docs/plan/*/spec.md` | "없음" 기록 |
| 완료 기준 | `docs/plan/*/checklist.md` + `checklist-status.md` 장부 (형식: 젭마인 `references/acceptance-checklist-guide.md`). `checklist.md`가 없으면 `sections/section-*.md`에서 Acceptance Criteria 추출 | 건너뜀 |

### 1-2. 코드 품질 최종 실행

가능하면 general-write 역할에 아래 검증 명령을 실행시킵니다. 이 역할은 테스트·린트·타입 검사와
도구가 생성하는 지정 임시 산출물만 소유하고, 소스나 Clio 문서를 수정하지 않습니다. 위임할 수
없으면 메인 컨텍스트에서 명령을 순차 실행합니다.

```bash
# 테스트 실행
npm test 2>&1 || pytest 2>&1 || go test ./... 2>&1 || dotnet test 2>&1

# 린트
npx eslint src/ 2>&1 || ruff check . 2>&1 || golangci-lint run 2>&1

# 타입 체크
npx tsc --noEmit 2>&1 || mypy . 2>&1

# 테스트 커버리지 (가능하면)
npx jest --coverage 2>&1 || pytest --cov=src 2>&1
```

프로젝트에 해당 도구가 없으면 건너뜁니다 (에러 무시).

### 1-3. 누락 탐지

spec이 있으면, **설계 대비 구현 누락**을 읽기 전용 탐색·검토 역할로 확인합니다. 이 역할은
근거와 누락 목록만 반환하고 파일을 수정하지 않습니다. 위임이 없으면 메인이 순차 확인합니다:

1. spec.md에서 기능 목록 추출
2. 소스 코드에서 해당 기능이 구현되었는지 Grep으로 확인
3. 완료 기준: 장부가 있으면 `proved`가 아닌 AC를 누락으로 집계하고, 장부가 없으면 AC별 충족 여부를 직접 확인 ("이행 장부 없음" 경고)
4. 누락된 기능/AC 목록 생성

### 1-4. GO / NO-GO 판정

| 판정 | 조건 |
|------|------|
| **GO** | 테스트 1개 이상 존재 + 전체 통과 + 린트 에러 0 + 타입 에러 0 + 누락 기능 0 + (minos 실행 시) minos PASS |
| **CONDITIONAL GO** | 테스트 통과 + Minor 린트 경고만 있음, 또는 argos/minos 미실행, 또는 minos CONDITIONAL, 또는 **테스트가 아예 없음** (0개 통과는 "전체 통과"가 아님 — GO 승격 금지) |
| **NO-GO** | 테스트 실패, 또는 누락 기능 있음, 또는 완료 기준 AC 중 `missing`·`contradicted` 있음, 또는 argos FAIL, 또는 minos FAIL |

> **공허한 통과 방지**: "테스트 전체 통과"는 테스트가 1개 이상 존재할 때만 성립합니다.
> **우회 표기**: `--force` 또는 `--docs-only`로 게이트를 건너뛴 경우, 모든 산출물(FINAL-REPORT 포함) 상단에 "점검 게이트 미통과/미수행 상태로 생성됨"을 표기합니다.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
마무리투수 판정: {GO / CONDITIONAL GO / NO-GO}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  테스트:       {PASS (N/N) | FAIL (N/M)}
  린트:         {CLEAN | WARN N개 | ERROR N개}
  타입 체크:    {PASS | FAIL N개}
  커버리지:     {N% | 미측정}
  argos 감리:   {PASS | CONDITIONAL | FAIL | 미실행}
  minos QA:     {N% 통과 | 미실행}
  구현 누락:    {없음 | N개 항목}
  완료 기준:    {M/N proved | 장부 없음 | 해당 없음}

  블로커: {없음 | 목록}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NO-GO 시:**
- 블로커 목록을 사용자에게 보고
- "블로커를 해결한 뒤 `/clio`를 다시 실행해주세요" 안내
- Phase 2~4 진행하지 않음 (문서를 만들어봤자 코드가 바뀔 것)

**CONDITIONAL GO 시:**
- 경고 목록을 보고하고 사용자에게 확인
- 사용자가 승인하면 Phase 2로 진행

**GO 시:**
- Phase 2로 즉시 진행

**Phase 1 출력:** `docs/clio/latest/CHECKLIST.md`

---

## Phase 2: 소스 기반 프로세스 흐름도 추출

**목적:** 최종 확정된 소스 코드에서 실제 프로세스 흐름을 Mermaid 다이어그램으로 추출

### 절차

1, 2, 4번은 같은 읽기 전용 계약을 사용합니다. 3번만 지정된 흐름도 출력 파일을 소유하는
general-write 역할이 수행하며, 메인이 초안과 근거를 검증한 뒤 파일 소유권을 배정합니다.

1. **엔트리포인트 탐색**
   - API: 라우터/컨트롤러에서 엔드포인트 목록 추출
   - UI: 페이지/라우트 목록 추출
   - 서비스: 주요 public 메서드 추출

2. **핵심 흐름 식별** (읽기 전용 탐색·검토 역할)
   - `MODULE_SKILL[mermaid-diagrams]`를 직접 읽어 Mermaid 문법 계약 적용
   - 사용자 요청 → 응답까지의 주요 흐름 추적
   - 분기(if/else, switch), 에러 처리, 외부 호출 식별
   - 흐름별 Mermaid flowchart 초안과 `file:line` 근거 반환, 파일 쓰기 금지

3. **다이어그램 파일 저장** (메인이 출력 경로를 배정한 general-write 역할 또는 순차 폴백)
   - `docs/clio/latest/flow-diagrams/{feature-name}.mmd`
   - 전체 시스템 개요 다이어그램: `system-overview.mmd`

4. **기존 흐름도와 비교** (읽기 전용 탐색·검토 역할, 있는 경우)
   - `docs/flow-diagrams/` 또는 `docs/plan/*/flow-diagrams/`에 기존 다이어그램이 있으면
   - `MODULE_SKILL[flow-verifier]`에서 직접 읽은 verify 모드로 기존 설계 ↔ 최종 코드 차이 표시
   - 차이가 있으면 리포트에 기록 (설계 변경 이력으로 활용)
   - 모듈 해석 실패 시 위 native fallback을 사용하고 모듈 적용으로 표기하지 않음

**Phase 2 출력:**

```
✅ Phase 2 완료: 프로세스 흐름도 추출
  생성: {N}개 다이어그램
  시스템 개요: system-overview.mmd
  핵심 흐름: {feature-1}.mmd, {feature-2}.mmd, ...
  설계 대비 차이: {있음/없음}
```

---

## Phase 3: 문서 산출물 생성

**목적:** Phase 2의 흐름도 + 기존 검증 결과 + 소스 코드를 기반으로 문서 생성

**원칙: "코드가 진실"** — 설계 문서가 아니라 최종 확정된 코드에서 문서를 추출합니다.

3종 문서의 입력/출력 경로 및 포함 항목 상세: See [document-templates.md](references/document-templates.md)

메인은 PRD, 기술 문서, 사용자 매뉴얼, 변경 이해 퀴즈를 서로 겹치지 않는 출력 파일로 나누고
파일별 general-write 역할에 배정합니다. 각 역할은 자기 파일만 생성·윤문하고 변경 경로와 검증
결과를 반환합니다. 위임이 없으면 메인이 아래 순서대로 문서를 하나씩 생성합니다.

### Phase 3 시작: 도메인사전 컨텍스트 로드

`docs/domain-dictionary.md`가 있으면 메인이 읽어 각 문서 general-write 역할에 읽기 전용 컨텍스트로
전달합니다. 없으면 이 단계는 건너뜁니다. 사전 원본과 공유 작업 상태는 메인만 갱신합니다.

**문서별 사전 활용:**

| 문서 | 사전 활용 |
|------|----------|
| PRD.md | 기능명/엔터티명을 사전 영문 식별자로 표기 + 한글 표기 병기. 금지 표현 검출 시 정정 |
| TECHNICAL.md | 모듈명/클래스명/타입명이 사전 영문 식별자 따르는지 확인. 위반 시 보고 (코드 수정은 clio 권한 외) |
| USER-MANUAL.md | UI 라벨/메뉴명/메시지가 사전 한글 표기 따르는지 확인. 매뉴얼 본문은 사전 표기로 통일 |

**용어 색인 자동 생성**: 3종 문서 모두에 마지막 부록으로 "용어 색인" 섹션 자동 추가 (사전을 alphabetical로 나열, 한글 표기 + 한 줄 정의).

신규 멤버 온보딩 시 USER-MANUAL.md 한 장으로 도메인 어휘 + 사용법을 동시에 학습 가능.

### Phase 3 공통: 한국어 윤문 (humanizer 연동)

한국어로 생성되는 문서는 `MODULE_SKILL[humanizer]`와
`MODULE_ROOT[humanizer]/references/korean-translationese.md`를 직접 읽어 한국어 모듈을 두 단계로
적용합니다. 둘 중 하나라도 없으면 아래의 축약 fallback만 적용하고 전체 패턴 검사는
`UNVERIFIED`로 기록합니다.

**생성 시 (제약 주입):** 각 문서 general-write 역할의 작업 계약에 포함 —
- 번역투 금지: 연결어미 뒤 쉼표 습관("하며,"·"하고,"), ~성/~적/~화 명사화 남발, 불필요한 진행형, 대명사 직역("그것은"·"이것은")
- AI 문체 금지: 과장 수식어, 3개 나열 습관, 공허한 마무리 문장

**생성 후 (윤문 패스):** 3종 문서 완성 후 humanizer 한국어 모듈로 1회 점검 —
- S1 등급(항상 제거) 패턴 중심, 정량 지표(연결어미 뒤 쉼표 밀도 등)로 빠르게 진단
- 과잉편집 가드 준수: 변경률 30% 경고 / 50% 중단. 고유명사·수치·코드 블록·도메인사전 표기는 수정 금지
- 우선순위: USER-MANUAL.md(외부 공유) > PRD.md > TECHNICAL.md(S1만)
- 상세 패턴: `MODULE_ROOT[humanizer]/references/korean-translationese.md`

### Phase 3 공통: 사실 검증 게이트 (생성 후)

윤문 패스 직후, 생성 역할과 분리된 읽기 전용 검토 역할에 3종 문서가 단정하는 식별자·수치를
소스 코드와 대조시킵니다. 검토 역할은 근거와 필요한 교정 목록만 반환하며 문서를 수정하지 않습니다.
메인이 근거를 확인한 뒤 해당 문서에 교정을 반영합니다. 위임할 수 없으면 같은 대조를 메인 컨텍스트에서 순차 수행합니다.

**대조 대상:** API/엔터티 이름, 커버리지 %, 의존성·API 개수, NFR("코드에서 감지된 것"으로 적힌 항목).

**절차:** 각 주장의 식별자/수치를 소스에서 Grep으로 확인 → 일치하면 유지, 소스에서 확인되지 않으면 해당 표기를 `[확인 필요]`로 교체.

> **가드(필수):** 소스로 확인되지 않은 수치/식별자는 단정하지 말고 `[확인 필요]`로 표기. 추측으로 숫자/이름을 채우지 말 것.

### 3-1. PRD — `docs/clio/latest/PRD.md`

Clio의 `references/document-templates.md`를 계약으로 삼습니다.
소스 코드 기준으로 기능 요구사항, 데이터 모델, API 목록, 화면 흐름을 추출합니다.

### 3-2. 기술 문서 — `docs/clio/latest/TECHNICAL.md`

아키텍처 개요(Mermaid C4), 기술 스택, 핵심 모듈, 환경 설정, 빌드/배포 절차를 포함합니다.

### 3-3. 사용자 매뉴얼 — `docs/clio/latest/USER-MANUAL.md`

기능별 사용법, 화면 가이드(UI), 또는 API 레퍼런스(API only), FAQ/트러블슈팅을 포함합니다.

### 3-3b. 변경 이해 퀴즈 — `docs/clio/latest/CHANGE-QUIZ.md`

긴 구현 후에는 리뷰어가 변경 맥락을 놓치기 쉽습니다. PRD/TECHNICAL/USER-MANUAL 생성 직후, 최종 코드와 diff를 기준으로 사람이 이해해야 할 핵심을 5-10문항 퀴즈로 만듭니다.

포함 항목:
- 변경의 의도와 사용자 영향
- 데이터 모델/API/권한/상태 흐름처럼 리뷰어가 잘못 이해하면 위험한 결정
- 테스트와 검증 증거
- `implementation-notes.md`가 있으면 `Deviations`의 이유와 후속 조치

정답과 해설은 각 문항 바로 아래 접기 가능한 형식 또는 별도 "Answer Key" 섹션에 둡니다. 최종 보고에는 "퀴즈 통과 전 병합 금지" 권고를 남깁니다.

**Phase 3 출력:**

```
✅ Phase 3 완료: 문서 산출물 생성
  PRD.md          — {N}개 기능 요구사항, {M}개 API 엔드포인트
  TECHNICAL.md    — {N}개 모듈, {M}개 의존성
  USER-MANUAL.md  — {N}개 기능 가이드
  CHANGE-QUIZ.md  — {N}개 변경 이해 문항
```

### 3-3c. 에디토리얼 다이어그램 렌더링 (선택, `--render-diagrams`)

`--render-diagrams` 지정 시 또는 사용자가 발표용·에디토리얼 다이어그램을 요청한 경우에만 진행합니다.
`MODULE_SKILL[diagram-design]`을 직접 읽어 표현 계층 계약을 적용합니다.

- **입력**: Phase 2의 `flow-diagrams/*.mmd` 중 PRD/TECHNICAL에 실제 인용된 핵심 다이어그램만 (전량 렌더링 금지)
- **절차**: `MODULE_ROOT[diagram-design]/scripts/mermaid_extract.py`로 IR 추출 → 브랜드 토큰 기반 HTML+inline SVG 렌더링. 대상 프로젝트에 `DESIGN.md`가 있으면 토큰을 매핑하고, 없으면 기본 스킨을 쓰며 질문하지 않습니다
- **출력**: `docs/clio/latest/diagrams/{이름}.html`. 정본 `.mmd`는 수정하지 않고, 문서 본문의 Mermaid 블록 아래에 렌더 파일 링크만 병기합니다
- **분할**: 노드 9개 초과 도면은 diagram-design 규칙대로 개요+상세로 나눠 렌더링합니다 (정본은 분할하지 않음)

### 3-4. PDF 출력 (한국 기본값: A4 + Pretendard)

**`--no-pdf`가 아니면 진행.** 사용자에게 페이지 구성을 묻고 적합한 옵션으로 PDF를 자동 생성합니다.

**현재 CLI의 질문 방식으로 묻기 (한 번만):**

> 산출물을 PDF로도 출력하시겠어요? (외부 공유/인쇄용)

옵션:
- A) 3종 모두 PDF (PRD + TECHNICAL + USER-MANUAL)
- B) USER-MANUAL만 PDF (외부 공유용)
- C) PDF 출력 안 함

**A 또는 B 선택 시 후속 질문:**

> 페이지 구성은 어떻게 할까요?

옵션:
- A) **출판 모드** — 표지 + TOC + H1마다 새 페이지 (외부 공유, 인쇄)
- B) **간단 모드** — TOC만 (내부 문서)
- C) **메모 모드** — 옵션 없음 (짧은 문서)

> 워터마크가 필요한가요?

옵션:
- A) "초안" (작업 중)
- B) "검토용" (리뷰 요청)
- C) "대외비" + CONFIDENTIAL 푸터
- D) 없음 (최종본)

**PDF 생성 명령 (선택에 따라 자동 구성):**

먼저 `PDF_SCRIPT`를 해석된 절대경로
`MODULE_ROOT[pdf]/scripts/markdown_to_pdf.py`로 설정하고 파일 존재를 확인합니다. 아래 명령의
`PDF_SCRIPT`에는 상대경로가 아니라 그 절대경로만 넣습니다.

```bash
# 실행 전에 이 값을 MODULE_ROOT[pdf]에서 파생한 실제 절대경로로 치환
PDF_SCRIPT="<absolute MODULE_ROOT[pdf]>/scripts/markdown_to_pdf.py"

# 출판 모드 + 워터마크 없음 예시
python "$PDF_SCRIPT" generate \
  --cover --toc \
  --title "{프로젝트명} 사용자 매뉴얼" \
  --author "{팀/저자}" \
  --org "{조직}" \
  docs/clio/latest/USER-MANUAL.md

# 검토용 워터마크 예시
python "$PDF_SCRIPT" generate \
  --cover --toc --watermark "검토용" \
  --title "{프로젝트명} PRD" \
  docs/clio/latest/PRD.md

# 대외비 예시
python "$PDF_SCRIPT" generate \
  --cover --toc --watermark "대외비" --confidential \
  --title "{프로젝트명} 기술문서" \
  docs/clio/latest/TECHNICAL.md
```

**산출물 위치:**

```
docs/clio/latest/
├── PRD.md         + PRD.pdf          (--cover --toc)
├── TECHNICAL.md   + TECHNICAL.pdf    (--cover --toc)
└── USER-MANUAL.md + USER-MANUAL.pdf  (--cover --toc, 외부 공유 빈도 높음)
```

**Phase 3-4 출력:**

```
✅ Phase 3-4 완료: PDF 출력
  PRD.pdf            — {N} 페이지 ({size} KB)
  TECHNICAL.pdf      — {N} 페이지 ({size} KB)
  USER-MANUAL.pdf    — {N} 페이지 ({size} KB)
  페이지 구성:        {출판 모드 / 간단 모드 / 메모 모드}
  워터마크:          {초안 / 검토용 / 대외비 / 없음}
```

**의존성 자동 점검:**

```bash
PDF_SCRIPT="<absolute MODULE_ROOT[pdf]>/scripts/markdown_to_pdf.py"
if [ ! -f "$PDF_SCRIPT" ]; then
  echo "PDF: NOT RUN — resolved pdf script not found: $PDF_SCRIPT"
elif ! python -c "import playwright, markdown" 2>/dev/null; then
  echo "⚠️  playwright 미설치. 다음 명령으로 설치:"
  echo "    pip install playwright markdown pygments"
  echo "    playwright install chromium"
  echo "또는 한 방에:"
  echo "    python \"$PDF_SCRIPT\" setup"
  echo "PDF 출력 건너뜁니다."
fi
```

`/minos` 스킬이 이미 설치되어 있다면 playwright는 중복 없이 재사용됩니다.
PDF 모듈·스크립트·Python 의존성 중 하나라도 없으면 PDF만 `NOT RUN`으로 기록하고 Phase 3.5로
진행합니다(블로커 아님). 출력 파일이 실제로 생성되고 열리는지 확인하기 전에는 PDF 단계를 완료로
표기하지 않습니다.

**상세 사용법:** `MODULE_SKILL[pdf]`의 "Markdown → 출판품질 PDF" 섹션을 직접 참조합니다.

---

## Phase 3.5: 문서 사이트 생성 (웹 매뉴얼)

**목적:** Phase 3에서 만든 마크다운 문서를 docs.example.com 같은 문서 웹사이트로 빌드

> 마크다운 파일만 있으면 아무도 안 본다. 웹 문서로 만들어야 실제로 쓰인다.

### 3.5-1. 기존 문서 프레임워크 감지

```bash
# 기존 문서 사이트 감지
_DOC_FRAMEWORK=""
[ -f "docusaurus.config.js" ] || [ -f "docusaurus.config.ts" ] && _DOC_FRAMEWORK="docusaurus"
[ -f "mkdocs.yml" ] && _DOC_FRAMEWORK="mkdocs"
[ -f ".vitepress/config.ts" ] || [ -f ".vitepress/config.js" ] && _DOC_FRAMEWORK="vitepress"
[ -f "astro.config.mjs" ] && grep -q "starlight" "astro.config.mjs" && _DOC_FRAMEWORK="starlight"

echo "DOC_FRAMEWORK: ${_DOC_FRAMEWORK:-없음}"
```

### 3.5-2. 프레임워크 선택 (없으면)

기존 프레임워크가 없으면 프로젝트 스택에 맞게 자동 선택:

| 프로젝트 스택 | 추천 | 이유 |
|-------------|------|------|
| React / Next.js | **Docusaurus** | React 기반, MDX 지원, 버전 관리 |
| Vue / Nuxt | **VitePress** | Vue 기반, Vite 빌드, 가벼움 |
| Python / FastAPI | **MkDocs Material** | pip install 한 줄, 가장 간단 |
| 기타 / 범용 | **VitePress** | 빠르고 가볍고 마크다운 그대로 사용 |

### 3.5-3. 셋업 + 문서 배치

메인이 문서 사이트 출력 경로와 허용되는 manifest 변경을 명시한 뒤 general-write 역할에 실행을
맡깁니다. 이 역할은 지정 경로 밖을 수정하지 않고 변경 경로와 빌드 검증을 반환합니다. 위임이
없으면 메인 컨텍스트에서 아래 셋업과 검증을 순차 실행합니다.

**핵심: 복사가 아니라 직접 참조.** 문서 프레임워크가 `docs/clio/latest/`를 소스로 읽도록 설정하면, md를 수정할 때 Hot Reload로 즉시 반영됩니다.

**VitePress 예시:**
```bash
# 초기화 (docs/clio/latest/를 소스 루트로 지정)
npm add -D vitepress

# .vitepress/config.ts에서 srcDir을 clio 산출물로 지정
# → 별도 복사 불필요, md 수정 시 즉시 반영
```

```ts
// docs/clio/latest/.vitepress/config.ts
export default {
  title: '{프로젝트명} 문서',
  themeConfig: {
    sidebar: [
      { text: '시작하기', items: [
        { text: '소개', link: '/PRD' },
        { text: '사용자 가이드', link: '/USER-MANUAL' },
      ]},
      { text: '기술 문서', items: [
        { text: '아키텍처', link: '/TECHNICAL' },
        { text: '최종 보고서', link: '/FINAL-REPORT' },
      ]},
    ]
  }
}
```

```bash
# dev server (md 수정 → 즉시 반영)
npx vitepress dev docs/clio/latest
```

**MkDocs 예시:**
```bash
pip install mkdocs-material
```

```yaml
# mkdocs.yml (docs_dir을 clio 산출물로 지정)
site_name: '{프로젝트명} 문서'
docs_dir: docs/clio/latest
nav:
  - 소개: PRD.md
  - 사용자 가이드: USER-MANUAL.md
  - 기술 문서: TECHNICAL.md
  - 최종 보고서: FINAL-REPORT.md
```

```bash
mkdocs serve  # md 수정 → 즉시 반영
```

### 3.5-4. 사이드바/네비게이션 자동 생성

Phase 3 문서가 이미 `docs/clio/latest/`에 있으므로 그대로 소스 디렉토리로 사용합니다.
문서가 많아지면 분할하되, **원본 .md 파일이 유일한 소스**입니다:

```
docs/clio/latest/               ← 문서 사이트의 소스 루트
├── .vitepress/config.ts        # 또는 mkdocs.yml (사이트 설정)
├── index.md                    # 프로젝트 소개 (자동 생성)
├── PRD.md                      # Phase 3 원본 그대로
├── TECHNICAL.md                # Phase 3 원본 그대로
├── USER-MANUAL.md              # Phase 3 원본 그대로
├── CHECKLIST.md                # Phase 1 원본 그대로
├── FINAL-REPORT.md             # Phase 4 원본 그대로
└── flow-diagrams/              # Phase 2 원본 그대로
    ├── system-overview.mmd
    └── {feature}.mmd
```

> `.md`를 수정하면 문서 사이트가 즉시 반영됩니다. 별도 빌드/동기화 불필요.

### 3.5-5. 프리뷰 실행

```bash
# VitePress
npx vitepress dev docs

# MkDocs
mkdocs serve

# Docusaurus
npm start
```

사용자에게 프리뷰 URL 안내: `http://localhost:5173` (또는 해당 포트)

### Phase 3.5 건너뛰는 경우

- `--check-only`, `--flow-only` 옵션 사용 시
- 사용자가 "문서 사이트 불필요" 명시 시
- API만 있는 프로젝트에서 사용자가 거부 시

**Phase 3.5 출력:**

```
✅ Phase 3.5 완료: 문서 사이트 생성
  프레임워크: {VitePress / Docusaurus / MkDocs}
  페이지: {N}개
  프리뷰: http://localhost:{port}

  빌드: npx vitepress build docs
  배포: Vercel / Netlify / GitHub Pages
```

---

## Phase 4: 최종 보고서

메인이 모든 Phase 결과를 정규화하고 GO/NO-GO와 미검증 범위를 확정한 뒤, `FINAL-REPORT.md`만
소유하는 general-write 역할에 템플릿 기반 생성을 맡깁니다. 메인이 결과를 검증해 공유 상태에
반영하며, 위임이 없으면 직접 순차 생성합니다.

**출력:** `docs/clio/latest/FINAL-REPORT.md`

보고서 마크다운 전체 템플릿: See [report-template.md](references/report-template.md)

### 사용자에게 안내

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Clio 기록 완료! 마무리투수가 판정하고, 역사의 뮤즈가 기록했습니다.

🏟️ 판정: {GO / CONDITIONAL GO}

📁 산출물 위치: docs/clio/latest/
  CHECKLIST.md      — 최종 점검 결과 (Phase 1)
  flow-diagrams/    — 프로세스 흐름도 (Phase 2)
  diagrams/         — 에디토리얼 렌더 (3-3c, --render-diagrams 지정 시)
  PRD.md (+ .pdf)            — 제품 요구사항 문서 (Phase 3)
  TECHNICAL.md (+ .pdf)      — 기술 문서 (Phase 3)
  USER-MANUAL.md (+ .pdf)    — 사용자 매뉴얼 (Phase 3, 외부 공유용)
  FINAL-REPORT.md   — 최종 보고서 (Phase 4)

📖 문서 사이트: http://localhost:{port} (Phase 3.5)
  프레임워크: {VitePress / Docusaurus / MkDocs}
  빌드: {빌드 명령어}

📂 이전 이력: docs/clio/archive/

👉 다음 단계:
  /commit              → 산출물 커밋
  /release             → 버전 태그 + CHANGELOG
  /launch              → 배포 전 체크리스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--check-only` | Phase 1만 실행 (GO/NO-GO 판정만) | false |
| `--docs-only` | Phase 2~3만 실행 (문서 생성만, 점검 건너뜀) | false |
| `--flow-only` | Phase 2만 실행 (흐름도만) | false |
| `--no-site` | 문서 사이트 생성 건너뜀 (Phase 3.5 스킵) | false |
| `--no-pdf` | PDF 출력 건너뜀 (Phase 3-4 스킵) | false |
| `--render-diagrams` | Phase 3-3c 실행 — 핵심 흐름도를 에디토리얼 HTML+SVG로 렌더링 (diagram-design 모듈) | false |
| `--pdf=user-manual` | USER-MANUAL만 PDF (PRD/TECHNICAL은 마크다운만) | false |
| `--output-dir` | 산출물 디렉토리 변경 | `docs/clio/latest/` |
| `--force` | NO-GO여도 문서 생성 강제 진행 | false |

---

## 예외사항

다음은 **문제가 아닙니다**:

1. **argos/minos 미실행** — CHECKLIST에 "미실행"으로 기록, CONDITIONAL GO로 판정
2. **기존 설계 산출물 없음** — 누락 탐지 건너뜀, 코드 기준으로 문서 생성
3. **UI 없음** — Phase 3에서 API 레퍼런스 매뉴얼로 대체
4. **기존 흐름도 없음** — Phase 2에서 새로 생성 (비교 단계만 건너뜀)
5. **테스트 프레임워크 없음** — CHECKLIST에 "미설정"으로 기록, 경고. 단 판정은 **최대 CONDITIONAL GO** (테스트 0개로 GO 불가)

---

## 연관 스킬

| 스킬 | 역할 | 연결 |
|------|------|------|
| zephermine | 설계 산출물 생성 | spec + AC 참조 (누락 탐지) |
| agent-team | 구현 수행 | 선행 완료 |
| argos | 감리 (준공검사) | Phase 1에서 결과 수집 |
| minos | Playwright QA 실사 | Phase 1에서 결과 수집 |
| flow-verifier (source-only module) | 프로세스 흐름도 생성/검증 | Phase 2에서 `MODULE_SKILL` 직접 읽기 |
| humanizer (source-only module) | 한국어 윤문 (번역투/AI 문체 제거) | Phase 3에서 `MODULE_SKILL`과 참조 직접 읽기 |
| mermaid-diagrams (source-only module) | Mermaid 문법 가이드 | Phase 2에서 `MODULE_SKILL` 직접 읽기 |
| release-notes | 버전 + CHANGELOG | Phase 4 이후 후속 |
| shipping-and-launch | 배포 전 체크리스트 | Phase 4 이후 후속 |
| documentation-and-adrs | ADR 작성 | Phase 4 보고서에 ADR 목록 포함 가능 |
| pdf (source-only module) | Markdown → 출판품질 PDF | Phase 3-4에서 해석한 절대 스크립트 경로 실행 |
| zeus | 전체 파이프라인 | zeus 완료 후 /clio로 마무리 |

## Related Files

| 파일 | 역할 |
|------|------|
| `references/document-templates.md` | 3종 문서 포함 항목 상세 |
| `references/report-template.md` | 최종 보고서 마크다운 템플릿 |
| `MODULE_SKILL[flow-verifier]` | 프로세스 흐름도 생성/검증 로직 |
| `skills/argos/SKILL.md` | 감리 검증 프로세스 |
| `skills/minos/SKILL.md` | QA 시나리오 생성 + Playwright 테스트 |
| `MODULE_SKILL[mermaid-diagrams]` | Mermaid 문법 가이드 |
| `MODULE_SKILL[pdf]` | Markdown → 출판 PDF 계약 |
| `MODULE_ROOT[humanizer]/references/korean-translationese.md` | 한국어 번역투 패턴 (Phase 3 윤문 패스) |
| `MODULE_ROOT[pdf]/scripts/markdown_to_pdf.py` | PDF 변환 스크립트 (playwright/Chromium) |
