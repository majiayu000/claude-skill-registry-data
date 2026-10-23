---
name: prp-implement
description: 'Executes PRP plan files with validation loops, reports, and archiving. Use when implementing a .plan.md file, executing a PRP plan, or running parallel PRP tasks.'
argument-hint: '[--parallel | --team] [--worktree] [--no-worktree] [--dry-run] <path/to/plan.md>'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Agent
  - AskUserQuestion
  - TaskCreate
  - TaskGet
  - TaskList
  - TaskUpdate
  - SendMessage
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - Bash(mv:*)
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pnpm:*)
  - Bash(yarn:*)
  - Bash(bun:*)
  - Bash(uv:*)
  - Bash(python:*)
  - Bash(python3:*)
  - Bash(pytest:*)
  - Bash(cargo:*)
  - Bash(go:*)
  - Bash(make:*)
  - Bash(curl:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/*.sh:*)'
---

# PRP Implement

Execute a plan file step-by-step with continuous validation. Every change is verified immediately; never accumulate broken state. Detect the package manager, prepare the Git branch, execute tasks, validate static/unit/build/integration/edge cases, write `docs/prps/reports/`, and archive the plan. Detect parallel-capable plans and prompt for execution mode unless a flag selects it.

> Adapted from PRPs-agentic-eng by Wirasm. Part of the PRP workflow series.

## Gates

- If validation fails, fix it before moving on. Never accumulate broken state.
- Reject mutually exclusive flags and invalid team/dry-run combinations in Phase 0.
- `--team` requires a parallel-capable plan; never silently fall back.
- Prepare the feature branch before any agent dispatch. All execution and later artifacts use the single execution tree, not per-agent isolation.
- Dry-run prints the roster and exits without team/task/agent tools.
- Parallel validation failure stops the pipeline before the next batch. No auto-retry, no skipping a failed batch; preserve completed work and let the user decide.

**Questions:** class `choose-path` (execution mode for a parallel-capable plan): headless (no question tool or chat turn), run sequential (Path A); class `failure-recovery` (batch validation): stop, preserve completed work, and print the failing batch plus the resume command. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Phase 0 — DETECT

### Flag Parsing

Extract flags from `$ARGUMENTS` before treating the remainder as a plan path:

| Flag            | Effect                                                                                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--parallel`    | Force standalone parallel execution when the plan has `Batches`; skip the prompt. Otherwise warn and fall back to sequential. Works in Claude Code, Cursor, Codex. |
| `--team`        | Claude Code only: force agent-team parallel execution with shared task-graph observability. Abort if no `Batches`.                                                 |
| `--worktree`    | Silent legacy no-op; isolation is on by default.                                                                                                                   |
| `--no-worktree` | Force worktree mode off regardless of annotations; use the prepared current checkout.                                                                              |
| `--dry-run`     | Only with `--team`: print team name, full task graph with dependencies, and per-batch roster, then exit without teammates.                                         |

Set `PARALLEL_FLAG=true|false`, `AGENT_TEAM_FLAG=true|false`, `WORKTREE_MODE=true|false`, `DRY_RUN=true|false`. The remaining text is the plan file path.

Validation (abort with these exact messages):

- Both `--parallel` and `--team`: `--parallel and --team are mutually exclusive. Pick one.`
- `--team` without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`: `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`
- `DRY_RUN=true` and `AGENT_TEAM_FLAG=false`: `--dry-run requires --team.`
- Both `--worktree` and `--no-worktree`: `--worktree and --no-worktree are mutually exclusive. Use --no-worktree to opt out of the default.`

`--no-worktree` combines freely with `--parallel` and `--team`. Cursor/Codex bundles lack team tools: reject `--team` with guidance to use `--parallel`.

### Package Manager and Validation Scripts

Read `references/detection.md` now for the lockfile/package-manager/runner table. Inspect `package.json` (or equivalent) and record available type-check, lint, test, build commands.

## Dispatch Contract

Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/standalone-dispatch.md` for standalone dispatch and common preparation (§§8–9).
Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md` §8.2 only when `--team` is passed.

## Phase 1 — LOAD

Read the stripped plan path (`PLAN_PATH`); extract Summary, Patterns to Mirror, Files to Change, Step-by-Step Tasks, Validation Commands, Acceptance Criteria. Missing or invalid plan:

```
Error: Plan file not found or invalid.
Run /ycc:prp-plan <feature-description> to create a plan first.
```

Read `references/detection.md` (Parallel-Capable Detection and Execution Mode Decision) now. A `## Batches` section makes the plan parallel-capable: parse its ordering and task `BATCH:` fields. Select sequential or parallel standalone execution; record `EXECUTION_MODE=sequential|parallel`.
With `--team`, select Path C and record `EXECUTION_MODE=agent_team`.

Apply the common worktree precedence/deduction in standalone-dispatch.md §8.1. Scan the plan's worktree annotations:

```bash
grep -c "^## Worktree Setup" "$PLAN_PATH" || echo 0
grep -c "^\- \*\*Worktree\*\*:" "$PLAN_PATH" || echo 0
```

With a parent annotation, use its path before whitespace/comment and slug segment after `<repo>-`. Otherwise derive `WT_FEATURE_SLUG` from plan basename: strip `.plan.md`, lowercase, replace `[^a-z0-9-]` with `-`, collapse runs, truncate to 40 chars. `WORKTREE_ACTIVE` follows common mode selection; sequential tasks use the parent execution tree too.

**CHECKPOINT**: Plan loaded. All sections identified. Tasks extracted. Parallel capability detected. Execution mode chosen.

## Phase 2 — PREPARE

Follow standalone-dispatch.md §8.2 for Git-state inspection, required branch preparation, one-time parent worktree setup, and one-way plan relocation. Input plan is the stripped `$ARGUMENTS`; optional companion artifacts ride as extra move arguments. Retain `$PLAN_PATH` as the canonical path for validation, prompts, report, and archive. All subsequent git operations and writes run in `$WT_PARENT_PATH` when active; `--no-worktree` uses the prepared current checkout.

Sync remote after preparation in the execution tree:

```bash
git pull --rebase origin $(git branch --show-current) 2>/dev/null || true
```

**CHECKPOINT**: On correct branch. Working tree ready. Remote synced. Parent worktree created (if `WORKTREE_ACTIVE=true`).

## Phase 3 — EXECUTE

Branch on `EXECUTION_MODE` chosen in Phase 1.

### Path A — Sequential Execution

Process each task from Step-by-Step Tasks in order:

1. Read the MIRROR reference source before writing code; understand the convention.
2. Implement following the pattern exactly, applying GOTCHA warnings and specified IMPORTS.
3. After every file change run the Phase 0 type-check. Fix errors before the next file.
4. Print `[done] Task N: [task name] — complete`.

### Parallel Batch Execution

For standalone parallel execution, use common batching from standalone-dispatch.md §9; the plan's `Batches` table and task `BATCH: BN` fields select tasks. Read `references/agent-task-prompt.md` once before dispatch for the full ACTION/IMPLEMENT/MIRROR/IMPORTS/GOTCHA/VALIDATE prompt and Patterns to Mirror excerpt.
Dispatch one `Agent` call per task in one parallel message: `subagent_type="ycc:implementor"`, `description="<task title>"`, `prompt="<complete task spec and Patterns to Mirror excerpt>"`. Use the shared foreground result contract for the batch.
Every prompt includes `Working directory: ${WT_PARENT_PATH}` when `WORKTREE_ACTIVE=true`, otherwise `Working directory: ${REPO_ROOT}`. Apply standalone-dispatch §8.3 working-directory rules; no per-agent worktree isolation.
With `--team`, use agent-team-dispatch.md §8.2 instead, with the same prompt and working directory.

Path C adapter: context = plan basename stripped of `.plan.md`; team prefix `prpi-`, sanitization per team §1 (20-char context, fallback `untitled`); description `PRP-implement team for: <plan basename>`. Full spec supplies registered task descriptions. At C.2, if `DRY_RUN=true`, print `references/dry-run.md` and exit without any team/task/agent tools; otherwise continue the team adapter. Registration, spawn, monitoring, shutdown, and cleanup follow agent-team-dispatch.md §8.2 only.

#### Between-Batch Validation (Levels 1 + 2)

After every batch, run Phase 0 type-check (zero errors) and affected-area unit tests (green) in the execution tree. If either fails, stop the parallel pipeline; report batch and type errors/test failures; do not dispatch the next batch.

Use `AskUserQuestion`: _"Batch {BN} validation failed. Choose: (1) fix manually and resume from batch {BN+1}, (2) switch to sequential mode for remaining batches, (3) abort."_ Apply the choice. No auto-retry or skipped failure. Preserve completed work. Fix/resume in the same feature worktree, without child branches to merge or clean up. Switching modes continues sequential execution for remaining batches.
With `--team`, cleanup on switch/abort/resume follows agent-team-dispatch.md §8.2.

After validation, print `[done] Batch BN: K tasks — complete (type-check + tests pass)`.

After all batches, proceed to Phase 4's full five levels; between-batch checks do not replace build, integration, or edge cases.

### Handling Deviations

Record what changed and why; continue with the corrected approach. Collect parallel/team implementors' deviations verbatim in the final report.

**CHECKPOINT**: All tasks executed. Deviations logged.

## Phase 4 — VALIDATE

Read `references/validation-and-failures.md` now. Run every level in order; fix issues at each level before proceeding:

1. Static analysis: zero type errors; lint auto-fix, then manual fixes if needed.
2. Unit tests: test every new function per Testing Strategy, at least one each; cover specified edge cases. Fix implementation, not the test unless the test is wrong.
3. Build: zero errors.
4. Integration if applicable: start server, bounded readiness check, run tests, stop server, preserve test exit code (exact shell template in reference).
5. Edge cases: run the plan's Testing Strategy checklist.

**CHECKPOINT**: All 5 validation levels pass. Zero errors.

## Phase 5 — REPORT

Read `references/report-output.md` now for report template, PRD update, archive commands, and worktree section.

1. Create `docs/prps/reports/{plan-name}-report.md`, including assessment vs reality, task status, all validation levels, changed files, verbatim deviations, issues, tests, next steps.
2. If a PRD phase: change `in-progress` to `complete`, add report path.
3. Archive canonical `$PLAN_PATH` to its sibling `completed/` inside the execution tree (fallback to stripped `$ARGUMENTS` under `--no-worktree`).
4. If `WORKTREE_ACTIVE=true`, capture `list-worktrees.sh` output after archive; include full table and cleanup commands under `## Worktree Summary` in the report.

**CHECKPOINT**: Report created. PRD updated. Plan archived. Worktree summary captured (if applicable).

## Phase 6 — OUTPUT

Print the user-output template from `references/report-output.md`, including mode, validation, deviations, artifacts, conditional PRD progress/worktree summary, and all seven Goal Signals verbatim. Use `PASS` only when the matching criterion below holds; otherwise `FAIL`.

## Handling Failures

Read `references/validation-and-failures.md` when any type-check, test, lint, build, or integration check fails. Fix the source/root cause and re-run until clean before proceeding. Parallel pipeline failures additionally use Phase 3's user choice gate.

## Success Criteria

- **TASKS_COMPLETE**: All tasks from the plan executed.
- **TYPES_PASS**: Zero type errors.
- **LINT_PASS**: Zero lint errors.
- **TESTS_PASS**: All tests green, new tests written.
- **BUILD_PASS**: Build succeeds.
- **REPORT_CREATED**: Implementation report saved.
- **PLAN_ARCHIVED**: Plan moved to `docs/prps/plans/completed/`.

## /goal pairing and Next Steps

Read `references/report-output.md` (Goal pairing) for the condition template; read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/goal-pairing.md` before relying on a `/goal` loop. Done conditions use printed signals, not file paths. Next: `/ycc:code-review`, `/ycc:prp-commit`, `/ycc:prp-pr`, or `/ycc:prp-plan <next-phase>`.

## References — read when

- `references/detection.md`: Phase 0 package manager/scripts and Phase 1 parallel detection/mode selection.
- `references/agent-task-prompt.md`: once before parallel implementor dispatch.
- `references/dry-run.md`: C.2 `--team --dry-run` output.
- `references/validation-and-failures.md`: Phase 4 validation and any failed check.
- `references/report-output.md`: Phase 5 report/PRD/archive, Phase 6 user output, or `/goal` condition.
