---
name: test-design
description: "Design the test matrix and hard edge cases for a feature before writing tests: equivalence/boundary/decision-table/state/pairwise, data-type and systemic edge-case checklists, property-based tests. Feeds tdd."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (ISTQB-style derivation, Meszaros test doubles, Pact, property-based and mutation-testing practice). Checklists in references/."
---

# test-design

Turn a feature into a prioritized list of test cases, including the edge cases most features miss, then hand them to the `tdd` skill to write. This chooses *what* to test; `tdd` writes it and `qa` drives the browser. Finding the bug cheaply is the goal, not maximizing case count.

## Procedure

1. **Restate the behavior** as testable statements: explicit requirements, implicit invariants ("balance never negative"), and acceptance criteria.
2. **Name inputs, outputs, state, side effects, limits.**
3. **Derive cases** with the fitting technique (see `references/techniques.md`):
   - ranges/inputs → equivalence partitioning + **boundary value analysis** (the highest-yield one: test `min-1, min, min+1, max-1, max, max+1`)
   - combinational rules → decision table
   - stateful feature → state-transition, including **illegal** transitions
   - many parameters → pairwise
4. **Run the checklists** over each input and over the architecture: `references/edge-cases.md` (strings, numbers, collections, dates/time, money, IDs/auth) and the systemic list (concurrency, idempotency/retries, ordering, partial failure, network, resource exhaustion, pagination, caching, compatibility, i18n). Keep only what applies to this feature.
5. **Pick the highest-value cases**: one per equivalence class, every boundary, every rejected/illegal case, and the top systemic risks for this feature. Collapse redundant combinations (pairwise). Where a round-trip or invariant exists, prefer one property-based test over many examples (`references/property-and-coverage.md`).
6. **Assign level and doubles** per case (`references/levels-and-doubles.md`): the lowest level that still catches the bug; real deps or fakes for code you own, mocks only for external/slow/nondeterministic things. When a case has no clean seam and would need mocks of code you own, name the missing seam and point to `/honey:architecture` for a behavior-preserving refactor instead of mocking around it; mark cases that need a controlled clock or seeded randomness; flag UI/accessibility cases for `qa`.
7. **Hand to `tdd`** as an ordered list — each case: name, level, inputs, expected result/assertion, doubles needed — starting from the simplest failing happy path.

## Two rules that matter most
- **Test the rejected and illegal cases, not just the happy path.** Most real bugs live there. Never fold two invalid inputs into one case; they mask each other.
- **Line coverage is not quality.** It proves a line ran, not that anything checked it. On critical logic, judge the suite with **mutation testing** (Stryker / mutmut / PITest): a surviving mutant is a bug your tests would miss. Treat line/branch coverage only as a floor that finds untested code.

## Worked examples
`references/worked-examples.md` carries two end-to-end case lists — "transfer money between accounts" (concurrency, idempotency, partial-failure rollback, money conservation) and "paginated search" (empty/last/beyond-end pages, cursor invalidated mid-scan) — as templates.

Done when: every behavior, boundary, rejected input, and applicable systemic risk has a listed case with a level and expected result, and the list is handed to `tdd`.
