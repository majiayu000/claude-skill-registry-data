---
name: zeus
description: >
  Zero-interaction full pipeline skill. 사용자가 한 줄 설명만 제공하면
  설계(zephermine) → 구현(agent-team) → 감리(argos) → Docker 구성 → 테스트(minos) 전체를 자동 완료.
  인터랙티브 질문 도구 절대 호출 금지. /zeus로 실행. 제우스.
---

# Zeus (제우스) — Zero-Interaction Full Pipeline

> "이런 프로그램 만들어줘" 한 줄이면 설계부터 구현, 테스트까지 전부 자동으로.

---

## Pipeline Overview

```
/zeus "쇼핑몰 만들어줘. React+Spring Boot"
    │
    ▼
Phase 0: Description Parsing ─── 산업군, 기술스택, 기능 추출
    │
    ▼
Phase 1: Planning (zephermine) ─ 합성 인터뷰 → 26단계 설계 자동 완료
    │
    ▼
Phase 2: Implementation (agent-team) ─ 포세이돈 PM이 섹션 기반 병렬 구현
    │
    ▼
Phase 3: Verification (argos) ─ 설계 대비 준공검사
    │
    ▼
Phase 4: Docker Setup (docker-deploy) ─ Docker 환경 구성 + 포트 충돌 해결
    │
    ▼
Phase 5: Testing (minos) ─ E2E 테스트 + Healer 루프
    │
    ▼
Phase 6: Final Report ─────────── docs/zeus/zeus-report.md 생성
```

---

## CRITICAL RULES

0. **메타 요청 구분** — 사용자가 Zeus 자체를 점검/수정/설명하라고 한 경우에는 제품 파이프라인을 시작하지 말고 이 SKILL.md와 관련 런타임만 점검한다. 제품/기능을 "제우스로 진행"하라는 요청일 때만 Phase 0~6을 실행한다.
1. **NEVER call interactive question tools** — 모든 결정은 자동선택 규칙으로 처리 (`Recommended` 우선, 없으면 자동 응답 테이블)
2. **절대 멈추지 않는다** — 에러 시 기록하고 계속 진행
3. **Phase 완료 즉시 다음 Phase 시작** — "다음을 진행합니다" 같은 중간 보고 금지. Phase 0→1→2→3→4→5→6을 한 턴에 연속 실행
4. **[ZEUS-AUTO] 태그 + 결정 장부(Decision Ledger)** — 질문을 사전에 하지 않는 대신 결재를 사후로 미룬다.
   자동 결정에는 태그와 분류를 표시:
   - `[ZEUS-AUTO:mechanical]` — 정답이 하나인 결정 (기본값 선택, 폴백 등). 기록만.
   - `[ZEUS-AUTO:taste]` — 합리적인 사람이 다르게 판단할 수 있는 결정 (디자인 톤, 기능 우선순위 등).
     **결정 장부 형식으로 기록**: 결정 + 근거 + 기각한 대안 + **되돌리는 법**.
     Phase 6 리포트의 Decision Ledger 섹션에 모아서 표시 — 사용자가 사후 결재(검토 후 뒤집기)할 수 있게 유지.
     가능하면 되돌리기 쉬운(reversible) 기본값을 우선 선택한다.
   - 예: `[ZEUS-AUTO:taste] 인증 JWT 선택 | 근거: SPA 표준, 무상태 확장 | 대안: 세션(서버 상태 필요) | 되돌리기: auth 모듈 교체, API 계약 변경 없음`
