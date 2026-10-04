---
name: kit
description: x-mesh toolkit — list available tools and their status
---

<Purpose>
Show available x-mesh tools and their installation status.
</Purpose>

<Use_When>
- User asks "what tools are available"
- User says "xm", "x-mesh tools"
</Use_When>

<Do_Not_Use_When>
- User wants a specific tool (use x-build or x-op directly)
</Do_Not_Use_When>

# xm — x-mesh Toolkit

## First-Run Init Check

**Before executing any xm subcommand** (except `init` itself), verify the project is initialized:

1. Check `test -f .claude/hooks/trace-session.mjs` in the current working directory.
2. If **missing**, pause the requested command and prompt via AskUserQuestion:
   - header: `xm init`
   - option 1 label: `Yes (권장)` — description: `hooks + settings + x-sync client 설치`
   - option 2 label: `Skip sync` — description: `hooks + settings만, x-sync 제외`
   - option 3 label: `No` — description: `이번만 건너뛰기`
3. Before the AskUserQuestion, print:
   ```
   ⚠ xm이 이 프로젝트에 초기화되지 않았습니다.
     설치 항목: trace hook, block-marketplace hook, .claude/settings.json, x-sync client
   ```
4. On **Yes** → run `xm init`. On **Skip sync** → run `xm init --skip-sync`. On **No** → proceed with the original command without init (do not re-prompt this session).
5. After init completes, resume the originally requested subcommand.

Skip this check when the user explicitly invokes `xm init`, `xm doctor`, or passes `--no-init-check`.

For a fuller picture (not just trace-session.mjs), suggest `xm doctor` — but the fast `test -f` check is sufficient as the entry gate.

## Model Routing

| Subcommand | Model | Reason |
|------------|-------|--------|
| `version`, `update`, `agents list/match/get` | **haiku** (Agent tool) | Read-only, no reasoning needed |
| `cost`, `cost --session` | **haiku** (Agent tool) | Read-only aggregation |
| `config show/set/get/reset` | **haiku** (Agent tool) | Simple command execution |
| `config` (interactive wizard) | **session** (leader) | Requires AskUserQuestion — leader-only |
| `init`, `init --dry-run`, `init --skip-sync`, `init --with-server`, `init --rollback` | **session** (leader) | Multi-step install orchestration (backup + hooks + settings merge + curl) |
| `doctor`, `doctor --fix` | **session** (leader) | Diagnostic reasoning + conditional AskUserQuestion for network fixes |
| `pipeline list`, `validate` | **haiku** (Agent tool) | Read-only display |
| `pipeline <name>` | **session** (leader) | Multi-step orchestration with AskUserQuestion |

For haiku-eligible commands, delegate via: `Agent tool: { model: "haiku", prompt: "Run: [command]" }` <!-- managed-model: writer -->

### Model Guardrail

Before delegating to haiku, verify the task is display/query only. If ANY of the following apply, use sonnet or higher — never haiku:

| Signal | Example | Why |
|--------|---------|-----|
| Produces analysis or recommendations | code review, plan critique, risk assessment | Reasoning quality degrades |
| Generates or modifies code | implement feature, fix bug, refactor | Edge case handling (NaN, negative, boundary) drops significantly |
| Multi-step orchestration | strategy execution, pipeline run | Loses coherence across steps |
| Evaluates quality | x-eval scoring, x-probe validation | Calibration requires stronger model |

If a haiku-eligible command receives `--thorough` or similar depth flags, escalate to sonnet.

**Scope:** This guardrail applies to top-level command routing only. Sub-agents spawned by the leader inherit the leader's model context and do not require a separate routing check.

**Violation output:** If the leader detects a reasoning task routed to haiku (e.g., via user override or misconfigured pipeline), prepend this warning to the output:
```
⚠️ Model mismatch: this task requires reasoning but is running on haiku.
   Results may miss edge cases. Re-run without --model haiku for full quality.
```

