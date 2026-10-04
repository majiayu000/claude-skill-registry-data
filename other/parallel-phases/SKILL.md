---
name: parallel-phases
description: |
  Execute phased plans with multiple independent tasks per phase by fanning out one agent per task,
  reconciling outcomes per wave, gating between phases with verify commands, and emitting a phase × outcome report.
  Triggers include "execute this plan", "work through these phases", "swarm over this backlog", "parallelize this plan".
triggers:
  - execute this plan
  - work through these phases
  - swarm over this backlog
  - parallelize this plan
  - fan out per task
---

# Parallel Phases

## What It Does

Composite skill that executes a multi-phase plan with ≥3 total tasks or ≥2 per-phase tasks by dispatching one agent per task per wave, reconciling outcomes after each wave, enforcing phase gates (type-check, test, build), and emitting a final phase × task × result report.

Replaces: sequential walk-throughs of markdown plans, manual `parallel-investigate` + write loops, hand-rolled reconciliation tables.

## When to Use

- Plans with ≥3 independent tasks total OR ≥2 tasks in a single phase
- Tasks involve write-work (code edits, issue closure, releases, PR merges) — not read-only investigation
- You want to avoid sequential execution bottleneck + manual outcome tracking
- Source: `.claude/plans/*.md` (markdown with phases + tasks), GitHub issues (via `--from-issues "<query>"`), or inline prompt with structured tasks

## When NOT to Use

- Pure read-only investigation → use `parallel-investigate`
- Single task per phase → use sequential workflow or `loop`
- Task dependencies are complex, tightly coupled, or unknown → use `orchestrate` for routing

## Core Patterns

**Wave-based fan-out & reconciliation:**
1. **Phase 0** — RAG pre-flight: query knowledge graph for cached similar runs (skip if fresh run confirmed)
2. **Phase 1** — Ingest: parse plan source into structured `phases[]` with task metadata (id, scope, dependencies, specialist, model tier)
3. **Phase 2** — DAG analysis: assign tasks to waves using Kahn's algorithm; conflict-guard demotes tasks overlapping file scope to later waves
4. **Phase 2.5** — Critic gate: adversarial read-only review of wave assignments for deadlocks, missed file overlaps, underestimated scope
5. **Phase 3** — Pre-snapshot: capture repo state baseline (SHA, branch, issue/PR counts, release tags)
6. **Phase 4** — Per-phase execution: for each wave, dispatch ALL agents concurrently, reconcile per-wave (status map), run phase gate (typecheck/test/build), advance or stop
7. **Phase 5** — Post-snapshot: capture end state, compute deltas
8. **Phase 6** — Reconciliation: emit phase × task × result table, state changes, deferred/blocked tasks, gate pass rate, handoff

**Per-wave reconciliation status:**
- `DONE` → advance
- `DONE_WITH_CONCERNS` → advance unless correctness concerns
- `NEEDS_CONTEXT` → re-dispatch ONCE with context; if repeats, mark `BLOCKED`
- `BLOCKED` → stop phase, write handoff

**Conflict resolution:** If two agents in same wave touch same file, keep smaller-task-id change; demote other to fix-wave at phase end.

## Rules

1. Do NOT fan out write-agents over the same file/branch in one wave without `--worktrees` (use conflict-guard + worktrees to isolate)
2. Do NOT skip per-wave reconciliation — all agents must return before next wave dispatches
3. Do NOT advance past a failed phase gate (red typecheck/test/build halts the phase)
4. Do NOT inherit parent chat history into sub-agent prompts (context isolation enforced)
5. Phase gates auto-detect: `package.json` → npm run typecheck && npm test; `Cargo.toml` → cargo check && cargo test; `pyproject.toml` + pytest → pytest -q

## Related Skills

- `parallel-investigate` — read-only fan-out (use when no writes)
- `orchestrate` — meta-router; chains to this skill when ≥3 independent tasks
- `loop` — sequential when tasks share state
- `three-man-team` — single feature (architect/builder/reviewer)
- `subagent-driven-development` — sequential same-session execution
- `repo-state-snapshot` — integrated into phases 3 & 5
- `verify-before-done` — optional stricter post-phase gate