5. **재개 지원** — docs/zeus/zeus-state.json으로 중단 지점부터 재개
6. **모든 Phase 강제 실행** — Phase 0~6 모두 최소 1회 실행 시도 필수. "건너뜀"은 물리적 불가(Docker 미설치 등)일 때만 허용하며, 그 경우에도 폴백 경로를 실행
7. **완료 전 최종 응답 금지** — Phase 0~5 실행 증거가 없으면 "다음 구현 순서"를 사용자에게 넘기지 않는다. 실행 가능한 다음 작업은 즉시 수행하고, 불가능하면 `zeus-state.json`과 핸드오프를 남긴다.
8. **스코프 게이트 (pass/reduce/hold)** — zero-interaction에는 스코프 확장을 승인해줄 사용자가 없으므로, `plan.md`/`sections/` 확정 이후 계획에 없던 태스크·기능·신규 의존성을 추가하기 전에 자문 3개를 통과시킨다:
   - 사용자의 한 줄 목표에 직접 기여하는가? / 지금 필요하게 만든 관찰된 근거(실패한 테스트, 감리 지적, 명시 요청)가 있는가? / 기존 산출물 재사용이나 더 작은 변경으로 같은 결과가 나오는가?
   - 판정은 셋 중 하나로 결정 장부에 기록: `pass`(최소 범위로 진행) / `reduce`(축소 후 진행) / `hold`(실행 보류 — Phase 6 리포트 Decision Ledger에 Deferred로 표시, 사용자가 사후 승격)
   - **과적용 금지**: 계획된 섹션 구현·버그 수정·Phase 폴백 실행은 게이트 대상이 아니다 (폴백은 스코프 축소이지 확장이 아님). 게이트가 규칙 6(모든 Phase 강제 실행)을 약화시키지 않는다.
   - 예: `[ZEUS-AUTO:taste] 스코프 게이트 hold: 관리자 통계 차트 | 근거: 한 줄 요구·섹션에 없음, 감리 지적 아님 | 되돌리기: Deferred에서 승격 후 재실행`

## Source-only internal module resolution (mandatory)

`docker-deploy`와 조건부 `orchestrator`는 Zeus가 내부에서 읽는 source-only 모듈입니다.
등록된 스킬이나 slash command로 호출하지 않습니다.

각 모듈을 다음 순서로 해석하고 처음 확인된 exact `SKILL.md` 파일 하나를 읽습니다.

1. 현재 프로젝트의 `skills/{name}/SKILL.md`가 실제로 있으면 그 exact 파일.
2. 없으면 현재 런타임 active root의 exact 파일: Claude/Grok은
   `~/.claude/skills/{name}/SKILL.md`, Codex는 `~/.codex/skills/{name}/SKILL.md`, Antigravity는
   `~/.gemini/antigravity-cli/skills/{name}/SKILL.md` (명시 opt-in 설치 지원).
3. 둘 다 없으면 현재 런타임 전역 카탈로그(Claude/Grok
   `~/.claude/SKILLS-CATALOG.md`, Codex `~/.codex/SKILLS-CATALOG.md`, Antigravity
   `~/.gemini/antigravity-cli/SKILLS-CATALOG.md`)에서 모듈명과 정확히 일치하는 행을 찾습니다. 행이 정확히
   하나일 때만 `읽을 경로`의 절대 `SKILL.md`를 그대로 읽고, 누락·중복 행은 fail-closed입니다.
   기본 경로가 보통 `.olympus/source-skills` 아래여도 직접 조합하거나 추측하지 않습니다.
4. `module_root`는 그 `SKILL.md`의 부모입니다. 모듈의 `references/`, `scripts/`,
   `commands/`는 모두 이 루트를 기준으로 해석합니다.
5. Phase 4에 도달했을 때만 `docker_deploy_root`를 만듭니다. Phase 2에서 hard lock,
   외부 ledger, 크로스-CLI 혼합 분기를 실제 선택했을 때만 `orchestrator_root`를 만들고
   `${orchestrator_root}/commands/workpm-mcp.md`를 읽습니다. 선택하지 않은 모듈은 로드하지 않습니다.

이 exact 파일 읽기는 내부 모듈 로드입니다. 런타임 Skill 목록/레지스트리를 가용성 근거로
호출하거나 모듈 이름을 slash command로 실행하지 않습니다.

