---
name: swift-testing
description: "Use when Swift tests are written, migrated or reviewed and the risk is a test that passes while asserting nothing, hangs, or fails only in parallel: XCTest assertions inside Swift Testing tests or #expect inside an XCTestCase (cross-library issues and the interoperability mode), migrating an XCTestCase to a suite, setUp and tearDown versus init and deinit, #expect versus #require and why a pre-evaluated Boolean gives an empty failure, testing errors and optionals, async tests with await, confirmation and its expected count, wait(for:) versus fulfillment(of:) in async XCTest code, completion handlers bridged with a continuation, time limits, injected clocks instead of sleeps, tests that run in parallel in one process and share state, the serialized trait, main-actor isolation of test functions, and leak checks."
---

# swift-testing

Step 6 and step 7 of the pipeline (`WORKFLOW.md`), for the Swift test failures that are silent: a suite that is green
because its assertions were ignored, a test that hangs CI, a flake that appears only when tests run in parallel.
The four sections share one premise: **Swift Testing and XCTest are two frameworks with different execution models
(parallel in one process against sequential in a suite, an arbitrary task against the main actor), so a test is only
as trustworthy as its mapping to one of them, and the mapping has to be explicit**. What to test, how many tests,
mocking style and snapshot or UI testing are out of scope; `testing-anti-patterns` carries the general rules.

## When
- Writing a new Swift test, or migrating an XCTest class to Swift Testing.
- A test passes but a failure was expected, or fails only on CI or only with parallel execution on.
- A test waits for a callback, an event, a delegate or the clock.
- Reviewing a test file that imports both `XCTest` and `Testing`.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Two frameworks in one target: cross-library issues, the interoperability mode by toolchain, migrating a class to a suite, setup and teardown | a file or target uses both frameworks, or a class is migrated | [`01-two-frameworks.md`](./references/01-two-frameworks.md) |
| 2 | Expectations: `#expect` and `#require`, the expression the macro captures, errors, optionals, known issues | an assertion is written, or a failure message says nothing | [`02-expectations.md`](./references/02-expectations.md) |
| 3 | Asynchronous code and time: `await`, confirmations, `fulfillment(of:)`, continuations, time limits, injected clocks | a test waits for anything | [`03-async-and-time.md`](./references/03-async-and-time.md) |
| 4 | Parallelism and isolation: shared state, the serialized trait, main-actor tests, suite types, leak checks | a test is flaky, touches shared state, or a main-actor model is tested | [`04-parallelism-and-isolation.md`](./references/04-parallelism-and-isolation.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a deliberately failing assertion of each kind was run and the test
went red (§1, §2), the suite was run with parallel testing on and then repeated several times with the order
shuffled (§4), an async test with a callback was driven so that the callback fires after, and then never, and both
cases failed or passed as intended (§3), and the toolchain and package tools version were read to know which
interoperability mode was in force (§1). A test that was only read, or that was never seen failing, is not
verified.

## Guardrails
- Never leave an XCTest assertion inside a Swift Testing test, or `#expect` inside an `XCTestCase`, without knowing
  the interoperability mode in force (§1.1).
- Never pass a pre-evaluated Boolean to `#expect` (§2.2).
- Never call the blocking `wait(for:)` in an async XCTest method (§3.2).
- Never expect a confirmation to wait: it is checked when its closure returns (§3.1).
- Never use `.serialized` as the fix for shared state; it is a stopgap (§4.2).
- This block states Swift Testing and XCTest behaviour as of the Apple documentation pages read on the date in
  [`references/origin.md`](./references/origin.md); the toolchain thresholds are those pages' own. Nothing was
  compiled or run while writing it.
- Changing the toolchain, the package tools version or the interoperability environment variable on CI is the
  user's step; this block names it and stops.

## Origin
Rewritten from the Apple documentation pages for Swift Testing (migrating from XCTest, expectations,
asynchronous code, confirmations, parallelisation) and XCTest expectations, and one MIT-licensed iOS testing skill
for the points the pages do not state (read 2026-10-08). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). Overlaps with `skills/swift-conventions` (2026-10-19); cross-referenced, not merged.
