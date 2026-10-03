---
name: agent-team-codex
description: Codex CLI의 내장 default, explorer, worker를 조합해 병렬 구현을 수행한다. zephermine 섹션 모드와 자유 모드를 지원하며 /agent-team, /poseidon, /agent-team-codex로 실행한다.
---

# Agent Team Codex

Codex CLI의 stable multi-agent 기능을 사용해 작업을 병렬 분배하는 운영 스킬입니다.
Codex의 `default/explorer/worker` 역할을 기준으로 실행하며 특정 모델을 강제하지 않습니다.

## Prerequisites

1. 현재 Codex에서 subagent 도구가 노출되는지 확인합니다. 현행 Codex는 `[agents].enabled` 기본값이 `true`입니다.
2. 사용자가 명시적으로 비활성화한 경우 그 선택을 존중하고 메인 컨텍스트에서 Wave를 순차 실행합니다.
3. 동시성 상한을 사용자가 조정하려는 경우에만 현재 설정명을 사용합니다:

```toml
[agents]
max_concurrent_threads_per_session = 6
```

사용자 정의 `.toml` agent는 필요하지 않습니다. 고유한 sandbox·MCP·모델 계약이 입증된 경우에만 별도 opt-in으로 추가합니다.

## Source-only internal module resolution (mandatory)

`code-reviewer`와 조건부 `orchestrator`는 이 하네스가 내부 정책으로 읽는 source-only
모듈입니다. 등록된 스킬이나 slash command로 호출하지 않습니다.

각 선택된 모듈을 다음 순서로 해석하고 처음 확인된 exact `SKILL.md` 파일 하나를 읽습니다.

1. 현재 프로젝트의 `skills/{name}/SKILL.md`가 실제로 있으면 그 exact 파일.
2. 없으면 Codex active root의 `~/.codex/skills/{name}/SKILL.md` exact 파일
   (명시 opt-in 설치 지원).
3. 둘 다 없으면 Codex 전역 `~/.codex/SKILLS-CATALOG.md`에서 정확한 모듈명 행을 찾습니다.
   행이 하나일 때만 `읽을 경로`에 적힌 절대 `SKILL.md`를 그대로 읽고, 누락·중복 행은
   fail-closed입니다. 기본 경로가 보통 `.olympus/source-skills` 아래여도 직접 조합하거나
   추측하지 않습니다.
4. `module_root`는 읽은 `SKILL.md`의 부모입니다. 모듈의 `references/`, `scripts/`,
   `commands/`는 모두 이 루트에서 해석합니다.
5. Step 6 코드 리뷰에 도달했을 때만 `code_reviewer_root`를 만듭니다. hard file lock,
   외부 ledger, 크로스-CLI 혼합이 실제로 필요해 MCP 분기를 선택한 뒤에만
   `orchestrator_root`를 만들고 `${orchestrator_root}/commands/workpm-mcp.md`를 읽습니다.

이 exact 파일 읽기는 내부 모듈 로드입니다. 런타임 Skill 목록/레지스트리를 근거로 호출하거나
모듈 이름을 slash command로 실행하지 않습니다.

code-reviewer를 읽지 못하면 `codex review` 1회와 explorer의 bounded 품질·보안·타입
체크만 실행하고 `policy module: NOT RUN (native fallback)`, gate `DEGRADED`를 기록합니다.
orchestrator/MCP를 읽지 못하면 파일 소유권을 직렬화할 수 있는 경우에만 메인 순차 경로로
축소하고 `MCP: NOT RUN`을 기록합니다. hard lock이 필수이면 해당 Wave는 `BLOCKED`입니다.
어느 누락도 PASS로 처리하지 않습니다.

## Modes

### 1) 섹션 모드

- 입력에 `docs/plan/*/sections/index.md` 또는 zephermine 산출물이 있는 경우 (archive/ 경로 제외)
- 섹션 의존성을 Wave로 분리해 병렬 실행

### 2) 자유 모드

- 일반 작업 요청(예: "auth 리팩토링 + 테스트")
- 파일/모듈 기준으로 태스크를 직접 분해 후 병렬 실행

### 조건부 MCP 정책 분기

기본 경로는 Codex native agent이며, agent가 없으면 메인 컨텍스트 순차 실행입니다. hard file
lock, 외부 task ledger, 크로스-CLI 혼합 중 하나가 실제 요구사항일 때만 MCP 분기를 선택하고,
그때 위 resolver로 `orchestrator` 모듈과 `${orchestrator_root}/commands/workpm-mcp.md`를
읽습니다. 선택 전에는 모듈·서버·활동 로그 도구를 로드하지 않습니다.

## Workflow

### Step 0: 산출물 검토 (PM 게이트)

> Claude 버전 agent-team의 Step 0과 동일한 역할. 설계 없이 구현을 시작하지 않는다.

