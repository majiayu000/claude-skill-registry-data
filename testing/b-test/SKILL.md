---
name: b-test
description: >
  Test-driven development, test debugging, and test coverage evaluation.
  Use for writing tests, fixing failing tests, evaluating coverage, or
  working TDD-style. Unlike b-debug, which traces runtime bugs, b-test
  owns test-specific failures and simulated-DOM/component-test work: wrong
  assertions, missing mocks, fixture or setup issues, and coverage gaps.
  Real-browser, visual, browser-session, and e2e verification belongs to
  b-browser. Routing signals: tests, coverage, failing test, snapshot,
  mock, component test, jsdom, happy-dom, React Testing Library.
metadata:
  phase: Validate
  execution_mode: main
---

<!-- Generated from skills/registry.yaml and skills/b-test/prompt.md. Edit those sources, not this file. -->

# b-test

Own code-level and simulated-DOM tests: add coverage, fix test-only failures, and avoid confusing red tests with product bugs.

## When to use

- The user asks to write tests, fix failing tests, evaluate coverage, or work TDD-style.
- The issue is assertion, mock, fixture, setup, snapshot, or test coverage.
- Non-browser unit, integration, contract, simulated-DOM, and component tests are in scope.

## When NOT to use

- The failing test likely exposes product behavior -> use **b-debug**.
- Real browser, visual, session, or e2e evidence is needed -> use **b-browser**.
- Intended behavior is unclear -> use **b-plan** or **b-debug**.
- A new test framework is needed -> use **b-plan** first.

## Tool guidance

- `bash` - run tests via `rtk` when supported (`rtk pytest`, `rtk vitest`, `rtk jest`, …) and inspect failure output.

- `read`/`edit` - use native tools for routine and unsupported file work.
- `codegraph` - per the kernel CodeGraph rule, ask for changed-symbol/file impact and affected tests in an indexed project; report an absent or stale index as a gap and never initialize one.
- `context7` - versioned test-framework/API semantics only when local tests and contracts do not settle them.

## Steps

1. Find the test framework and narrowest runnable command from manifests, CI, or existing tests (using Bash). Use native inspection and test discovery for the runner; use CodeGraph for source-to-test impact when an index is available.
2. Confirm intended behavior from user intent, product contract, source change, existing passing tests, and materially relevant repo context. Use Context7 only for unresolved versioned framework semantics: one bounded lookup (resolve once, query once) inside this skill; a broader or user-requested external question goes to **b-research**.
3. For failing tests, run the narrow target, read the test and exercised source, edit tests only after classifying the failure.
4. For new tests, cover requested or changed behavior through the highest practical public interface first; add edge cases only when risk requires them.
5. For explicitly requested TDD, use vertical tracer bullets: add one failing behavior test, make the smallest production change needed to pass it, verify, then continue to the next behavior. Outside explicit TDD, route frontend/UI production changes to **b-frontend** and other production changes to **b-implement**.
6. Select affected tests before broad suites: ask an available CodeGraph index for changed-symbol/file impact and affected tests; without an index, or on a staleness notice, use local search, test discovery, and repository scripts and disclose the limitation. Do not initialize an index. Run the narrow affected set first, then expand only when the change or risk requires it.
7. Report the selected tests, whether CodeGraph or fallback discovery supplied them, and any remaining coverage gap. A partial or affected-only run must never be described as full-suite coverage.
8. Run diagnostics when useful, then the narrowest relevant test, and verify the test proves the intended behavior.

## Output format

Test scope, changes, verification, and remaining gaps.

## Rules

- Never change production code only because a test is red.
- When an edit anchor (oldText) fails to match, re-read the target region and re-anchor the edit from current content; never blind-retry the same anchor or widen context speculatively.
- Keep production-code changes in **b-implement** unless they are frontend/UI changes, which belong to **b-frontend**, or the user explicitly requested a tightly scoped TDD red-green loop.
- Never update assertions, snapshots, or goldens without confirming intended behavior. If the intended contract is materially unresolved, use `ask_user_question` with 2–4 concrete intent options (for example, keep the current expectation, adopt the changed behavior, or defer the test change); if unavailable or noninteractive, ask one focused plain-text question. Do not use the question tool for routine test-result updates or no-choice confirmations.
- Avoid implementation-coupled tests and mocks derived from buggy implementation instead of the real interface.
- Do not introduce frameworks without approval.
- Keep fixture and mock changes local when practical.
