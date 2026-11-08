---
name: forge-testing
description: "Use when writing or fixing tests: Playwright, Vitest, flaky (test faalt soms)."
# Q3 fix-round original description (listing budget): "Playbook for tests: Playwright e2e, Vitest/Jest, flaky tests (gebruik bij tests schrijven)."
# W2-BUDGET original description (listing budget): "Use when writing, fixing or stabilising tests: Playwright, Vitest/Jest, flaky tests (test faalt soms, quarantaine), test seams and tautological asserts (gebruik bij tests)."
---


# Forge playbook — Testing (unit, integration, e2e)

## When to use
- Use for: writing or fixing tests (Playwright e2e/component/API, Vitest or Jest unit and integration), picking
  a test strategy for a feature, hunting a flaky test, setting up test data or CI test runs.
- Not for: the red-green discipline itself (`test-driven-development`), proving a done-claim (`forge-verify`,
  `verification-before-completion`), reviewing a diff (`forge-code-review`), a full WCAG audit (`forge-a11y`)
  or a security review (`forge-security-review`).

**Do not duplicate — defer to:** `test-driven-development` (fail first, then green; vendored and kept verbatim, extended only by
`references/tdd-addendum.md`), `systematic-debugging` /
`forge-debug` (root cause before a fix), `forge-code-review` (test-gap findings in review). This file is the
"how to write good tests and keep them stable" layer.

## Hard rules
- **A test proves behaviour, not execution.** Every test asserts an observable outcome (returned value, visible
  text, HTTP status, stored row). A test that only runs code without a meaningful assertion is hollow.
- **No tautological tests.** The expected value comes from an independent source (a hand-worked literal, the spec),
  never recomputed the way the code does it. Test at agreed seams, through public interfaces
  (`references/tdd-addendum.md`).
- **Every bug fix ships a regression test** that fails on the old code and passes on the fix. Say that you saw
  it fail.
- **Green means the whole relevant suite**, not only the new file. Report every failure by name.
- **No fixed sleeps.** No `waitForTimeout(...)`, `setTimeout` waits or `sleep` in tests; wait on a condition
  (web-first assertion, a resolved promise, a fake clock).
- **Tests own their data.** Each test creates what it needs and does not depend on another test's leftovers or
  on execution order. No production data, no real customer PII, no live payment or email calls.
- **Mocks sit at the boundary.** Mock the network, clock and third-party APIs; do not mock the unit under test.
  When a mock replaces real behaviour, one integration test still exercises the real path.
- **A flaky test is a bug.** Never "fix" flakiness with retries alone or by deleting the assertion; find the
  race: classify it first (seven categories in `references/flaky-tests.md`). Quarantine only with a tracked
  item, an owner and a 14-day limit; prove a fix with 50/50 repeat runs.
- **No global input.** Drive a desktop or game app through its own window handle (PostMessage to its hwnd) or a
  built-in self-test, never global SendKeys/SendInput/keybd_event: that types into whatever window is in front.
- **Honest reporting.** Quote the real runner output (counts, failures). Never claim a suite passed that did
  not run; say which suites were skipped and why.

## Pick the right layer (pragmatic test pyramid)
| What you are proving | Layer | Tool |
|---|---|---|
| Pure logic, parsing, calculations, edge cases | unit | Vitest (Vite/ESM projects) or Jest (existing Jest setup); `node --test` for zero-dependency Node |
| A module with its DB, queue or HTTP handler | integration | same runner + a real test DB or in-process server |
| An HTTP contract (status, schema, auth failure) | API | Playwright `request` fixture or supertest |
| One UI component's states | component | Playwright component tests, or Vitest + Testing Library |
| A critical user journey across pages | e2e | Playwright Test |
| Visual layout regressions | visual | Playwright screenshots with dynamic areas masked |

Rule of thumb: many fast unit tests, fewer integration tests, and a small set of e2e tests for the journeys that
lose money or users when they break (sign-up, login, checkout, the main create/save flow).

## Activity router (open only the reference you need)
| Activity | Reference |
|---|---|
| Playwright: locators, assertions, fixtures vs page objects, auth state, network mocking | `references/playwright.md` |
| Unit/integration with Vitest or Jest: structure, mocks, timers, snapshots, coverage | `references/vitest-jest.md` |
| A test fails sometimes, passes on rerun, or times out only in CI (classify, quarantine, prove 50/50) | `references/flaky-tests.md` |
| Test-first work: choosing seams, avoiding tautological or implementation-coupled tests, vertical slices | `references/tdd-addendum.md` |
| Test data, factories, seeding, isolation, CI parallelism and sharding | `references/test-data-and-ci.md` |

