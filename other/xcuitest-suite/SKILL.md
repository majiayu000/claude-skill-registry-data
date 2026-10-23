---
name: xcuitest-suite
description: "Authors XCUIest UI tests for iOS / iPadOS / tvOS and macOS desktop apps - uses the three-class XCUIApplication / XCUIElement / XCUIElementQuery pattern, sets accessibility identifiers on production code, runs via `xcodebuild test` with destination, parses the `xcresult` bundle. The macOS desktop delta (platform=macOS destination flags, TCC privacy-permission resets, per-device performance baselines) is in references/macos.md. Use when an iOS or macOS app needs UI tests in Apple's first-party framework (no external runtime; native to Xcode)."
---

# xcuitest-suite

## Overview

XCUITest is Apple's first-party UI testing framework, integrated
with Xcode and built on the XCTest framework
([xcui-fundamentals][xcui]).

[xcui]: https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/testing_with_xcode/chapters/09-ui_testing.html

> "UI testing in Xcode is built on three fundamental classes:
> XCUIApplication, XCUIElement, XCUIElementQuery." ([xcui-fundamentals][xcui])

The general pattern: **Query → Synthesize → Assert**.

> "1. Query - Use XCUIElementQuery to find an XCUIElement
> 2. Synthesize - Synthesize an event and send it to the XCUIElement
> 3. Assert - Use an assertion to compare the element's state against expected reference state" ([xcui-fundamentals][xcui])

## When to use

- An iOS app needs UI tests using Apple's native framework.
- A team prefers no external runtime (Appium, Detox) and wants
  Xcode-native test integration.
- The app is iOS-only and there's no need for cross-platform reuse.

If the app is React Native, see
`detox-testing`. For cross-platform
Appium-style coverage, see
`appium-testing`.

## macOS desktop apps

The same framework tests macOS desktop apps (AppKit, SwiftUI, Catalyst) - every
step below carries over. The macOS delta - `-destination 'platform=macOS'`
flags, TCC privacy-permission resets (`tccutil reset`), per-device performance
baselines, and headless-runner constraints - is in
[references/macos.md](references/macos.md).

## Step 1 - Add a UI test target

In Xcode: File → New → Target → UI Testing Bundle. The template
generates a `.swift` test class with a default `setUp`:

```swift
import XCTest

final class CartUITests: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false   // critical (default)
        XCUIApplication().launch()
    }
}
```

Per [xcui-fundamentals][xcui]:

> "`continueAfterFailure = NO` is the default (recommended) because
> UI test steps are dependent on previous steps."

## Step 2 - Set accessibility identifiers in production code

XCUITest finds elements via the accessibility tree. Hard-coded
labels / text are brittle - set explicit identifiers in the SUT:

```swift
// Production code
let placeOrderButton = UIButton()
placeOrderButton.accessibilityIdentifier = "place-order-button"
```

Then in tests:

```swift
let app = XCUIApplication()
app.buttons["place-order-button"].tap()
```

`accessibilityIdentifier` (not `accessibilityLabel`) - labels are
user-facing and translated; identifiers are dev-only and stable.

## Step 3 - Query patterns

```swift
let app = XCUIApplication()

// By accessibility identifier (preferred)
app.buttons["place-order-button"].tap()
app.textFields["email-field"].typeText("user@example.com")

// By type + text
app.staticTexts["Welcome"].swipeUp()

// Predicate-based query
let cells = app.tables.cells.matching(
    NSPredicate(format: "label CONTAINS[c] 'BOOK-001'")
)
cells.element(boundBy: 0).tap()

// Wait for an element
XCTAssert(app.staticTexts["Order confirmed"].waitForExistence(timeout: 5))
```

## Step 4 - Synthesize events

```swift
// Tap
app.buttons["submit"].tap()

// Type
app.textFields["email"].typeText("user@example.com")

// Swipe / drag
app.cells.element(boundBy: 0).swipeLeft()

// Pinch
app.images["map"].pinch(withScale: 2.0, velocity: 1.0)

// Press for duration (long-press)
app.buttons["context-menu"].press(forDuration: 1.0)

// System keyboard return
app.keyboards.buttons["return"].tap()
```

