---
name: split-initiative
description: Turn a framed initiative into a reviewed child-task graph in `TASK_GRAPH.md`, using vertical slices, explicit dependencies, canonical child statuses, and reviewable child boundaries.
---

# split-initiative

## Read first
- `../references/initiative-packet-contract.md`
- `../references/initiative-workflow-contract.md`
- `../references/final-state-authoring-policy.md`
- initiative `BRIEF.md`, `UBIQUITOUS_LANGUAGE.md`, `DECISIONS.md`, `INVARIANTS.md`, `REPO_MAP.md`, `CONTRACTS.md`, `OPEN_QUESTIONS.md`
- optional `SPLIT_OPTIONS.md`
- `../../references/communication-mode.md`

## Goal
Write the first semantic `TASK_GRAPH.md` so each child is independently understandable, has explicit dependencies, and is small enough for a normal Atelier child loop.

## Heuristics to internalize
- prefer vertical slices over horizontal phase buckets
- make each child understandable without giant hidden context
- state explicit scope, out-of-scope, validation expectations, and dependencies
- sequence by uncertainty and risk reduction
- keep one main change seam per child when possible
- prefer one clear owner repo per child; treat truly multi-repo children as a smell unless the boundary is genuinely inseparable

## Write into `TASK_GRAPH.md`
For each child:
- slug / title
- owner or owning repo / boundary
- `Packet Root:` repo root where the child packet will live
- dependency edges
- scope summary
- contract surface summary
- validation expectations
- optional blocker note
- `Child Status: ready` when dependencies are already satisfied, otherwise `Child Status: pending`

## Status
- enter initiative `Status: split_drafting` if no split-drafting phase already exists
- exit with initiative `Status: split_review`

## Writing rule
Write the task graph as the canonical execution decomposition.
Do not leave superseded split vocabulary or transitional child-state names in the graph.

## Do not
- create giant catch-all children
- use the parent packet as a delivery plan
- reference outside Atelier skill files for split heuristics

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
