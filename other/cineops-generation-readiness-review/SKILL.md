---
name: cineops-generation-readiness-review
description: Review shots, keyframes, prompts, storyboards, or generated clips before expensive generation and issue a ready, revise, or blocked decision. Use to catch continuity, spatial, performance, camera, transition, and generation-clarity failures without rewriting the creative work.
---

# CineOps Generation Readiness Review

## Purpose

Act as an independent quality gate. Diagnose and return actionable defects; do not take over screenplay writing, shot design, prompt authoring, or media generation unless explicitly asked after the review.

Read `references/readiness-rubric.md`. Use `assets/readiness-report.template.json` for machine-checkable decisions.

## Inspect Evidence

1. List what is actually available: script beat, shot plan, ledger state, prompt, references, first/last frames, or clip.
2. Mark unavailable evidence as `unknown`. Never claim visual inspection of an inaccessible asset.
3. Compare the shot with its dramatic purpose and adjacent entry/exit states.
4. Evaluate continuity, spatial blocking, performance endpoint, camera logic, transition viability, and generation clarity.
5. Distinguish source defects from generation defects. A weak result does not prove the prompt was wrong, and a polished prompt does not prove the shot is ready.

## Decision Rules

- `ready`: all critical checks pass; remaining notes are optional refinements.
- `revise`: no fundamental contradiction exists, but one or more fixable failures are likely to waste a generation.
- `blocked`: required evidence is missing, canon conflicts, staging is impossible, or the shot's dominant action cannot be interpreted reliably.

Any failed critical check prevents `ready`. Any critical `unknown` prevents `ready` unless the uncertainty is intentionally delegated to controlled generation variation.

## Write Findings

Each finding must contain severity, evidence, likely visible failure, minimum repair, owner, and recheck condition. Prefer instructions such as "end with the right hand still gripping PROP-CARD" over vague notes such as "improve continuity."

Save decisions in `readiness-report.json`, then run:

```bash
cineops validate path/to/project
```

## Result Review

For generated media, inspect temporal continuity, identity drift, unintended object changes, screen direction, gaze, weight shift, reaction timing, camera path, and whether the final frame can connect to the next shot. Return the smallest set of changes worth another generation.

Do not approve based on aesthetics alone. A beautiful shot that breaks canon or cannot edit into the sequence is not ready.
