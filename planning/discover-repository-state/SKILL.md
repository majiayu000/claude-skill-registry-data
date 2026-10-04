---
name: discover-repository-state
user-invocable: true
version: 1.2.2
description: >
  Discover repository evidence and write a frozen Normalized Repository State.
  Produces verified repository evidence and keeps facts, decisions, planned
  work, documentation, and inference separate. It does not make
  recommendations or infer implementation from documentation. Triggers: "discover
  repository state", "normalize repository state", "freeze repository facts".
---

# Discover Repository State

Create a reviewable evidence snapshot before planning or implementation.

## Turn contract

```
✓ Repository evidence was read or commands were run for every fact
✓ Facts, documentation, planned work, decisions, and inference are separated
✓ Snapshot status is frozen unless a contradiction was recorded
✓ No accepted decision or existing frozen fact was silently changed
✓ The closing → Next: block is printed last
```

## Step 0 — Discover the project (always first)

Read the agent guide, documentation map, and any existing repository-state
ledger before collecting evidence.

## Process

1. Read the project guide, documentation map, and any existing
   `docs/workflow/REPOSITORY_STATE.md`.
2. Inspect repository files, tests, git state, and declared tooling. Record only
   directly observed statements in **Repository Facts**, each with file:line or
   command evidence.
3. Record design records under **Accepted Decisions**, roadmap entries under
   **Planned work**, and document-only claims under **Documentation**. Do not
   copy them into facts without separate implementation evidence.
4. Place reasoning under **Inference** and unresolved ambiguity under **Open
   Questions**.
5. If the existing snapshot is already `contradicted`, preserve that status and
   do not alter its unresolved contradiction; hand off to
   `resolve-repository-state`. Otherwise, if new evidence conflicts with a
   frozen fact, append a **Contradiction**, set snapshot status to
   `contradicted`, and do not alter the fact. Hand off to
   `resolve-repository-state`.
6. Only if neither an existing nor a newly recorded contradiction is present,
   set the snapshot status to `frozen`. Commit the artifact and cite the source
   revision.

## Guardrails

- Discovery records repository facts and preserves decisions, planned work,
  documentation, inference, questions, and contradictions in their own sections.
- The repository remains authoritative; refresh when the snapshot is stale.
- Never create implementation recommendations or silently accept decisions.

## Portability

Without a slash menu, open this file and follow its process in a fresh turn.

## Relationship to other skills

`resolve-repository-state` resolves contradictions; planners and executors
consume the frozen result.

## Done when

The ledger is frozen or explicitly contradicted, and every fact carries direct
evidence.

If a contradiction was recorded:

→ Next: /resolve-repository-state <contradiction-id> — resolve the contradicted snapshot first
  · provide missing evidence → rerun /discover-repository-state

Otherwise:

→ Next: /unit-lane <slug> — triage and run the lane from frozen facts
  · already-triaged unit → /execute-phase <NN>