Phase 4의 `docker-deploy` 계약은 필수입니다. 카탈로그 행이나 `읽을 경로`, 필요한 reference를
읽지 못하면 `docs/zeus/zeus-log.md`에 `BLOCKED: docker-deploy source module unavailable`을
기록하고 dev-server 폴백을 실행합니다. 이 경우 Phase 4 증거는 `weak`이며 전체 결과를
SUCCESS로 표시하지 않습니다. MCP 분기가 선택됐지만 `orchestrator`를 읽지 못하면 동시 편집을
직렬화할 수 있는 경우에만 메인 순차 경로로 축소하고 `MCP: NOT RUN`을 기록합니다. hard lock
자체가 필수이면 Phase 2를 `BLOCKED`로 남깁니다. 어느 경우도 모듈 미발견을 PASS로 기록하지 않습니다.

### CLI Auto-Continue Contract

Zeus는 `zephermine → agent-team/workpm → argos → docker-deploy → minos → report`를 하나의 긴 작업으로 밀어붙이는 스킬입니다. 모델 지시만으로는 중간 보고 후 멈출 수 있으므로, 제품 파이프라인 요청으로 Zeus를 실행할 때는 Phase 0 전에 Chronos 자동 재개 가드를 부트스트랩합니다.

**네이티브 /goal과의 관계:** Claude/Codex/Antigravity에는 네이티브 `/goal`이 있고, 크로노스는 이를 1순위 지속성 엔진으로 씁니다. 그러나 `/goal`은 사용자 입력으로만 켜지므로(스킬이 자동 호출 불가), zero-interaction이 원칙인 Zeus는 **사용자 입력이 필요 없는 훅 자동 재개를 기본 엔진으로 유지**합니다. 단:
- 사용자가 `/zeus` 실행 전에 `/goal`을 이미 설정했다고 밝힌 경우 → goal이 지속성을 담당하므로 **setup-loop 부트스트랩을 생략**합니다 (goal + 훅 이중 Stop 게이트 방지 — 크로노스 `--goal-mode`와 동일한 충돌 방지 원칙)
- 파이프라인을 멈추고 `/goal` 설정을 요청하지 않습니다 (zero-interaction 위반)

CLI별 재개 방식:
- Claude Code: `.claude/loop-state.md` + Claude stop lifecycle hook
- Codex: `.codex/loop-state.md` + notify `save-turn -> continue-loop -> codex exec resume --last`
- Antigravity: `.chronos/loop-state.md` + Stop 훅/worker 루프

**부트스트랩 조건:**
- 사용자 요청이 Zeus 자체 점검/문서 수정이 아니라 제품/기능 구현 파이프라인일 것
- `auto-continue-loop/scripts/setup-loop.ps1` 또는 `.sh`를 찾을 수 있을 것. 현재 프로젝트의 `skills/auto-continue-loop/`를 먼저 쓰고, 없으면 현재 CLI의 글로벌 스킬 경로를 사용한다.
- 이미 현재 CLI의 상태 파일(Claude: `.claude/loop-state.md`, Codex: `.codex/loop-state.md`, Antigravity: `.chronos/loop-state.md`)이 활성 상태면 새로 만들지 말고 기존 루프를 존중할 것. 다른 CLI의 오래된 상태 파일은 현재 CLI의 Zeus 부트스트랩을 막지 않는다.

**Windows PowerShell:**
```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File skills/auto-continue-loop/scripts/setup-loop.ps1 `
  --max-iterations 20 `
  --completion-promise "Zeus Phase 0-6 complete" `
  "Zeus pipeline: {사용자 원문}. Run zephermine through minos and final report. Execute missing Phase 0-6 from docs/zeus/zeus-state.json; do not stop at next steps."
```

**Linux/macOS:**
```bash
bash skills/auto-continue-loop/scripts/setup-loop.sh \
  --max-iterations 20 \
  --completion-promise "Zeus Phase 0-6 complete" \
  "Zeus pipeline: {사용자 원문}. Run zephermine through minos and final report. Execute missing Phase 0-6 from docs/zeus/zeus-state.json; do not stop at next steps."