## AskUserQuestion Dark-Theme Rule

**CRITICAL:** The `question` field in AskUserQuestion is invisible on dark terminals.

**Visibility map:**
| Element | Visible | Use for |
|---------|---------|---------|
| `header` | ✅ YES | Short context tag (e.g., "x-op bump", "Pipeline") |
| `question` | ❌ NO | Keep minimal — user cannot see this text |
| option `label` | ✅ YES | Primary info — must be self-explanatory |
| option `description` | ✅ YES | Supplementary detail |

**Always follow this pattern:**
1. Output ALL context (descriptions, status, analysis) as **regular markdown text** BEFORE calling AskUserQuestion
2. `header`: put the key context here (visible, max 12 chars)
3. `question`: keep short, duplicate of header is fine (invisible to user)
4. Option `label` + `description`: carry all decision-relevant information

**WRONG:** Putting context in `question` field → user sees blank space above options
**RIGHT:** Print context as markdown first, use `header` for tag, options for detail

Show available tools:

```
x-mesh Toolkit (xm) — pick a tool by what you're doing ("쓸 때")

Plan & build:
  /xm:build     PRD → tasks → DAG 실행·비용예측    쓸 때: 멀티스텝 기능을 계획·관리
  /xm:batch     topic별 병렬 PR (plan→구현→merge)   쓸 때: 독립 기능 여러 개를 PR 여러 개로 한 번에
  /xm:op        17 전략 오케스트레이션              쓸 때: 한 문제를 여러 전략으로(refine/debate/tournament…)
  /xm:agent     fan-out · delegate · consensus      쓸 때: 에이전트 여러 개를 직접 오케스트레이션
  /xm:solver    decompose · iterate · constrain     쓸 때: 막힌 문제를 구조적으로 분해

Review & quality:
  /xm:review    PR 코드 리뷰 (severity + LGTM)       쓸 때: 변경 코드를 다관점 리뷰
  /xm:eval      출력 품질 채점 (multi-rubric, A/B)   쓸 때: 에이전트/프롬프트 출력을 점수화
  /xm:panel     크로스모델 적대 패널 (claude/codex…)  쓸 때: 여러 LLM으로 교차검증/적대 리뷰
  /xm:plan      구현 계획 작성·검증                    쓸 때: lifecycle 없이 계획을 만들고 `.xm/plan/`에 저장
  /xm:probe     전제 검증 — 나쁜 아이디어 조기 사살   쓸 때: 만들기 전에 가정이 맞는지
  /xm:mutate    mutation testing — 기존 test 탐지력 확인 쓸 때: test 사각지대 후보를 찾기

Knowledge & memory:
  /xm:recall    과거 산출물 인덱스 (review/op/plan…)  쓸 때: 지난 세션의 리뷰/op/plan을 찾기
  /xm:memory    교차세션 결정·패턴 기억              쓸 때: 결정을 영속화·자동 주입
  /xm:trace     실행 타임라인·토큰/비용 추적          쓸 때: 멀티에이전트 실행을 관찰/리플레이

Writing & retro:
  /xm:humanize  AI 글투 제거 (EN+KO)                 쓸 때: AI스러운 텍스트를 자연스럽게
  /xm:write     PR·issue·릴리스 문서 작성             쓸 때: diff 근거로 PR/issue 올리기
  /xm:humble    구조적 회고 — 실패 근본원인          쓸 때: 실패를 함께 돌아보고 배우기

Ops:
  /xm:dashboard .xm 상태 웹 대시보드                  쓸 때: 빌드/리뷰/op 상태를 한 화면에
  /xm:ship      릴리스 자동화 (commit→bump→push)      쓸 때: 릴리스 컷
  /xm:sync      다기기 .xm 동기화                     쓸 때: 여러 머신에서 상태 공유
  /xm:wt        세션 worktree — 격리 후 부모로 land    쓸 때: 세션 전체를 worktree에서 작업
  /xm:remote    Discord로 원격 Claude/Codex 세션 조종   쓸 때: Linux host 세션을 밖에서 모니터·개입
  /xm:kit       이 개요 + config/version/doctor/cost  쓸 때: 도구 목록·설치 상태·설정

대부분 직접 호출. review/eval/solver/trace/humble는 op/build/panel 파이프라인 안에서도
자동 실행되므로 직접 /xm:<도구> 호출 통계엔 잘 안 잡힐 수 있음 — 미사용이 아니라 간접 사용.

Pipeline:
  /xm:kit pipeline <name>    Run a named plugin pipeline (release, full, etc.)
  /xm:kit pipeline list      Show all pipelines (config + auto-discovered)
  /xm:kit validate           Check Wiring DAG for cycles and errors

Install bundle:     /plugin install xm@kit
Install individual: /plugin install xm@build
```

