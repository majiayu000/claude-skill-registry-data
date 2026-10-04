---
name: execute
description: Dispatch and execute implementation plans with TDD and checkpoints. Use when plan is ready. Parallel by default for independent tasks.
mcp: codebase-memory-mcp
---

# /supergraph:execute

Dispatch plan tasks with TDD. Parallel by default when tasks are independent.

Usage: `/supergraph:execute` | `task N` | `tasks N,M` | `from task N` | `plan auth-login task 2` | `plan auth-login sequential`

## Steps

### 0. Announce
"I'm using /supergraph:execute to implement this plan."

### 1. Load Context
- `/supergraph:scan` should already be done. If `.supergraph-env` missing → STOP: "Run `/supergraph:scan` first."
- Commands from `.supergraph-env` (if present) or plan `## Environment Context`

### 2. Select Plan
Count plan files in `docs/supergraph/plans/*.md`:

| Count | Action |
|---|---|
| 0 | STOP: "Run `/supergraph:plan` first" |
| 1 | Auto-select |
| >1, no `plan <slug>` arg | STOP: list plans, ask user |
| `plan <slug>` provided | Match filename. If >1 match ask. |

Parse task scope: `task N`, `tasks N,M,K`, `from task N`, or all incomplete.
Parse `sequential` flag → force sequential mode.

### 3. Critical Review
Read plan before dispatch:
- Has `## Environment Context`?
- Selected tasks have all required fields (Status, Risk, Dependencies, Files, Acceptance, TDD, Steps, Checkpoint)?
- Commands real, not placeholders? File paths exact?
- Plan-reviewer returned `Approved` (or user explicitly approved)?

If missing or not Approved → STOP, dispatch `supergraph:plan-reviewer`, wait for Approval.
Also check: plan has user approval step (step 11)? If not → ask user: "Plan was not reviewed by you. Proceed anyway? [yes / no]"
Check dependencies: Task X depends on Task Y → is Y `Status: completed`? If not → STOP.
**If any concern: STOP, ask. Never guess.**

### 4. Branch Protection
If main/master → STOP, suggest new branch or worktree.
User approves → continue.

### 5. Determine Execution Mode & Group by Waves

Parse tasks from plan:
- **Wave-based DAG:** Group incomplete tasks by `Wave: N` (e.g. Wave 1, Wave 2, Wave 3).
- **Auto-Wave fallback:** If plan lacks `Wave:` fields, group tasks dynamically by dependencies:
  - Wave 1: Tasks with `Dependencies: none`.
  - Wave N: Tasks whose dependencies are all satisfied by Wave < N.
- **Wave Strategy:**
  - Wave with 1 task → Sequential dispatch.
  - Wave with >1 tasks → **Parallel dispatch** of concurrent subagents.

### 6. Wave-by-Wave Dispatch

Execute wave by wave in strict DAG order:

```text
Wave 1 (Base/Schema) ──> Wave 2 (Independent Features: PARALLEL) ──> Wave 3 (Integration/UI)
```

Shared executor instructions (see `serena/SKILL.md:Setup`): per task RED→GREEN→REFACTOR→Lint→Format, `get_diagnostics_for_file` after GREEN, prefer `replace_symbol_body`/`rename_symbol` over raw edits. Commit once per task. Max 3 retries.

For each Wave:
1. **Prepare Wave Scope:** Identify tasks belonging to current Wave.
2. **Sequential (1 task):** Dispatch `Agent(subagent_type="supergraph:executor")` — run baseline tests first, execute task respecting dependencies, report task done/stuck + files changed.
3. **Parallel (>1 tasks):**
   - **Antigravity / Subagent Runners:** Call `invoke_subagent` with concurrent executors in a single call:
     - `Workspace: "branch"` (isolated git worktree/branch — guarantees zero file conflicts & avoids git index lock collisions).
     - `Model: task.Model || "inherit"` (use `flash` for low-risk boilerplate/tests, `pro` for complex logic).
     - Each subagent receives only its self-contained `## Task N` snippet + `## Environment Context`.
   - **Claude Code / CLI:** Spawn one subagent per task in one message with self-contained task scope.
   - Subagents execute TDD, report `ACCEPTANCE_PASSED: Task N`.
   - Orchestrator waits for all subagents in current Wave to report completion.
4. **Wave Synchronization & Merge:**
   - Merge worktree/branch changes back to target branch.
   - Run Wave Verification `$TEST_CMD`.
   - Orchestrator updates task statuses to `completed` in plan file.
   - If tests pass → proceed to Wave N+1.
   - If any task fails/stuck (after max 3 retries) → trigger `/supergraph:fix` or STOP and consult user.

### 6.5 Durable Task Artifacts and Dispatch Safety

Before dispatch, create the plan workspace with `sdd-workspace PLAN_FILE`, then run a **Pre-dispatch conflict scan** over task file sets and dependencies. Record the scan and any non-catastrophic ruling in `.supergraph/sdd/<plan-basename>/ledger.md`.

- batch only tasks with disjoint write sets and the same execution shape.
- Send each worker `task-N-brief.md`; require `task-N-report.md` with exact RED/GREEN/REFACTOR and verification evidence.
- Implementers and reviewers **must not spawn subagents**. The controller owns dispatch depth and parallelism.
- On a conflict that is not catastrophic, the controller records the ruling, affected files, and why execution can continue. Catastrophic conflicts stop the wave.
- Generate `review-<base>..<head>.diff` with `review-package` before scoped review.

### 7. Post-Execution Safety
If same-file edits for `CBM_PROJECT`: reindex if stale (`index_status`→`index_repository`, see `references/codebase-memory-contract.md`), then `detect_changes`/`trace_path`/`cross-boundary` via `codebase-memory-mcp`.

### 8. Final Verification
Run `$TEST_CMD`/`$LINT_CMD`/`$BUILD_CMD`. Reindex `CBM_PROJECT` if stale (`index_status`→`index_repository`), then `codebase-memory-mcp` `detect_changes`/`trace_path`, recipes `cycles/test-gaps/complexity/cross-boundary`.

### 9. Handoff
`/supergraph:fix` → `/supergraph:integration` → `/supergraph:verify` → `/supergraph:review`

### 10. Report
```
✅ Execution Complete
Plan: [path] | Scope: [tasks]
Tasks: N/N done | Stuck: [none | list]
Tests: PASS | Lint: PASS | Graph: updated
```
Announce completion in user's language.

## Stop Conditions (Ask Instead of Guessing)
- Plan not found or ambiguous | Missing Environment Context | Unclear instruction or placeholder
- Branch is main/master without permission | Baseline tests fail | Dependency not completed
- Agent stuck after 3 retries

## Rules
- Parallel when zero file overlap + no dependencies | Sequential for dependencies
- One commit per task, NEVER mid-TDD | Never `git add -A`
- Max 3 retries per step | Self-contained prompt per parallel agent
- Always verify after parallel | Always review plan before dispatch
- Never create plan — only execute
- Prefer Serena symbol tools over text edits when available
