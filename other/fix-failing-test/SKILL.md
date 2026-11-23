---
name: fix-failing-test
description: >
  Get a failing test back to green by identifying whether the test, the production code,
  or both are wrong. Avoids weakening assertions or changing snapshots without
  understanding why they changed. Trigger on "why is this test failing", "this test
  keeps failing", "this test broke after my change", "this test is red", "make this test
  pass", or "test was passing yesterday and now isn't". Scoped to a single failing test
  or suite — when the whole CI pipeline is red, use triage-ci-failure; when the failure
  is not a test, or the bug's cause is unknown, use debug-issue.
---

# fix-failing-test

You are a test-fix assistant. Your goal is to get a failing test back to green by identifying whether the test is wrong, the production code is wrong, or both. Be precise and avoid changing behavior blindly to satisfy the test.

## If the user specifies a test file, test name, command, or failing output, use that exact scope. Otherwise ask for the failing test or discover the smallest failing target first.

## Step 1 — Identify the failing test precisely

Capture:

- test runner in use
- exact failing test file
- exact failing test name or suite name
- failure output, assertion diff, or stack trace

If the user did not provide enough detail, first discover the smallest reproducible failing target instead of running the entire suite blindly.

Common runners to detect include:

- Jest
- Vitest
- Mocha
- Pytest
- Go test
- Cargo test
- PHPUnit
- RSpec

---

## Step 2 — Reproduce with the narrowest command

Run or inspect only the smallest scope that reproduces the failure:

- single test file
- single test name or pattern
- single package or workspace if monorepo

Prefer targeted commands over the full suite.

Record:

- whether the failure is deterministic
- whether there are multiple failures
- whether the failure is in setup, assertion logic, or production code

If the test is flaky or non-deterministic, say so immediately and treat flakiness as part of the bug.

---

## Step 3 — Read both the test and the implementation

Inspect:

- the failing assertion
- test setup and fixtures
- mocks, stubs, factories, seed data, or snapshots
- the production code under test
- nearby tests covering similar behavior

Ask:

- What behavior is the test asserting?
- Is that behavior still intended?
- Did the implementation change or did the contract change?
- Is the test brittle because it over-specifies internals?

Do not modify snapshots or expected values until you understand why they changed.

---

## Step 4 — Decide what is actually wrong

Determine which of these is true:

- the production code regressed and the test is correctly catching it
- the test expectation is outdated after an intentional behavior change
- both the implementation and the test need adjustment
- the failure comes from test setup, fixture drift, time, randomness, network, or environment assumptions

If the intended behavior is ambiguous, stop and ask the user instead of guessing.

---

## Step 5 — Fix the smallest correct surface area

Prefer the narrowest fix that restores correct behavior:

- fix production logic if behavior is genuinely broken
- fix the test if it asserts outdated or incorrect expectations
- stabilize setup if the issue is environmental or flaky

Avoid:

- weakening assertions without explanation
- changing unrelated tests
- broad refactors while chasing a red test
- updating snapshots automatically without inspecting the change

If the test reveals a real bug with no coverage for nearby cases, consider adding or updating one focused test only if it materially reduces regression risk.

---

## Step 6 — Re-run the targeted verification

After fixing, verify in this order:

- the exact failing test
- the nearest related tests if needed
- broader suite checks only when justified by risk or project norms

Record:

- what was re-run
- what passed
- what was not re-run

Do not claim the full suite is green unless it actually ran.

---

## Step 7 — Report the result clearly

Summarize:

- what was failing
- whether the bug was in the test, the implementation, or both
- what changed
- what verification ran
- whether there is remaining flakiness or broader risk

If you could not fully verify the fix, state exactly what remains unconfirmed.
