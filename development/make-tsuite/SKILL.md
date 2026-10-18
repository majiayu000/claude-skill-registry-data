---
name: make-tsuite
description: Audit an automated software test portfolio for signal, overlap, ownership, and placement, or implement test-only suite cleanup and coverage. Use for suite evaluation, redundant-test removal, test reorganization, or adding automated tests without changing production behavior; use tdd for production behavior changes.
---

# Make TSuite

Build a risk-driven automated software test portfolio. `TSuite` means test suite, not TypeScript; apply this skill across languages, frameworks, toolchains, and repository layouts.

## Boundary

Production-reachable content is immutable. Writable scope is limited to automated tests and test-scoped fixtures, harnesses, seeds, artifacts, configuration, and dependencies. Inline tests or shared manifests are writable only where changed regions are mechanically isolated to test compilation or execution. Ambiguous isolation is a blocker. Report the uncertainty and required scope decision before editing.

Before editing, classify every allowed path or hunk as test-scoped. After editing, inspect the complete source-control diff; completion requires every changed region and dependency to remain unreachable from production behavior, artifacts, and deployable wiring.

Keep a product defect visible as a failing test with observed failure evidence, then report a separate production requirement. A test-only task reaches GREEN only through test-scoped changes.

## Modes

- **Audit:** inspect and report; make no changes. Match the output to the request: a cleanup audit returns removable groups, while a portfolio evaluation includes all dispositions.
- **Implement:** create, strengthen, move, merge, or remove tests only when the user authorized changes.

Mode selection is complete when one mode is named and writable scope is explicit.

## Establish authority

Read repository and scoped instructions, then inspect relevant tests, fixtures, owned public seams, and their execution mechanism. Where present, inspect discovery or selection configuration and required delivery gates. Consult history or design records only when current files do not explain an important convention.

Authority discovery is complete when every test package in scope has an identified behavior owner, public or owned seam, execution and selection path, applicable repository rule, and required delivery gate when one exists.

## Semantic lock

Before changing an existing test, record its semantic fingerprint:

- capability and current behavior;
- public or owned seam;
- actor, authority, and isolation boundary;
- material setup, input, and fixture state;
- observable result or typed failure;
- side effect, absence of side effect, or recovery invariant.

A test transformation is equivalent only when the same behavior still passes and the same regression still fails. A changed actor, authority, input class, seam, outcome, or side effect is a new test decision.

Semantic lock is complete when every changed case maps its before-and-after fingerprint with no unexplained material difference.

## Route by work

- For inventory, signal classification, overlap, or removal, read [audit-portfolio.md](references/audit-portfolio.md).
- For authorized test changes, read [implement-suite.md](references/implement-suite.md).
- For routes, APIs, messages, commands, or protocol scenarios, also read [route-api-design.md](references/route-api-design.md).
- For browser, mobile, desktop, or other user journeys, also read [user-journey-design.md](references/user-journey-design.md).

## Report

Separate observed facts from recommendations. Report execution failures as blockers, never passes.

An audit report is complete when each requested finding names the cohesive test group, disposition, protected or absent invariant, and evidence. An implementation report is complete when it includes changed and retained proof, semantic-lock results, execution invocation when available and observed results, unresolved product defects, and production-immutability proof for every changed region.