## Sub-file Loading

**Progressive disclosure — use the Read tool to load the required sub-file BEFORE emitting any subcommand output.** The stubs below give you routing + key flags; the sub-file holds the executable procedure (bash blocks, schemas, node -e heredocs). If you generate a subcommand response without first reading the sub-file, you have fabricated the procedure.

Mechanism (strict):
1. **Locate the base directory.** The Claude Code skill loader substitutes `${CLAUDE_PLUGIN_ROOT}` to an absolute path when rendering this SKILL.md, and also injects a `Base directory for this skill: <absolute path>` header at the top of the prompt. Either source gives you the real absolute path already — just read it off.
2. **Resolve the sub-file path** — look up the subcommand in the routing table below to get the `Required file` (e.g., `commands/init.md`), then pass `${CLAUDE_PLUGIN_ROOT}/skills/kit/<Required file>` to the Read tool. Since the skill loader substitutes `${CLAUDE_PLUGIN_ROOT}` in the rendered SKILL.md content you see, the path you send to Read is already absolute.
3. **Fallback (only if step 2 fails — corrupted cache, edge case):** resolve the path via Bash `ls -d ~/.claude/plugins/cache/xm/xm/*/skills/kit/ | sort -V | tail -1` — `sort -V` on the full path picks the semver-latest version (so `1.31.10` beats `1.9.0`). Use that path as your base.
4. Then execute the procedure found in that file.

| Subcommand | Required file |
|------------|---------------|
| `cost`, `cost --session` | `commands/cost.md` |
| `init`, `init --dry-run`, `init --skip-sync`, `init --with-server`, `init --rollback` | `commands/init.md` |
| `doctor`, `doctor --fix` | `commands/doctor.md` |
| `version`, `update`, `update <plugin>` | `commands/version-update.md` |
| `pipeline <name>`, `pipeline list`, `validate` | `commands/pipeline.md` |
| `config`, `config show/set/get/reset` | `commands/config.md` |
| `agents list/match/get` | `references/agent-catalog.md` |
| (any cross-plugin data flow question) | `references/cross-plugin-pipeline.md` |

## Status Symbols

Two parallel conventions — do not mix them.

**Install actions** (init output):
| Symbol | Meaning |
|--------|---------|
| `➕ installed` | New item written |
| `🔄 updated` | Existing item replaced with newer content |
| `✅ already installed` | Content matches, no change |
| `🚫 skipped` | User flag skipped this step |
| `🔍 would install/update` | Dry-run preview only |

**Health status** (doctor output):
| Symbol | Meaning |
|--------|---------|
| `✅` | OK |
| `⚠️` | Degraded — works but suboptimal |
| `❌` | Broken — feature unavailable |
| `⏭️` | Not applicable for this context |

## Cost

Load `commands/cost.md` before executing. Aggregates `cost_usd` from `.xm/build/metrics/sessions.jsonl`, grouped by type and model. Flags: `--session` (current session only).

## Init

