---
name: review-gaps
description: Review a scope for gaps — what the surface promises but does not deliver — with evidence, then fill after confirm
argument-hint: "[scope-or-area]"
related:
  - review
  - review-issues
  - design-cli-prototype
  - design-tui-prototype
  - design-web-prototype
  - design-html-prototype
  - report-not-implement
  - implement-to-production
  - deep-review-codebase
  - deep-review-codebase-then-fix
  - create-plan-in-dot-devin
  - report-review
  - ask-me
  - suggest-next-action
  - refactor
  - deep-thinking
  - deep-analyze
  - deep-validate
---

## Goal

Review one dimension only: `gaps` — capability the scope promises but does not deliver (missing implementation, stub left in place, unwired feature, declared-but-unused, no empty/error state, docs claim with no code). Every finding must show both the promise location and the proof of absence, then get filled after user confirmation. Complements `/review-issues` (what is wrong) and is folded into `/review` for a general pass.

## Scope

- Use when the user asks what is missing / unfinished / not really wired in an area, or from `/review` `### 2` as the gaps dimension
- Not wrong-behavior hunting (→ `/review-issues`), not a full multi-dimension scan (→ `/deep-review-codebase`), not ideating new features (→ `/idea-features`)
- If the user appends `and fix` → treat as confirmed; fill every gap without asking again (still report before filling)
- A gap whose surface was never designed (command tree, TUI screens, web UX) → design it first: `/design-cli-prototype` / `/design-tui-prototype` in chat, or `/design-web-prototype` / `/design-html-prototype` when it must be seen — then fill it; never fill a gap with a new stub

## Execute

### 1. Deep Pre-Pass And Inventory Promises

> Goal: a gap is only measurable against a promise

1. Start with the deep pre-pass: `/deep-thinking` → `/deep-analyze` → `/deep-validate` (convention: `update-devin-global-skills` `## Conventions → Templates` row `review-*`)
2. Take `scope` from the argument — if missing or unclear → `/ask-me`
3. Collect every promise the surface makes: `README.md`/`USAGE.md`/`FEATURES.md` claims, UI labels and menu items, route and command lists, type fields, config keys, feature flags, permissions, `TODO`/`FIXME`/`MOCK` markers, test names
4. Pull the machine-made gap inventory as a baseline: `/report-not-implement` on the scope (`missing`/`fake`/`partial`/`unwired`/`promised` with `file:line`) — then verify each entry yourself, never copy it blindly

### 2. Classify Each Gap

> Goal: name the kind of missing, because the fix differs

| No. | Gap class | Signal | Fill by |
|-----|-----------|--------|---------|
| 1 | Promised but absent | Docs/UI name it, no implementation exists | `/implement-to-production` |
| 2 | Partial implementation | Happy path only; error, empty, or edge branch missing | `/implement-to-production` |
| 3 | Fake or stub left in place | Hardcoded return, `TODO`, mock data shipped in the real flow | `/implement-to-production` |
| 4 | Unwired capability | Code exists but no route, entry point, or permission reaches it | Wire it end to end |
| 5 | Declared but unused | Type field, env var, flag, permission, i18n key nothing consumes | Consume or delete |
| 6 | Missing state coverage | No loading/empty/error/success state for a real async flow | Implement the states |
| 7 | Dead integration | Dependency or module exported but never called in the flow | Use it or drop it |
| 8 | Docs-vs-reality gap | Documented command/option/behavior that does not work | Fix docs or code, then `/update-usage-md` |
| 9 | Test gap | A promised surface no test asserts | `/update-tests` + `/deep-test` |
| 10 | Accessibility gap | Affordance is visible but not reachable (keyboard, label, focus) | Fix the interaction |

### 3. Evidence And Report

> Goal: prove the gap, not just suspect it

1. Every finding needs two pieces of evidence: the promise (`file:line` of the claim) and the absence proof (the search that found no implementation, or the stub location)
2. Severity: `Critical` (paid/advertised capability absent, security or data path missing) → `High` (user-visible flow incomplete) → `Medium` (edge or state coverage missing) → `Low` (unused declaration, doc drift)
3. Exclude intentional scope cuts: an explicitly deferred feature in `TODO.md` or a documented limitation is not a gap — list it separately as "known deferral"
4. Produce a `/report-review` table (chat, no files): `No.`, `Area`, `Gap Class`, `Finding`, `Severity`, `Promise Evidence`, `Absence Evidence`, `Fill Skill`

### 4. Confirm And Fill

> Goal: close the gap for real, no new stub

1. If the user did not append `and fix` → ask which gaps to fill and wait
2. Route each confirmed gap to its `Fill by` from `### 2`; anything that becomes net-new code goes through `/implement-to-production` so the result is production code, not a placeholder
3. Multi-file or architectural fills → `/create-plan-in-dot-devin` first, then implement
4. Domain-matched findings may be handed to `/deep-review-codebase-then-fix` instead of fixing inline
5. After filling → `/refactor` (SRP split) on touched files (≤250 lines, 1 responsibility), run build/lint/test, re-check the promise list from `### 1` step 3 is now honest → `/suggest-next-action`

## Rules

### 1. Promise-And-Absence
- No promise, no gap: a thing nobody advertised is a feature idea, not a gap
- Absence must be proven by search over the real surface, not by not having seen it

### 2. One Dimension
- `/review-gaps` reports only what is missing; wrong existing behavior goes to `/review-issues`, sibling drift to `/review` `### 2`
- Don't invoke `/review` from inside this skill (it would re-enter the same pass)

### 3. No New Placeholders
- Filling a gap never introduces a new stub, `TODO`, or hardcoded return
- Don't fix without confirmation unless the user puts `and fix` in the command

### 4. Formatting
- Never use `*` bold markers — use backticks for emphasis; every report table starts with a `No.` column

## Expected Outcome

- Every promise in the scope is matched against real implementation, with promise + absence evidence per gap
- A prioritized `/report-review` table is presented and the fill set is confirmed by the user
- Confirmed gaps are closed with production code (no new stubs), verified by build/lint/test, and docs stay truthful
