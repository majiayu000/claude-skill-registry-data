---
name: spark-replace-xctests
description: Migrate the XCTests unit tests of a spark-ios-component-XXX (or common/theming) to Swift Testing, folder by folder, without adding or removing tests.
---

# Spark Replace XCTests Skill

## Overview

This skill migrates the unit tests (`Tests/UnitTests`) written with **XCTest** to **Swift Testing**.

## Component Selection

- If the skill is invoked with a parameter (e.g., `/spark-replace-xctests button`):
  - Use the parameter as the component name and verify the folder exists in `Modules/Components/{component-name}/`.
- If no parameter is provided, ask the user which component (or module) to migrate.

## Rules

- **Keep the same tests**: do not add, remove or merge any test. Each `func test_xxx()` becomes exactly one `@Test` function, with the same GIVEN / WHEN / THEN logic and the same assertions.
- **Every test must have a name**: `@Test("Purpose of the test")`. The name is a short readable sentence describing what is tested (e.g. `@Test("Setup should call all use cases")`).
- Wrap the tests in a `struct` annotated with `@Suite("Component Xxx Tests")` (e.g. `@Suite("SegmentedControl Item ViewModel Tests")`).
- Rename the functions in lowerCamelCase without the `test_` prefix (e.g. `test_setup_shouldCallUseCases` -> `setupShouldCallUseCases`).
- Keep the `// MARK: -` structure of the file.
- Keep the `@_spi(SI_SPI)` and `@testable` imports, replace `import XCTest` by `import Testing`.
- Do not touch the snapshot tests (`Tests/SnapshotTests`): they are already on Swift Testing.
- Do not update the Deprecated files/folders.

## Conversion Table

| XCTest | Swift Testing |
|---|---|
| `final class XxxTests: XCTestCase` | `@Suite("...") struct XxxTests` |
| `override func setUp()` | `init()` (or a local `Stub`) |
| `XCTAssertEqual(a, b, "msg")` | `#expect(a == b, "msg")` |
| `XCTAssertNotEqual(a, b)` | `#expect(a != b)` |
| `XCTAssertTrue(a)` / `XCTAssertFalse(a)` | `#expect(a)` / `#expect(!a)` |
| `XCTAssertNil(a)` / `XCTAssertNotNil(a)` | `#expect(a == nil)` / `#expect(a != nil)` |
| `XCTAssertIdentical(a, b)` | `#expect(a === b)` |
| `XCTUnwrap(a)` | `try #require(a)` |
| `XCTFail("msg")` | `Issue.record("msg")` |
| `XxxMockTest.XCTAssert(...)` | `XxxMockTest.expect(...)` |
| `XxxMockTest.XCTCalled(...)` / not called helpers | `XxxMockTest.expectCalled(...)` |
| `file: StaticString = #filePath, line: UInt = #line` | `sourceLocation: Testing.SourceLocation = #_sourceLocation` |
| `for case in Xxx.allCases { ... }` (when only to iterate) | keep the loop (do not convert to arguments, it would change the number of tests) |

## Steps

Run sourcery first (`cd Modules/Components/{component-name} && sourcery`) to be sure the `MockTest` helpers with `expect` are generated.

Migrate **step by step, folder by folder**, in this order, and build/run the tests after each folder before moving to the next:

1. [ ] `AccessibilityIdentifier`
2. [ ] `Constants`
3. [ ] `Enum`
4. [ ] `Model`
5. [ ] `Token`
6. [ ] `Environment`
7. [ ] `UseCase`
8. [ ] `ViewModel`
9. [ ] Any other remaining folder

For each folder:
- [ ] List the XCTest files (`grep -rl "XCTestCase" Tests/UnitTests/<Folder>`).
- [ ] Convert each file following the rules and the conversion table.
- [ ] Check that the number of tests is identical before/after (count `func test` before, `@Test(` after).
- [ ] Run `swiftlint` at the root of the module.
- [ ] Give a short summary to the user, then continue with the next folder.

### Exceptions (stay on XCTest unless the user asks otherwise)

- The use cases which contain other use cases (as described in the project CLAUDE.md).
- The snapshot tests.

## ViewModel Folder

The ViewModel tests are the most complex. **Keep the current structure** of the existing test file (same tests, same Stub, same helpers) and adapt it to the reference:
`Modules/Components/SegmentedControl/Tests/UnitTests/ViewModel/SegmentedControlItemViewModelTests.swift`

Expected structure:

```swift
import Testing
@testable import SparkComponentXxx
@_spi(SI_SPI) @testable import SparkComponentXxxTesting
@_spi(SI_SPI) import SparkThemingTesting
@_spi(SI_SPI) import SparkTheming
@_spi(SI_SPI) import SparkCommonTesting

@Suite("Xxx ViewModel Tests")
struct XxxViewModelTests {

    // MARK: - Initialization

    @Test("Initialization should use default values")
    func initializationShouldUseDefaultValues() {
        // GIVEN / WHEN
        let stub = Stub()
        let viewModel = stub.viewModel

        // THEN
        expectEqualToExpected(on: stub, otherColors: XxxColors())
        expectNotCalled(on: stub, getColorsUseCase: true)
    }

    // MARK: - Setup

    @Test("Setup should call all use cases")
    func setupShouldCallAllUseCases() {
        // GIVEN
        let stub = Stub()
        let viewModel = stub.viewModel

        // WHEN
        viewModel.setup(stub: stub)

        // THEN
        expectEqualToExpected(on: stub)

        XxxGetColorsUseCaseableMockTest.expect(
            stub.getColorsUseCaseMock,
            expectedNumberOfCalls: 1,
            givenTheme: stub.givenTheme,
            expectedReturnValue: stub.expectedColors
        )
    }

    // MARK: - Property Changes
    // ...
}

// MARK: - Stub

private final class Stub {
    // given values, expected values, use case mocks, viewModel, init(), resetMockedData()
}

// MARK: - Extension

private extension XxxViewModel {
    func setup(stub: Stub) { ... }
}

// MARK: - Expectations

private func expectNotCalled(
    on stub: Stub,
    getColorsUseCase: Bool = false,
    sourceLocation: Testing.SourceLocation = #_sourceLocation
) {
    XxxGetColorsUseCaseableMockTest.expectCalled(
        stub.getColorsUseCaseMock,
        executeWithThemeCalled: !getColorsUseCase,
        sourceLocation: sourceLocation
    )
}

private func expectEqualToExpected(
    on stub: Stub,
    otherColors: XxxColors? = nil,
    sourceLocation: Testing.SourceLocation = #_sourceLocation
) {
    #expect(
        stub.viewModel.colors == (otherColors ?? stub.expectedColors),
        "Wrong colors value",
        sourceLocation: sourceLocation
    )
}
```

ViewModel specific rules:
- The Stub becomes `private final class Stub` (no inheritance from an XCTest stub base class). If the existing stub uses Combine publishers (`PublisherMock`, `sink`), keep the same logic.
- The `XCTAssert...` helper functions (`XCTAssertNotCalled`, `XCTAssertEqualToExpected`, ...) become `expectNotCalled`, `expectEqualToExpected`, ... with a `sourceLocation` parameter forwarded to every `#expect` / `MockTest.expect...` call.
- If the ViewModel uses `@MainActor`, annotate the suite with `@MainActor`.
