---
name: orchestrate
description: 'Coordinates specialized agents in dependency-resolved batches. Use when delegating a complex task, splitting independent implementation work, or coordinating multiple specialists.'
argument-hint: '[--team] [--dry-run] [--plan-only] [--sequential] [--worktree] [--no-worktree] <task-description>'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Agent
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - SendMessage
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/setup-worktree.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/list-worktrees.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/prepare-feature-branch.sh:*)'
---

# Multi-Agent Orchestration Skill

You are an orchestration expert coordinating multiple specialized agents to accomplish complex tasks. **Your role is to coordinate agents, not do the work yourself.** **Operational context:** Worktree isolation is on by default; all parallel and sequential agents share one feature worktree. --no-worktree runs in the current checkout. Standalone sub-agents are default.

Parallelism is the baseline: every batch's tasks dispatch concurrently. The only choice is how the implementor agents are dispatched:

- **Standalone sub-agents** (default): plain `Agent` calls per batch, no shared task list. Works in Claude Code, Cursor, and Codex.
- **Agent team** (`--team`, Claude Code only): use the implicit session team with all subtasks registered up front (`TaskCreate` + `addBlockedBy`), per-batch teammate spawn via `Agent(name=...)`, inter-batch shutdown via `SendMessage`, and confirmation that all teammates shut down at the end.

## Current Task

**Orchestrating**: `$ARGUMENTS`

Parse flags first, then treat the remainder as the task description:

- `--team`: (Claude Code only) dispatch each batch under the implicit session team with up-front `TaskCreate` + `addBlockedBy` wiring and per-batch shutdown via `SendMessage`. Aborts from a Cursor or Codex bundle (team dispatch absent there).
- `--dry-run`: show the orchestration plan without deploying agents. Print a `Worktree:` line when worktree mode is active (no scripts called).
- With `--team --dry-run`, also print the team name and per-batch teammate roster.
- `--plan-only`: write the plan to `docs/orchestration/[sanitized-task].md` without execution. With worktree mode active, the plan gains a `## Worktree Setup` section.
- `--sequential`: force single-task batches (tightly dependent tasks). With worktree mode active, all sequential tasks run in the single feature worktree.
- `--worktree`: legacy, now default; accepted as a silent no-op.
- `--no-worktree`: force worktree mode off. All tasks run in the current checkout; no feature worktree is created.
- `<task-description>`: the task to orchestrate (required, may be multi-word).

Strip flags from `$ARGUMENTS` and set `TEAM_FLAG=true|false`, `DRY_RUN=true|false`, `PLAN_ONLY=true|false`, `SEQUENTIAL=true|false`, `WORKTREE_MODE=true|false` (true unless `--no-worktree`). Join the remaining tokens into `TASK_DESCRIPTION`.

**Feature slug**: before any `WORKTREE_MODE` branching, derive `FEATURE_SLUG` from `TASK_DESCRIPTION`: lowercase, replace `[^a-z0-9-]` with `-`, collapse runs of `-`, trim leading/trailing `-`, truncate to 20 characters, fall back to `untitled` if empty. The team name is `orch-<FEATURE_SLUG>`; sanitization matches `agent-team-dispatch.md` section 1.

## Gates (hold across the whole run)

