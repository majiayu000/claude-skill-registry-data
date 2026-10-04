---
name: goal
description: Creates and maintains an agent-owned goal ledger that pairs with long-running coding work, compaction recovery, chained engineering goals, or codebase status tracking. Use when the user says "$goal", "/goal mode", "start a goal", "continue this goal", "chain goals", "agent progress ledger", "flight recorder", "implementation notes", or asks the agent to save progress separately from a PRD. When the runtime exposes a native goal tool (for example Codex `/goal`), couple the file ledger to the runtime goal objective. Keeps `GOAL.md` as the contract and `implementation-notes.html` as the canonical readable state for progress, decisions, validation, compaction resume, blockers, and next-goal links.
---

# Goal Ledger

Use this skill as durable execution memory beside `/goal` mode.

The PRD says what should become true. The goal ledger records what is currently true during execution. Keep the ledger small and navigable so compaction, interruption, or chained goals preserve execution reality.

## Core Rule

Use one canonical readable state file: `implementation-notes.html`.

Keep current truth in `implementation-notes.html`. A single source of readable state is stronger than several partial state files.

The HTML file embeds its own progress timeline directly inside the page. There is no separate JSONL log to keep in sync. The HTML is the canonical state and the canonical history in one self-contained artifact that opens cleanly as a local file.

Default layout:

```text
.agent/
  GOALS.md
  runs/
    <goal-id>/
      GOAL.md
      implementation-notes.html
      evidence/             # optional bulky proof files linked from implementation-notes.html
```

## File Roles

`GOAL.md` is the contract:

- objective
- finishing criteria
- parent goal, if any
- runtime goal coupling line
- escape hatch

`implementation-notes.html` is the canonical live state:

- top `Resume Here` section for compaction and interruption recovery
- current phase, completed work, active work, blockers, and next exact action
- decisions made because the spec was silent
- changes made because the repo disagreed with the spec
- tradeoffs, shortcuts, and sequencing choices the next reader should know
- validation status and links to bulky proof files
- protected paths and user-owned work
- next-goal candidates
- an inline progress timeline rendered from a `progressEvents` array inside the page itself

`evidence/` is optional attachment storage. Use it only for large logs, screenshots, command output, reports, or artifacts that would make the HTML hard to read. Link every evidence file from `implementation-notes.html`.

## Native Goal Tool Coupling

When the user explicitly asks for `$goal`, `/goal mode`, `start a goal`, `continue this goal`, `goal ledger`, or equivalent goal-mode language, and the runtime exposes a native goal tool (for example Codex `/goal`), use it.

1. Read the existing native goal with `get_goal` when available, then locate its matching ledger before creating files.
2. Keep an existing unfinished native goal. Use `create_goal` only for an explicitly requested goal when the tool permits creation; include the known absolute ledger path in the objective. Set a token budget only when the user requested one.
3. Follow the tools actually exposed: `update_goal` changes completion or blocked status; it cannot edit the objective, pause, resume, or change budgets. Do not recreate a goal to repair a stale badge or add a missing ledger pointer. Record the association in `GOAL.md` and the resume notes instead.
4. Mark the native goal complete only when its objective is finished and verified. Mark it blocked only when the native tool's stated blocking conditions are met; a local blocked item alone does not establish that the whole goal is blocked.

When native goal tools are unavailable or an unrelated unfinished native goal prevents coupling, record that limitation and continue authorized work in its matching file ledger. Do not replace an unrelated goal or infer that a running task means its native goal is active.

## Starting A Goal

1. Locate any existing ledger using `Resuming A Goal` below and resume it if found. Use the following steps only for a new goal, with finishing criteria defined before implementation.
2. Pick a stable `goal-id`: lowercase words, date when useful, no spaces.
3. Create the ledger with `scripts/init_goal_ledger.py`:

```bash
uv run scripts/init_goal_ledger.py \
  --root . \
  --goal-id "<goal-id>" \
  --title "<short title>" \
  --objective "<one sentence objective>" \
  --mode light
```

Use `--mode full` for multi-step goals. Full mode uses the same simplified file layout. Add `--parent "<previous-goal-id>"` when this goal became possible because another goal completed.

The initializer preserves existing ledger files and an existing index entry; rerunning it does not resume or reactivate a completed goal. When the script is unavailable, create only the missing files manually.

## Resuming A Goal

1. Follow the ledger path in the current task or native objective. If absent or stale, inspect the relevant project's `.agent/GOALS.md` and search that project for `GOAL.md` and `implementation-notes.html`. Reuse the established canonical ledger, including a legacy location; do not start another ledger just because the working directory or task changed.
2. Read the contract and `Resume Here`, preserving the user's objective, settled decisions, protected paths, and authorization boundaries. Verify the current workspace and relevant evidence needed for the next action; recorded progress is a checkpoint, not proof of current runtime or deployment state.
3. Reconcile the file ledger, native goal state, and actual work explicitly. Correct stale notes from evidence without discarding history or changing the user's goal. If an index entry is missing, restore it from the existing ledger's status rather than initializing it as active.
4. Continue the next authorized action. Ask only if competing ledgers or contradictory instructions leave the intended goal or a consequential decision unresolved; continue independent work meanwhile.

