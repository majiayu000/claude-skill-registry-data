---
name: Swift Unit Testing Skill
description: "Design, write, migrate, and review Swift unit and integration tests using Swift Testing by default, with XCTest retained for UI automation, performance metrics, Objective-C interoperability, and legacy suites. Use for @Test, #expect, #require, parameterized tests, async tests, dependency injection, mocks/fakes, test plans, XCTest, XCUITest, TDD, flaky tests, and test architecture. Do not use UI-test polling or XCTest subclasses for ordinary new Swift unit tests, and do not introduce third-party snapshot frameworks unless the user requests one."
---

# Swift Unit Testing

Build deterministic tests around observable behavior. Prefer Swift Testing for new Swift unit and integration tests; choose XCTest only where it still provides the required runner or API.

## Compatibility baseline

- Swift Testing requires Swift 6 / Xcode 16 or newer. It supports Apple platforms, Linux, and Windows.
- XCTest remains appropriate for `XCUIApplication`, `XCTMetric`, Objective-C tests, and incremental maintenance of existing XCTest suites.
- Swift Testing and XCTest can coexist in one test target. Do not mix `@Test` methods into an `XCTestCase` subclass.
- State the app's actual deployment targets and CI Xcode version before recommending availability-sensitive traits or APIs.
- Treat APIs first introduced after the installed SDK as future-cycle features and gate them explicitly.

## Select the test layer

| Goal | Default |
| --- | --- |
| Pure Swift unit or integration behavior | Swift Testing |
| Async/throws, parameterized cases, traits, tags | Swift Testing |
| UIKit/SwiftUI end-to-end interaction | XCTest UI testing |
| Runtime, CPU, memory, launch, or signpost metrics | XCTest performance APIs |
| Objective-C test code or legacy suite | XCTest |

Do not replace a unit test with a UI test. Keep network, database, clock, randomness, and notification boundaries injectable so unit tests remain fast and deterministic.

## Workflow

1. Identify the behavior and public boundary under test.
2. List failure cases, cancellation behavior, and state transitions before writing assertions.
3. Inject dependencies through small capability protocols or closures. Prefer a semantic transport protocol over subclassing framework classes.
4. Write a failing test, implement the smallest behavior, then refactor.
5. Run the narrow test, its containing suite, and then the affected test plan.
6. Check parallel safety: avoid mutable globals, shared files, fixed ports, real sleeps, and order dependence.
7. Confirm the test fails when the production behavior is deliberately broken.

## Swift Testing defaults

Use `#expect` for nonfatal checks and `try #require` when later assertions need a value. Test asynchronous functions directly:

```swift
import Testing
@testable import MyApp

@Test("The profile includes the requested user")
func profileLookup() async throws {
    let profile = try await ProfileStore.preview.profile(id: 42)
    #expect(profile.id == 42)
    #expect(!profile.displayName.isEmpty)
}
```

Prefer parameterized tests to copied methods:

```swift
@Test(arguments: [0, 1, 12, 99])
func roundTrip(_ value: Int) throws {
    #expect(try Codec.decode(Codec.encode(value)) == value)
}
```

Use `#expect(throws:)` for failures and `confirmation` for callback counts. Convert one-shot callbacks to checked continuations when that mirrors the production abstraction. Never make an async mock call synchronously merely to simplify a test.

Read [examples/example_basic_test.swift](examples/example_basic_test.swift) for standalone Swift Testing structure and parameterization. Read [examples/example_async_test.swift](examples/example_async_test.swift) for a strict-concurrency-safe async HTTP boundary.

## Dependency doubles

Choose the smallest double that proves behavior:

- Stub: returns configured data.
- Spy: records messages for later assertions.
- Fake: implements a lightweight in-memory behavior.
- Mock: verifies a specific interaction contract; use sparingly.

Do not subclass `URLSession`, `URLSessionDataTask`, or other framework classes just to override one method. Their async convenience methods are not required to dispatch through callback overrides. Inject an `HTTPTransport` with an async requirement, or use a custom `URLProtocol` with an ephemeral session when URL loading itself is the subject.

Always complete every callback path exactly once. Validate malformed responses and HTTP status codes instead of treating every non-nil body as success.

## XCTest-specific work

### UI automation

- Assign stable semantic identifiers in production views, such as `login.username` and `login.success`; do not query localized display text.
- Wait for state transitions with `waitForExistence(timeout:)` or an `NSPredicate` expectation.
- Set launch arguments and environment before `launch()` to make the backend and account state deterministic.
- Mark UI tests `@MainActor` where required by the active SDK.

```swift
final class LoginUITests: XCTestCase {
    @MainActor
    func testSuccessfulLogin() {
        let app = XCUIApplication()
        app.launchArguments = ["-use-stub-auth"]
        app.launch()

        app.textFields["login.username"].tap()
        app.textFields["login.username"].typeText("sample")
        app.buttons["login.submit"].tap()

        XCTAssertTrue(app.staticTexts["login.success"].waitForExistence(timeout: 2))
    }
}
```

### Performance

Use XCTest metrics and baselines instead of a one-shot `Date` threshold. Keep setup outside `measure` unless setup is intentionally measured.

```swift
measure(metrics: [XCTClockMetric(), XCTCPUMetric(), XCTMemoryMetric()]) {
    _ = processor.process(fixture)
}
```

Record the build configuration, device class, and baseline environment. Do not compare absolute timings across dissimilar CI workers.

## Swift concurrency rules

- Let Swift Testing run independent tests in parallel; use `.serialized` only for unavoidable shared external state.
- Prefer actors or immutable `Sendable` values in doubles used across tasks.
- Inject a clock rather than sleeping. Drive the test clock explicitly.
- Verify cancellation and cleanup, not only successful completion.
- Do not silence Sendable diagnostics with `@unchecked Sendable` unless the type has a documented synchronization invariant.

## Review checklist

- The test imports the production module or clearly labels a standalone teaching fixture; it never redeclares an imported production type.
- The assertion checks behavior, not an implementation detail.
- Every asynchronous path is awaited and bounded by the test runner.
- No real network, wall-clock sleep, shared account, or random order controls the result.
- Failure, empty-response, malformed-response, and cancellation paths are covered where applicable.
- UI queries use identifiers and explicit waits.
- Performance tests use metrics and baselines.
- Availability and CI toolchain requirements are stated.

## Supporting material

- [README.md](README.md) summarizes framework selection and minimum tools.
- [examples/example_basic_test.swift](examples/example_basic_test.swift) is a dependency-free Swift Testing example.
- [examples/example_async_test.swift](examples/example_async_test.swift) demonstrates async transport injection without `URLSession` subclassing.
- [examples/prompts.md](examples/prompts.md) contains realistic activation prompts.

When adapting an example to an app, move the sample system-under-test declaration into the production target and replace it in the test target with `@testable import AppModule`.