**섹션 모드에서 필수 확인:**
1. `plan.md` — 전체 구현 방향 파악
2. `sections/index.md` — 의존성 그래프 → Wave 분리 기준
3. `flow-diagrams/` — 공정 도면 존재 여부 (있으면 각 worker에게 담당 노드 배분)
4. 보조 문서 매핑:
   - `api-spec.md` → API 관련 worker에게 전달
   - `db-schema.md` → DB 관련 worker에게 전달
   - `design-system.md` → 프론트엔드 worker에게 전달
5. 완료 기준 계약 — `checklist.md` 확인(없으면 섹션 AC에서 기계적으로 생성), `checklist-status.md` 장부 생성 또는 재개. 형식·상태·증거 규칙은 젭마인 `references/acceptance-checklist-guide.md`

**자유 모드에서는 건너뜀.**

### Step 1: 작업 분해

1. 목표를 3~8개의 독립 태스크로 분할
2. 태스크별 담당 파일 범위를 고정
3. 의존성 있는 태스크는 후행 Wave로 배치

상세 규칙: `references/role-mapping.md`

### Step 2: 역할 매칭

- `explorer`: 분석, 리스크 점검, 편집 금지
- `worker`: 구현/수정/테스트
- `default`: 조율, 병합 판단, 최종 보고

### Step 3: 에이전트 스폰

Codex 프롬프트에서 자연어로 spawn 지시를 보냅니다.
템플릿은 `references/prompt-templates.md`를 사용합니다.

스폰 전 한 번: 소유권 기준점을 기록합니다. `git stash create` 출력 SHA(빈 출력이면 `git rev-parse HEAD`)와
`git ls-files --others --exclude-standard`의 기존 untracked 목록을 Lead가 activity log의 `## Ownership baseline`에 적습니다.
작업 중에는 커밋하지 않으므로 Step 7의 충돌 확인은 커밋 이력이 아니라 이 기준점과 비교합니다.
`git stash create`는 작업 트리를 바꾸지 않고, 작업 전부터 있던 미커밋 수정을 기준점에 포함합니다.

핵심 규칙:

- 각 worker는 파일 소유권 범위를 벗어나지 않음
- explorer는 코드 수정 금지
- 충돌 가능성이 있으면 즉시 `default`가 재분배
- 각 worker는 담당 AC ID 목록을 받고, 변경 파일·테스트·계획 이탈·남은 위험과 AC별 `ID | 증거 | 상태 제안`을 반환하고, Lead만 `conversations/{YYYY-MM-DD}-team-poseidon.md`와 공유 `implementation-notes.md`를 기록

### Step 4: 모니터링

1. 진행 중 실패 태스크를 우선 확인
2. 실패 원인을 한 번에 하나씩 재시도
3. 3회 이상 반복 실패 시 아키텍처 이슈로 분류 후 사용자 보고

### Step 5: Activity Log Summary

통합 전 활동 로그 요약:

1. Lead가 기록한 `conversations/{YYYY-MM-DD}-team-poseidon.md` 읽기
2. 에이전트별 활동 통계: 완료 보고 수, 에러 수, 파일 수
3. `orchestrator` source module과 MCP command를 성공적으로 읽고 실제 분기를 시작한 경우에만
   `orchestrator_get_activity_log`로 JSONL 로그도 확인. 그 외에는 `MCP: NOT SELECTED` 또는
   `MCP: NOT RUN`으로 기록
4. 요약을 최종 보고에 포함

### Step 6: 코드 리뷰 게이트

구현 완료 후, 통합 전 품질 검증:

1. Step 6 진입 후 전역 카탈로그의 `code-reviewer` 행을 해석하고
   `${code_reviewer_root}/SKILL.md`의 Codex native 경로와 포세이돈 정책 레이어를 읽습니다.
   등록 스킬로 호출하지 않습니다. 보안 감사 reference가 필요한 범위만
   `${code_reviewer_root}/references/security-audit.md`를 추가로 읽습니다.
2. native-first로 `codex review --uncommitted` 또는 적절한 base review를 실행하고, 필요한
   보강 검토를 **explorer 에이전트**에게 위임합니다:
   - 각 worker가 생성한 파일의 품질, 보안, 타입 안전성 확인
   - Acceptance Criteria 대조 (Step 0에서 추출한 마스터 체크리스트)
   - flow-diagrams 노드 매핑 (있는 경우) — 담당 노드가 구현되었는지
3. source module 미가용 시 native review + 위 세 항목만 bounded fallback으로 실행하고
   `policy module: NOT RUN`, `review gate: DEGRADED`를 보고합니다.
4. 미통과 항목 → 해당 worker 재spawn하여 수정 (최대 2회)
5. 2회 후에도 미통과 → 사용자 보고

### Step 7: 통합 게이트 (완료 권한 — 필수)