## Goal Mode Coupling

When creating the matching native goal, include this ledger pointer in the goal objective:

```text
Maintain the agent-owned ledger at <absolute-or-project-relative-ledger-path> and keep implementation-notes.html current at checkpoints, before compaction, and before final handoff.
```

This keeps the ledger path and maintenance requirement available when compaction preserves the native objective but drops conversation context.

The helper script writes a `Goal Mode Coupling` section into `GOAL.md`. Copy that line when creating the native goal. Preserve an existing objective when the tool cannot edit it.

## Implementation Notes

When the user uses wording like this:

```text
implement <SPEC> and while you do, keep a running implementation-notes.html file with decisions you had to make that weren't in the spec, things you had to change, tradeoffs you had to make or anything else I should know
```

Create or update the goal ledger, create or update `implementation-notes.html`, and make the notes part of the finishing criteria. Prefer HTML when the user wants a viewable artifact; use Markdown only when the project or user asks for Markdown.

Keep the top section named `Resume Here`. It should be short enough to read in under a minute and concrete enough to resume work immediately.

Recommended `Resume Here` content:

- status
- current phase
- completed work
- active work
- blockers
- next exact action
- last validation
- protected paths and user-owned work

Keep a section named `Progress Timeline`. It renders directly from the inline `progressEvents` array embedded in the page. Append one entry to that array whenever execution reality changes meaningfully.

Recommended event object (appended directly into the inline `progressEvents` array in the HTML):

```js
{
  ts: "2026-05-19T10:00:00Z",
  status: "done",
  phase: "database-hardening",
  actor: "agent",
  summary: "Migration 0025 applied and database types regenerated.",
  evidence: ["evidence/db-reset.log"]
}
```

## Compaction

Before compaction, interruption, or a long handoff:

1. Update the top `Resume Here` section of `implementation-notes.html`.
2. Append a checkpoint event into the inline `progressEvents` array.
3. Record current phase, completed work, active work, blockers, next exact action, validation state, and protected paths.
4. Link any bulky proof files from `evidence/`.
5. Record the native goal association and any status mismatch in the resume notes. Keep using the established ledger even when its pointer cannot be added to an existing native objective.

The next agent should be able to resume from `GOAL.md` and `implementation-notes.html` without needing the full conversation.

## Chained Goals

When one goal unlocks another, link them explicitly:

- In the new `GOAL.md`, set `Parent goal: <goal-id>`.
- In the old `implementation-notes.html`, add `Next goal candidate: <goal-id>`.
- In `.agent/GOALS.md`, keep one entry per goal with its current status and relationship; update existing entries instead of appending duplicates.

Why: chained work loses context fast. The relationship is often more important than the individual tasks because it explains why the next goal exists now.

## Status States

Use these states in `implementation-notes.html`:

- `[todo]` - known and not started
- `[doing]` - currently active
- `[done]` - completed and validated
- `[blocked]` - waiting on external input or dependency
- `[incomplete]` - attempted, not fully solvable inside current constraints
- `[abandoned]` - intentionally stopped because the goal changed or no longer pays rent

Use `[incomplete]` only with this full explanation:

```md
- [incomplete] <item>
  - reason:
  - proof:
  - attempted:
  - impact:
  - next human/agent decision:
```

This gives the agent a clean honesty path when a checkpoint is impossible inside the current constraints.

## Escape Hatch

Every serious goal must include an escape hatch in `GOAL.md`:

```md
## Escape Hatch

If validation fails, the repo disagrees with the plan, progress stalls, or the ledger affects validation, investigate and correct the recoverable issue within the existing scope. Record what changed and continue.

Ask the user only when progress requires a scope or product decision, destructive changes to durable state, missing authorization, or information that cannot be established from available evidence. Mark the affected item `[blocked]` / `[incomplete]` with the reason and continue independent authorized work. Do not silently relax finishing criteria or overwrite history to make the ledger look complete.
```

The escape hatch is the honesty path for impossible, contradictory, or scope-changing checkpoints.

## During Work

Update `implementation-notes.html` when reality changes:

- after validation establishes or changes a relevant result
- after a meaningful implementation checkpoint
- before handing off to another agent
- before compaction
- when a blocker or incomplete item appears
- when the next goal becomes obvious

Append a single event into the inline `progressEvents` array at the same checkpoints. Write compact events. The ledger is a state surface plus a durable progress log, not a transcript.

Choose checks that establish the requested behavior or catch a plausible regression in actual code. A coverage percentage is not a finishing criterion unless the user explicitly chose it; do not invent unrealistic scenarios or expand testing after sufficient evidence is available.

## Finishing A Goal

Before reporting completion:

1. Re-read `GOAL.md` finishing criteria.
2. Run the stated validation or explain why it cannot run.
3. Save bulky proof under `evidence/` only when needed, and link it from `implementation-notes.html`.
4. Mark completed items `[done]`, and any scoped misses `[blocked]` or `[incomplete]` with evidence.
5. Update `implementation-notes.html` with final status, decisions, tradeoffs, validation, and next-goal candidates.
6. Append a final event into the inline `progressEvents` array with validation and outcome.
7. Update `.agent/GOALS.md` with final status.

Report the ledger path in the final answer.
