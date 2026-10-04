---
name: access-control-safety-testing
description: >-
  Use when writing or reviewing the must-fail fixture for a gate that bans direct role or permission
  membership checks — an ESLint `no-restricted-syntax` selector, a dependency-cruiser rule, or a
  hand-rolled permission validator. Symptoms include a fixture that seeds only `.includes()`, a role
  check that slipped past a gate with a passing test, and a membership ban resolved at `warn`, which
  never fails a lint run.
---

# Access Control Safety Testing

## Profile keys consumed

- `make.lint_eslint`
- `make.lint_deps`
- `make.lint`
- `make.test_unit_client`

Every gate invocation goes through the profile's `make` target map. A `null` value for one of these
keys means the capability is absent in this repository: skip the dependent step with a recorded
note instead of improvising a raw host command.

## Overview

A gate that forbids reading a principal's roles directly is only as strong as the fixture proving it
fires. JavaScript offers at least fourteen ways to ask "is this role in this array"; a fixture built
around `.includes()` leaves the other thirteen enforced by nothing, which is worse than no gate
because it manufactures confidence.

## When to use

- Adding or reviewing a lint selector that bans direct `roles` / `permissions` array access.
- Writing the must-fail fixture that pins such a selector, or auditing an existing one.
- A reviewer reports that a role check "slipped past" a gate that has a passing test.
- Choosing between a regex or AST selector for a membership-check ban.
- Not for: gates unrelated to membership checks, or runtime authorization on a server — this is
  about static enforcement of a client-side convention, which is never the authorization boundary.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — the rules themselves run under the targets mapped by `make.lint_eslint` /
  `make.lint_deps`, and the must-fail fixture harnesses that pin them
  (`scripts/ci/eslint-gate-fixtures.mjs` with `tests/unit/tooling/eslint-gate-fixtures.test.ts`,
  `scripts/ci/depcruise-rule-fixtures.mjs` with `tests/unit/tooling/depcruise-rules.test.ts`) run in
  the unit suite mapped by `make.test_unit_client`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — the same
  `no-restricted-syntax` and dependency-cruiser gates run under the targets mapped by `make.lint` /
  `make.lint_deps`, but there is no fixture rot-guard harness, so the fixture and its assertions
  have to be written alongside the rule.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  `eslint.config.mjs` and `.dependency-cruiser.js` carry the same rule kinds under the targets
  mapped by `make.lint` / `make.lint_deps`; again no fixture harness ships with the repository.

## The fourteen spellings

Every one of these has to appear in the fixture and be rejected:

1. `roles.includes(ROLES.admin)`
2. `roles.some((r) => r === ROLES.admin)`
3. `roles.every((r) => r === ROLES.admin)`
4. `roles.find((r) => r === ROLES.admin)`
5. `roles.findIndex((r) => r === ROLES.admin) !== -1`
6. `roles.findLast((r) => r === ROLES.admin) !== undefined`
7. `roles.findLastIndex((r) => r === ROLES.admin) !== -1`
8. `roles.indexOf(ROLES.admin) !== -1`
9. `roles.lastIndexOf(ROLES.admin) !== -1`
10. `roles.filter((r) => r === ROLES.admin).length > 0`
11. `roles.at(0) === ROLES.admin`
12. `roles[0] === ROLES.admin`
13. `new Set(roles).has(ROLES.admin)`
14. `roles[0] === 'admin'` — the hardcoded literal, which no token-based selector catches

`findLast`, `findLastIndex` and `lastIndexOf` are the three most often missed; they are ordinary
`Array.prototype` members and read exactly like their forward counterparts.

## Procedure

1. Write the selector against the AST, not the raw file text. A regex over source cannot tell an
   executable call from the same characters inside a comment or a string literal, so it either fails
   open or fires on prose.
2. Put all fourteen spellings in one fixture file and run it through the real resolved config, the
   way the rule runs in CI — the targets mapped by `make.lint_eslint` / `make.lint_deps`, and the
   fixture harness under `make.test_unit_client` — not through a hand-built config object that may
   not match.
3. Assert the finding count equals the number of seeded violations, so an over-broad selector that
   also flags unrelated lines is visible.
4. Assert the resolved **severity** is `error`. A downgrade to `warn` never fails a lint run, so the
   gate keeps reporting while enforcing nothing, and no fixture that only checks "a finding exists"
   notices.
5. Keep the selector comment, the fixture, and the documentation of the banned list as one stated
   three-way contract; when a spelling is added, all three change together.

## Common mistakes

- Fixture covers `.includes()` only — seed all fourteen spellings in the same file.
- Fixture asserts "at least one finding" — assert the exact count so over-broad selectors surface.
- Rule left at `warn` — resolve the severity in the test and assert it is `error`.
- Regex over source text — an AST selector is the only way to skip comments and string literals.
- Banned list documented in one place only — the selector, the fixture, and the docs drift apart.
- Treating the passing gate as authorization — it is a convention gate; the upstream API service
  still has to reject an unauthorized request.
