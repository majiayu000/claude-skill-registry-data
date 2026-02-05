---
name: phase-implementation-runbook
description: Enforce the phase implementation workflow for Palette Kit v0.3 phases. Use when implementing a roadmap phase, creating a phase branch, validating the lint/typecheck/test/build pipeline, generating a patch for review, or preparing commit/push/PR steps.
---

# Phase Implementation Runbook

Use this skill whenever implementing a roadmap phase. It enforces the agreed step-by-step process and adds guardrails for clean reviews.

## Workflow (must follow in order)

1) Preflight and scope

- Read the target phase from `src/planning/roadmap-v0.3.md` and any referenced specs.
- Confirm branch name format: `phase-<number>-<short-slug>`.
- Check `git status -sb` and call out unrelated changes before proceeding.
- If unrelated changes are present, stop and ask how to proceed.

2) Create branch

- Create the branch from `v0.3` (or current branch if already on `v0.3`).
- Prefer `git switch -c phase-<number>-<short-slug>` for branch creation.
- Verify with `git status -sb`.

3) Implement the phase

- Make only changes required for the phase.
- Keep docs updated when required by the phase (e.g., spec references).
- Do not add unrelated refactors.
- If editing `.md` files, follow the markdownlint rules (use the markdownlint-writer skill).
- Do not expand scope beyond what is explicitly listed in the phase.
- If an improvement is identified but out of scope, document it and stop.
- Prefer adding new files over modifying existing ones unless explicitly required.
- Avoid moving files or renaming symbols without spec justification.

4) Validate in order

- Run these commands in an order that surfaces fast failures first:
  1. `npm run lint:md` (if docs touched)
  2. `npm run lint`
  3. `npm run typecheck`
  4. `npm run test`
  5. `npm run build`
- If any step fails, fix and rerun from the failing step onward.
- If a command is not applicable, note it explicitly as "not run" in the report.

5) Summarize changes and produce diff patch for review

- Capture a quick summary with `git diff --stat`.
- Generate a patch file for external review, e.g.:
  - `git diff > /tmp/phase-<number>-<short-slug>.patch`
- Report the patch path and wait for explicit confirmation to commit and push.

6) After confirmation: commit, push, PR

- Craft Conventional Commit message(s) in English.
- Commit only the phase-related changes.
- Push the branch.
- Open a PR with base `v0.3` and a clear summary.

## DX Quality Gate (mandatory)

Before producing the patch:

- All new public APIs MUST:
  - have complete TypeScript autocomplete
  - include clear JSDoc explaining:
    - intent
    - defaults
    - inferred vs explicit behavior
- If an API is correct but awkward to discover or use, stop and revise.
- DX regressions are considered phase failures, even if tests pass.

## Guardrails

- If you notice unexpected changes you did not make, stop and ask how to proceed.
- Never amend commits unless explicitly requested.
- Do not run destructive git commands.
- Do not reinterpret or redesign specs.
- All architectural and API decisions are considered frozen for the phase.
- If the spec is ambiguous or incomplete, stop and ask before implementing.

## Output checklist

Always end the phase work (pre-confirmation) with:

- Tests/validation results summary.
- Patch path.
- A prompt asking for confirmation to commit/push/PR.
- Confirmation that all phase goals are satisfied and no extra features were added.
- Confirmation that no architectural or API decisions were changed.
- Short note explaining how the implementation maps to the spec requirements.
