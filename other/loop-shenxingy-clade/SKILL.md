---
name: loop
description: Clade goal-driven autonomous improvement loop (Blueprint architecture — deterministic pre/post phases + LLM supervisor/worker nodes, converges on goal met or max-iter). NOT the Claude Code built-in /loop (interval polling like `/loop 5m /foo`) — route those to the built-in.
when_to_use: "run loop with goal file, autonomous supervisor+worker loop, keep fixing until tests pass in background workers, iterate until converged, goal.md, Blueprint loop, 自动循环, run until converged — NOT for TODO.md tasks (/batch-tasks), task decomposition (/orchestrate), in-session iteration (/iloop), or interval polling (CC built-in /loop)"
argument-hint: 'GOAL_FILE [--model haiku|sonnet|opus] [--worker-model MODEL] [--max-iter N] [--max-workers N] [--supervisor-timeout N] [--dry-run] [--status] [--stop] [--resume]'
user_invocable: true
---

# Loop Skill

Runs an autonomous improvement loop driven by a **goal file** (ideal end state description).

## Architecture

```
You write: goal.md  (what the system should do — NOT a task list)
                ↓
PRE (deterministic):
  pre_flight       — goal exists, no blockers
  hydrate_context  — git log + status
  parse_todo       — extract unchecked items from goal file
                ↓
LLM CORE:
  Supervisor       — plans 1–4 tasks (output: JSON task array)
  Workers          — execute ALL tasks IN PARALLEL
                ↓
POST (deterministic + conditional LLM):
  syntax_check     — validate all changed files
  fix_syntax       — [LLM] one attempt to fix failures
  test_sample      — run verify_cmd from CLAUDE.md
  mid-iter fix     — [LLM] if test fails → fix → re-test (Stripe pattern)
  verify           — require an explicit final-state pass
  reconcile_goal   — coordinator marks exact task-bound goal items
  commit_changes   — sweep leftovers and count every iteration commit
                ↓
Deterministic convergence check:
  - remaining unchecked items = 0 → CONVERGED
  - max iterations hit        → exit
  - stuck (N× no-commits)    → exit
                ↓
Repeat until CONVERGED or max iterations
```

## What you write (goal.md)

```markdown
# Goal: Improve orchestrator loop mode

## Requirements
- Oracle rejection re-queues task with rejection reason as context
- Worker context budget warning auto-injected at 80%
- Workers get AGENTS.md prepended automatically

## Success criteria
- python -m py_compile server.py passes
- Existing features unaffected
```

The **supervisor** does the task breakdown — not you.

## Usage

```
/loop goal.md                                # Start loop (sonnet, max 10 iter, 4 parallel workers)
/loop goal.md --model haiku                  # Cheaper/faster supervisor+workers
/loop goal.md --max-iter 3                  # Short run to test
/loop goal.md --max-workers 2                # Limit parallel workers
/loop goal.md --max-consecutive-failures 5  # Stop after 5 consecutive worker failures (default: 3)
/loop --status                               # Check current loop progress
/loop --stop                                 # Stop loop after current iteration
/loop --dry-run goal.md                      # Preview without running (goal may precede or follow flags)
/loop goal.md --supervisor-timeout 600      # Bigger planning budget (default 300s)
/loop --resume goal.md                       # Resume an exact matching interrupted loop
```

Resume is explicit and fail-closed: the checkpoint must match the current
checkout, goal path, branch, and HEAD. A normal launch starts fresh and never
silently consumes an older checkpoint.

Workers never mutate the shared goal file. The supervisor binds each task to
exact goal line/text evidence, and the coordinator marks those items only
after the worker, syntax, test, and final verification gates all pass. Commit
progress counts commits created directly by workers as well as the final sweep.
If the supervisor runtime is unavailable, Loop preserves its raw response,
reports `supervisor_failed`, and leaves the checkpoint resumable instead of
misclassifying repeated provider failures as empty plans or max-iteration work;
terminal execution failures also propagate a non-zero process exit.

## After convergence

Run `/review` to verify all behavior anchors still pass after autonomous changes.