## Step 5 - Assert state

```swift
let confirmation = app.staticTexts["Order confirmed"]
XCTAssertTrue(confirmation.exists)

XCTAssertEqual(app.staticTexts["order-id"].label, "ORD-12345")

XCTAssertTrue(app.buttons["submit"].isEnabled)
```

`exists` returns immediately; `waitForExistence(timeout:)` waits
up to N seconds. Use `waitForExistence` for any post-tap state
that depends on async work.

## Step 6 - Run

```bash
# From the project directory:
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15,OS=latest' \
  -resultBundlePath TestResults.xcresult
```

Per-destination patterns:

| Use                | Destination string                                                |
|--------------------|-------------------------------------------------------------------|
| Latest sim         | `'platform=iOS Simulator,name=iPhone 15,OS=latest'`               |
| Specific OS        | `'platform=iOS Simulator,name=iPhone 14,OS=17.4'`                 |
| Connected device   | `'platform=iOS,id=<UDID>'`                                         |
| Multi-device matrix | Pass `-destination` multiple times.                              |

## Step 7 - Parse `.xcresult`

The result bundle is binary. Extract via `xcresulttool`:

```bash
xcrun xcresulttool get test-results summary --path TestResults.xcresult --format json > results.json
```

Then use `junit-xml-analysis` (in the qa-test-reporting plugin)
on the JUnit-equivalent shape (or directly on the JSON for richer
data).

## Step 8 - CI integration

```yaml
# .github/workflows/ios-tests.yml
jobs:
  ui-tests:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v5
      - run: xcodebuild test -project MyApp.xcodeproj -scheme MyApp \
              -destination 'platform=iOS Simulator,name=iPhone 15,OS=latest' \
              -resultBundlePath TestResults.xcresult
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: xcresult
          path: TestResults.xcresult
```

GitHub Actions provides `macos-15` runners with Xcode pre-installed.

## Anti-patterns

| Anti-pattern                                                         | Why it fails                                                              | Fix |
|----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Querying by `accessibilityLabel`                                     | Labels are translated; tests fail in non-English locales.                 | Use `accessibilityIdentifier` (Step 2-3). |
| `Thread.sleep` for async waits                                        | Flaky on slow runners; slow on fast.                                      | `waitForExistence(timeout:)` (Step 5). |
| `continueAfterFailure = true`                                         | One failure cascades into N false positives.                              | Default `false` (Step 1). |
| Hard-coded text in queries                                            | Copy changes break tests.                                                 | accessibility identifiers (Step 2). |
| Running against wrong destination ("latest" without pin)              | Test passes on Xcode 16, fails on 15; reproducibility issues.            | Pin OS version explicitly in CI. |
| Skipping `xcresult` upload                                            | Failure debugging needs the screenshots / videos in the bundle.           | Always upload (Step 8). |

## Limitations

- **macOS only.** Xcode + Simulator require macOS hosts.
- **Slower than unit tests.** Each test launches the app; expect
  10-30s per test. Keep UI test count modest.
- **Flaky on Simulator under load.** CI runners under contention
  produce intermittent failures; use retries cautiously (don't mask
  real bugs).
- **No first-party visual regression.** Pair with
  `percy-visual-regression-testing` (in the qa-visual-regression plugin)
  or screenshot-comparison helpers.

## References

- [xcui][xcui] - Apple's XCUITest fundamentals: three-class
  pattern (XCUIApplication / XCUIElement / XCUIElementQuery),
  Query→Synthesize→Assert, `continueAfterFailure = NO` default.
- [references/macos.md](references/macos.md) - the macOS desktop delta
  (destination flags, TCC permissions, CI, per-device baselines).
- `espresso-suite` - Android sibling.
- `appium-testing` - cross-platform
  alternative when iOS + Android share tests.
- `junit-xml-analysis` - downstream parser for JUnit-converted xcresult.
