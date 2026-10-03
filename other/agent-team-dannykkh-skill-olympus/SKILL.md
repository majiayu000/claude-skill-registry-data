---
name: agent-team
description: >
  zephermine 섹션 기반 네이티브 멀티에이전트 오케스트레이션. 의존성 분석, Wave 그룹핑,
  파일 소유권 분리, 병렬 구현과 통합 검증을 수행한다. Claude, Codex, Antigravity, Grok의
  내장 탐색자·작업자를 사용하며 /agent-team 또는 /poseidon으로 실행한다. Antigravity의
  일반 장기 팀 작업은 가용하면 /teamwork-preview를 우선하고, 이 스킬은 Olympus Wave·소유권·검증 계약이 필요할 때 사용한다.
---

# Agent Team — Zephermine 섹션 병렬 실행

> **포세이돈(Poseidon)**: 젭마인 산출물을 받아 체계적으로 구현합니다.
> 바다의 신 포세이돈이 파도(Wave)를 일으키듯, 섹션 의존성을 Wave 단위로 정렬하고
> teammate들을 병렬로 출항시킵니다.

zephermine이 생성한 섹션(sections/)의 의존성 그래프를 분석하여 Wave 단위로 teammate에게 배정하고 병렬 실행합니다.

## 다이달로스 vs 포세이돈

| 상황 | 사용할 도구 |
|------|-----------|
| **젭마인 없이** 바로 구현 시작 | **다이달로스** (`/daedalus`) — 직접 리서치 → 제안 → 구현 |
| **젭마인 산출물**(sections/) 기반 구현 | **포세이돈** (`/agent-team` 또는 `/poseidon`) — 섹션 파싱 → Wave → 구현 |

## Lead(PM) 핵심 원칙

> 다이달로스의 PM 철학을 포세이돈 Lead에도 적용합니다.

### 1. 조건부 외주화 — 병렬 이득이 있을 때 Lead는 조율한다

Lead의 기억 공간이 전체 작전을 기억하는 **유일한 곳**이다.
코드까지 짜면 기억이 순식간에 꽉 찬다.
작업자가 가용하고 파일 범위가 독립적이면 코딩·리서치를 위임합니다. 작업자가 없거나 같은 파일을 순차 수정해야 하면 Lead가 실행자 역할도 소유합니다.

### 2. 기억 외부화 — 기억력을 믿지 마라

대화가 길어지면 오래된 내용이 자동 압축된다.
**중요한 결정이 나올 때마다 activity log에 즉시 기록한다.**

### 3. 체크리스트 완수 — 모든 Acceptance Criteria가 통과할 때까지 끝이 아니다

젭마인 산출물에는 섹션별 **Acceptance Criteria**(체크리스트)와 **flow-diagrams**(공정 도면)이 있다.
teammate가 "완료"라고 보고해도 Lead가 직접 체크리스트를 대조하여 **모든 항목이 통과할 때까지 반복**한다.
완료 기준은 젭마인이 ID를 붙여 고정한 `checklist.md`(약속)이고, 이행은 Lead가 `checklist-status.md` 장부에 증거와 함께 기록한다.
형식·상태·증거 규칙의 정본은 젭마인 `references/acceptance-checklist-guide.md`이다. 대화로만 대조하면 컨텍스트가 압축될 때 함께 사라지므로 장부에 남긴다.
한 번 구현하고 끝내는 것은 PM이 아니라 실행자다.

### Lead 운영 규율

**Lead가 직접 하는 것:**
- 젭마인 산출물 검토 (plan, sections, flow-diagrams, acceptance criteria)
- teammate 보고 수신 및 체크리스트 대조
- 의사결정 + activity log 기록
- teammate 배정/교체
- 미통과 항목 → teammate에게 재지시
- 네이티브 위임이 없거나 순차 실행이 더 안전한 작업의 직접 수행

**작업자가 가용한 병렬 경로에서 Lead가 하지 않는 것:**
- 작업자와 같은 파일을 동시에 수정
- 독립 작업자의 조사·테스트를 중복 실행
- 외부 검증 없이 완료 선언

**자기검증 3질문** — Wave 완료 보고 시 반드시 자문:
1. 가장 어려운 결정이 뭐였나?
2. Acceptance Criteria 중 위험한 항목은?
3. 도면과 실제 구현이 일치하는가?

### 팀원 관리 원칙

| 규칙 | 설명 |
|------|------|
| **파일 영역 분리** | 같은 파일을 두 teammate가 동시에 수정 금지 |
| **idle 방치** | teammate idle 알림이 와도 task 진행 중이면 절대 개입 안 함 |
| **교체 정책** | 다음 Wave가 이전 작업과 무관하면 → 새 teammate. 연장선이면 유지 |
| **이름 규칙** | 교체 시 같은 이름 재사용 불가 |