Load `commands/init.md` before executing. Installs `trace-session.mjs` hook, merges hook entries into `.claude/settings.json` (auto-backup of prior settings, keeps 5 most recent), and runs `curl ... | bash -s client` to install x-sync. Flags: `--dry-run` (preview, no writes), `--skip-sync` (hooks only), `--with-server` (also installs x-sync server, needs Bun), `--rollback` (restores settings.json from most recent backup). Uses install-action symbols above.

## Doctor

Load `commands/doctor.md` before executing. Checks: trace-session hook presence + freshness, settings.json hook entries, x-sync PATH, Bun. Emits health symbols above. Flags: `--fix` (auto re-runs `xm init` for local fixes; AskUserQuestion before network installs). **Note:** `block-marketplace-copy.mjs` check only applies inside the xm repo — it is intentionally omitted from per-project installs.

## Version & Update

Load `commands/version-update.md` before executing. `version` compares `installed_plugins.json` vs marketplace `.claude-plugin/marketplace.json`. `update [plugin]` **MUST** run `cd ~/.claude/plugins/marketplaces/xm:kit && git pull origin main` first (step 1, non-skippable), then `claude plugin update <name>@xm -s user`. After update, hint user to run `/reload-plugins` and consider `xm init` for hook refresh.

## Cross-Plugin Pipeline

Load `references/cross-plugin-pipeline.md` — data-schema reference. Defines the `xkit_payload` v1 envelope (version, source, type, content, metadata) and the producer/consumer matrix for x-build ↔ x-op ↔ x-eval. Use this when reasoning about what data flows between plugins.

## Pipeline

Load `commands/pipeline.md` — runtime execution reference. Combines SKILL.md Wiring declarations (`after:` = auto-run, skip on upstream failure; `suggests:` = prompt user, default N, show regardless) with user-defined named pipelines in `.xm/config.json` under `pipelines.<name>`. **Config pipeline overrides SKILL.md Wiring completely — no merge.** Modes: interactive (default, `[Y/n/skip]` per step), `--auto` (silent, halt on failure), `--dry-run` (plan only).

## Shared Config

Load `commands/config.md` before executing. `config` with no args = interactive wizard via AskUserQuestion over 5 settings (model_profile, budget, agent_max_count, mode, model_overrides). `set/get/show/reset` are direct CLI. Scope: default global (`~/.xm/config.json`); `--local` writes to `.xm/config.json`; `budget` defaults to local (per-project).

## Agent Catalog

Load `references/agent-catalog.md` before executing. 37 specialist agents at `xm/agent-catalog/` (NOT `agents/`, which Claude Code would auto-register as native subagents) with two layers — `rules/<name>.md` (full, ~240 lines) and `slim/<name>.md` (~30 lines, for prompt injection). CLI: `node ${CLAUDE_PLUGIN_ROOT}/lib/agent-catalog.mjs {list|match "<topic>" --count N|get <name> [--slim]}`. Consumed by x-op broadcasts, x-review `--specialists`, x-solver fan-out, x-build research.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll write my own config parser" | xm's shared config exists for cross-plugin consistency. Duplicating it creates drift that sync-bundle can't catch and that users can't debug. |
| "I'll guess the cost, close enough" | Cost estimates are cheap; surprise bills are expensive. Use the cost engine — it's one call. |
| "Model routing is overengineering" | Model routing is ~78% savings on haiku-eligible commands. That's math, not engineering. |
| "This doesn't need a DAG, tasks are trivial" | DAGs make dependencies explicit. Trivial tasks with implicit dependencies are how parallel runs silently serialize on shared state. |
| "The model guardrail will catch wrong routing" | The guardrail is a safety net, not a planner. Use it for defense in depth, not as your first line of thinking. |
| "I don't need to read shared config, defaults are fine" | Defaults are fine in isolation. Cross-plugin coordination requires reading the actual config — otherwise plugins disagree about state. |
| "Agent catalog is a nice-to-have" | The catalog is how agent rules get discovered across sessions. Without it, every new agent spawn starts from scratch. |
