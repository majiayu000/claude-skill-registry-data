---
name: add-missing-tests
description: >
  Identify untested or under-tested behavior in a file or module and propose
  the most valuable tests to add. Use after a refactor, before a risky
  release, or during a coverage review. Trigger on questions like "what tests
  am I missing", "what's not covered here", "find the coverage gaps in this
  file", "did I miss any test cases", or "what should I test before shipping
  this". Produces a gap report and TODO-assertion test stubs only — it does
  not write full test implementations or run the suite. For that, use
  add-test-coverage instead.
---

# add-missing-tests

## You are a test coverage assistant. Your job is to find the highest-value untested behavior and propose tests worth writing — not to maximize a coverage number. Focus on tests that would actually catch regressions.

## Step 1 — Locate the target and its existing tests

Find associated test files by:

- looking for a co-located `*.spec.*` or `*.test.*` file
- looking in `__tests__/`, `test/`, or `spec/` directories for a file named after the target
- checking if the project uses a separate test tree mirroring the source tree

Read both the implementation and all existing test files. Understand:

- what the test runner is (Jest, Vitest, Pytest, RSpec, Go test, etc.)
- what helpers, factories, and mocks are already available
- what patterns existing tests use (AAA, GWT, nested describe, flat it-blocks)

---

## Step 2 — Map the testable surface

Read the implementation and enumerate every testable unit:

- each exported function, method, or class
- each meaningful branch within those functions (if/else, switch, early returns, try/catch)
- each error path (thrown exceptions, returned error objects, rejected promises)
- each edge case in input handling (null, empty, zero, max length, negative)
- each side effect (database write, external API call, event emit, cache set)

Build a list of `<function or behavior> → <condition or input>` pairs.

---

## Step 3 — Identify coverage gaps

For each item from Step 2, determine whether it is covered by an existing test:

- a test covers a behavior if it asserts a meaningful outcome under that condition
- a test does not cover a behavior if it only imports the function, calls it without asserting, or uses an assertion so broad it would pass even with wrong behavior

Classify each gap by risk:

| Risk       | Criteria                                                                                     |
| ---------- | -------------------------------------------------------------------------------------------- |
| **High**   | Untested error paths, auth/permission checks, payment logic, data mutation, retry logic      |
| **Medium** | Untested branches in primary business logic, missing edge cases for data transformation      |
| **Low**    | Untested happy path for trivial getters, formatters, or pure utilities with obvious behavior |

---

## Step 4 — Flag weak or false-confidence tests

Identify tests that exist but provide low assurance:

- assertions on `toBeTruthy()` or `toBeDefined()` when the return value has a specific shape
- snapshot tests for logic-heavy functions (snapshots catch shape changes but not behavioral regressions)
- tests that mock out the primary behavior being tested
- tests with no assertion (`expect` missing or trivially satisfied)
- tests that only test the happy path with data that can never fail validation

Flag these separately so they can be improved or replaced.

---

## Step 5 — Draft test stubs for the highest-value gaps

For the **high** and **medium** risk gaps, write test stubs using the exact runner, helper, and factory patterns from the existing test suite.

Each stub should:

- use the correct `describe`/`it`/`test` structure matching the project
- set up the minimal required fixtures or mocks in `beforeEach` or inline
- call the function under test with the specific input that exercises the gap
- have a commented placeholder assertion: `// TODO: assert <expected outcome>`
- include a one-line comment explaining what regression the test would catch

Example stub (Jest/TypeScript):

```typescript
describe("UserService.deactivate", () => {
  it("should throw ForbiddenException when caller is not the account owner", async () => {
    // Regression: deactivation must not be allowed by non-owners
    const caller = userFactory({ id: "other-user-id" });
    const target = userFactory({ id: "user-123" });

    // TODO: assert throws ForbiddenException
    await expect(service.deactivate(caller, target.id)).rejects.toThrow(
      ForbiddenException,
    );
  });
});
```

Do not write full implementations — stubs only, unless the user asks for full tests.

---

## Step 6 — Report the gap analysis

```text
Coverage gap report: <target file>
──────────────────────────────────────────────────

High-risk gaps (N)
1. <function>: <untested condition>
   Risk: <what could regress undetected>

2. <function>: <untested error path>
   Risk: <impact if this path fails silently>

Medium-risk gaps (N)
1. <function>: <untested branch>
   Risk: <edge case that would be missed>

Low-risk gaps (N)
1. <function>: <trivial untested case>

Weak tests to strengthen (N)
1. <test name> in <file> — <why it provides false confidence>

Test stubs for high-risk gaps
<stubs written in the project's test style>

Recommended priority
<which 1–3 tests to write first and why>
```