1. No task description after stripping flags: print the usage block from `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/dispatch-playbook.md` section 1 (read it only on this abort path), then abort.
2. `--team` from a Cursor or Codex bundle: abort with a clear message. `--worktree` works everywhere via `git worktree add`; on Cursor emit the `git worktree add` commands as instructions instead of auto-creating.
3. `--team` without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`: abort with `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`
4. Set all flag variables before any side effect.
5. `DRY_RUN=true` or `PLAN_ONLY=true`: no branch prep, no worktree script calls, no team or agent calls. Stop after Phase 3 output.
6. Non-dry runs: prepare the feature branch (Phase 2.5) before any agent dispatch, or agents commit on the starting branch (usually `main`).
7. Never pass `isolation: "worktree"` to dispatch calls: it makes one harness worktree per agent and breaks the single-worktree contract.
8. Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/standalone-dispatch.md` for standalone dispatch, worktree prep and dependency batches (sections 8-10).
   Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md` only when `--team` is passed (section 8: orchestrate adapter).

## Phase 0: Task Analysis

**Step 1**: run the analysis script (outputs complexity estimate, decomposition approach, likely agent types, parallel vs sequential recommendation):

```bash
${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/scripts/analyze-task.sh "$TASK_DESCRIPTION"
```

**Step 2**: read `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/agent-catalog.md` (agents by category, capabilities, use cases; read now, use its Contents to jump).

**Step 3**: assess the task: scope (feature, bug, refactor, docs, infrastructure), components involved, complexity (Simple 1-2 agents, Medium 3-5, Complex 6+), and whether subtasks are independent or sequential.

## Phase 1: Task Decomposition & Team Creation

**Step 4**: read `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/task-breakdown.md` (patterns for decomposing by feature area, technical layer, cross-cutting concern, and dependency).

**Step 5**: register standalone subtasks with `TaskCreate`, tracking batch completion in-context. Read `references/dispatch-playbook.md` section 10 now for exact registration formats. With `DRY_RUN=true` or `PLAN_ONLY=true`, skip registration and proceed to Step 10.
With `--team`, use the implicit session team (run label `orch-<FEATURE_SLUG>`) and register/wire every subtask up front; abort if `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is unset and shut down any spawned teammates on registration/wiring failure. For dry-run or plan-only, skip registration and compute the run label in memory only.

**Step 6**: validate each subtask: clear specific scope, single responsibility, completable in one focused session, dependencies stated, success criteria clear, agent assignment justified. Optionally run:

```bash
if [[ -f "${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/scripts/validate-agents.sh" ]]; then
  ${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/scripts/validate-agents.sh
fi
```

## Phase 2: Agent Assignment

**Step 7**: map each subtask to an agent:

| Task Type                | Recommended Agent                                         |
| ------------------------ | --------------------------------------------------------- |
| Code exploration/finding | `explore`, `code-finder`                                  |
| Architecture research    | `codebase-research-analyst`                               |
| Frontend UI work         | `frontend-ui-developer`, `nextjs-ux-ui-expert`            |
| Backend API work         | `nodejs-backend-architect`, `go-api-architect`            |
| Database changes         | `db-modifier`, `sql-database-architect`                   |
| Documentation            | `documentation-writer`, `api-docs-expert`                 |
| Testing strategy         | `test-strategy-planner`                                   |
| Bug diagnosis            | `root-cause-analyzer`                                     |
| Infrastructure           | `terraform-architect`, `cloudflare-architect`             |
| DevOps/automation        | `ansible-automation-expert`, `systems-engineering-expert` |

**Step 8**: read `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/agent-prompts.md` for standard prompt templates and the standalone coordination block before building prompts.
With `--team`, use its Path B Team Communication section.

**Step 9**: prepare per subtask: context, scope (files/areas), deliverables, constraints (what not to do, to avoid overlap).

## Phase 2.5: Worktree Setup

Follow standalone-dispatch §8 for mode decision (with this skill's inputs: no `## Worktree Setup` auto-detect, so `--no-worktree` is the only opt-out; EXECUTION_MODE and PLAN_ONLY are orchestrate-local), preparation, and agent lines. Summary inputs: `FEATURE_SLUG` per team-sanitizer (20 chars, fallback `untitled`); one shared parent worktree `<repo-root>/.claude/worktrees/<repo>-<FEATURE_SLUG>/`.

When `DRY_RUN=false` and `PLAN_ONLY=false`, follow standalone-dispatch §8.2: prepare the feature branch before any worktree setup or dispatch; if `WORKTREE_MODE=true`, create one parent with `<repo-name>` + `FEATURE_SLUG` and store its echoed path as `PARENT_WORKTREE_PATH`; otherwise skip setup. No plan-move call here (orchestrate builds its own decomposition, not a pre-existing plan file). Every agent uses §8.3 directory lines; treat `PARENT_WORKTREE_PATH` as `WT_PARENT_PATH` and derive `REPO_ROOT` there. Branch-prep exit contract: `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/branch-prep.md`.

- `WORKTREE_MODE=true` and `DRY_RUN=true`: no script calls; compute `<repo-root>/.claude/worktrees/<repo>-<FEATURE_SLUG>/` for the dry-run output.
- `WORKTREE_MODE=true` and `PLAN_ONLY=true`: no script calls; add the worktree annotation to the written plan.

Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/worktree-strategy.md` when writing the `## Worktree Setup` plan section (section 2 annotation format).

## Phase 3: Dry Run Check

**Step 10**: when `DRY_RUN=true`, read `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/dispatch-playbook.md` section 2 for the default dry-run format and the `Worktree:` line.
With `--team --dry-run`, also use the team roster below.

`--dry-run`: print the dry-run output, with the `Worktree:` line when worktree mode is active.
With `--team`, also print this block:

```
Team name:    orch-<sanitized-task>
Total subtasks: <N>  (across <M> batches, max parallel width <X>)
Dependencies: <K edges>

Batch 1: <comma-separated subtask IDs>
Batch 2: <comma-separated subtask IDs>  (depends on Batch 1)
...
Batch M: <comma-separated subtask IDs>  (depends on Batch M-1)

Per-batch teammate roster:
  Batch 1:
    - subtask-1  subagent_type=<agent-type>  focus=<short>
    - subtask-2  subagent_type=<agent-type>  focus=<short>
  ...
```

Do not dispatch agents or run worktree scripts in dry-run mode.
With `--team`, do not call `TaskCreate`, `Agent`, or `SendMessage` in dry-run mode.
**Stop here.**

`--plan-only`:

- Write the plan to `docs/orchestration/[sanitized-task-name].md`, save the complete orchestration plan for later execution, display its location and a summary.
- Team creation is skipped entirely; no team cleanup needed.
- With `WORKTREE_MODE=true`, read dispatch-playbook.md section 3 now and include a `## Worktree Setup` section immediately after frontmatter and before Batch 1, listing only the parent path. No child paths, no `**Children**:` list.
- **Stop here.** Do not deploy agents.

## Phase 4: Parallel Agent Deployment

**Step 11**: group subtasks by dependency using standalone-dispatch §9.1. With `--sequential`, create single-task batches.

**Step 12**: execute dependency-resolved batches per the shared dispatch contract (Gate 8) and the orchestrate-specific rules in `references/dispatch-playbook.md` sections 10-11; section 4 holds the standalone call shapes. Spawn each batch in one message, never start a subtask before its dependencies complete, continue independent work after failures, and report deadlock and stop if pending subtasks remain but none can be unblocked. Registration, failure handling, dry-run formats, worktree rules, agent assignments, and output formats defined here take precedence over the generic confirmed-plan defaults.
With `--team`, section 5 holds the Path B call shapes.

**Step 13**: repeat Step 12 for each subsequent batch until all subtasks are completed or none can be unblocked.

## Phase 5: Result Synthesis & Summary

**Step 14**: consolidate outputs by running:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/scripts/summarize-results.sh
```

Organize agent outputs by files created, files modified, documentation added, tests created, issues encountered.

**Step 15**: integration check: no conflicting changes between agents, dependencies integrated, cross-references valid, consistent patterns and conventions.

**Step 16**: standalone completion needs no cleanup.
With `--team`, confirm all teammates have received shutdown requests before completing.

**Step 17**: final summary. With `WORKTREE_MODE=true`, run this and append its output (feature worktree path, branch, and the `git worktree remove` command for manual cleanup; the worktree survives until removed, and there are no child worktrees):

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/list-worktrees.sh <repo-name> <FEATURE_SLUG>
```

Then print the completion summary using the template in `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/dispatch-playbook.md` section 6 (read it now).

## Reference Index

- `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/agent-catalog.md`: read in Step 2.
- `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/task-breakdown.md`: read in Step 4.
- `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/agent-prompts.md`: read in Step 8.
- `${CLAUDE_PLUGIN_ROOT}/skills/orchestrate/references/dispatch-playbook.md`: usage block (section 1, abort path), dry-run and plan-only formats (sections 2-3, Phase 3), standalone dispatch call shapes (section 4, Step 12), final summary (section 6, Step 17), registration formats (section 10, Step 5), batch adapter (section 11, Step 12), quality checklists (section 7, Steps 6 and 15), coordination principles and patterns (section 8) and troubleshooting (section 9; read when agents conflict, batches misorder, or the task is unclear).
- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/branch-prep.md`: read in Phase 2.5 when helper behavior matters.
- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/worktree-strategy.md`: read in Phase 2.5 for plan-only annotations.
