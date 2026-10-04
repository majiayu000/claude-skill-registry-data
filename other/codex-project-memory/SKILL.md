---
name: codex-project-memory
description: Maintain a minimal, token-aware, verified project memory for Codex repositories. Use when initializing project context files, resuming work across sessions, changing architecture or project goals, recording decisions, updating current state after implementation, or reducing bloated and stale agent documentation.
---

# Codex Project Memory

Preserve the smallest verified project state needed for reliable future work.

## Core Rules

1. Treat code and tests as evidence; do not turn assumptions into project memory.
2. Keep always-loaded context small.
3. Read detailed documents only when the task needs them.
4. Replace stale state instead of appending an endless activity log.
5. Mark future work as `Planned` and shortcuts as `Temporary`.
6. Use Git history for exhaustive history; do not duplicate it in active context.
7. Never store secrets, credentials, tokens, personal data, or private
   machine-specific information in project memory.
8. Do not bypass sandboxing, approval requirements, repository permissions, or
   other user-controlled security boundaries.

## Start A Task

1. Read the nearest applicable `AGENTS.md`.
2. Read `docs/PROJECT_CONTEXT.md` and `docs/CURRENT_STATE.md`.
3. Inspect relevant code before relying on documentation.
4. Load additional context by task type:
   - Architecture, interfaces, data flow, storage, dependencies: read `docs/ARCHITECTURE.md`.
   - A choice whose rationale matters: read relevant entries in `docs/DECISIONS.md`.
   - Historical investigation only: search targeted entries in `docs/CHANGELOG.md` or Git.
5. If documentation conflicts with implementation, verify behavior and repair the documentation as part of the task.

## Finish A Task

Update only documents affected by verified changes:

- Goal, scope, audience, constraints: `PROJECT_CONTEXT.md`
- Current progress, active work, blockers, next steps: `CURRENT_STATE.md`
- Implemented structure, interfaces, data flow, dependencies: `ARCHITECTURE.md`
- Significant choices and trade-offs: `DECISIONS.md`
- Concise user-visible or architectural change summary: `CHANGELOG.md`

Then:

1. Remove or replace stale statements.
2. Keep each document within the budgets defined in `AGENTS.md`.
3. Review the memory diff for sensitive or proprietary information.
4. Run `python scripts/validate.py <project-root>` when the script is installed.
5. Report which memory documents changed and why.

## Decision Test

Create a decision record only when reversing the choice later would be costly or confusing. Include context, decision, rationale, alternatives, consequences, date, and status.

Do not create decision records for routine edits, formatting, or obvious implementation details.

## Compaction

When a document exceeds its budget:

1. Preserve current truth, non-obvious constraints, and active risks.
2. Remove completed task narration from `CURRENT_STATE.md`.
3. Collapse superseded architecture descriptions into the current design.
4. Move durable rationale into `DECISIONS.md`.
5. Leave detailed historical reconstruction to Git.

## Evidence And Claims

When evaluating whether project memory saves context:

1. Prefer reproducible measurements over intuition.
2. Label character-based token calculations as estimates.
3. Keep static fact coverage separate from agent task success.
4. Report real token usage or success rates only when supplied by an actual run.
5. Never infer model quality from context size alone.

If the repository includes `benchmarks/run.py`, run it after changing document
routing, budgets, benchmark tasks, or report methodology.

Read [references/document-contracts.md](references/document-contracts.md) when initializing files or deciding where information belongs.
