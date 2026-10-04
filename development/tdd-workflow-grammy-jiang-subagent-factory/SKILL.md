---
name: tdd-workflow
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P039
  - P016
  - P015
  - P049
  - P071
  - P026
  claims:
  - C00250
  - C00252
  - C00254
  - C00269
  - C00270
  - C00271
  evidence:
  - E00206
  - E00207
  - E00209
  - E00217
  - E00218
  - E00219
  source_anchors:
  - e5bd744baa21-c0000
  - e5bd744baa21-c0001
  - e5bd744baa21-c0002
  - 8cdadfe35329-c0000
  - 8cdadfe35329-c0001
  - 8cdadfe35329-c0004
  authored_from_digest: 98a05befb13720eb6e8cd3ce8e6d8a2ccd1e476662ff54764ee7bbb5183d9e38
---

# Skill: tdd-workflow

## Purpose

Guide a developer through outside-in, test-first development: turn a described behaviour into the
next expected-failing test, make the smallest change that moves the failure forward, and refactor
only under passing tests, committing in small tested milestones. Grounded in principles P003, P039,
P016, P015, P049, P071, P026.

## When to use

- The caller wants to build a feature test-first rather than writing code then tests.
- A design change is large and needs to be broken into safe, working-state steps.
- The caller is unsure what to do next and needs the current failure to choose the move.

## Procedure

1. **Start from a user-level expectation.** Write a functional/acceptance test that expresses the
   behaviour a user should see and let it drive the work outside-in; use functional tests for
   user-visible behaviour and wiring confidence, and unit tests for implementation details and edge
   cases (P026).
2. **Remember why you test.** Without tests you cannot know the software works, and writing tests
   before or during implementation shapes the code toward a modular, maintainable structure (P039).
3. **Let the current failure choose the smallest next move.** Read the current expected failure and
   make the single smallest code change that moves it forward, repeating until the user-level
   behaviour passes; avoid speculative features not demanded by a failing test (P003, P016).
4. **Work working-state to working-state.** Change broad designs through controlled steps that each
   leave the suite green, rather than a big rewrite, using the current expected failure to pick one
   narrow next move (P016).
5. **Refactor only under green.** Refactor only when tests pass, do not mix new behaviour into a
   refactor, and commit the completed structural change as its own milestone (P015).
6. **Commit in small, reviewable steps.** Inspect status and diffs, separate substantial
   functional-test specification changes from implementation, and commit at coherent tested
   milestones (P049).
7. **Test even simple behaviour while learning.** While building the TDD habit, write tests for even
   simple behaviour so tests are already present when complexity grows (P071).

## Inputs

- The behaviour or feature the caller wants to build.
- The current test suite state (what passes, what the next failure is).
- The application framework context (e.g. Django/Selenium) when relevant.

## Output

The next expected-failing test to write, the smallest change that should make it pass, and the
refactor/commit step — each tied to a principle id.

## References

- `references/pytest-cli-and-config.md` — run-control (`-x`, `--lf`) that supports fast cycles.

## Provenance

Derived from principles P003, P039, P016, P015, P049, P071, P026 and their evidence records over
*Test-Driven Development with Python* (source `tdd-with-python-perc-e5bd744b`) and *Testing In
Python* (source `testing-in-python-ro-8cdadfe3`). Distillation-only sources: paraphrased, no
verbatim quotation.