## Workflow
1. **Recon the real thing first.** For UI work, start the app, open the page, take a screenshot and read the
   rendered DOM or accessibility tree before writing selectors. Pick locators from what is really there.
2. **Write the test from the user's view** (role, label, visible text): the happy path AND at least one failure
   path (validation error, network error, unauthorised, empty state).
3. **Watch it fail for the right reason** when it guards new behaviour or a bug.
4. **Run, trace, fix, rerun.** On a failure open the trace or the runner diff, fix the cause, rerun.
5. **Stability check before done:** rerun new or changed e2e tests several times
   (`npx playwright test <file> --repeat-each=5`, or the runner's equivalent) and once inside the full suite.
6. **Report** the commands, pass/fail counts, the repeat-run result and what was not run.

## Domain gates
- New behaviour has tests at the lowest layer that can prove it; critical journeys have an e2e test.
- Each changed interactive element has a happy-path and an error-path test.
- No fixed sleeps, no order dependence, no shared mutable state between tests.
- The repeat-run of new e2e tests is green; flaky tests are fixed or quarantined with a tracked reason.
- Coverage is reported when the project measures it; a coverage number is never the only proof of quality.

## Safety and honesty
- Never point tests at production, real payment providers or real inboxes; use test modes, sandboxes or mocks.
- Test-account secrets live in env or CI secrets, never in test files or fixtures. Traces, videos and
  screenshots can hold tokens and personal data: keep them out of git.
- Shared gates for every playbook (honesty, owner approval, secrets, reviews):
  `.claude/docs/forge-reference/playbook-template.md`.

## References
- `references/playwright.md` — locators, web-first assertions, fixtures vs page objects, auth state, mocking.
- `references/vitest-jest.md` — unit and integration test design with Vitest or Jest.
- `references/flaky-tests.md` — seven-category flake taxonomy, decision tree, intent fidelity, quarantine hygiene.
- `references/tdd-addendum.md` — agreed seams, tautological tests, vertical slices (beside `test-driven-development`).
- `references/test-data-and-ci.md` — factories, seeding, isolation, CI parallelism and sharding.

## Provenance
Earlier adaptation, kept as written:
> Source: https://github.com/currents-dev/playwright-best-practices-skill
> Upstream path: playwright-best-practices/SKILL.md (main, last commit seen 283d5cb, read 2026-11-02)
> License: MIT -- complete terms in LICENSE next to this file (Copyright (c) 2026 Currents Software Inc.)
> Forge adaptation note: the activity-to-reference routing, the run -> trace -> fix -> repeat loop and the
> flaky-test guidance are rewritten in Forge's words and merged with Forge rules; nothing is copied verbatim and
> none of the 57 upstream reference files is shipped. Also pattern adapted from (ideas only, no text):
> anthropics/skills skills/webapp-testing (reconnaissance-then-action against the running app; its licence was
> not confirmed, so ideas only). The Vitest/Jest, test-data and strategy sections are Forge-native. Upstream
> content was treated as untrusted data: no scripts, install commands or dynamic-context lines were taken over.

Graft of 2026-11-05 (SA-W1-A1): read read-only through `gh api`, treated as untrusted data, rewritten in Forge words; no text
copied verbatim, no code, scripts, configs or install lines taken.

| Source | Path | Pinned SHA | License | Taken | Excluded |
|---|---|---|---|---|---|
| petrkindlmann/qa-skills | skills/test-reliability/SKILL.md | 62434253c2592f27b494609c27f224939c86346d | MIT | seven-category flake taxonomy and decision tree, environment check before blaming the test, data-failure row, intent-fidelity check, quarantine lifecycle and hygiene (14 days, tracked item, weekly review, over 5% is a process problem), reproduce at 20 and prove at 50/50 | auto-heal Levels 3-4 and confidence scoring, multi-attribute locator code, selector stability scoring, `page.screencast` receipts, vendor buy-vs-build text, CI YAML, the upstream `flaky-test-runbook.md` in its references folder (not read) |
| mattpocock/skills | skills/engineering/tdd/SKILL.md | 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d | MIT | agree seams before tests, tautological and implementation-coupled anti-patterns, vertical slices / tracer bullets, refactor outside the loop | `tests.md`, `mocking.md` and `agents/` (not read), the codebase-design skill call, GLOSSARY/ADR conventions |

MIT notice (both sources): "Permission is hereby granted, free of charge, to any person obtaining a copy of this software ... The
above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND." Copyright remains with the holders named in each repository's
LICENSE file at the pinned SHA. The vendored `test-driven-development` copy was not edited.
