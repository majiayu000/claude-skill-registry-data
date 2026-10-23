---
name: implement-plan
description: 'Executes parallel-plan.md with dependency-aware implementor batches. Use when implementing a planned feature, running parallel-plan tasks, or resuming a batched implementation.'
argument-hint: '[--team] [--dry-run] [--worktree] [--no-worktree] <feature-name>'
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
  - Bash(grep:*)
  - Bash(git:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/implement-plan/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/*.sh:*)'
---

# Parallel Plan Executor

Execute a parallel implementation plan by deploying implementor agents in dependency-resolved batches. This is Step 3 of the planning workflow, transforming the plan into working code. **Operational context:** require parallel-plan.md from parallel-plan. Worktree isolation is on by default: create or reuse one feature worktree on a feature branch; `--no-worktree` uses only the current-checkout feature branch, and `--worktree` is a legacy no-op. Standalone sub-agents are the default dispatch mode.

Parallelism is the baseline of this skill — every batch's tasks dispatch concurrently. The only choice is how the implementor agents are dispatched: standalone sub-agents (default, plain `Agent` calls per batch, works in Claude Code, Cursor, and Codex) or agent team (`--team`, Claude Code only: implicit session team, up-front `TaskCreate` + `addBlockedBy`, per-batch teammate spawn, `SendMessage` shutdown).

## Hard Gates

- `--worktree` and `--no-worktree` together → abort (exact message in Arguments).
- `--team` without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` → abort (exact message in Arguments).
- `--dry-run` → print the plan only; never dispatch agents or manage team state. STOP HERE.
- Always run the branch-prep helper before any dispatch — narrative-only branch instructions are how agents end up committing to `main`.
- Never pass `isolation: "worktree"` per agent — all agents in all batches share the one feature worktree (or the prepared checkout under `--no-worktree`).
- Standalone task failure: record it and continue only independent tasks. Team failure: no auto-retry or skipping; ask the user before advancing.

**Questions:** class `failure-recovery` (team batch failure); headless (no question tool or chat turn): stop, keep the feature worktree, and print the failing batch plus the resume command. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Workflow Integration

Final step of the planning workflow; requires `parallel-plan.md` from the parallel-plan skill.

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ shared-context  │ ──▶ │  parallel-plan  │ ──▶ │  implement-plan │
│  (Step 1)       │     │  (Step 2)       │     │  (this skill)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
     Creates:                Creates:               Executes:
     shared.md              parallel-plan.md      parallel-plan.md
```

If parallel-plan.md doesn't exist, run `/parallel-plan [feature-name]` first.

## Arguments

**Target**: `$ARGUMENTS`

Parse flags first, then treat the remainder as the feature name:

- `--team` — (Claude Code only) Dispatch each batch's implementor agents as teammates under the implicit session team with up-front `TaskCreate` + `addBlockedBy` dependency wiring and per-batch shutdown via `SendMessage`. Aborts if invoked from a Cursor or Codex bundle (team dispatch is absent there).
- `--dry-run` — Show the execution plan without deploying agents. With `--team`, also prints the team name and per-batch teammate roster.
- `--worktree` — (legacy — now default; safe to omit) Accepted as a silent no-op. Worktree isolation is on by default; this flag matches the new default and has no additional effect.
- `--no-worktree` — Force worktree mode **OFF** regardless of plan annotations. Create/use `feat/<feature-name>` in the current checkout and run tasks there. No feature worktree is created.
- `<feature-name>` — The name of the feature to implement (matches directory name in `docs/plans/`).

Strip the flags from `$ARGUMENTS` and set `TEAM_FLAG=true|false`, `DRY_RUN=true|false`, `WORKTREE_MODE=true|false`, and `WORKTREE_FLAG_PRESENT=true|false`. The remaining non-flag token is the feature name.

**Validation**:

- `--worktree` and `--no-worktree` together → abort with: `--worktree and --no-worktree are mutually exclusive. Use --no-worktree to opt out of the default.`
- `--team` passed and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` not set to `1` → abort with: `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`

If no feature name remains after stripping flags, abort with this usage line followed by the Examples in `references/plan-inputs.md` (default worktree, `--team`, `--dry-run`, `--no-worktree`, and the combinations):

Usage: /implement-plan [--team] [--dry-run] [--worktree] [--no-worktree] <feature-name>

**Compatibility note**: from a Cursor or Codex bundle, `--team` must abort with a clear message — those bundles ship without team tools (`TaskCreate`, `SendMessage`, etc.); the standalone path is the only mode available there. `--worktree` is compatible with all targets through a single pre-created feature worktree plus `Working directory:` prompts. Do not request tool-side per-agent worktree isolation — that creates separate harness worktrees and breaks the single-worktree contract. Codex and opencode use Bash `git worktree add`; Cursor emits manual setup commands only.

## Dispatch Lifecycle

Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/standalone-dispatch.md` for standalone dispatch and common preparation (§§8–9).
Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md` §8.2 only when `--team` is passed.

## Phase 0: Prerequisites Check

### Step 1: Validate Prerequisites

After flag parsing, extract the feature name (first non-flag argument) and run:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/implement-plan/scripts/check-prerequisites.sh [feature-name]
```

If the script exits with error: display the error message, instruct the user to run `/parallel-plan` first to create the implementation plan, and **STOP HERE** — do not proceed.

### Step 2: Read Planning Documents

1. `docs/plans/[feature-name]/parallel-plan.md` — the implementation plan
2. `docs/plans/[feature-name]/shared.md` — architecture context

Also read files listed in the "Critically Relevant Files" section of parallel-plan.md.

## Phase 1: Parse Plan & Build Dependency Graph

### Step 3: Extract Tasks

Run when building the execution graph (Phase 1 task extraction):

```bash
${CLAUDE_PLUGIN_ROOT}/skills/implement-plan/scripts/parse-dependencies.sh docs/plans/[feature-name]/parallel-plan.md
```

The script emits optional header lines (`WT_PARENT_PATH=<path>`, `WT_FEATURE_SLUG=<slug>` — present only when the plan has a `## Worktree Setup` section) followed by per-task rows (`TASK_ID|TASK_TITLE|DEPENDENCIES`). Row fields and the monorepo `.plans-config` behavior are documented in `references/plan-inputs.md`.

### How Worktree Mode Is Decided

Use standalone-dispatch.md §8.1 for precedence and variables in both modes. Skill input: `WT_FEATURE_SLUG` is the parsed annotation slug if present, otherwise the feature-name argument (no extra sanitization/cap). Always derive `WT_REPO_NAME` and `FEATURE_BRANCH`; `--no-worktree` sets `WORKTREE_ACTIVE=false` even when parser headers exist.

### Step 4: Build Dependency Graph

Build the independent-vs-dependent graph using standalone-dispatch.md §9; example in `references/plan-inputs.md` (Dependency graph). Keep the graph for standalone batch ordering.
With `--team`, also use that graph for `addBlockedBy` wiring.

## Phase 2: Create Task List

### Step 5: Register Tasks

Use `TaskCreate` for each plan item with `subject="[Task ID] [Task Title]"` and
`description="<full specification and dependencies>"`. Capture the returned task IDs;
wire dependencies via `TaskUpdate` with `addBlockedBy` using those IDs. See
`references/plan-inputs.md` (Task list format).

### Step 6: Identify First Batch

All tasks with `Depends on [none]` form the first batch; mark them ready for execution.

## Phase 2.5: PREPARE — Branch / Worktree Setup

### Steps 6.5–6.7

Use standalone-dispatch.md §8.2 in both dispatch modes for Git inspection, required branch preparation, one-time parent setup, and one-way artifact relocation. Expected dirty artifacts: `docs/plans/${WT_FEATURE_SLUG}/` only; unrelated dirty files stop and require user cleanup. Move `docs/plans/${WT_FEATURE_SLUG}/parallel-plan.md` with `docs/plans/${WT_FEATURE_SLUG}/shared.md` as companion; other research artifacts from the same feature directory may ride as extra arguments. Keep returned `$PLAN_PATH` canonical; later validation/reports use the execution tree. Branch-prep exit contract: `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/branch-prep.md`.

## Phase 3: Execute in Batches

### Step 7: Dry Run Gate

If `--dry-run` is present, read `references/output-formats.md` (Dry-run formats), print the default batch roster, and do not dispatch any agents.
With `--team --dry-run`, also print the team name and per-batch teammate roster; do not call `TaskCreate`, `Agent`, `SendMessage`, or any task-tracking tools.
**STOP HERE** after either dry-run output.

### Step 8: Branch on `TEAM_FLAG`

- `TEAM_FLAG=false` → **Path A — Standalone sub-agent batches** (default).

Execute the dependency-ready standalone batches described below.

- `TEAM_FLAG=true` → **Path B — Agent team batches**.

### Path A — Standalone Sub-Agent Batches (default)

Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/standalone-dispatch.md` for the `Agent` contract; use its §§9–10 for dependency-ready batches. Coordinate agents, do not implement tasks yourself. Read `${CLAUDE_PLUGIN_ROOT}/skills/implement-plan/references/agent-task-prompt.md` once before the loop. Per ready task, one `Agent` call per batch message: `subagent_type=ycc:implementor`, `description="Implement [Task ID]: [Title]"`, full substituted template.

**When `WORKTREE_ACTIVE=true`**, every task prompt (parallel and sequential) carries the lines below; when `WORKTREE_ACTIVE=false` (`--no-worktree`) use `Working directory: ${REPO_ROOT}` and `All parallel agents in this batch share the current feature branch; batching guarantees no two agents touch the same file.` Never pass `isolation: "worktree"`. Agents read the plan, shared context and "READ THESE BEFORE TASK" files first, implement only assigned files/instructions, lint and compile/parse modified files, then report files created/modified and issues.

```
Working directory: ${WT_PARENT_PATH}
All parallel agents in this batch share this path; batching guarantees no two agents touch the same file.
```

Implementor prompt template: `references/agent-task-prompt.md` — read once before the loop for the full task prompt.

#### Process Batch Results (Path A)

After each batch: validate in the execution tree, review reports, update task status, identify newly dependency-ready tasks, and print `[done] Batch BN: K tasks — complete` to the transcript. A failed task is recorded; continue independent tasks, never tasks depending on failed work.

#### Repeat Until Complete (Path A)

Repeat from the ready-task selection until no tasks remain, then Phase 4.

### Path B — Agent Team Batches (`--team`)

Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md` §8.2 (plus standalone-dispatch.md §§8–9). Inputs: context = feature name; prefix `impl-`; sanitize per team §1 (20-char context, fallback `untitled`); team description `implement-plan team for: <feature-name>`; task subject `<task-id>: <task title>`; task description = full spec (files to read/create/modify and instructions); dependencies = Phase 1 graph; same implementor template plus own-`TaskUpdate` completion; same `Working directory:` lines. Print the same `[done] Batch BN: K tasks — complete` marker per batch. Failure: no auto-retry or skipping; use `AskUserQuestion`: _"Batch {BN} had failures. Choose: (1) fix manually and resume, (2) switch to sequential standalone sub-agents for remaining batches, (3) abort."_ Cleanup and worktree survival follow §8.2. After all batches, Phase 4.

## Phase 4: Final Verification & Summary

### Step 9: Verify Implementation

1. Run linting on all modified files and print the outcome to the transcript (zero errors, or the list of errors) — `LINT_PASS` is derived from this printed outcome; the `/goal` evaluator only reads transcript text.
2. Verify all "Files to Create" exist.
3. Sanity-check the modifications.

### Step 10: Display Summary

When `WORKTREE_ACTIVE=true`, first capture: `bash ${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/list-worktrees.sh "${WT_REPO_NAME}" "${WT_FEATURE_SLUG}"`.

Print the completion summary from `references/output-formats.md` (Completion summary), including the `## Worktree Status` section only when `WORKTREE_ACTIVE=true` and the Goal Signals block verbatim as the last lines. Use `PASS` only when the matching `## Success Criteria` criterion is met; otherwise `FAIL` (e.g. `FILES_CHANGED_NONEMPTY: FAIL` when the "Files Changed" section enumerated no files).

## Quality Standards

Each batch must: deploy all ready tasks in parallel (single message — multiple `Agent` calls in Path A, multiple `Agent` calls with `name=` in Path B); wait for all agents before the next batch; update task status with `TaskUpdate` after completion; handle failures gracefully; in Path B, shut down completed-batch teammates before the next batch.

Each agent must: read all required context files first; implement only the assigned task; validate changes before returning; return a clear summary of changes; in Path B, call `TaskUpdate` to mark its own task complete.

The implementation must: complete all tasks in the plan, respect dependency ordering, maximize parallel execution, and report failures clearly.

## Monorepo Support

Plans are read from the git repository root in `docs/plans/` by default; running from any subdirectory still reads from the root. A `.plans-config` at repo root (`plans_dir: docs/plans`) customizes the directory; with `scope: local` in a package-level `.plans-config`, plans are read from that package's local `docs/plans/`. Structure example in `references/plan-inputs.md` (Monorepo Support).

## Success Criteria

- **ALL_BATCHES_DONE**: every batch printed `[done] Batch BN: K tasks — complete` and no batch was left unprocessed.
- **FILES_CHANGED_NONEMPTY**: the Step 10 "Files Changed" section enumerates at least one created or modified file.
- **LINT_PASS**: Step 9 linting printed zero errors across all modified files.

## /goal pairing

Pair with the `/goal` session directive to loop the batch executor to completion without re-prompting between batches. The condition template and the shared transcript-output caveats are in `references/output-formats.md` (Goal pairing); the cross-skill contract lives at `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/goal-pairing.md` — read it before relying on a `/goal` loop.

## References

- `references/plan-inputs.md` — read when parsing tasks, building the dependency graph, registering tasks, showing usage, or resolving the monorepo plans directory.
- `references/agent-task-prompt.md` — read once before dispatching implementor agents.
- `references/output-formats.md` — read when printing `--dry-run` output or the Phase 4 completion summary, or writing a `/goal` condition.