> **I-1**: 병렬 구현 후 "함수가 존재하는가"를 Grep/Read로 확인하는 코드-존재 검증은 자기 판단이며,
> 컴파일/통합되지 않는 코드도 통과시킬 수 있다. 빌드/타입체크는 선택이 아니다.

1. 파일 충돌 여부 확인 — 변경 파일 = `git diff --name-only {기준점 SHA}` ∪ (`git ls-files --others --exclude-standard` − 기준점의 기존 untracked). 각 파일을 담당 worker 소유와 worker가 반환한 변경 파일에 대조해, 같은 Wave의 둘 이상이 소유하면 `CONFLICT`(다른 Wave가 순차로 고친 공유 파일은 `SHARED` — 각자 맡은 부분만 바꿨는지 diff 확인), Lead 기록(activity log·`checklist-status.md`·`implementation-notes.md`)은 제외하고, 소유자가 없으면 `UNOWNED`(조립 지점에서 기준점 대비 diff에 `-` 줄 없이 등록 줄만 추가된 경우 제외), 아무도 보고하지 않았으면 `UNREPORTED`로 표시합니다. 근거 없는 변경은 revert하고, 필요한 변경은 소유에 추가해 activity log에 기록합니다
2. **사전 점검(PRE-CHECK, 완료 권한 아님):** 코드-존재 / Acceptance Criteria grep 대조 — 빠뜨린 작업 식별용일 뿐, 이것만으로 완료 선언 금지. AC는 proved/weak/missing/contradicted로 채점(028 완료 계약)해 Lead가 `checklist-status.md`에 증거와 함께 기록 — 코드는 있으나 동작 증거가 약하면 `weak`로 분리(존재=완료 둔갑 방지). 또한 **경계면 정합성 교차 비교**(웹앱: API 응답 shape↔훅 타입·경로↔href·엔드포인트↔훅 1:1 / 비웹: 해당 경계 / 없으면 skip) — 빌드 통과가 숨기는 런타임 mismatch를 게이트 전에 정적으로 거른다(양쪽 동시 읽기)
3. **병합 결과에 대해 통합 게이트를 1회 실행 (이 게이트만이 완료 권한):**
   1. 빌드 / 타입체크
   2. 전체 테스트 스위트 1회 실행 (병합된 결과 대상)
   3. (가능하면) 통합/E2E 1회 실행
4. 게이트 결과에 따라:
   - 전부 통과하고 `checklist-status.md`의 모든 행이 `proved`(게이트 뒤 재확인) → 완료 선언 가능. 아니면 "M/N proved, 남은 ID"로 보고
   - 실패 → 해당 worker 재spawn하여 수정 후 게이트 재실행
   - **빌드/테스트 도구가 없으면** 그 사실을 명시하고 사용자에게 수동 확인을 요청 (자동 PASS 금지)
5. 남은 리스크/미해결 항목 정리

> **Guard:** 게이트 미통과 상태로 완료 선언 금지; 빌드/테스트 도구가 없으면 명시하고 수동 확인 요청(자동 PASS 금지).

## Output Format

최종 보고는 아래 포맷을 따릅니다:

```text
Codex Agent Team 실행 결과
- 완료 태스크: N개
- 실패 태스크: N개
- 마스터 체크리스트: M/N 통과 (XX%)
- 주요 변경 파일: ...
- 테스트 결과: 통과 N / 실패 N
- 내부 모듈: code-reviewer {LOADED|NOT RUN}, orchestrator MCP {NOT SELECTED|LOADED|NOT RUN}
- 잔여 리스크: ...

👉 다음 단계 (선택):
  /argos               → 감리 (설계 대비 구현 검증, Phase 0~6)
  /aphrodite           → 디자인 정교화 (design-system.md가 있는 UI 프로젝트)
  /minos          → Playwright 자동 테스트 + Healer 루프
  /review              → 코드 리뷰
  /commit              → 변경사항 커밋
```

## Troubleshooting

### subagent 도구가 보이지 않음

- `codex features list`와 현재 `[agents].enabled` 설정을 확인합니다.
- 현행 버전인데 도구가 없으면 Codex를 갱신하고 세션을 다시 시작합니다.
- 사용자가 agents를 껐거나 갱신할 수 없으면 메인 컨텍스트 순차 실행으로 계속합니다.

### 에이전트 충돌(같은 파일 동시 수정)

- 파일 소유권을 다시 나눠 재스폰
- 공통 모듈은 별도 single-owner 태스크로 분리

### 스레드 과다로 품질 저하

- `max_concurrent_threads_per_session`을 줄여 재실행 (예: 6 → 4)
- explorer를 1개로 고정하고 worker 수만 조절

## References

- 역할/소유권 규칙: `references/role-mapping.md`
- 스폰 프롬프트 템플릿: `references/prompt-templates.md`