---

## CLI별 실행 모드

> **native-first 원칙** (learned/020): 실행 엔진은 각 CLI의 네이티브 멀티에이전트에 위임하고,
> orchestrator MCP는 네이티브가 없는 구버전 CLI의 폴백 + hard file-lock 정책 레이어로만 남긴다.

### Antigravity `/teamwork-preview` 경계

- 별도 `sections/`·Wave·파일 소유권·자재검사 산출물이 필요 없는 일반 장기·다중 에이전트 작업은,
  현재 플랜과 런타임에서 사용할 수 있으면 Antigravity 네이티브 `/teamwork-preview`가 소유합니다.
- 사용자가 `/teamwork-preview`를 명시적으로 시작했거나 현재 세션에 그 팀 상태가 이미 노출돼 있으면
  이를 실행 엔진으로 사용하고, Poseidon은 섹션 파싱·Wave ledger·파일 소유권·검증 게이트만 덧붙입니다.
- 이 스킬이 slash command를 프로그램적으로 호출할 수 있다고 가정하지 않습니다. 활성 팀 문맥이 없으면
  공식 `invoke_subagent`/`define_subagent`로 같은 계약을 수행하고, 그 기능도 없으면 메인 순차 실행으로 축소합니다.
- `/teamwork-preview`의 플랜·가용성 조건을 우회하거나 유료 기능을 자동 활성화하지 않습니다.

| CLI | 읽기 전용 탐색·검토 | 구현·명령 실행 | 팀 조율 |
|-----|--------------------|----------------|----------|
| **Claude** | 내장 `Explore` | 내장 `general-purpose` 또는 이름 있는 background teammate | Agent Teams가 활성화된 경우 `Agent` + shared task list + `SendMessage` |
| **Codex** | 내장 `explorer` | 내장 `worker` (`default`는 범용 폴백) | 현재 세션에 노출된 spawn/message/wait/interrupt 도구 |
| **Antigravity** | 내장 `research` | 활성 `/teamwork-preview` 팀 또는 메인/쓰기 도구를 명시한 사용자 정의 서브에이전트 | 활성 팀 상태나 `invoke_subagent` 반환을 Lead가 Wave ledger에 반영 |
| **Grok** | 내장 `explore` | 내장 `general-purpose` | subagent 호출 결과를 Lead가 Wave ledger에 반영 |

역할명은 **의미 계약**입니다. 읽기 전용 역할에는 파일 생성을 지시하지 않고, 구현 역할에는 담당 파일·검증 명령·완료 보고 형식을 함께 전달합니다. CLI별 도구 이름이나 인자 스키마가 달라지면 현재 런타임이 노출한 도구를 사용하며, 이 문서의 예시 이름을 억지로 호출하지 않습니다.

네이티브 위임이 없거나 실패하면 같은 Wave의 독립 작업을 메인 컨텍스트에서 순차 실행합니다. hard file lock, 외부 task ledger, 크로스-CLI 혼합이 실제로 필요할 때만 `workpm-mcp`를 선택합니다.

## Source-only internal module resolution (mandatory)

`code-reviewer`와 조건부 `orchestrator`는 포세이돈이 내부 정책으로 읽는 source-only
모듈입니다. 등록된 스킬이나 slash command로 호출하지 않습니다.

각 선택된 모듈을 다음 순서로 해석하고 처음 확인된 exact `SKILL.md` 파일 하나를 읽습니다.

1. 현재 프로젝트의 `skills/{name}/SKILL.md`가 실제로 있으면 그 exact 파일.
2. 없으면 현재 런타임 active root의 exact 파일: Claude/Grok은
   `~/.claude/skills/{name}/SKILL.md`, Codex는 `~/.codex/skills/{name}/SKILL.md`, Antigravity는
   `~/.gemini/antigravity-cli/skills/{name}/SKILL.md` (명시 opt-in 설치 지원).
3. 둘 다 없으면 현재 런타임 전역 카탈로그(Claude/Grok
   `~/.claude/SKILLS-CATALOG.md`, Codex `~/.codex/SKILLS-CATALOG.md`, Antigravity
   `~/.gemini/antigravity-cli/SKILLS-CATALOG.md`)에서 정확한 모듈명 행을 찾습니다. 행이 하나일 때만
   `읽을 경로`의 절대 `SKILL.md`를 읽고, 누락·중복 행은 fail-closed입니다. 기본 경로가
   `.olympus/source-skills` 아래여도 조합하거나 추측하지 않습니다.
4. `module_root`는 읽은 `SKILL.md`의 부모입니다. `references/`, `scripts/`, `commands/`는
   모두 이 루트에서 해석합니다.
