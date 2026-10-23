---
name: tdd
description: Use when the tests step starts, before any implementation code, write the tests first, one vertical slice at a time (test-casebook doctrine), and turn every acceptance criterion into a contract line that fails by default.
---

# tdd

Step 5 of the pipeline (`WORKFLOW.md`). Tests first, and a **default-FAIL contract** that will
make the GATE (step 7) mechanical.

**Where the doctrine lives.** The testing doctrine itself — `data-test-*` selectors, the `task-test.md`
plan, the permission/persona matrix, the coverage floor, the per-stack guides — is owned by the
`test-casebook` family (MIT, `techmefr/*`), which also ships its own executing agents and a
plan-before-tests hook. **Where it's installed, it is the authority and this block defers to it**; install
the sibling that matches the stack rather than restating its rules here — `test-casebook` for the frontend,
`test-casebook-back-js` for a Node backend, `test-casebook-back-php` for a PHP one, each `npm i -D` and
pinned. What stays ours
is the **default-FAIL contract** and its link to the gate — that has to hold in a repo with no package
installed at all.

## When
After `plan`, before writing the implementation.

## Steps
The plan cuts the work as vertical slices (`skills/plan`, reference 17, point 16). Do steps 1 to 4 for one slice,
then take the next slice.

0. **Initialise the whole contract up front.** For **every acceptance criterion of the feature**, create a line in
   `test-results.json` as `{ "passes": false }` (the contract starts as a failure). Lines of later slices stay
   `false` until their own slice reaches the gate, so the gate stays mechanical.
1. Take the slice's acceptance criteria and write the matching tests following **test-casebook** (`data-test-*`
   selectors, exhaustive, persona matrix, target coverage >= 90%), by a different agent than the one that will
   implement the slice.
2. Run the slice's set: **all of it is red**, that's the expected result at this step. Scoped runs once
   implementation starts follow `skills/run-generated-tests` — this step is the one deliberate exception where
   the slice's whole new set is meant to run together, because "all red" is the thing being checked.
3. **Read each failure**: red has to mean the assertion failed, not that the test file crashed on a
   broken import or an incomplete mock. A setup error satisfies the contract while proving nothing,
   and it turns green later for reasons unrelated to the behaviour.
4. Implement the slice to green, then repeat from step 1 for the next slice.

Delegate the writing to `dozer` (tests only, never implementation) when you want that separation
enforced rather than relied on. That separation is the whole defence against a specific failure mode:
the same agent that just wrote the implementation editing the test's expectation instead, later, to
turn a red result green. This block's guardrail (below) covers the moment these tests are **written**;
`code`/`debug` carry the sibling rule for the moment one of them **fails during implementation** —
adding a case is fine, loosening or retargeting an existing assertion to match broken output isn't,
whichever agent is at the keyboard.

The sections below are read when their trigger is met.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Excuses, red flags, the test that names its break, the regression test proven by reverting | you are tempted to write the code first, to loosen a test, or to trust a test that never failed | [`01-excuses-and-red-flags.md`](./references/01-excuses-and-red-flags.md) |
| 2 | End-to-end tests | the criteria describe a journey through a real interface | [`02-end-to-end.md`](./references/02-end-to-end.md) |

## Output / checkpoint
`tests_written` + `test-results.json` (every line `{ passes: false }` at the start; only the GATE flips a slice's lines).

## Guardrails
**No production code without a failing test that demanded it.** Code that came first is set aside and the test is
written from the criterion, not fitted to what the code does.

A test names the break it catches (the regression or decision it guards); one whose break you cannot name is
a candidate for deletion. A regression test is proven by reverting the fix and watching it fail (`01-excuses-and-red-flags.md`).

The project's own suite defines green, a targeted test is not enough, and every failure is named even when this change did not cause it.
No test bypassed, hidden or disabled. The default contract is **failure**: nothing is
"passing" until the GATE has proven it. Never loosen an assertion or lower a coverage threshold to
close a gap: a test that can't fail reports safety that isn't there.

## Origin
`test-casebook` (MIT, `techmefr/test-casebook`) for the doctrine, plus market long-running agent patterns
for the default-FAIL contract, rewritten. **Aligned with `test-casebook` 1.1.0**, `test-casebook-back-js`
1.0.0 and `test-casebook-back-php` 1.0.0 — all three published on npm at that version. The doctrine is
still only ever "as fresh as the copy installed in the project": a stamp here dates a reading, not the
installed package. Re-verify
against the installed package rather than from memory (`skills/source-freshness`). Stamped 2026-08-11.

The law, the excuses table, the red flags and the break-naming rule (§1) come from the `test-driven-development` and
`writing-good-tests` skills of `superpowers` (MIT, read 2026-10-02), rewritten in our words; the excuses are
predicted, not yet recorded from a run. The end-to-end section (§2) is written from the `e2e-testing` skill of
`ECC` (MIT, same date) and from the documentation of the browser automation tools, keeping only the
driver-neutral rules.
