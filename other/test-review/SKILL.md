---
name: test-review
layer: stage
description: Propose the test(s) FIRST and get a human to sign off on the behaviour before writing the code — the test analog of /schema-review and /ui-proposal. For hand-written LOGIC in packages/* (apps opt-in, pocs exempt). Renders the proposed failing test as a reviewable contract, holds for lgtm/approve, then you write the code to make it green. Use when an agent is about to implement packages/* logic, or when asked to "write the test first", "TDD this", "agree on the test", run /test-review.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Test Review — agree on the test before you write the code

Turns "I'm about to write some logic" into a **reviewable contract**: the proposed *failing*
test(s) — the cases being asserted, in plain language plus the actual test code — so a human can
sign off on the **behaviour** *before* any implementation exists. The agreed test is the
definition of done: "done" = that test passes.

This is the third sign-off gate (epic #774), alongside **`schema-review`** (#314, the data model)
and **`ui-proposal`** (#307, the look). Pick the gate by *what the change is*: a data model → schema
gate; how it looks → UI gate; **hand-written logic → here**. It reuses the same revision/approval
loop and signal as the other two (#310/#572).

> **Why test-first?** The test is cheap to change while it's just a proposal and expensive to change
> after the code is built around the wrong assumption. Agreeing on the cases first ("no
> double-booking; adjacent slots OK; buffer respected") means the code has one job — go green —
> instead of being a moving target.

## Step 0 — Self-scope (skip when out of scope). This gate is deliberately narrow.

Decide by **where the code currently lives (#779)**, then by **what kind of change** it is. Skip
loudly (one line saying why + which gate, if any, fits instead) rather than gating everything.

**By location — resolved from the stage model.** Run `node scripts/harness-stages.mjs <path>`
(or `gateMode(path, 'test-first')`) for the verdict (`on` / `opt-in` / `off`) rather than matching
the folder by hand; the canonical source is `harness.config.mjs` (epic #952). The table below is
the **default profile** rendered for humans:

| Current home | Stage | Action |
|---|---|---|
| `packages/*` | `package` | **Proceed** (default — what we maintain; every consuming app inherits its correctness) |
| `apps/*` | `app` | **Skip unless the app has explicitly opted in** (may be another user's app — not ours to impose) |
| `pocs/*` | `poc` | **Skip** — the incubator must stay fast and safe-to-fail; a POC graduating to `packages/*` is the checkpoint to backfill its tests |

**By change kind (only once location is in scope):**
- Collection schema / data model → **skip**, use `/schema-review` (+ the e2e fixture smoke covers generated CRUD).
- `.vue` component / layout / theme — how it *looks* → **skip**, use `/ui-proposal`.
- Deterministic **generated** code (CLI output, templated CRUD) → **skip**, the e2e smoke harness owns it.
- **Hand-written logic** — a composable rule, server util, permission check, calculation, layout-engine transform, a generator's own logic → **proceed.**

> Rule of thumb: `packages/*` *logic* almost always proceeds; everything else almost always skips.
> When unsure whether something is "logic", ask: *can a human just eyeball it for correctness?* If
> yes, it probably doesn't need a test-first contract.

## Step 1 — Pin down the behaviour

Before writing any test, state — in one or two plain sentences — what the logic must do, and
**enumerate the edge cases** that matter. This list IS the thing being agreed on; the test code is
just its executable form. Example (a slot-availability rule):

- a booking that overlaps an existing one is rejected
- two back-to-back bookings (end == next start) are both allowed
- a booking inside another's buffer window is rejected
- times are compared in the resource's timezone, not the server's

## Step 2 — Write the proposed failing test(s)

Author the test next to the code it will cover, following the package's existing test layout
(`*.test.ts` beside the source, or its `__tests__/` dir — match the neighbours; see
`packages/crouton-core` for examples). Vitest is the runner (`pnpm test`).

- One `describe` per unit; one `it` per edge case from Step 1, named in plain language.
- The test must **fail first** — it asserts against code that doesn't exist yet (or asserts the
  new behaviour the current code lacks). Red before green is the point; surface that.
- Keep it a **general** contract (all valid inputs), never assertions reverse-engineered to pass a
  specific implementation.

## Step 3 — Hand off for sign-off (review happens on the test itself)

**The proposed test is the review surface.** Present both the plain-language case list (Step 1) and
the test code, so the reviewer agrees on *behaviour*, not syntax.

- **Interactive session:** show the case list + test in chat and hold. The reviewer says
  `lgtm`/`approve` to proceed, or asks for changes (add a case, fix an expectation) → revise and
  re-show.
- **Agent pipeline / PR:** commit the failing test (via `/commit`, scope = the package, e.g.
  `test(crouton-core): …`) so it lands in the PR's "Files changed". The reviewer comments inline on
  any `it(...)` to change a case. Set the issue to `status:blocked` while holding. Approval is a
  **comment** containing `lgtm`/`approve` — **not** a reaction or label (#572) — and it unblocks
  implementation.

Iterate Step 1–3 until approved. Do **not** write implementation code before the test is agreed.

## Step 4 — Go green (only after approval)

Write the implementation to make the agreed test pass — and **only** that. Run `pnpm test` (and
`pnpm typecheck`) until green. The agreed test is now the regression guard; it stays in the diff and
ships with the code. Resume the normal workflow (typecheck → update issue → `/commit`).

## Conventions
- The case list (Step 1) is the contract; keep the test code honest to it — never quietly drop or
  weaken a case to make implementation easier (that's a re-negotiation → go back to Step 3).
- One concern per test file, mirroring the source it covers.
- Red first, then green. If the proposed test passes *before* you write any code, the behaviour
  already exists — say so and skip (nothing to build).
- This is about *order* (test before code), not *enforcement* — the CI `test` job already hard-gates
  `pnpm test`.
