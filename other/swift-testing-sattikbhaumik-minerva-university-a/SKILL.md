---
name: swift-testing
description: "Writes and migrates tests using the Swift Testing framework with @Test, @Suite, #expect, #require, confirmation, parameterized tests, test tags, traits, withKnownIssue, XCTest UI testing, XCUITest, test plan, mocking, test doubles, testable architecture, snapshot testing, async test patterns, test organization, and test-driven development in Swift. Use when writing or migrating tests with Swift Testing framework, implementing parameterized tests, working with test traits, converting XCTest to Swift Testing, or setting up test organization and mocking patterns."
---

# Swift Testing

Swift Testing is the modern testing framework for Swift (Xcode 16+, Swift 6+). Prefer it over XCTest for all new unit tests. Use XCTest only for UI tests, performance benchmarks, and snapshot tests.

## Contents

- [Basic Tests](#basic-tests)
- [@Test Traits](#test-traits)
- [#expect and #require](#expect-and-require)
- [@Suite and Test Organization](#suite-and-test-organization)
- [Execution Model](#execution-model)
- [Known Issues](#known-issues)
- [Additional Patterns](#additional-patterns)
- [Common Mistakes](#common-mistakes)
- [Test Attachments](#test-attachments)
- [Exit Testing](#exit-testing)
- [Review Checklist](#review-checklist)
- [References](#references)

---

## Basic Tests

```swift
import Testing

@Test("User can update their display name")
func updateDisplayName() {
    var user = User(name: "Alice")
    user.name = "Bob"
    #expect(user.name == "Bob")
}
```

## @Test Traits

```swift
@Test("Validates email format")                                    // display name
@Test(.tags(.validation, .email))                                  // tags
@Test(.disabled("Server migration in progress"))                   // disabled
@Test(.enabled(if: ProcessInfo.processInfo.environment["CI"] != nil)) // conditional
@Test(.bug("https://github.com/org/repo/issues/42"))               // bug reference
@Test(.timeLimit(.minutes(1)))                                     // time limit
@Test("Timeout handling", .tags(.networking), .timeLimit(.seconds(30))) // combined
```

## #expect and #require

```swift
// #expect records failure but continues execution
#expect(result == 42)
#expect(name.isEmpty == false)
#expect(items.count > 0, "Items should not be empty")

// #expect with error type checking
#expect(throws: ValidationError.self) {
    try validate(email: "not-an-email")
}

// #expect with specific error value
#expect {
    try validate(email: "")
} throws: { error in
    guard let err = error as? ValidationError else { return false }
    return err == .empty
}

// #require records failure AND stops test (like XCTUnwrap)
let user = try #require(await fetchUser(id: 1))
#expect(user.name == "Alice")

// #require for optionals -- unwraps or fails
let first = try #require(items.first)
#expect(first.isValid)
```

**Rule: Use `#require` when subsequent assertions depend on the value. Use `#expect` for independent checks.**

## @Suite and Test Organization

See [references/testing-patterns.md](references/testing-patterns.md) for suite organization, confirmation patterns, known-issue handling, and execution-model details.

## Execution Model

Swift Testing runs tests in parallel by default. Do not assume test order, shared suite instances, or exclusive access to mutable state unless you explicitly design for it.

```swift
@Suite(.serialized)
struct KeychainTests {
    @Test func storesToken() throws { /* ... */ }
    @Test func deletesToken() throws { /* ... */ }
}
```

Use `.serialized` when a test or suite must run one-at-a-time because it touches shared external state. It does not make unrelated tests outside that scope run serially.

**Rules:**
- Each test must set up its own state.
- Shared mutable globals are a bug unless protected or intentionally serialized.
- `@Suite(.serialized)` is for exclusive execution, not for expressing logical ordering between tests.
- If tests depend on sequence, combine them into one test or move the sequence into shared helper code.

## Known Issues

Mark expected failures so they do not cause test failure:

```swift
withKnownIssue("Propane tank is empty") {
    #expect(truck.grill.isHeating)
}

// Intermittent / flaky failures
withKnownIssue(isIntermittent: true) {
    #expect(service.isReachable)
}

// Conditional known issue
withKnownIssue {
    #expect(foodTruck.grill.isHeating)
} when: {
    !hasPropane
}
```

If no known issues are recorded, Swift Testing records a distinct issue notifying you the problem may be resolved.

## Additional Patterns

See [references/testing-patterns.md](references/testing-patterns.md) for parameterized tests, tags and suites, async testing, traits, and execution-model details.

## Test Attachments

Attach diagnostic data to test results for debugging failures. See [references/testing-patterns.md](references/testing-patterns.md) for full examples.

```swift
@Test func generateReport() async throws {
    let report = try generateReport()
    Attachment.record(report.data, named: "report.json")
    #expect(report.isValid)
}
```

Image attachments are available via cross-import overlays — import both `Testing` and a UI framework:

```swift
import Testing
import UIKit

@Test func renderedChart() async throws {
    let image = renderer.image { ctx in chartView.drawHierarchy(in: bounds, afterScreenUpdates: true) }
    Attachment.record(image, named: "chart.png")
}
```

## Exit Testing

Test code that calls `exit()`, `fatalError()`, or `preconditionFailure()`. See [references/testing-patterns.md](references/testing-patterns.md) for details.

```swift
@Test func invalidInputCausesExit() async {
    await #expect(processExitsWith: .failure) {
        processInvalidInput()  // calls fatalError()
    }
}
```

## Common Mistakes

1. **Testing implementation, not behavior.** Test what the code does, not how.
2. **No error path tests.** If a function can throw, test the throw path.
3. **Flaky async tests.** Use `confirmation` with expected counts, not `sleep` calls.
4. **Shared mutable state between tests.** Each test sets up its own state via `init()` in `@Suite`.
5. **Missing accessibility identifiers in UI tests.** XCUITest queries rely on them.
6. **Using `sleep` in tests.** Use `confirmation`, clock injection, or `withKnownIssue`.
7. **Not testing cancellation.** If code supports `Task` cancellation, verify it cancels cleanly.
8. **Mixing XCTest and Swift Testing in one file.** Keep them in separate files.
9. **Non-Sendable test helpers shared across tests.** Ensure test helper types are Sendable when shared across concurrent test cases. Annotate MainActor-dependent test code with `@MainActor`.
10. **Assuming tests run in declaration order.** Swift Testing runs in parallel by default; use `.serialized` only when exclusive execution is required.
11. **Using `.serialized` to express workflow steps.** Serialized execution does not make one test feed another; keep dependent steps in one test.

## Review Checklist

- [ ] All new tests use Swift Testing (`@Test`, `#expect`), not XCTest assertions
- [ ] Test names describe behavior (`fetchUserReturnsNilOnNetworkError` not `testFetchUser`)
- [ ] Error paths have dedicated tests
- [ ] Async tests use `confirmation()`, not `Task.sleep`
- [ ] Parameterized tests used for repetitive variations
- [ ] Tags applied for filtering (`.critical`, `.slow`)
- [ ] Mocks conform to protocols, not subclass concrete types
- [ ] No shared mutable state between tests
- [ ] Tests do not rely on declaration order or shared suite instances
- [ ] `.serialized` used only for truly exclusive state, not to model workflow sequencing
- [ ] Cancellation tested for cancellable async operations

## References

- Testing patterns: [references/testing-patterns.md](references/testing-patterns.md)
- Advanced testing (warnings, cancellation, image attachments): [references/testing-advanced.md](references/testing-advanced.md)