```

Phase 6에서만 완료 조건을 출력합니다:

```text
<promise>Zeus Phase 0-6 complete</promise>
```

중간에 컨텍스트가 부족하면 `docs/zeus/zeus-state.json`의 `currentPhase`를 다음 누락 phase로 저장하고 핸드오프를 생성한 뒤 종료합니다. 이 경우 완료 promise를 출력하지 않습니다.

### 실행 보장 게이트 (Phase 6 시작 전 필수)

모든 Phase의 실행 증거가 있어야 Phase 6를 시작할 수 있습니다:

- Phase 1: `plan.md` 존재
- Phase 2: `docs/zeus/zeus-log.md`에 agent-team 실행 기록 (완료 기준 장부 `checklist-status.md`의 proved 비율과 남은 AC ID)
- Phase 3: `docs/zeus/zeus-log.md`에 argos 실행 기록 (최소 정적 분석)
- Phase 4: `docs/zeus/zeus-log.md`에 Docker/dev-server 시도 기록
- Phase 5: QA 결과 파일 또는 `docs/zeus/zeus-log.md`에 minos 실행 기록

위 중 하나라도 없으면 Phase 6을 시작하지 말고, 누락된 phase를 먼저 실행.
컨텍스트가 부족하여 누락 phase 실행이 불가능하면: `zeus-state.json`의 `currentPhase`를 누락 phase로 설정하고 핸드오프.

### 완료 계약 (Completion Contract) — Phase별 증거 채점

> Loop Library 028 기반. "실행됨"이 아니라 "증명됨"을 완료 기준으로 삼아, 부분 파이프라인이 완료로 둔갑하는 것을 막는다.

실행 보장 게이트의 각 Phase 증거를 단순 존재 여부가 아니라 **4상태로 채점**해 `zeus-log.md`에 기록한다:

| 상태 | 의미 |
|------|------|
| `proved` | 증거가 현재 산출물에서 재현됨 (예: minos 통과율 100%, argos 통과 수치 충족) |
| `weak` | 실행은 됐으나 증거가 불충분 (예: 통과율 일부, 정적 분석만) |
| `missing` | 해당 Phase 증거 없음 |
| `contradicted` | 증거가 실패를 가리킴 (예: 빌드 실패, 테스트 레드) |

- Phase 6 리포트의 SUCCESS 판정은 **5개 Phase 증거가 모두 `proved`일 때만** 허용된다.
  하나라도 `weak`/`missing`/`contradicted`면 결과를 `PARTIAL` 또는 `BLOCKED`로 표기하고, 리포트에 미증명 항목을 명시한다.
- **`--max-iterations`(20) 소진이나 컨텍스트 부족은 `exhausted`(미완)이며 success가 아니다.** 이 경우 거짓 완료 promise 대신 핸드오프를 남긴다.
- 채점 결과는 Phase 6 리포트의 **요구사항→증거 표**(Decision Ledger 옆)에 모아 표시한다.

### 컨텍스트 보전 규칙

- Phase 2 완료 후 컨텍스트가 80% 이상 사용되었다면, **Phase 3~6을 다음 세션으로 위임**:
  1. `docs/zeus/zeus-state.json`에 `currentPhase: "verification"` 저장
  2. 핸드오프 파일 생성
  3. 사용자에게 "`/zeus`를 다시 실행하면 Phase 3(감리)부터 재개됩니다" 안내
- **Phase 6(리포트)만 먼저 작성하고 Phase 3~5를 건너뛰는 것은 금지**

---

## Phase 0: Description Parsing

사용자 한 줄 설명에서 구조화된 데이터 추출.

**절차:**
1. 사용자 입력 원문 저장
2. **산업군 매칭**: 키워드 테이블로 산업군 판별 (쇼핑몰→ecommerce, 병원→healthcare 등)
3. **기술스택 추출**: 정규식으로 frontend/backend/db/mobile 추출
4. **DB 추론**: 미명시 시 백엔드에서 추론 (Spring Boot→PostgreSQL 등)
5. **기능 목록 생성**: 산업별 기본 기능 세트 + 설명에서 명시된 기능
6. **프로젝트 타입 판별**: fullstack-web / api-only / static-site / cli / mobile / library
7. **프로젝트명 추론**: 핵심 명사 → kebab-case

**상세 파싱 규칙**: [references/description-parser.md](references/description-parser.md)

파싱 결과 예시:
```
입력: "쇼핑몰 만들어줘. React+Spring Boot"
→ industry: "ecommerce"
→ techStack: { frontend: "React", backend: "Spring Boot", db: "PostgreSQL" }
→ features: ["상품관리", "장바구니", "결제", "주문", "회원", "검색", "리뷰"]
→ projectType: "fullstack-web"
→ projectName: "shopping-mall"
```

**이전 실행 아카이브**: Phase 0의 첫 번째 동작으로 이전 산출물을 타임스탬프 디렉토리로 이동합니다.
[상세 아카이브 절차 → references/archive-procedure.md](references/archive-procedure.md)

파싱 완료 시 `docs/zeus/zeus-state.json` 생성 (재개 지원용).
**상세 스키마**: [references/phase-transitions.md](references/phase-transitions.md)

---

## Phase 1: Planning (zephermine 26단계)

zephermine SKILL.md를 읽고 26단계를 따르되, **모든 사용자 질문을 자동선택으로 대체**.

**질문 자동선택 규칙 (Recommended First):**
1. 질문 옵션에 `(Recommended)` 라벨이 있으면 해당 옵션을 자동 선택
2. 다중 선택 질문이면 `(Recommended)` 옵션을 모두 선택
3. `(Recommended)` 옵션이 없으면 아래 자동 응답 테이블의 단계별 기본값 사용
4. 모든 자동 선택 결과는 `[ZEUS-AUTO]` 태그로 로그 기록

**자동 응답 테이블 (Fallback)**: [references/auto-interview-generator.md](references/auto-interview-generator.md) 참조

- zephermine: 코드 리서치(코드 있으면 YES), GitHub 유사 프로젝트(YES), 웹 리서치(ALL)
- zephermine Step 6: **합성 트랜스크립트 생성** / Step 9: **셀프 리뷰** / Step 12~13: 수용+즉시 승인
- zephermine Step 21~22: SKILLS-CATALOG.md 참조, 추가 설치 불필요 (글로벌 스킬)
- argos: 결과 즉시 승인 / agent-team: Wave Plan 즉시 실행, 실패 섹션 재시도
- minos: 전체 시나리오, docker-compose 우선, 없으면 dev server 자동 실행

**Step 6 합성 인터뷰 생성**: Phase 0 파싱 결과 + 산업별 프리셋 조합으로 CPS Phase C/P/S + Gate 1/2/3 구조의 인터뷰 트랜스크립트를 자동 생성.
[생성 로직 → references/auto-interview-generator.md](references/auto-interview-generator.md)
[산업별 프리셋 → references/autopilot-defaults.md](references/autopilot-defaults.md)

**Phase 1 완료 조건:**
- `plan.md` 존재
- `sections/` 디렉토리에 1개 이상 섹션 파일 존재

---

## Phase 2: Implementation (포세이돈 → 메인 순차 폴백)

구현 도구를 자동 선택합니다:

```
Phase 1 완료 (plan.md + sections/ + flow-diagrams/)
    ▼
