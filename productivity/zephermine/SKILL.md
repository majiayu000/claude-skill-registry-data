---
name: zephermine
description: >
  Creates a persisted, sectionized implementation artifact suite through research, stakeholder interviews,
  domain analysis, database and API design, and multi-LLM review. Use for feature or product plans consumed by
  downstream implementation and QA. Prefer lightweight native plan/interview workflows for small tasks; on
  Antigravity those are /plan and /grill-me. /zephermine로 실행. Also known as 젭마인, 제퍼마인, 제퍼미네.
---

# Zephermine

> **Zephyr**(제퍼: 산들바람/서풍, 부드럽고 빠른 흐름) + **Minerva**(미네르바: 지혜·전략·판단)의 합성어.
> 바람처럼 가볍고 빠르게 상황을 읽고, 미네르바처럼 논리적으로 설계해 실행 가능한 계획으로 만드는 능력을 뜻합니다.
> [softaworks/gepetto](https://github.com/softaworks/gepetto) 스킬을 벤치마킹하여 커스터마이징한 버전입니다.

Orchestrates a multi-step planning process: Research → Interview → Spec Synthesis → Team Analysis → Plan → External Review → Sections → Verify

> **네이티브 plan mode와의 구분:** 현재 CLI가 제공하는 plan mode는 "이 작업을 어떻게 구현할까"를 다루는
> 단일 작업용 계획 승인 게이트이고, 젭마인은 다운스트림(포세이돈·아르고스·미노스·제우스·견적)이 소비하는
> **디스크 아티팩트**(plan.md, sections/, flow-diagrams/, qa-scenarios)를 만드는 설계 파이프라인입니다.
> 단일 버그픽스·소규모 리팩토링은 plan mode, 기능/제품 단위 설계는 젭마인.
> Antigravity에서는 가벼운 구현 계획은 `/plan`, 누락 요구를 집중 인터뷰로 좁히는 일은 `/grill-me`가 먼저입니다.
> 그 결과만 필요하면 젭마인을 시작하지 않습니다. `spec.md`, 도메인 사전, API/DB, flow, sections,
> operation/QA 시나리오까지 디스크에 남겨 downstream이 소비해야 할 때만 젭마인을 사용합니다.
> slash command를 프로그램적으로 호출한다고 가정하지 않으며, 현재 plan mode가 쓰기·승인 전용이면 그 안에서
> 젭마인을 실행하지 않습니다. 사용자가 만든 네이티브 계획·인터뷰 결과는 쓰기 가능한 모드에서 입력으로 이어받습니다.

## CRITICAL: First Actions

**BEFORE anything else**, do these in order:

### 1. Print Intro

간결하게 진행 순서만 출력:
```
젭마인(Zephermine) 시작
순서: Research → Blindspot → Interview → Spec(+Domain Dictionary v1) → Persona/Journey → Team Review(+Dictionary v3) → Plan → External Review → DB Schema → API Spec → Flow Diagrams → Sections → Operation Scenarios → QA Scenarios → Skill Discovery
```

### 2. Resolve Spec File Path

**Check if user provided @file at invocation AND it's a spec file (ends with `.md`).**

**경로가 제공된 경우:** 그대로 사용

**경로가 없는 경우:** 사용자 대화에서 주제를 추론하여 자동 경로 생성 후 바로 진행:
1. 대화 컨텍스트에서 기능/프로젝트명 추출 (예: "UI 재설계" → `ui-redesign`)
2. 기본 경로 패턴: `docs/plan/{feature-name}/spec.md`
3. 사용자에게 경로만 간단히 확인:
   ```
   계획 경로: docs/plan/ui-redesign/spec.md
   이 경로로 진행합니다. (변경하려면 알려주세요)
   ```
4. **확인을 기다리지 않고 바로 다음 단계 진행** (사용자가 변경 요청하면 그때 수정)

**주제를 추론할 수 없는 경우에만** 간단히 질문:
```
어떤 기능을 계획할까요? (예: "로그인 리팩토링", "결제 시스템")
```

### 3. Setup Planning Session

Determine session state by checking existing files:

1. Set `planning_dir` = parent directory of the spec file
2. **If `planning_dir` doesn't exist, create it automatically**
3. **Archive 기존 산출물** — `planning_dir`이 이미 존재하고 **spec.md가 있는 완료된 계획**이면:
   ```
   a. {planning_dir}/archive/ 디렉토리 생성 (없으면)
   b. 기존 파일 전체 → {planning_dir}/archive/{YYYY-MM-DD-HHMM}/ 로 이동 (Bash mv)
      - archive/ 폴더 자체는 이동하지 않음
   c. planning_dir을 클린 상태로 시작
   ```
   **resume 모드일 때는 archive 하지 않음** — 이어서 작업할 때는 기존 파일을 유지.
   사용자가 "새로 시작"이라고 명시하거나, 모든 단계가 완료된 상태에서 재실행할 때만 archive.
4. Set `initial_file` = the spec file path
5. If spec file doesn't exist, create an empty template:
   ```markdown
   # Feature Spec

   ## Overview
   [Describe what you want to build]

   ## Requirements
   - [Requirement 1]
   - [Requirement 2]
   ```
6. Scan for existing planning files (research-decision.md, research.md, research/, unknowns.md, interview.md, spec.md, team-review.md, domain-dictionary-delta.md, plan.md, api-spec.md, db-schema.md, integration-notes.md, design-system.md, operation-scenarios.md, qa-scenarios.md, checklist.md, team-reviews/, reviews/, flow-diagrams/, sections/)

   > 마스터 사전(`docs/domain-dictionary.md`)은 프로젝트 단일이므로 planning_dir 스캔에서 제외. planning_dir에는 변경 이력 델타만 보관.

7. **Import upstream artifacts** — 사전 파이프라인 산출물이 있으면 컨텍스트로 로드:
   - `docs/athena/*.md` (excluding archive/) → Athena Go/No-Go 판정, 스코프 조정, MVP 범위
   - `docs/hermes/*.md` (excluding archive/) → Hermes 사업 분석 (BMC, TAM/SAM, GTM)
   - 있으면: interview-protocol.md Phase C의 기정 사실(given context)로 활용, 사업 관련 질문 생략
   - 없으면: 무시하고 정상 진행

8. Determine mode and resume point:

| Files Found | Mode | Resume From |
|-------------|------|-------------|
| None | new | Step 4 |
| research-decision.md only | resume | Step 5 or Step 5A (depending on selected research) |
| research/ partial files only | resume | Step 5 (finish/merge research) |
| research.md only | resume | Step 5A (blindspot pass) |
| research + unknowns | resume | Step 6 (interview or inferred interview) |
| research + unknowns + interview | resume | Step 8 (spec synthesis) |
| + spec | resume | Step 9 (persona) |
| + personas-and-journeys.md | resume | Step 10 (team analysis) |
| + team-review.md | resume | Step 12 (plan) |
| + plan | resume | Step 13 (external review) |
| + reviews | resume | Step 14 (integrate) |
| + integration-notes | resume | Step 15 (integrated plan checkpoint) |
| + db-schema.md | resume | Step 17 (API spec) |
| + api-spec.md | resume | Step 18 (flow diagrams) |
| + flow-diagrams/ | resume | Step 19 (section index) |
| + sections/index.md | resume | Step 20 (write sections) |
| all sections complete | resume | Step 22 (operation scenarios) |
| + qa-scenarios.md | resume | Step 22A (acceptance checklist) |
| + checklist.md | resume | Step 23 (final status) |

**도메인사전 Resume 보정 규칙** (위 테이블과 별도, Resume 시 항상 점검):

| 조건 | 처리 |
|------|------|
| spec.md 있고 `docs/domain-dictionary.md` 없음 | Step 8 끝부산물(사전 v1 생성)을 먼저 실행한 후 정해진 Resume Step으로 진행 |
| team-review.md 있고 사전이 v1에 머무름 (Dictionary Updates 미반영) | Step 10 끝부산물(사전 v2 자동 병합)을 먼저 실행 |
| plan.md 있고 사전이 v3 미확정 (`<planning_dir>/domain-dictionary-delta.md`에 v2→v3 항목 없음) | Step 11 끝부산물(사전 v3 최종화)을 먼저 실행 — 충돌만 확인 |

**판정 방법**: `<planning_dir>/domain-dictionary-delta.md`의 `## v1 → v2`, `## v2 → v3` 섹션 존재 여부로 진행 단계 추정. 델타가 없으면 마스터 사전이 어떤 버전인지 모르므로 안전하게 v1부터 다시 실행.

이 보정은 사용자가 Resume할 때 사전이 누락된 채로 다음 Phase가 진행되는 것을 막습니다.
Resume에서 Step 8/10/11의 사전 부산물을 보정하기 전에도 전역 카탈로그에서
`domain-dictionary` 모듈을 다시 해석합니다. 이전 세션이 기록한 경로나 런타임 등록 상태를
그대로 신뢰하지 않으며, 모듈을 읽지 못하면 보정 Step을 `BLOCKED`로 둡니다.

9. Create or update the current runtime's task ledger from the detected state. Use a native task-list tool only
   when the runtime exposes one; otherwise record the remaining steps in the planning index and continue without
   inventing a vendor-specific tool call.

Print status:
```
Planning directory: {planning_dir}
Mode: {mode}
```

If resuming:
```
Resuming from step {N}
To start fresh, delete the planning directory files.
```

---

## Logging Format

```
═══════════════════════════════════════════════════════════════
STEP {N}/26: {STEP_NAME}
═══════════════════════════════════════════════════════════════
{details}
Step {N} complete: {summary}
───────────────────────────────────────────────────────────────
```

---

## Question Tool Compatibility

Question tools differ by CLI. To avoid `Invalid tool parameters`, use plain text numbered questions by default.

- Use structured question tools only for short bounded choices.
- Structured calls must use max 3 questions per call, and each question should have 2-3 short options.
- Do not send open-ended interview prompts through a structured question tool.
- Do not use structured multi-selection fields unless the current CLI explicitly supports them. Otherwise, show a numbered checklist and ask the user to answer with multiple numbers.
- If a structured question tool fails once, immediately fall back to plain text and do not retry the same payload.

Default no-stop policy:

- Do not ask preference questions that can be inferred from the spec, codebase, research, or existing project conventions.
- Ask only when the answer could materially change architecture, data model, security boundary, UX flow, rollout strategy, legal/compliance handling, or an irreversible external action.
- If the question is non-blocking, choose the conservative default, mark it as `[inferred]` in the relevant artifact, and continue.
- Put non-blocking uncertainty in `unknowns.md`, `interview.md`, `integration-notes.md`, or the final Open Questions section instead of stopping the workflow.

This applies most strongly to Step 6 critical unknowns, Step 11 unresolved domain/dictionary conflicts, and Step 15 only when the user explicitly requested a review gate.

---

## Native Delegation Contract

Use semantic roles instead of hardcoded tool calls, agent files, or models:

| Semantic role | Claude | Codex | Antigravity | Grok | Boundary |
|---------------|--------|-------|--------|------|----------|
| `read-only-analysis` | `Explore` | `explorer` | `research` | `explore` | Read-only; return findings only; never write files |
| `artifact-writer` | `general-purpose` | `worker` | 메인 또는 쓰기 도구를 명시한 사용자 정의 서브에이전트 | `general-purpose` | Write only the one unique output file assigned to the work item |

- Every delegated work item must have either one unique output file or a return-only contract.
- Main/Lead owns shared state and integration artifacts, including `research.md`, `team-review.md`, `plan.md`, `integration-notes.md`, domain dictionaries, manifests, and indexes.
- Workers must not edit another worker's output or shared state. Main/Lead reads completed outputs and performs all merges.
- If native delegation is unavailable, execute the same bounded work items sequentially in the main context. Preserve the same output ownership and budgets.
- Use the runtime's configured default model. Do not hardcode model names in delegation instructions.

---

## Source-only internal module resolution (mandatory)

`domain-dictionary`, `flow-verifier`, `mermaid-diagrams`, 조건부 `frontend-design`은 젭마인
내부 단계가 읽는 source-only 모듈입니다. 사용자 호출용 스킬이나 등록된 slash command로
실행하지 않습니다.

각 모듈을 다음 우선순위로 해석하고, 처음 확인된 **정확한 `SKILL.md` 파일** 하나를 사용합니다.

1. 현재 프로젝트에 `skills/{name}/SKILL.md`가 실제로 있으면 그 exact 파일을 읽습니다
   (소스 저장소 개발 경로).
2. 없으면 현재 런타임 active root의 exact 파일을 확인합니다: Claude/Grok은
   `~/.claude/skills/{name}/SKILL.md`, Codex는 `~/.codex/skills/{name}/SKILL.md`, Antigravity는
   `~/.gemini/antigravity-cli/skills/{name}/SKILL.md` (명시 opt-in 설치 지원).
3. 둘 다 없으면 현재 런타임의 전역 카탈로그를 엽니다: Claude/Grok은
   `~/.claude/SKILLS-CATALOG.md`, Codex는 `~/.codex/SKILLS-CATALOG.md`, Antigravity는
   `~/.gemini/antigravity-cli/SKILLS-CATALOG.md`. 모듈명과 정확히 일치하는 행이 **하나일 때만** 그 행의
   `읽을 경로`에 적힌 절대 `SKILL.md`를 그대로 읽습니다. 행이 없거나 중복이면 fail-closed입니다.
   기본 경로가 보통 `.olympus/source-skills` 아래여도 경로를 조합하거나 추측하지 않습니다.
4. `module_root`는 읽은 `SKILL.md`의 부모 디렉터리입니다. 모듈이 지시하는
   `references/`, `scripts/`, `commands/`는 모두 이 루트에서만 해석합니다.
5. 모듈은 소비 단계에 도달했을 때만 지연 로드합니다. Step 8/10/11은
   `domain_dictionary_root`, Step 18은 `flow_verifier_root`와 `mermaid_diagrams_root`를
   사용합니다. UI design-system 분기에서만 `frontend_design_root`를 사용합니다.

위 exact 파일 읽기는 내부 모듈 로드입니다. 런타임 Skill 목록/레지스트리 가용성을 근거로
호출하거나 모듈 이름을 slash command로 실행하지 않습니다.

사전과 도면의 세 소비 경로는 설계 산출물의 필수 계약입니다. exact 파일, 카탈로그의 유일한 행,
`읽을 경로`, 필수 reference
중 하나라도 없거나 읽을 수 없으면 해당 Step을 `BLOCKED: source module unavailable`로 기록하고
중단합니다. placeholder 사전·도면·인덱스를 만들어 통과시키거나 다음 Step을 PASS 처리하지 않습니다.
핵심 용어 수처럼 **모듈 계약 자체가 허용한** 비적용 조건만 `NOT APPLICABLE`로 기록할 수 있으며,
모듈 미발견을 비적용으로 바꾸면 안 됩니다.

`frontend-design`은 UI design-system 분기의 보조 모듈입니다. 해석 실패 시 이 가이드의 bounded
anti-slop 규칙만 적용하고 `frontend-design: NOT RUN (native fallback)`을 기록합니다. fallback을
모듈 PASS로 표시하지 않습니다.

---

## Workflow

26단계는 **6 Phase**로 그룹화됩니다. `5A. Blindspot Pass`는 Step 5와 6 사이의 보조 단계이며, 기존 Step 번호는 변경하지 않습니다. Phase는 단순 라벨이며 다른 스킬이 "Phase X 후 호출"로 참조할 때 사용합니다.

| Phase | Step | 핵심 산출물 |
|-------|------|-------------|
| **Phase 1: Discovery** | 4-7 | research-decision.md, research.md, unknowns.md, interview.md |
| **Phase 2: Spec** | 8-9 | spec.md, personas-and-journeys.md, **docs/domain-dictionary.md v1** |
| **Phase 3: Domain** | 10-11 | team-review.md, **docs/domain-dictionary.md v3**, domain-dictionary-delta.md |
| **Phase 4: Plan** | 12-15 | plan.md, integration-notes.md |
| **Phase 5: Design** | 16-19 | db-schema.md, api-spec.md, flow-diagrams/, sections/ |
| **Phase 6: Validation** | 20-26 | section-*.md, operation-scenarios.md, qa-scenarios.md, checklist.md |

**도메인사전은 Step이 아니라 Step의 부산물입니다.** Step 8 끝에서 v1 초안, Step 10 끝에서 전문가 입력으로 v2 자동 병합, Step 11 끝에서 충돌만 확인하고 v3 확정. 별도 단계가 추가되지 않으며, 각 Step 본문 끝의 평범한 단락으로 처리됩니다.

---

## Phase 1: Discovery

리서치와 인터뷰로 도메인을 파악하는 단계.

### 4. Research Decision

See [research-protocol.md](references/research-protocol.md).

1. Read the spec file
2. Extract potential research topics (technologies, patterns, integrations)
3. Auto-select research scope from the spec, local repo, and risk level
4. Ask only if the research choice changes scope/cost/compliance and no conservative default exists
5. Record selected and skipped research types in `<planning_dir>/research-decision.md`

### 5. Execute Research

See [research-protocol.md](references/research-protocol.md).

Based on decisions from step 4, launch bounded `artifact-writer` work items:
- **Codebase:** one writer → `<planning_dir>/research/codebase.md` — **요청 기능이 이미 구현됐는지 먼저 확인**(`codemap/index.md` → 핵심어 grep → README/docs). 이미 있으면 신규 설계가 아니라 *개선*으로 분류해 spec/plan 머리에 "기존: {위치}/{경계}" 명시(재구현 방지).
- **GitHub/Web/Academic/Competitor:** one writer and one unique file per research type under `<planning_dir>/research/`; use web search only where available
- **Concurrency cap:** max 2 research work items at a time; if `API Error: Overloaded`/rate limit occurs, retry the failed item once with concurrency 1 and half budget

Writers return only 1-2 line summaries. Main/Lead combines `<planning_dir>/research/*.md` → `<planning_dir>/research.md`.

Skip Step 5 only when Step 4 auto-selection finds no useful research target. Record that decision in `research-decision.md`.

### 5A. Blindspot Pass

Before the interview, convert research findings into an unknowns map. Write `<planning_dir>/unknowns.md` with:

- Known knowns: explicit requirements already stated by the user or discovered in existing code/docs
- Known unknowns: decisions the user has not made yet
- Unknown knowns: likely implicit preferences, conventions, taste, or "obvious once seen" expectations
- Unknown unknowns: risks, hidden dependencies, edge cases, domain assumptions, or validation gaps the user may not know to ask about
- Architecture-changing questions: 3-7 questions where the answer could change data models, APIs, security boundaries, UX flow, or rollout strategy

Use `unknowns.md` to drive Step 6. Ask the highest-impact architecture-changing question first, one question at a time when a single answer could materially redirect the plan. If there are no critical blockers, synthesize inferred answers and continue without a live interview.

### 6. Detailed Interview

See [interview-protocol.md](references/interview-protocol.md)

Run in main context. Informed by: initial spec + research findings + `unknowns.md`. Use the Question Tool Compatibility and Default no-stop policy above.

### 7. Save Interview Transcript

Write Q&A or inferred assumptions to `<planning_dir>/interview.md`. Include Soft Gate summaries even when no live questions were asked.

---

## Phase 2: Spec

Spec과 Persona를 합성하고, 도메인사전 v1 초안을 자동 생성하는 단계.

### 8. Write Initial Spec (Spec Synthesis)

Combine into `<planning_dir>/spec.md`:
- Initial input + research findings + interview answers + Test Scenarios

**필수 포함: Context Map 섹션** — interview.md의 Soft Gate 1 결과 또는 inferred summary에서 가져옴:

```markdown
## Context Map

### 공유 전제
- 목표: {궁극적 목표}
- 산업: {산업} | 범위: {MVP/풀/리뉴얼}
- 성공 기준: {성공의 정의}

### 이해관계자
| 역할 | 설명 | 관련 섹션 |
|------|------|-----------|
| {역할} | {설명} | (Step 19에서 backfill) |

### 시스템 역할 (Role Inventory) — 이후 모든 산출물의 역할명 정본
이해관계자와 **다른 표**입니다. 이해관계자에는 시스템에 로그인하지 않는 의사결정자(구매 결정자, 스폰서)가 포함되고, 반대로 시스템에만 존재하는 주체(배치 서비스 계정, 슈퍼관리자, 비로그인 방문자)는 이해관계자에 안 잡힙니다. 여기에는 **인증 주체로 시스템에 존재하는 역할만** 적습니다.

| 역할 ID | 표시명 | 주요 업무 | 금지 행동 | 화면 | 인증 주체 | 상위 역할 |
|---------|--------|-----------|-----------|------|-----------|-----------|
| {superadmin} | {슈퍼관리자} | 전 기능 접근 | - | 공용 | 사람 | - |
| {admin} | {관리자} | {업무} | {금지} | {공용 권한차등 / 별도 화면} | 사람 | superadmin |
| {guest} | {비로그인} | {공개 페이지 열람} | 쓰기 전체 | 공용 | 익명 | - |

- 출처는 Step 6 인터뷰의 **C-R 블록**(역할 목록 / 역할별 업무 / 화면 분리 / 금지 행동)입니다. 인터뷰가 비어 있으면 여기서 지어내지 말고 `[inferred]`로 표시합니다.
- `역할 ID`는 영문 소문자 식별자이며 Step 16~21의 DB·API·도면·운영 시나리오가 **이 값을 그대로** 사용합니다. 어느 하위 문서에서도 새 역할을 만들지 않습니다.
- 기본 적용(`[inferred]`): 전 기능 접근 역할 1개를 항상 두고, 상위 역할은 하위 역할 권한을 포함하며, 본인이 만든 데이터는 본인이 조회·수정합니다. 예외가 확인되면 그 역할 행에 명시합니다.
- `화면` 열이 '별도 화면'인 역할이 있으면 Step 19 섹션 분할에서 해당 화면을 독립 섹션으로 잡습니다.
- 도메인사전 v3에 역할 용어가 등재되면 표기(한글 표시명)는 사전을 따르되, **식별자 정본은 이 표**입니다. 사전이 `NOT APPLICABLE`(핵심 용어 5개 미만)이어도 이 표는 독립적으로 유효합니다.
- 인증이 없거나 역할이 1개뿐이면 `NOT APPLICABLE: single role`로 기록하고 이후 RBAC 산출물을 모두 생략합니다.

### 에코시스템 맵
| 시스템 | 대상 | 연동 방식 | 관련 섹션 |
|--------|------|-----------|-----------|
| {시스템} | {대상} | {내장/외부API/제외} | (Step 19에서 backfill) |

### 기존 환경
{기술 스택, 기존 코드, 인프라 요약}
```

**필수 포함: Problem Statement 섹션** — interview.md의 Soft Gate 2 결과 또는 inferred summary에서 가져옴:

```markdown
## Problem Statement

| # | 핵심 문제 | 영향 | 우선순위 | 해결 섹션 |
|---|-----------|------|----------|-----------|
| P1 | {문제} | {영향} | 🔴 필수 | (Step 19에서 backfill) |
| P2 | {문제} | {영향} | 🟠 중요 | (Step 19에서 backfill) |
```

> Context Map과 Problem Statement의 '관련 섹션'/'해결 섹션' 열은 Step 19에서 backfill됩니다.
> 이 두 섹션은 다운스트림(섹션 분할, argos 감리)에서 추적성 검증의 앵커로 사용됩니다.

**필수 포함: Risk Assessment 섹션**

| 위험 요소 | 영향도 | 발생 확률 | 완화 전략 |
|-----------|--------|-----------|-----------|
| {기술적 위험} | High/Med/Low | High/Med/Low | {대응 방안} |

**조건부 생성: Design System** — 인터뷰 Phase S-1(디자인 비전)이 수집되었거나 spec/research/unknowns에서 추론 가능한 경우:
See [design-system-guide.md](references/design-system-guide.md)
UI 분기에 진입하면 위 resolver로 `frontend-design`을 지연 해석해 `frontend_design_root`를 만들고,
가이드가 지정한 blacklist reference를 그 루트에서 읽습니다. `<planning_dir>/design-system.md` 생성.
UI/프론트엔드가 없는 프로젝트는 `NOT APPLICABLE`로 기록합니다.

**필수 포함: Test Scenarios 섹션** — 각 주요 기능마다 정상/에러/엣지 케이스.
See [test-scenario-guide.md](references/test-scenario-guide.md)

**Step 8 끝부산물 — 도메인사전 v1 초안 생성** (사용자 개입 없음):
spec.md 작성 직후 위 resolver로 `domain-dictionary` 행의 정확한 `SKILL.md`를 읽고,
`${domain_dictionary_root}/references/global-sync.md`를 읽은 뒤 컨텍스트 모드 계약을 직접 수행합니다.
등록 스킬 또는 이름 기반 slash command를 호출하지 않습니다. 입력은 spec.md + interview.md입니다.
글로벌 사전(`~/.agent-memory/domain-dictionaries/{도메인}.md`, `AGENT_DOMAIN_DICTIONARY_HOME`
override 가능)이 있으면 명확히 맞는 후보 용어만 자동 시드하고, 애매한 후보는
`[inferred-skip]`로 델타에 기록합니다. 글로벌이 비어있으면 사용자 개입 없이 프로젝트
사전만 만듭니다. 산출물은 마스터(`docs/domain-dictionary.md`, 신규 또는 갱신)와 델타
(`<planning_dir>/domain-dictionary-delta.md`)입니다. 모듈을 성공적으로 읽은 뒤 핵심 용어가
5개 미만이면 계약에 따라 `NOT APPLICABLE: fewer than 5 core terms`를 델타에 기록하고 진행합니다.
모듈을 읽지 못한 상태는 건너뛰기가 아니라 위의 `BLOCKED`입니다.

### 9. User Persona & Journey Map

See [persona-journey-guide.md](references/persona-journey-guide.md)

인터뷰와 리서치 결과를 기반으로 페르소나(2~4개)와 여정맵 생성.
UI/프론트엔드가 없는 프로젝트는 자동 건너뜀.

**출력:** `<planning_dir>/personas-and-journeys.md`

---

## Phase 3: Domain

전문가 분석으로 도메인을 깊이 이해하고, 사전을 v3까지 확정하는 단계.

### 10. Multi-Expert Team Analysis

See [team-review-protocol.md](references/team-review-protocol.md)

**⚠️ CONTEXT MANAGEMENT**: This step runs 6 bounded work items. Consider `/compact` before launching.

**Default execution profile:** time-boxed standard mode. Deep domain research runs only when the feature is clearly domain-heavy (regulated industry, safety-critical workflow, payment/medical/finance/logistics/manufacturing integrations) or the user explicitly asks for deep research.

**Phase A — 4개 병렬:** UX / Architecture / Red Team / Domain Research

- Domain Researcher first performs domain-complexity triage.
- Low-complexity projects write a short `domain-research.md` stub without web search.
- Medium/high-complexity projects use bounded, non-duplicative research only. Do not redo Step 5.

**Phase B — 2개 병렬 (Phase A 완료 후):** Domain Process Expert / Domain Technical Expert

- Domain experts do not perform fresh web research by default.
- They synthesize `spec.md`, `interview.md`, `research.md`, `domain-research.md`, and `docs/domain-dictionary.md`.
- External AI domain experts are time-boxed; timeout/failure falls back to the runtime's `artifact-writer`, then to sequential main-context execution or a warning stub.

> Phase B 실행: Codex/Antigravity 외부 CLI가 가용하면 분배하고, 없거나 실패하면 현재 CLI의 `artifact-writer` 역할로 실행합니다.

**CRITICAL — Work-item return protocol:** Each writer owns one unique file and returns ONLY a 2-3 line summary. Main/Lead alone writes `team-review.md` and dictionary merges.

**도메인사전 컨텍스트 주입:** 6명 전문가 모두에게 Step 8에서 생성된 사전 v1을 컨텍스트로 전달합니다. 전문가들은 같은 어휘로 분석하며, 분석 중 발견한 신규 용어/정의 다듬음/모호성을 결과물 끝 `## Dictionary Updates` 섹션에 기록합니다. 자세한 프롬프트는 [team-review-protocol.md](references/team-review-protocol.md) 참조.

Results → `<planning_dir>/team-reviews/` (개별 6개) + `<planning_dir>/team-review.md` (통합).

**Step 10 끝부산물 — 도메인사전 v2 자동 병합** (사용자 개입 없음):
Step 8에서 읽은 `domain-dictionary` 계약을 유지한 상태에서 6개 전문가의
`## Dictionary Updates` 섹션을 추출하여 v1 → v2로 자동 병합. ADD(신규 추가)/REFINE(정의 다듬음)/MERGE(동의어 통합)는 자동 적용, CONFLICT(전문가 간 의견 갈림)는 자동 병합하지 않고 Step 11로 미룸. 갱신 대상: `docs/domain-dictionary.md` + `<planning_dir>/domain-dictionary-delta.md`.

### 11. Domain Conflict Resolution and Dictionary Finalization

See [domain-confirmation-guide.md](references/domain-confirmation-guide.md)

**Step 11은 자동 통합이 기본입니다.**

일반 도메인 전문가 제안, ADD/REFINE/MERGE 사전 변경, 명확한 글로벌 사전 후보는 보수적 기준으로 자동 채택 또는 보류하고 이유를 기록합니다. 사용자에게 묻는 경우는 다음뿐입니다.

1. **충돌 용어** — DB/API/타입/화면 문구에 들어갈 핵심 용어가 둘 이상으로 갈리고, 자동 통일이 이후 산출물을 크게 바꿀 때
2. **정책성 제안** — 보안, 개인정보, 결제, 법적 책임, 운영 프로세스를 바꾸는 제안일 때
3. **글로벌 사전 반영** — 전역 사전에 쓰기 작업을 해야 하는데 프로젝트 특수 용어인지 범용 용어인지 판단이 불가능할 때

질문이 필요하면 한 번에 하나만 묻습니다. 그 외 항목은 `accepted-by-default`, `deferred-by-default`, `inferred-skip` 중 하나로 `<planning_dir>/domain-dictionary-delta.md`와 `team-review.md`에 기록하고 계속 진행합니다.

**Step 11 끝부산물 — 도메인사전 v3 최종화**:
로드한 `domain-dictionary` 계약에 따라 마스터(`docs/domain-dictionary.md`)를 v3로 확정,
델타에 최종 변경 이력 기록, 글로벌 반영 항목은 출처 메타데이터와 함께 추가합니다. 전역 쓰기가 애매하면 전역 반영을 건너뛰고 프로젝트 사전만 확정합니다.

**Phase 4 이후로 이 사전은 변경되지 않습니다.** Plan, DB Schema, API Spec, Sections는 모두 v3을 따릅니다.

---

## Phase 4: Plan

전략 후보 비교·선택 → 상세 구현 계획 수립 + 외부 LLM 리뷰 + 사용자 검토 단계.

### 12. Generate Implementation Plan (전략 후보 비교 → 선택 → 작성)

**Inputs:** `spec.md` + `team-review.md` + `domain-process-analysis.md` + `domain-technical-analysis.md`

단일 계획을 선형으로 바로 쓰지 않는다. 넓은 설계 결정은 **후보를 만들어 채점한 뒤 고른다(Tree of Thoughts).**
plan.md 하나를 바로 쓰면 외부 리뷰(Step 13)는 "그 하나"를 다듬을 뿐, 더 나은 접근 자체를 놓친다.

**12a. 전략 후보 2-3개 생성** — 서로 *다른 접근*이어야 한다(동일 계획의 변주 금지). 예: 점진적 스트랭글러 vs 빅뱅 재작성, 모놀리식 우선 vs 모듈 경계 우선, 자체 구현 vs 외부 의존. 분기의 독립성을 위해 **return-only `read-only-analysis` 작업으로 각 후보를 생성**하는 것을 권장(앵커링 방지). 각 후보는 6-10줄 개요: 핵심 접근, 주요 컴포넌트, 시퀀싱, 가정. Main/Lead만 후보를 채점·통합하고 `plan.md`를 작성합니다.

**12b. 루브릭 채점** — 후보를 아래 기준으로 1-5점 채점(표로 출력). 감이 아니라 **근거 한 줄씩**. 채점 없이 후보만 나열하고 끝내지 않는다.

| 기준 | 무엇을 보나 |
|------|------------|
| 요구사항 충족 | spec.md Problem Statement(P1/P2) + team-review Critical Findings를 얼마나 커버 |
| 도메인 적합성 | domain-process/technical 분석 및 사전 v3와 정합 |
| 리스크/복잡도 | 실패 표면·미지수가 적을수록 고점 |
| 점진성·되돌리기 | 작은 단위로 배포·검증·롤백 가능할수록 고점 |
| 노력/비용 | 구현 규모가 작을수록 고점 |

**12c. 선택 + 작성** — 최고점 후보를 채택하되, 차점 후보의 더 나은 아이디어는 흡수(graft)한다. 동점이거나 트레이드오프가 첨예하면 그 사실을 명시.
선택한 전략으로 상세 계획을 작성 → `<planning_dir>/plan.md`. Address all "Critical Findings", Step 11에서 채택된 항목만 반영. Write for an unfamiliar reader — fully self-contained document.

**plan.md 필수 머리 섹션 — `## 전략 선택 (Strategy Decision)`:** 채택 전략 + 채점표 + 기각한 후보와 사유 + (해당 시) 남은 트레이드오프를 기록한다. 이는 외부 리뷰(Step 13)·감리(argos)가 "왜 이 접근인가"를 검증하는 앵커이며, 후속 세션이 결정을 되짚을 수 있게 한다.

### 13. External Review

See [external-review.md](references/external-review.md)

Run the **Antigravity** and **Codex** external CLI review processes in parallel when available. Treat them as independent review processes, not native delegation workers.
Each process writes only its unique file under `<planning_dir>/reviews/`; Main/Lead owns feedback integration and all edits to `plan.md`.

### 14. Integrate External Feedback

Analyze `<planning_dir>/reviews/`. You are the authority on what to integrate.

1. Write `<planning_dir>/integration-notes.md` (통합/미통합 이유 기록)
2. Update `<planning_dir>/plan.md` with integrated changes

### 15. Integrated Plan Checkpoint

Do not stop for plan approval by default. Write `<planning_dir>/integration-notes.md`, update `<planning_dir>/plan.md`, and continue to Step 16.

Stop here only when:
- the user explicitly asked for a plan review gate before detailed design
- the external reviews expose an unresolved critical contradiction
- the remaining decision would materially change architecture, data model, security boundary, UX flow, rollout strategy, or compliance handling

When stopping is required, ask one plain-text question that names the blocking decision and the recommended default.

---

## Phase 5: Design

DB 스키마, API, 공정 도면, 섹션을 모두 도메인사전 v3에 따라 작성하는 단계.

### 16. Generate Database Schema

See [schema-design-guide.md](references/schema-design-guide.md)

**Inputs:** `domain-process-analysis.md` + `domain-technical-analysis.md` + `plan.md`
**Output:** `<planning_dir>/db-schema.md` (ERD + DDL + Design Rationale + Index Strategy)
**Process:** DB 감지 → 엔티티 추출 → 관계 분석 → DB 특성 반영 → 정규화 → ERD/DDL/인덱스

DB가 없는 프로젝트(CLI, 라이브러리, 정적사이트)는 자동 건너뜀.

### 17. Generate API Specification

See [api-spec-guide.md](references/api-spec-guide.md)

**Inputs:** `plan.md` + `db-schema.md` + 화면 재료(`spec.md` 시스템 역할 표의 `화면` 열, `personas-and-journeys.md` 터치포인트, `design-system.md`, `research.md` 메뉴 구조 중 있는 것)
**Output:** `<planning_dir>/api-spec.md` (Conventions + Screen Data Requirements + Endpoints + Summary)
**Process:** 화면 데이터 요구 표 → 엔드포인트 도출(DB CRUD + 화면이 쓰는 조인·집계 조회) → Conventions 적용(목록 페이지네이션·정렬 허용 컬럼, 공통 에러 형식) → 목록 필터·정렬 컬럼(서버 고정 조건 포함)을 `db-schema.md` 인덱스 표·DDL에 backfill → 화면↔API 대응 검사

DB 테이블에서만 엔드포인트를 뽑으면 화면이 쓰는 데이터가 빠져 구현 중 백엔드를 다시 만들게 되므로, 화면 요구 표를 먼저 씁니다. 재료에 없는 화면은 지어내지 않습니다.
각 엔드포인트: Method + Path, Request/Response 스키마, Auth(방식 + **허용 역할 목록**), Frontend Caller, 목록이면 Pagination·Sort·Filter·Index 포함.
UI가 없는 API 서버는 화면 표를 `NOT APPLICABLE: no UI`로 두고 소비자별 호출 시나리오로 대체합니다.
역할이 둘 이상이면 Authentication에 Roles 표를 두고 Summary 표에도 허용 역할 열을 포함합니다. 역할명은 `spec.md`의 시스템 역할 표(Role Inventory) 역할 ID를 그대로 씁니다.
API 없는 프로젝트(정적사이트, CLI)는 자동 건너뜀.

### 18. Generate Process Flow Diagrams (공정 도면) — MANDATORY

See [flow-diagrams-guide.md](references/flow-diagrams-guide.md)

> **⚠️ 이 단계는 건너뛸 수 없습니다.** 공정 도면이 없으면 다이달로스(workpm)가 기준선 없이 시공하게 됩니다.

Step 18 진입 시 위 resolver로 `flow-verifier`와 `mermaid-diagrams`의 정확한 `SKILL.md`를
모두 읽습니다. plan 모드와 Mermaid 문법 계약을 직접 적용하며 등록 스킬이나 slash command를
호출하지 않습니다. 어느 모듈도 읽지 못하면 Step 18은 `BLOCKED`이고 Step 19로 진행하지 않습니다.

`plan.md` + `api-spec.md` + `domain-process-analysis.md`에서 핵심 프로세스 추출 → Mermaid 다이어그램 작성.
각 프로세스를 별도 `artifact-writer` 작업으로 생성 → `<planning_dir>/flow-diagrams/{process-name}.mmd`에 저장. Main/Lead만 `flow-diagrams/index.md`를 작성합니다.

**타입 3종** (가이드 1-1 참조) — flowchart는 기본, 나머지 둘은 조건 충족 시 추가:

| 타입 | 조건 |
|------|------|
| `flowchart` | 모든 완결 흐름 (기본, 필수) |
| `stateDiagram-v2` | 엔티티 상태 필드 + 전이 3개 이상 |
| `sequenceDiagram` | 에코시스템 맵에 외부 시스템 + 호출 순서가 설계에 영향 |

**역할 레인** — 관여 역할이 둘 이상인 flowchart는 `subgraph {역할명}`으로 레인을 나누고, 권한 분기와 거부 경로(숨김/비활성/읽기전용/403/404 위장)를 종료 노드까지 그립니다. 역할명은 `spec.md`의 시스템 역할 표(Role Inventory) 역할 ID를 그대로 쓰며 여기서 새로 만들지 않습니다.

**출력:** `{process-name}.mmd` 파일들 + `flow-diagrams/index.md` (타입·역할 레인·미생성 타입 사유 포함)

### 19. Create Section Index

**⚠️ GATE CHECK:** `flow-verifier`와 `mermaid-diagrams` 상태가 모두 `LOADED`이고
`flow-diagrams/index.md`가 존재하는지 확인 → 아니면 Step 18로 돌아가거나 `BLOCKED` 보고.

See [section-index.md](references/section-index.md)

Read `plan.md`. Identify natural section boundaries → create `<planning_dir>/sections/index.md`.
**CRITICAL:** index.md MUST start with a SECTION_MANIFEST block.

**경계 규칙** — 섹션은 **기능 수직 분할**이 기본입니다. 한 섹션이 그 기능의 데이터·API·화면·테스트를
모두 소유해야 나중에 기능 하나를 열어서 고칠 수 있습니다. 레이어 분할(`api-layer`, `frontend`)은
기능을 흩뿌리므로 금지하고, 기존 코드베이스가 이미 레이어로 강제된 경우에만 사유와 함께 허용합니다.
공유 기반 섹션은 둘 이상의 기능 섹션이 실제로 공유하는 것만 만들고 `Shared Foundation Rationale`에
공유 섹션 목록을 기록합니다. `spec.md` 시스템 역할 표에서 `화면` 열이 '별도 화면'인 역할은 독립 섹션입니다.

**Harness** — index.md에 `## Harness` 절로 런타임 조립 지점을 기록합니다. 의존성 그래프는 빌드
순서이고 하네스는 조립이라 서로 다릅니다. **기존 조립 지점(라우터·DI 컨테이너·플러그인 레지스트리·
이벤트 버스)을 먼저 찾아 사용**하고, 없을 때만 새로 만들되 근거를 남깁니다. 각 기능 섹션은 정확히
하나의 조립 지점에 등록합니다. 조립 지점이 없는 프로젝트는 `NOT APPLICABLE: single composition point`.

**CPS Backfill:** SECTION_MANIFEST 생성 후, 반드시:
1. **에코시스템 커버리지 체크** — spec.md의 Context Map → 에코시스템 맵의 모든 시스템이 섹션에서 커버되는지 확인. See [section-index.md](references/section-index.md) Ecosystem Coverage Check.
2. **spec.md backfill** — Context Map의 '관련 섹션' 열과 Problem Statement의 '해결 섹션' 열을 실제 섹션명으로 업데이트.

---

## Phase 6: Validation

섹션 파일 작성, 운영/QA 시나리오, 후속 스킬 발견, 최종 보고 단계.

### 20. Write Section Files — Parallel Artifact Writers

See [section-splitting.md](references/section-splitting.md)

1. Parse `sections/index.md`의 SECTION_MANIFEST
2. 의존성 레이어별로 섹션을 묶고, 한 번에 최대 3개 `artifact-writer` 작업만 병렬 실행. 각 writer는 할당된 섹션 파일 하나만 쓰기
3. `Overloaded`/timeout이 나면 실패한 섹션만 단일 writer 작업으로 재시도
4. 각 섹션 파일은 **완전 자립형** (Background, Requirements, Dependencies, **Module Contract**, Reference Libraries, Implementation, Test Scenarios, Implementation Strategy, Quality Gate, Risk & Rollback, Acceptance Criteria, Files 포함)
5. `Module Contract`는 Provides / Consumes / Owns / Composition Point를 채웁니다. Provides가 비면 모듈이 아니라 다른 섹션의 내부 작업이므로 합치고, Owns가 다른 섹션과 겹치면 공유 기반 섹션으로 올립니다

Wait for each batch to complete before launching the next batch.

### 21. Generate Operation Scenarios — Artifact Writer

See [operation-qa-guide.md](references/operation-qa-guide.md)

**출력:** `<planning_dir>/operation-scenarios.md` (역할 정의 + **RBAC 매트릭스**(역할 x 리소스 x CRUD) + **거부 동작 표** + 메뉴별 시나리오 + E2E 시나리오 + 화면 흐름도)
역할이 1개뿐이거나 인증이 없으면 매트릭스와 거부 동작을 `NOT APPLICABLE: single role`로 기록합니다.
이 파일만 쓰는 `artifact-writer`로 실행하고, 위임 불가 시 메인 컨텍스트에서 순차 작성합니다.

### 22. Generate QA Scenarios Document — Artifact Writer

See [operation-qa-guide.md](references/operation-qa-guide.md)

**운영 시나리오를 기반으로** QA 테스트 케이스 생성 → `<planning_dir>/qa-scenarios.md`
(메뉴별 테스트 + E2E + 통합 테스트 + Summary)
이 파일만 쓰는 `artifact-writer`로 실행하고, 위임 불가 시 메인 컨텍스트에서 순차 작성합니다.

### 22A. Consolidate Acceptance Checklist

See [acceptance-checklist-guide.md](references/acceptance-checklist-guide.md)

섹션 파일의 Acceptance Criteria(정본)를 `<planning_dir>/checklist.md` 한 표로 모읍니다. 설계와 구현이 같은 ID로 완료 기준을 주고받는 약속이며, 구현 하네스는 이 파일을 기준으로 `checklist-status.md` 장부를 채웁니다.
1. 섹션 순서대로 각 AC의 ID·완료 기준·근거·검증을 옮깁니다. 새 기준을 지어내거나 문장을 고치지 않습니다.
2. `qa-scenarios.md`에서 이 AC를 `관련 AC`로 가리키는 QA ID를 검증 열에 덧붙입니다.
3. 문제(P)별로 어느 AC가 맡는지 `## 추적 요약`을 만듭니다.
빠진 근거·검증은 여기서 채우지 않고 Step 23 검사로 넘깁니다. Main/Lead가 직접 쓰고, 위임하지 않습니다.

### 23. Final Status

Verify all files were created successfully:
- `research-decision.md` and `unknowns.md` (Discovery trace)
- All section files from SECTION_MANIFEST
- `spec.md`에 `## Context Map`과 `## Problem Statement` 섹션이 있는지 확인
- Context Map/Problem Statement의 '관련 섹션'/'해결 섹션' 열이 backfill되었는지 확인
- `flow-diagrams/*.mmd` + `flow-diagrams/index.md` (**필수** — 없으면 Step 18 미실행)
- **역할명 정합성** — `spec.md` 시스템 역할 표를 기준으로 `db-schema.md` roles/permissions, `api-spec.md` 허용 역할, `flow-diagrams` 역할 레인, `operation-scenarios.md` RBAC 매트릭스가 같은 역할 ID를 쓰는지. 하위 문서에만 있는 역할이 발견되면 **역할 누락 신호**이므로 `spec.md` 시스템 역할 표에 역으로 추가(backfill)하고 `integration-notes.md`에 기록. 시스템 역할 표가 `NOT APPLICABLE: single role`이면 이 검사를 건너뜀
- **완료 기준 계약** — 아직 설계 단계이므로 젭마인이 직접 고친다(구현 시작 뒤에만 적용되는 가이드의 '계약 변경' 승인 규칙은 여기서는 해당 없음). 검사와 처리:
  - `checklist.md` 행 = 섹션 AC의 합집합(ID 중복·누락 없음, 형식 `AC-NN-k`) — 어긋나면 섹션 기준으로 다시 만든다
  - 모든 문제(P)에 AC 1개 이상 — 없으면 spec.md Problem Statement의 '해결 섹션'에 AC를 추가한다(다음 순번 k). '해결 섹션'이 `-`라 맡을 섹션이 없으면 계획 공백이므로 `integration-notes.md`에 `미배정 문제`로 기록하고 Step 24 출력에 표시한다
  - 모든 AC에 근거·검증 1개 이상 — 섹션 Test Scenarios·QA에서 찾을 수 있으면 채우고, 없으면 `검증 미정`을 남긴 채 `integration-notes.md`와 Step 24 출력에 경고한다
  - 모순되는 AC 쌍(같은 대상·입력에 다른 기대 결과)이 없는지 — 있으면 설계 결정이므로 Step 15의 정지 규칙대로 권장 기본값을 붙인 한 문장 질문으로 정하고(질문할 수 없는 자동 실행이면 권장 기본값을 쓰고 기록), 진 쪽 AC는 `(삭제 — 사유)`로 남긴다
  - `qa-scenarios.md`의 `관련 AC`가 실재하는 ID인지 — 아니면 QA 쪽을 고친다(맞는 AC로 바꾸거나, 그 동작이 약속이어야 하면 섹션에 AC를 추가)
  - `## 추적 요약`의 문제→섹션이 spec.md Problem Statement '해결 섹션'과 어긋나면 spec을 backfill한다
  섹션이나 QA를 고쳤으면 `checklist.md`를 다시 만들고 무엇을 왜 고쳤는지 `integration-notes.md`에 기록한다
- **화면↔API 대응** — `api-spec.md`의 Screen Data Requirements 기준으로 모든 표시 데이터·액션이 엔드포인트에 대응하는지, 모든 엔드포인트에 Frontend Caller(또는 `external`/`webhook`/`batch`/`system`, 화면 재료가 빠지면 `TBD (화면 누락)` + 미결)가 있는지, 모든 목록 엔드포인트가 Pagination을 선언하고 필터·정렬 컬럼이 `db-schema.md` 인덱스 표에 있는지, 에러 응답이 공통 에러 형식인지. 빠진 것은 두 문서에 보완하고 `integration-notes.md`에 기록. 화면 표가 `NOT APPLICABLE: no UI`이면 Pagination·인덱스 검사만 수행
- **모듈 경계와 하네스** — `sections/index.md`에 `## Harness`가 있고(또는 `NOT APPLICABLE: single composition point`), 모든 기능 섹션이 `Module Contract`의 Provides/Consumes/Owns/Composition Point를 채웠는지. Owns가 겹치는 섹션 쌍이 있으면 병렬 구현 충돌 신호이므로 공유 기반으로 올리고 기록. 레이어 분할을 썼으면 `Shared Foundation Rationale`에 사유가 있는지
- `api-spec.md` (API가 있는 프로젝트)
- `db-schema.md` (DB가 있는 프로젝트)
- `design-system.md` + `personas-and-journeys.md` (UI가 있는 프로젝트)
- `operation-scenarios.md` + `qa-scenarios.md`
- `checklist.md` (완료 기준 계약 — 구현 하네스가 `checklist-status.md` 장부로 이행)
- `team-reviews/domain-research.md` + `domain-process-analysis.md` + `domain-technical-analysis.md`
- `docs/domain-dictionary.md` + `<planning_dir>/domain-dictionary-delta.md`, 또는 모듈 계약이
  허용한 5개 미만 용어의 명시적 `NOT APPLICABLE` delta
- 내부 모듈 상태: `domain-dictionary`, `flow-verifier`, `mermaid-diagrams`, 조건부
  `frontend-design` 각각
  `LOADED`/`NOT APPLICABLE`/`BLOCKED` 중 하나 (`BLOCKED`가 있으면 Planning Complete 금지)

### 24. Output Summary

```
ZEPHERMINE: Planning Complete

Generated: research-decision/unknowns/research/interview/spec/domain-dictionary/
           personas-and-journeys/team-review/plan/
           api-spec/db-schema/design-system/integration-notes/
           operation-scenarios/qa-scenarios/checklist.md
           + team-reviews/ + reviews/ + flow-diagrams/ + sections/

Acceptance checklist: checklist.md — M개 AC / 미배정 문제 {없음 | P3, …} / 검증 미정 {0 | AC-02-2, …}

Implementation options:
  A. /agent-team <planning_dir> → 섹션 기반 병렬 구현 (권장)
  B. /chronos <planning_dir>    → 자율 반복 구현 루프
  C. Manual: sections/index.md  → 순서대로 수동 구현
  D. /argos <planning_dir>      → 감리 (설계 대비 구현 검증)

Design (design-system.md가 생성된 경우):
  /aphrodite <planning_dir>     → 디자인 시스템 정교화 (DB 기반 팔레트/폰트/스타일 매칭)

Other options:
  /estimate <planning_dir>      → 개발 견적서 (비용 산정이 필요한 경우)
```

### 25. Discover Implementation Skills

1. `plan.md`와 `sections/section-*.md`에서 기술 스택 키워드 추출
2. `Glob("skills/*/SKILL.md")`로 이미 설치된 스킬 확인 + 키워드 매칭
3. 미매칭 주요 키워드(최대 5개): `npx skills find "{keyword}"`
4. 이미 설치된 관련 스킬 + 새로 설치 가능한 스킬 목록 출력
5. 설치는 묻지 않고 권장 목록만 출력합니다. `npx skills add ...` 같은 전역 설치 명령은 사용자가 명시적으로 설치를 요청한 경우에만 실행합니다.

> 검색 결과가 없거나 모든 관련 스킬이 설치되어 있으면 자동 건너뛰기.

### 26. 감리 안내

```
✅ 젭마인 설계 완료!

📦 산출물: operation-scenarios.md, qa-scenarios.md, checklist.md (완료 기준 계약), sections/

👉 다음 단계 (선택):
  /aphrodite           → 디자인 시스템 정교화 (design-system.md가 있는 UI 프로젝트에서 권장)
  /agent-team          → 섹션 기반 병렬 구현 (Codex에서는 agent-team-codex로 해석, 권장)
  /chronos             → 자율 반복 구현 루프
  수동 구현             → 직접 코딩
  /argos <planning_dir> → 구현 후 감리 (설계 대비 준공검사)

📎 참고: docs/workflow-guide.md
```

> **참고:** 검증(감리)은 설계사와 감리의 역할 분리 원칙에 따라 `/argos`로 독립되었습니다.

---

## References

| 파일 | 내용 |
|------|------|
| [research-protocol.md](references/research-protocol.md) | Step 4-5 리서치 결정 기준, 위임 작업 프롬프트 |
| [interview-protocol.md](references/interview-protocol.md) | Step 6 Critical 질문 기준, 추론형 인터뷰 전략 |
| [test-scenario-guide.md](references/test-scenario-guide.md) | Step 8 테스트 시나리오 형식, 케이스 작성 기준 |
| [design-system-guide.md](references/design-system-guide.md) | Step 8 디자인 시스템 문서 구조 |
| [persona-journey-guide.md](references/persona-journey-guide.md) | Step 9 페르소나/여정맵 형식 상세 |
| [team-review-protocol.md](references/team-review-protocol.md) | Step 10 전문가별 분석 프롬프트, Phase A/B 상세 |
| [domain-confirmation-guide.md](references/domain-confirmation-guide.md) | Step 11 도메인 전문가 제안 + 사전 변경 + 글로벌 반영 충돌 해결 |
| [external-review.md](references/external-review.md) | Step 13 Antigravity/Codex 외부 리뷰 프롬프트 |
| [schema-design-guide.md](references/schema-design-guide.md) | Step 16 DB 스키마 설계 절차, ERD/DDL 형식 |
| [api-spec-guide.md](references/api-spec-guide.md) | Step 17 API 명세 형식, 엔드포인트 작성 규칙 |
| [flow-diagrams-guide.md](references/flow-diagrams-guide.md) | Step 18 공정 도면 생성 절차, Mermaid 규칙 |
| [section-index.md](references/section-index.md) | Step 19 SECTION_MANIFEST 형식, 의존성 그래프 |
| [section-splitting.md](references/section-splitting.md) | Step 20 섹션 파일 완전 자립형 형식 |
| [operation-qa-guide.md](references/operation-qa-guide.md) | Step 21-22 운영/QA 시나리오 구조 |
