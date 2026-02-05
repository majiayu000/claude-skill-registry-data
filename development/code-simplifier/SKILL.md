---
name: code-simplifier
description: Refactors for readability after verification is green, re-running checks and updating 20_verification.md.
---

# code-simplifier

## When to use
Use this skill when asked to:
- clean up, simplify, refactor, or make more readable
- reduce duplication / improve naming / reorganize code
- improve maintainability without changing observable behavior

## Rules
- Only refactor after verification is green for the current task.
- Preserve behavior: no semantic changes, no API changes unless explicitly requested.
- Keep diffs small and reviewable.
- Avoid introducing new dependencies unless explicitly approved.
- Follow `AGENTS.md` and the task handoff protocol in `tasks/`.

## Method
1. Confirm the latest `tasks/<date>_<slug>/20_verification.md` is green.
2. Apply a small, focused refactor.
3. Re-run the same checks used by the Verifier.
4. Append a rerun transcript and summary to `20_verification.md`.

## Output requirements
- Summarize what was simplified and why.
- Update `20_verification.md` with the rerun transcript.
