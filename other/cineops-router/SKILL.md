---
name: cineops-router
description: Route AI film-production work to the correct CineOps skill and preserve approved artifacts between screenplay, shot planning, continuity, and generation review. Use when a request spans multiple production stages, when the next step is unclear, or when an existing project needs a status and handoff audit.
---

# CineOps Router

## Purpose

Act as production control, not as an all-purpose creative writer. Identify the current stage, protect approved facts, choose the smallest useful next action, and leave an inspectable handoff.

Read `references/workflow-contract.md` when routing a multi-stage project. Use `assets/project-brief.template.md` when the project does not yet have a brief.

## Route The Request

1. Inventory available inputs: brief, screenplay, scene, shot plan, ledger, asset references, generated media, and review notes.
2. Classify each input as `approved`, `draft`, `superseded`, or `unknown`. Never silently promote a draft to canon.
3. Identify the requested decision, not just the requested document.
4. Route to one primary skill:
   - Story logic, scene value, dialogue, or producibility: `$cineops-screenplay-diagnostics`.
   - Blocking, framing, timing, coverage, or shot handoff: `$cineops-shot-planning`.
   - Canon, state transitions, cross-episode consistency, or change impact: `$cineops-continuity-ledger`.
   - Paid generation readiness or failed-output diagnosis: `$cineops-generation-readiness-review`.
5. Invoke multiple skills only when each produces a distinct artifact. State their order.

## Enforce Gates

Do not advance merely because a document exists.

- A screenplay passes when scene goals, causal turns, and observable actions are sufficiently clear for planning.
- A shot plan passes when each shot has a purpose, duration, blocking, camera intent, and entry/exit state.
- Continuity passes when all referenced entities exist and changed canon has an explicit impact review.
- Generation readiness passes only when no blocker remains and every unknown that could alter output has an owner.

Use `cineops validate <project-directory>` whenever CineOps JSON artifacts exist. Treat validation errors as blockers and warnings as review items.

## Handoff Format

End with:

```text
Current stage:
Approved inputs:
Unknowns:
Primary skill:
Artifact to produce:
Exit criteria:
Blocked by:
Next owner/action:
```

Keep creative alternatives separate from approved production state. Never claim an image, clip, or asset was inspected unless it was actually available.