독립 섹션 + 네이티브 위임 도구 + 병렬 이득이 있는가?
  ├── 예 → 포세이돈(agent-team / Codex: agent-team-codex) — 섹션 기반 병렬 구현
  └── 아니오 → workpm의 동일 계약을 메인 컨텍스트에서 순차 실행
```

**판별 방법**: Phase 2 시작 시 섹션별 파일 범위가 독립적인지와 현재 CLI의 네이티브 위임 기능을 함께 확인합니다. 위임 자체가 가능해도 같은 파일을 순서대로 고쳐야 하면 메인 순차 경로를 선택합니다.

| 의미 역할 | Claude | Codex | Antigravity | Grok |
|-----------|--------|-------|--------|------|
| 읽기 전용 탐색 | `Explore` | `explorer` | `research` | `explore` |
| 파일 수정·명령 실행 | `general-purpose` / named teammate | `worker` | 메인 또는 쓰기 도구를 명시한 사용자 정의 서브에이전트 | `general-purpose` |

읽기 전용 역할에는 파일 쓰기를 지시하지 않습니다. 메인 컨텍스트가 `zeus-log.md`, Wave ledger, 공유 활동 로그와 완료 판정을 단독 소유하고, 작업자는 고유 파일 범위 또는 반환값만 담당합니다.

**경로 A — 포세이돈** (병렬 팀/서브에이전트 사용 가능):
- Claude: `skills/agent-team/SKILL.md` / Codex: `skills/agent-team-codex/SKILL.md`
- Step 0(산출물 검토) → Step 1(index 파싱) → Step 2(Wave Plan, [ZEUS-AUTO] 즉시 "실행") → Step 3~4(Task + Wave) → Step 5(Code Review) → Step 6(체크리스트) → Step 7(Activity Log) → Step 8(Final Report)

**경로 B — workpm 메인 순차 실행** (위임 부재 또는 병렬 이득 없음):
- 활성 `workpm` 하네스의 5단계 계약 중 Phase 2부터 메인 컨텍스트에서 순차 실행합니다.
  젭마인 산출물이 있으므로 Phase 1 리서치는 다시 하지 않습니다. hard lock·외부 task ledger·혼합
  CLI가 실제로 필요할 때만 위 source-only resolver로 `orchestrator` 모듈을 읽고 MCP 분기를 사용합니다.

**공통 규칙:**
- 병렬 경로에서는 Lead가 조정에 집중하고, 메인 순차 경로에서는 같은 Lead가 실행자 역할도 소유
- zeus-log.md에 선택된 경로(A/B) + 완료 기준 proved 비율(`checklist-status.md`) + 도면 매칭률 기록
- 구현 중 섹션에 없는 작업이 필요해 보이면 스코프 게이트(CRITICAL RULES 8) 판정 후 진행 — 무단 스코프 확장 금지

**실패 시 폴백 (Phase 2는 skip 금지):**
- `plan.md` 미생성 → Phase 0 파싱 결과 기반 최소 plan 생성 후 즉시 실행
- `sections/` 미생성 → 최소 1개 통합 섹션 생성 후 단일 구현 실행
- 포세이돈 작업자가 모두 실패 → 같은 섹션을 workpm 메인 순차 경로로 자동 전환
- 순차 경로도 실패 → 실패한 단일 섹션만 최소 구현 단위로 축소해 재검증

---

## Phase 3: Verification (argos — 감리)

시공 완료 후 설계 대비 준공검사.

1. `<planning_dir>` 경로를 Phase 1에서 받아서 전달
2. argos Phase 0~7 순차 실행 → `verify-report.md` 생성 (Phase 6은 design-system.md 있을 때만, Phase 7 보안은 항상)
3. 검증 결과 자동 승인 (zeus는 무중단) — 단, argos 통과/미통과 **항목 수치**를 zeus-log.md에 기록. "실행됨"이 아니라 통과 수치가 SUCCESS 판정의 근거다 (→ references/final-report-format.md 판정 기준)

**교차모델 수렴 게이트 (034, 위험 트리거 시에만):**

argos의 1차 감리는 결정론적이다 — 정적 분석·빌드·테스트 수치가 PASS/FAIL을 가른다. 다른 모델은 여기서 부르지 않는다(느리고 새 신호가 없다).
아래 **위험 신호가 있는 변경에 한해**, 종료 직전 1회 교차모델 리뷰를 추가한다:

- 위험 신호: 인증/결제/보안 경로, DB 마이그레이션, 공개 API 변경, 동시성/트랜잭션, 테스트가 없는 영역, 큰 diff.
- 방식: Claude 구현분을 다른 패밀리(Antigravity의 Gemini 모델 또는 Codex `/review`)가 1패스 리뷰 → 블로커만 수정. 정말 중요한 소수는 양쪽이 동일 버전을 승인할 때까지 최대 2라운드.
- zero-interaction 유지: 리뷰는 백그라운드로 띄워 Phase 4와 병렬 진행한다. 한쪽 패밀리만 가용하면 single-model review로 라벨하고 consensus를 주장하지 않는다.
- 결과(적용 여부·사유·승인 커밋)를 Decision Ledger에 `[ZEUS-AUTO:taste]`로 기록한다.

**Workflow 검증 fan-out (ultracode 세션 한정, Claude 전용):**

> 정책: 스킬은 Workflow를 자동 호출하지 않는다 (과금 옵트인 전제). 이 분기는 시스템 리마인더가
> **ultracode ON을 확인해준 세션에서만** 활성 — 그 외에는 존재하지 않는 것처럼 취급하고,
> 파이프라인을 멈추고 ultracode를 켜달라고 요청하지도 않는다 (zero-interaction 유지).

- 조건 3개 모두 충족 시: Claude 세션 + ultracode ON 확인됨 + Workflow 도구 가용
- 동작: argos 1차 감리의 검증 항목(정적 분석·AC 대조·경계면 정합)을 Workflow로 fan-out —
  차원별 finder 병렬 → 발견별 적대적 검증(반박 시도, 과반 생존만 채택) → 수치 집계
- 산출은 동일: `verify-report.md` + zeus-log.md 통과 수치. **판정 기준·완료 계약 불변** — 엔진만 바뀌고 증거 형식은 같다
- 교차모델 수렴 게이트(034)와의 관계: 위험 트리거 시 교차모델 리뷰는 그대로 유지 — Workflow fan-out은 argos 내부 검증의 병렬화이지 타 모델 리뷰의 대체가 아니다
- ultracode OFF 또는 비-Claude CLI: 현행 argos 스킬 체이닝 그대로
- Decision Ledger 기록: `[ZEUS-AUTO:mechanical] Phase 3 엔진: Workflow fan-out (ultracode ON 세션)`

**폴백 조건 (Phase 3은 skip 금지):**
- 설계 산출물이 없어도 **정적 분석(코드 품질/보안)은 항상 실행**
- 빌드 실패 → 보고서에 기록하고 Phase 4로 진행

---

## Phase 4: Docker Setup (docker-deploy)

테스트 전에 Docker 환경 구성 및 컨테이너 실행.

[상세 절차 및 포트 충돌 해결 스크립트 → references/docker-setup.md](references/docker-setup.md)

**핵심 흐름:**
1. 위 resolver로 `docker-deploy` 행의 정확한 `SKILL.md`를 읽고 `docker_deploy_root` 설정
2. 모듈 계약의 프로젝트 분석과 필요한 `${docker_deploy_root}/references/*`를 읽음
3. `docker --version` 확인 → 없으면 dev server fallback
4. 로드한 모듈 계약이 선언한 Compose 산출물(현 계약: `docker-images/docker-compose.yml`)과
   프로젝트의 기존 Compose 파일을 확인해 실제 `compose_file`을 고정. 루트 파일을 가정하지 않음
5. `compose_file`이 없으면 Phase 0의 techStack·자동 기본값으로 모듈 계약을 직접 수행하고
   생성된 파일의 실경로를 다시 확인
6. `compose_file`에서 포트 추출 후 충돌 해결 (Windows: Get-NetTCPConnection, Linux: lsof)
7. `docker compose -f "{compose_file}" up -d --build` + 헬스체크 대기 (최대 120초)
8. 모듈 수행/Compose 실행 실패 시 dev server fallback + zeus-log.md에 `FAILED`, Phase 4 `weak` 기록

Zero-interaction 규칙 때문에 모듈의 질문 단계는 Phase 0 파싱 결과와 자동 응답 테이블로 채웁니다.
등록된 `docker-deploy` 호출을 시도하지 않습니다. 모듈 로드 실패와 Docker 런타임 부재를 구분해
기록하고, 전자는 Phase 4 `weak`, 후자는 계약을 읽은 뒤 실행 환경 폴백으로 판정합니다.
모듈 계약 수행 또는 생성된 Compose 실행이 실패한 경우도 Phase 4 `weak`이며 SUCCESS 근거로
승격하지 않습니다.

---

## Phase 5: Testing (minos)

구현 완료 후 자동 E2E 테스트.

1. `qa-scenarios.md` 존재 확인 (Phase 1에서 생성됨)
2. Playwright 미설치 시 `npx playwright install` 자동 실행
3. minos Step 1~6 실행:
   - Step 3: Phase 4에서 서버 이미 실행 중이면 헬스체크만
   - Step 5: Healer 루프 (최대 5회)
4. 결과 집계 — minos **통과율(통과/전체)**을 zeus-log.md에 기록 (SUCCESS 판정의 필수 근거. 통과율 없이 SUCCESS 금지)

**폴백 조건 (Phase 5는 skip 금지):**
- 서버 시작 불가 → `--api-only` 모드로 minos 실행
- QA 시나리오 미존재 → 프로젝트 구조에서 기본 시나리오 현장 생성 후 실행
- Playwright 설치 실패 → 실패 원인과 재실행 명령을 minos Step 1/2/6로 리포트

---

## Phase 6: Final Report

[리포트 형식 및 결과 판정 기준 → references/final-report-format.md](references/final-report-format.md)

`docs/zeus/zeus-report.md`에 저장. Phase 0~5 실행 증거가 모두 있어야 진입 가능.

리포트에는 Decision Ledger와 함께 **완료 계약 요구사항→증거 표**(Phase별 `proved`/`weak`/`missing`/`contradicted`)를 포함한다. 5개 Phase가 모두 `proved`가 아니면 SUCCESS로 표기하지 않는다(완료 계약 규칙).

---

## Error Handling Policy

**절대 멈추지 않는다 — 기록하고 계속한다.**

| 등급 | 예시 | 대응 |
|------|------|------|
| FATAL | 디스크 쓰기 불가 | 즉시 중단 + 메시지 |
| PHASE_FALLBACK | plan 미생성, 서버 시작 불가 | phase 폴백 경로 실행 + 로그 |
| STEP_RETRY | 개별 task 실패, 테스트 실패 | 1회 재시도 후 실패 내역 기록 |
| RECOVERABLE | 네트워크 타임아웃 | 1회 재시도 후 폴백 |

모든 에러는 `docs/zeus/zeus-log.md`에 타임스탬프와 함께 기록.

---

## Resume Support (재개)

`/zeus` 재실행 시:
1. `docs/zeus/zeus-state.json` 존재 확인
2. 존재하면: 현재 phase 확인 → 해당 phase부터 재개
3. 존재하지 않으면: 새로 시작

**상세 전환 규칙**: [references/phase-transitions.md](references/phase-transitions.md)

---

## Quick Start

```
# 기본 사용
/zeus "할일 관리 앱 만들어줘. React+Express"

# 기술스택 상세 지정
/zeus "병원 예약 시스템. Next.js+FastAPI+PostgreSQL"

# 간단한 요청
/zeus "블로그 만들어줘"
```

---

## Related Files

**Zeus references/**
- [description-parser.md](references/description-parser.md) — 파싱 규칙
- [autopilot-defaults.md](references/autopilot-defaults.md) — 산업별 프리셋
- [auto-interview-generator.md](references/auto-interview-generator.md) — 합성 인터뷰
- [phase-transitions.md](references/phase-transitions.md) — 상태 전환/재개
- [archive-procedure.md](references/archive-procedure.md) — Phase 0 아카이브
- [docker-setup.md](references/docker-setup.md) — Phase 4 Docker 상세
- [final-report-format.md](references/final-report-format.md) — Phase 6 리포트 형식

**외부 하네스와 내부 모듈 (Phase별)**
- Phase 1: `skills/zephermine/SKILL.md`
- Phase 2 경로 A: `skills/agent-team/SKILL.md` / `skills/agent-team-codex/SKILL.md`
- Phase 2 경로 B: 활성 `workpm` 하네스; MCP를 선택한 경우에만
  `${orchestrator_root}/commands/workpm-mcp.md`
- Phase 4: 전역 카탈로그 `docker-deploy` 행의 `읽을 경로` + `${docker_deploy_root}/references/*`
- Phase 5: `skills/minos/SKILL.md`

---

## Output Artifacts

- Phase 0: `docs/zeus/zeus-state.json` (재개용), `docs/zeus/zeus-log.md` (실행 로그), `docs/zeus/archive/{timestamp}/` (이전 실행 아카이브)
- Phase 1: `interview.md`, `plan.md`, `sections/`, `qa-scenarios.md`
- Phase 6: `docs/zeus/zeus-report.md` (최종 보고서)