5. Step 5 코드 리뷰 분기에 도달했을 때만 `code_reviewer_root`를 만듭니다. hard file lock,
   외부 task ledger, 크로스-CLI 혼합이 실제로 필요해 MCP 분기를 선택한 뒤에만
   `orchestrator_root`를 만들고 `${orchestrator_root}/commands/workpm-mcp.md`를 읽습니다.

이 exact 파일 읽기는 내부 모듈 로드입니다. 런타임 Skill 목록/레지스트리를 근거로 호출하거나
모듈 이름을 slash command로 실행하지 않습니다.

code-reviewer를 읽지 못하면 현재 CLI의 네이티브 review 1회와 아래 bounded 검수 항목만
실행하고 `policy module: NOT RUN (native fallback)` 및 게이트 `DEGRADED`를 기록합니다.
네이티브 review도 없으면 읽기 전용 작업자가 같은 bounded 항목을 점검하되 source module PASS를
주장하지 않습니다. orchestrator/MCP를 읽지 못하면 편집을 직렬화할 수 있는 범위만 메인 순차
경로로 축소하고 `MCP: NOT RUN`을 기록합니다. hard lock이 필수이면 해당 Wave는 `BLOCKED`입니다.
누락된 모듈을 조용히 PASS 처리하지 않습니다.

### CLI 감지 방법

Phase 0 시작 시 제품명보다 현재 도구 레지스트리를 우선합니다.

1. 읽기 전용 탐색 역할과 쓰기 가능한 작업 역할을 구분할 수 있는지 확인합니다.
2. 병렬 위임과 상태 회수가 모두 가능하면 네이티브 Wave 실행을 사용합니다.
3. 위임만 가능하고 병렬·중간 메시지가 보장되지 않으면 bounded sub-wave 또는 순차 위임으로 축소합니다.
4. 위임 도구가 없으면 메인 컨텍스트 순차 실행으로 계속합니다.
5. 병렬성이 필수이고 네이티브 경로가 없을 때만 `workpm-mcp`를 제안합니다.

## Prerequisites

