---
name: om-code-review
description: Repo-local extension of om-code-review for money-tracker.online - the context sources, the severity map and the suppression ban every review here applies.
---

# om-code-review (money-tracker.online)

This file extends the shared `om-code-review` skill installed at
`.claude/skills/om-code-review/SKILL.md`. Follow the shared skill's full workflow (validation gate,
breaking-change gate, checklist, output format, verdict) with the repo-specific rules below layered
on top.

## Context sources

Read before the first finding, per touched area:

- `AGENTS.md` (Always / Ask First / Never) and `CODE_REVIEW.md`.
- `docs/SPEC.md` §6 (layering), §7 (definition of done), §8 (one concept, one owner), §9
  (localisation), §10 (accessibility claim).
- `docs/MONEY.md` in full when the diff touches an amount, a rate, a currency or a date bucket.
- The ADR for the area in `docs/adr/`: 0002 tenant boundary, 0006 minor units, 0007 charts, 0010
  ledger, 0011 auth, 0012 billing, 0008 no bank connectors.
- `docs/agents/reference.md`: the clean-room rule. A string, a number, a name or a layout copied
  from the reference product is a blocker.
- `.ai/review-checklist.md` (the configured `reviewChecklist`) and `BACKWARD_COMPATIBILITY.md`.

## Severity map

| Finding                                                                                                                                                       | Severity |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Float arithmetic on an amount; a hard-coded scale of 2; a recomputed `ref_amount_minor`; a cross-currency amount without its `rate_e10`                       | blocker  |
| SQL outside `src/server/repos`; a removable tenant predicate; a write to `account_balances` outside `src/server/ledger`                                       | blocker  |
| A server-function input not Zod-validated or not re-parsed in the repository; a permission enforced only client-side                                          | blocker  |
| A new repository function without a tenant-isolation case; a money-touching write path without a money-invariant case                                         | blocker  |
| A key added to `en.ts` and not `pl.ts`, or the reverse: the parity test fails the build                                                                       | blocker  |
| A hand edit to `src/routeTree.gen.ts` or `drizzle/`; a migration that drops, renames or narrows in the same change that stops writing                         | blocker  |
| An added `@ts-ignore`, `@ts-expect-error`, `eslint-disable`, `.skip`, `.only`, `.todo`, `.fixme`, `xit` or `xdescribe`; a deleted test file                   | blocker  |
| A clean-room violation; a bank connector or credential capture (ADR 0008); a new dependency (SPEC §3); a broken surface in `BACKWARD_COMPATIBILITY.md`        | blocker  |
| A WCAG 2.2 AA regression: unlabelled control, no keyboard path beside a drag, a chart without its text table, colour as the only channel, a target under 44px | major    |
| A blanket "WCAG AAA" claim in copy, comment or commit                                                                                                         | major    |
| Slow work (import, export, email, backup, ledger rebuild, notification fan-out) run inline instead of enqueued on `TASKS`                                     | major    |
| A second implementation of an owned concept: rounding, formatting, conversion, `newId()`, dispatch, a dialog primitive (SPEC §8)                              | major    |
| A missing loading, empty or error state on a screen                                                                                                           | major    |
| `TODO`, `console.log`, commented-out code, placeholder copy                                                                                                   | minor    |

## Review personas

`CODE_REVIEW.md` -> **Review personas** holds the dispatch table and the boundary: four subagents in
`.claude/agents/` (`manual-tester`, `accessibility-specialist`, `security-tenancy-reviewer`,
`product-owner`), each dispatched on the paths it matches, each reporting only. Read the table
there rather than a second copy here.

Two rules apply to this skill when it dispatches one:

- A persona's finding enters the report at the severity of the map above, not at the severity the
  persona felt. Re-rank it; do not paste it.
- A persona that could not run - no browser, no environment, `Task` not granted - is named in the
  report as not run. Silence reads as a pass, and a review that claims a lens it never used is the
  one failure mode this whole arrangement can produce.

## Rules

- The gate's two drift commands run first. A dirty generated file is a finding; never regenerate
  it silently in the review worktree.
- A count or measurement in the review report came from a command whose output you read
  (`docs/SPEC.md` §7.7). When the number is `0`, say what the command was aimed at.
- Secrets never enter the report: no value from `.dev.vars`, `.env.local` or `.ai/qa/test-env.env`.
