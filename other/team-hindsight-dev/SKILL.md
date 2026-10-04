---
name: team-hindsight-dev
description: "Orchestrate a coding session with hindsight-dev-memory-lead plus GitNexus-safe implementation. Use for multi-step C# work, story implementation, or resuming deferred tasks with memory."
---

# Team: Hindsight + GitNexus Dev

Coordinates persistent session memory with code-intelligence gates.

## When to use

- `/dev-story` on non-trivial stories
- Multi-file delegation/sim changes
- Resuming work: "continue where we left off"
- Post-PR iteration with review memory

## Protocol

1. Read `hindsight-gitnexus` and `hindsight-dev-memory`.
2. Run `.\tools\hindsight\Test-HindsightServer.ps1` (non-blocking if down).
3. Spawn **`hindsight-dev-memory-lead`** via Task tool as the primary implementer.

Optional parallel specialists (only if scope requires):

| Need | `subagent_type` |
|------|-----------------|
| C# implementation | `c-sharp-engineer` |
| Tests | `c-sharp-test-engineer` |
| Determinism audit | `determinism-engineer` |
| Post-playtest AAR | `hindsight-aar-analyst` |
| Trait tuning | `balance-tuning-memory-agent` |

## Stop conditions

- HIGH/CRITICAL `gitnexus_impact` without user approval
- Hindsight down → proceed with GitNexus; note missing memory in report

## Deliverables

- Code changes (approved paths)
- Retain summaries on `dev-cmano-clone` / `dev-story-*`
- Closing note: banks used, tests run, `gitnexus_detect_changes` status