### Claude 모드
- Agent Teams는 실험 기능이며 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`일 때만 사용합니다. 스킬이 전역 설정을 자동 변경하지 않습니다.
- Claude Code 2.1.178+는 세션당 implicit team을 사용합니다. `TeamCreate`/`TeamDelete`는 호출하지 않고, 이름 있는 background teammate를 `Agent`로 직접 생성합니다. 세션 종료 시 팀 정리는 런타임이 담당합니다.
- teammate는 Lead의 permission mode를 상속합니다. 스폰 프롬프트에서 `bypassPermissions`를 지정하거나 권한을 우회하지 않습니다. 필요한 권한은 사용자가 Lead 세션에서 먼저 선택합니다.
- Agent Teams가 꺼져 있으면 독립 조사에는 내장 `Explore`, 구현에는 `general-purpose`를 사용하고, 병렬성이 없으면 순차 실행합니다.

### 추론 강도 선택 전략

런타임의 현재 모델과 사용자 설정을 상속합니다. 특정 vendor 모델을 스킬이 강제하지 않습니다.

| Wave 단계 | 팀원 역할 | 요구 강도 |
|-----------|----------|-----------|
| **Wave 0: 도메인 분석** | 아키텍처 조사, 기술 스택 평가, DB 스키마 설계 | 높은 추론 강도 |
| **Wave N: 구현** | 기능 코딩, 파일 생성, 테스트 작성 | 균형형 실행 |
| **Wave N: 자재검사** | 네이티브 읽기 전용 리뷰 + code-reviewer 정책 | 높은 추론 강도 |
| **Wave N: 테스트 실행** | 테스트 러너, 린트, 타입 체크 | 빠른 실행 |
| **최종 검증** | AC 대조, 공정 점검 | 높은 추론 강도 |

위임 프롬프트에는 역할, 담당 범위, 입력 아티팩트, 쓰기 허용 여부, 검증 명령, 반환 형식만 넣습니다. 모델 지정은 사용자가 요청했거나 런타임 설정이 명시적으로 제공된 경우에만 사용합니다.

### Wave 완료 후 테스트 검증 (필수)

각 Wave 구현 완료 시, Lead는 테스트 팀원을 투입한다:

1. **기존 테스트 실행**: `npm test`, `pytest`, `go test` 등 프로젝트 테스트 프레임워크 실행
2. **린트/타입 체크**: `tsc --noEmit`, `eslint`, `ruff check` 등
3. **실패 시**: 구현 팀원에게 수정 지시 → 재실행 (최대 3회)
4. **3회 연속 실패**: 해당 작업자를 중단하고 새 general-write 작업자로 교체한 뒤, 실패 원인 분석부터 재시작

### 에러 복구 전략

| 상황 | 조치 |
|------|------|
| 팀원이 잘못된 파일 수정 | 소유권 기준점 대비 변경 목록(verification-protocol.md 3단계)으로 확인 → revert 지시 |
| 테스트 3회 연속 실패 | 작업자 중단 → 새 general-write 작업자로 교체 → 원인 분석부터 |
| 자재검사 2회 미통과 | 구현 팀원 교체 → 리뷰 지적사항 포함 재구현 |
| 팀원 무응답 (1분+) | shutdown → 재스폰 (최대 2회) |

### Codex 모드
- Codex의 내장 `explorer`/`worker`/`default`를 사용합니다. 사용자 정의 `.toml` agent는 이 스킬의 필수 조건이 아닙니다.
- subagent는 현재 세션의 sandbox와 approval policy를 상속합니다. 스킬이 `--yolo`, 승인 우회, sandbox 해제를 권장하거나 설정하지 않습니다.

### Antigravity 모드
- 일반 장기 팀 작업이고 Olympus 섹션·Wave·소유권·검증 산출물이 필요 없으면 가용한 `/teamwork-preview`를 우선합니다. 이미 활성화된 팀 문맥은 실행 엔진으로 재사용하며 중첩 PM/팀을 만들지 않습니다.
- Antigravity TUI의 `/agents` 패널과 현재 세션의 도구 목록에서 내장 `research`와 사용 가능한
  사용자 정의 에이전트를 확인합니다.
- 읽기 전용 조사는 `research`, 구현은 메인 또는 쓰기 도구를 명시한 사용자 정의 서브에이전트에 맡깁니다.
- 공식 `invoke_subagent`와 필요 시 `define_subagent`를 사용합니다. 메시지·상태·중단 기능은 현재
  런타임이 실제 노출한 도구만 사용하고 이름을 추측하지 않습니다.
- 구현 전문성은 전역 페르소나가 아니라 섹션 내용·프로젝트 설정·인접 코드·테스트를 위임 프롬프트에 임베딩해 전달합니다. 병렬 실행이 불가하면 Wave 내 순차 위임으로 축소합니다.

### Grok 모드
- Grok Build는 네이티브 `general-purpose`, `explore`, `plan` 서브에이전트를 제공. Olympus source-only 프롬프트는 기본 설치하지 않음
- 일반 구현은 `general-purpose`, 읽기 전용 탐색은 `explore`를 사용합니다. 명명형 어댑터는 고유 런타임 계약이 있을 때만 명시 opt-in합니다.
- 자식 결과는 요약으로 회수되므로 완료 판정은 실제 파일·테스트 결과로 교차 검증합니다. 동시성은 런타임 제한과 독립 작업 수 중 더 작은 값으로 제한합니다.

### 공통
- zephermine 계획 산출물 (sections/index.md + section-NN-*.md 파일들)

## Team Name

팀 이름은 **포세이돈(Poseidon)**으로 고정합니다.
teammate 생성 시 이 팀명을 사용하세요.

**공식 호출명:** `/agent-team` (별칭: `/poseidon`, `포세이돈`, `Poseidon`)

> 포세이돈은 바다의 신이며, 파도(Wave)를 다스리는 존재입니다.
> 섹션 의존성 그래프를 Wave 단위로 정렬해 teammate들을 병렬 출항시키는
> 이 스킬의 본성과 일치합니다.

## CRITICAL: First Actions

### 1. Print Intro

```
포세이돈(Poseidon) 출항
```

모드 판별 후 표시:
```
[섹션 모드] 순서: 산출물 검토 → Parse → Wave Plan → Tasks → Execute → Review → Verify(반복) → Activity Log → Report
[자유 모드] 순서: Analyze → Wave Plan → Tasks → Execute → Review → Verify(반복) → Report
```

### 2. Determine Mode

**두 가지 모드를 자동 판별:**

#### 섹션 모드 (zephermine 산출물 있음)
- `$ARGUMENTS`로 planning_dir가 제공되었거나
- `docs/plan/*/sections/index.md`가 존재하면 (archive/ 경로 제외)
- → **섹션 모드**로 진행 (Step 0~8 워크플로우)

#### 자유 모드 (사용자 지시만 있음)
- planning_dir이 없고, sections/index.md도 없으면
- 사용자의 대화 컨텍스트에서 작업 지시를 추출
- → **자유 모드**로 진행 (Lead가 직접 분석 → 분배)

```
섹션 모드: "agent-team docs/plan/my-feature" → sections/ 파싱 → Wave 실행
자유 모드: "이 3개 파일 리팩토링해줘. 에이전트팀 진행하자" → Lead가 분석 → 분배
```

### 3. Setup (모드별 분기)

#### 섹션 모드 Setup
1. `sections/index.md` 존재 확인
2. `SECTION_MANIFEST` 블록 파싱 확인
3. 최소 1개 이상 `section-NN-*.md` 파일 존재 확인
4. → **Step 1 (Parse Sections)**로 진행

#### 자유 모드 Setup
1. 사용자 지시에서 작업 목표 추출
2. 관련 코드베이스 탐색 (Glob, Grep, Read)
3. 작업을 독립적인 태스크로 분해 (파일/모듈/기능 단위)
4. 각 태스크의 의존성 판별 → Wave 그룹핑
5. 구현 컨텍스트 매칭 ([expert-matching.md](references/expert-matching.md) 참조)
6. **Step 2 (Build Wave Plan)**의 사용자 확인 출력으로 합류
7. planning_dir이 없으므로 태스크별 완료 기준을 같은 형식(`AC-<태스크번호>-k`, 관찰 가능한 동작·검증)으로 정해 Step 2 실행 계획에 함께 출력하고, 이행 장부는 activity log의 `## Acceptance` 표로 둔다 (형식: 젭마인 `references/acceptance-checklist-guide.md`)

**자유 모드 태스크 분해 원칙:**
- 파일 충돌 없도록 담당 파일을 명확히 분리
- 태스크당 1~5개 파일 범위
- 의존성이 없으면 모두 Wave 1에 배치 (최대 병렬)
- description에 구현 지시 + 담당 파일 + 관련 코드 컨텍스트 포함

---

## Workflow

### Pre-Step: 런타임 상태 확인

현재 세션에 남아 있는 실행 중 작업자와 task를 조회합니다. 이전 세션의 팀 디렉터리를 수동 삭제하거나 정리 명령을 추측해 호출하지 않습니다. 재사용 가능한 작업자가 없으면 새 작업자를 만들고, 런타임 상태 조회가 불가능하면 현재 Wave ledger를 기준으로 진행합니다.

### Step 0: 산출물 검토 (PM 게이트)

> **Lead는 설계 도면을 확인하지 않고 공사를 시작하지 않는다.**

See [artifacts-review.md](references/artifacts-review.md)

젭마인 산출물을 PM 관점에서 검토합니다. 확인 항목:
1. `plan.md` — 전체 구현 방향 파악
2. `sections/index.md` — SECTION_MANIFEST + 의존성 그래프
3. `flow-diagrams/` — 공정 도면 존재 여부 (없으면 사용자 경고)
4. 보조 문서 (api-spec.md, db-schema.md 등) — teammate 전달 레퍼런스 등록
5. 완료 기준 계약 — `checklist.md` 확인(없으면 섹션 AC에서 기계적으로 생성), `checklist-status.md` 장부 생성 또는 재개
6. 영향도 분석 (기존 코드가 있는 경우) — 교차 영향 파일 경고

### Step 1: Parse Sections

See [section-parser.md](references/section-parser.md)

`sections/index.md`에서 다음을 추출:
1. **SECTION_MANIFEST** 블록 → 섹션 목록
2. **Dependency Graph** 테이블 → 의존성 관계
3. 각 `section-NN-*.md` 파일의 존재 여부 확인

**프로세스 도면 매핑**: `sections/index.md`에 **Flow Diagram Mapping** 테이블이 있으면 섹션↔도면 노드 매핑을 추출하여 Step 2, Step 4에 반영.

**구현 컨텍스트 매칭**: See [expert-matching.md](references/expert-matching.md) — 각 섹션의 파일 패턴으로 프로젝트 근거·역할·검증 계약을 구성.

### Step 2: Build Wave Plan

의존성 그래프를 위상 정렬(Kahn's Algorithm)하여 Wave 그룹으로 분류:

1. 의존성이 없는 섹션 → Wave 1
2. Wave 1에만 의존하는 섹션 → Wave 2
3. 반복... 순환 의존성 발견 시 경고 후 사용자 보고
4. **Wave당 최대 teammate 수: 5명** — 6개 이상 시 sub-wave 분할

**사용자에게 실행 계획 출력:**

```
═══════════════════════════════════════
포세이돈(Poseidon) 실행 계획
═══════════════════════════════════════
Wave 1 (병렬 3개):
  - section-01-foundation [풀스택] (파일: src/core/**)
  - section-02-config [풀스택] (파일: src/config/**)

Wave 2 (병렬 2개):
  - section-04-api [백엔드 전문가] (→ 01, 03 완료 후) 📐 user-auth.mmd
  - section-05-database [DB 전문가] (→ 01, 02 완료 후)

총 섹션: N개 | 총 Wave: M개 | 예상 teammate: K명
═══════════════════════════════════════
```

Wave Plan 출력 후 **확인 없이 바로 Step 3으로 진행** (사용자가 이미 실행 요청한 상태).

### Step 3: Create Tasks

See [teammate-context-template.md](references/teammate-context-template.md)

#### Claude 모드 (TaskCreate)
모든 섹션을 TaskCreate로 등록하고 blockedBy 관계 설정. `description`에 섹션 파일 전체 내용 임베딩.

#### Codex 모드 (spawn_agent)
Wave 단위로 agent spawn. `prompt`에 섹션 파일 전체 내용 + 담당 파일 + 프로젝트 기반 구현 계약 포함.

#### Antigravity 모드 (서브에이전트 위임)
Wave 단위로 기본/범용 서브에이전트를 호출하고, 섹션 파일 전체 내용 + 담당 파일 +
프로젝트 기반 구현 계약 + 파일 소유권 규칙을 위임 프롬프트로 전달.

#### Grok 모드 (spawn_subagent)
Wave 단위로 spawn. `prompt`에 섹션 파일 전체 내용 + 담당 파일 + 프로젝트 기반 구현 계약을 포함하고,
일반 구현의 `subagent_type`은 `general-purpose`를 사용.

**핵심 규칙**: teammate/agent는 lead의 대화 히스토리를 상속하지 않으므로, description/prompt에 섹션 파일 전체 내용을 반드시 임베딩해야 함.

### Step 4: Execute Waves

See [wave-executor.md](references/wave-executor.md)

Wave 1 시작 전 한 번: 소유권 기준점(`git stash create` SHA 또는 HEAD + 기존 untracked 목록)을 activity log에 기록 — [verification-protocol.md](references/verification-protocol.md) 0단계.

각 Wave별 실행 사이클:
1. 선행 Task의 blockedBy 해소 여부 확인
2. teammate/agent에게 지시 (담당 파일, 도면 노드, 파일 소유권 규칙 포함)
3. 진행 상황 모니터링 (Claude: shared task list/메시지, Codex: 현재 wait 도구, Antigravity/Grok: subagent 반환 — 모든 요약을 체크리스트·파일 실존과 대조)
4. 모든 Task completed → 다음 Wave로 진행

**teammate 지시 핵심 요소:**
- 프로젝트 기반 역할·근거, 섹션 내용, 담당 파일 목록
- 담당 섹션의 AC ID 목록 — 완료 보고에 AC ID별 증거(테스트 이름·명령 결과)와 상태 제안을 포함
- 📐 프로세스 도면 경로 + 담당 노드 ID (도면 있는 경우)
- ⚠️ 파일 소유권 규칙 (다른 teammate 파일 수정 금지)
- 작업자는 변경 파일·테스트·이탈 사유를 반환하고, Lead만 `conversations/{YYYY-MM-DD}-team-poseidon.md`에 activity log를 기록

### Step 5: Code Review Gate (자재검사)

각 Wave 완료 후, 다음 Wave 진행 전 코드리뷰 실행.

1. 이 Step에 도달한 뒤 전역 카탈로그의 `code-reviewer` 행을 해석하고
   `${code_reviewer_root}/SKILL.md`를 읽습니다. 이 모듈의 포세이돈 연동·정책 레이어를 적용하되,
   등록 스킬을 호출하지 않습니다. 보안 감사 reference가 필요한 Wave만
   `${code_reviewer_root}/references/security-audit.md`를 추가로 읽습니다.
2. 리뷰 엔진은 native-first로 선택합니다.
   - Claude: 내장 `/review`; 병렬화가 필요하면 읽기 전용 Explore 작업자에 로드한 gate 전달
   - Codex: `/review` 또는 `codex review`; 읽기 전용 explorer에 로드한 gate 전달 가능
   - Antigravity: 읽기 전용 `research` subagent에 로드한 경로 C gate 전달
   - Grok: bundled `review`; 실패하면 `explore` subagent에 같은 gate 전달
3. source module을 읽지 못하면 위 resolver의 bounded native fallback만 실행하고
   `policy module: NOT RUN`, `review gate: DEGRADED`로 남깁니다.
4. 미통과 시 → 수정 지시 → 재리뷰 (최대 2회)

**검수 항목:** 기능/책임 단위 분리, 보안 취약점, 타입, SRP, DRY

### Step 6: Verify Results — 완료 기준 장부 대조

See [verification-protocol.md](references/verification-protocol.md)

> **`checklist-status.md`의 모든 행이 `proved`가 될 때까지 반복한다.**

**검증 루프:**
```
while (checklist-status.md에 proved가 아닌 행 존재):
  1. 파일 존재 검증 (Files to Create/Modify 전수 확인)        ← 사전 점검
  2. AC 대조 — 작업자 보고 증거를 확인해 장부 갱신 (코드 존재만이면 weak) ← 사전 점검
  3. 도면 노드 검증 (flow-diagrams 존재 시)                   ← 사전 점검
  4. 파일 소유권 검증 (0단계 기준점 대비 변경 ↔ 섹션 소유 ↔ 작업자 보고) ← 사전 점검
  4b. 경계면 정합성 교차 비교 (웹앱: API 응답 shape↔훅 타입·경로↔href·엔드포인트↔훅 1:1 / 비웹: 해당 경계 / 없으면 skip) ← 사전 점검, verification-protocol.md 4.5단계
  5. 통합 게이트 (유일한 완료 권한): 병합 결과에 빌드/타입체크 + 전체 테스트 1회 — 1~4b는 사전 점검일 뿐, 이 게이트 통과로만 완료 (자동 PASS 금지). 상세 verification-protocol.md 5단계

  6. 통합 게이트 뒤 proved 행의 증거를 한 번 더 확인 (그 사이 관련 코드가 바뀐 행은 weak로 내리고 재확인)

  미통과 → 해당 teammate에 재지시 → 대기 → 재검증 (최대 2회)
  2회 후에도 미통과 → 사용자에게 보고 + 수동 개입 요청 (통과로 보고하지 않음 — 소진=미완)
```

> **완료 계약 (028):** Acceptance Criteria 대조는 이분(통과/미통과)이 아니라 proved/weak/missing/contradicted로 채점해 장부에 기록한다.
> 코드는 있으나 동작 증거가 약한 항목은 `weak`로 따로 잡아, "파일 존재 = 완료"로 둔갑시키지 않는다.

### Step 7: Activity Log Summary

모든 Wave 완료 후:
1. `conversations/{YYYY-MM-DD}-team-poseidon.md` 읽기
2. teammate별 활동 통계 집계 (기록 수, 에러 수, 파일 수)
3. source-only `orchestrator` 모듈과 MCP command를 성공적으로 읽고 실제 폴백을 시작한 경우에만
   `orchestrator_get_activity_log`로 JSONL 로그 확인. 선택하지 않았거나 로드 실패면
   `MCP: NOT SELECTED`/`NOT RUN`으로 기록
4. 요약을 Final Report에 포함

### Step 8: Final Report

```
═══════════════════════════════════════
포세이돈: 실행 완료
═══════════════════════════════════════
📋 완료 기준 (checklist-status.md): M/N proved (XX%) — 남은 ID: …
📐 도면 매칭: K개 노드 중 J개 구현 (YY%)
⏱️ 총 Wave: W개 | 검증 루프: R회
내부 모듈: code-reviewer {LOADED|NOT RUN} | orchestrator MCP {NOT SELECTED|LOADED|NOT RUN}

섹션별 결과:
  ✅ section-01-foundation — 체크 3/3, 파일 3개
  ⚠️ section-03-api — 체크 4/5 (테스트 1건 미통과)

Lead 의사결정 로그: conversations/{date}-team-poseidon.md
═══════════════════════════════════════
```

실패 섹션은 같은 범위를 1회 재시도합니다. 그래도 실패하고 대화형 실행이면 사용자에게 재시도 또는 실패 상태 종료를 한 문장으로 묻습니다. Zeus 같은 무중단 호출에서는 메인 순차 폴백 후 실패를 보고하며 성공으로 가장하지 않습니다.

---

## vs orchestrator

| 측면 | agent-team (이 스킬) | orchestrator (기존) |
|------|---------------------|---------------------|
| 설치 | 불필요 (4-CLI 네이티브 내장 — 구버전만 env var) | MCP 서버 빌드 필요 |
| 지원 CLI | Claude + Codex + Antigravity + Grok (네이티브) | 네이티브 멀티에이전트가 없는 구버전 CLI |
| 파일 충돌 방지 | 소유권 규칙 (soft) | MCP lock_file (hard) |
| 태스크 관리 | CLI별 네이티브 도구 | orchestrator MCP 도구 |
| 사용 조건 | zephermine 섹션 또는 자유 모드 | 폴백 또는 hard lock 필요 시 |

**공존 원칙 (native-first):** 실행은 항상 네이티브 우선. orchestrator는
① 네이티브 멀티에이전트가 없는 구버전 CLI 폴백, ② hard file lock·크로스 CLI task ledger가
꼭 필요한 대규모 동시 편집 — 이 두 경우에만 정책 레이어로 사용.

---

## Logging Format

```
═══════════════════════════════════════════════════════════════
STEP {N+1}/9: {STEP_NAME}     (Step 0~8, 총 9단계)
═══════════════════════════════════════════════════════════════
{details}
Step {N} complete: {summary}
───────────────────────────────────────────────────────────────
```

> 표시 예: Step 0 → `STEP 1/9`, Step 8 → `STEP 9/9`

## Error Handling

| 상황 | 대응 |
|------|------|
| SECTION_MANIFEST 파싱 실패 | 사용자에게 index.md 형식 확인 요청 |
| 순환 의존성 발견 | 경고 출력 + 관련 섹션 목록 표시 |
| teammate 상태 변화 없음 | 런타임 상태와 담당 파일·테스트 증거 확인 → 작업 범위를 줄여 1회 재위임; permission mode는 변경하지 않음 |
| teammate/agent 실패 | 오류와 부분 변경을 확인 → 같은 범위를 새 작업자에게 1회 재위임 → 실패 시 메인 순차 폴백 또는 사용자 보고 |
| 파일 충돌 감지 | 두 teammate/agent가 같은 파일 수정 → Lead가 merge 또는 사용자에게 보고 |
| 컨텍스트 한도 초과 | 현재 Wave까지 결과와 ledger를 저장 → 실행 중 작업자를 안전하게 중단 → 사용자에게 새 세션에서 재개 안내 |
| Codex spawn 실패 | 현재 세션의 multi-agent 가용성·thread cap·sandbox를 확인 → 범위를 줄여 재시도; 승인 우회 금지 |
| Codex wait 타임아웃 | 현재 interrupt 도구로 중단 → 부분 변경 확인 → 범위를 줄여 재spawn |
| Antigravity 에이전트 미인식 | TUI `/agents`와 현재 도구 목록으로 확인 → `invoke_subagent`가 없으면 Wave 내 메인 컨텍스트 순차 실행; hard lock 등이 필수일 때만 source-only resolver를 거친 orchestrator MCP 분기 |
| spawn_subagent 실패 (Grok) | `grok inspect --json`으로 네이티브 서브에이전트 레지스트리 확인 → 재spawn 1회 → 실패 시 사용자 보고 |
| 재시도 후에도 실패 | 해당 섹션을 메인 컨텍스트에서 순차 실행하거나 사용자에게 보고 |

## 작업자 정리

모든 Wave 완료, 중단, 컨텍스트 한도 도달 시 현재 런타임이 제공하는 정상 종료·중단 절차를 사용합니다.

- Claude 2.1.178+: implicit team이므로 `TeamDelete`를 호출하지 않습니다. 실행 중 named teammate에 shutdown을 요청하고 세션 정리는 런타임에 맡깁니다.
- Codex: 실행 중 thread만 현재 interrupt/stop 기능으로 중단합니다. 완료 thread의 정리는 런타임 UI나 현재 제공 기능을 따릅니다.
- Antigravity/Grok: 호출 단위 child가 반환되면 별도 팀 정리가 없습니다.
- 어떤 CLI에서도 런타임 상태 디렉터리를 수동 삭제하지 않습니다.

```
1. 실행 중 작업자 목록 확인
2. 필요한 결과가 회수됐는지 확인
3. 실행 중 작업자에 정상 종료 또는 interrupt 요청
4. Lead의 Wave ledger와 activity log를 최종 저장
```

---

## 다음 단계 안내

```
✅ 에이전트팀 구현 완료!

📊 결과: {통과/실패 요약}

👉 다음 단계 (선택):
  /argos               → 감리 (설계 대비 구현 검증, Phase 0~6)
  /aphrodite           → 디자인 정교화 (design-system.md가 있는 UI 프로젝트)
  /minos          → Playwright 자동 테스트 + Healer 루프
  /review              → 코드 리뷰 (품질/보안/성능)
  /commit              → 변경사항 커밋

📎 참고: docs/workflow-guide.md
```

---

## References

| 파일 | 내용 |
|------|------|
| [artifacts-review.md](references/artifacts-review.md) | Step 0 산출물 검토 상세 절차, 영향도 분석, 보조 문서 매핑 |
| [section-parser.md](references/section-parser.md) | SECTION_MANIFEST 파싱 규칙, 도면 매핑 추출 |
| [expert-matching.md](references/expert-matching.md) | 섹션 파일 패턴 → 프로젝트 기반 구현 컨텍스트 매칭 |
| [wave-executor.md](references/wave-executor.md) | Wave 실행 사이클, teammate 지시 형식, 모니터링 루프, Codex agent 형식 |
| [teammate-context-template.md](references/teammate-context-template.md) | teammate/agent 프롬프트 전체 템플릿 |
| [verification-protocol.md](references/verification-protocol.md) | 검증 5단계, 재시도 프로세스, 통과 기준 |
