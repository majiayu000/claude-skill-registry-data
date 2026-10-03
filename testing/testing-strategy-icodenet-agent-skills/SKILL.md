---
name: testing-strategy
description: >-
  Designs test coverage plans and verification gates. Use when writing tests,
  planning coverage, asking how to test a change, or designing a test plan
  before implementation. Do not use for red-green-refactor implementation loops
  (use tdd) or stop-the-line failure triage (use debug).
---

# Testing Strategy

Pick the smallest layer that catches the risk. Encode gates before coding.

## Workflow

1. **Name the risk** — what breaks for users or contracts if this change is wrong?
2. **Choose layer** — unit → component → integration → e2e → mutation/property. Prefer the lowest layer that would have caught the bug. See `references/layer-matrix.md`.
3. **Write the plan** — for each behavior: test name, command, pass/fail check.
4. **Regression first for bugs** — failing test before fix.
5. **Feature/bug sign-off** — include behavior verification beyond smoke (targeted e2e or exploratory checklist with expected outcomes).
6. **Strengthen** — mutation, property, or contract tests when logic is high-risk or shared.

## Constraints

- Prefer the project's package scripts; do not invent ad-hoc runners or silence output.
- Smoke-only green is not enough to claim “fixed” or “delivered” when user-visible behavior changed.
- Prefer behavior assertions over implementation-detail tests.

## Verification

- [ ] Each planned behavior has a named test + command
- [ ] Layer choice justified (not “e2e for everything”)
- [ ] Sign-off gates listed for the change type
- [ ] Blockers stated if a gate cannot run
