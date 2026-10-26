---
name: duo-testing
description: "Writes and runs tests for iPhone Duo apps, Apple's foldable with an outer display and an inner display, on the Mac and on the iPhone Duo simulator in Xcode 27.1. Use when adding logic tests (swiftc script, or Swift Testing with @Test and #expect), UI tests with XCTest and XCUIAutomation, launch arguments such as -uiTesting, -resetState and jump-to-screen switches with a TestSupport type, test markers with accessibilityIdentifier and accessibilityValue, when a tap or drag in a UI test doesn't reach a SwiftUI gesture (coordinate(withNormalizedOffset:), press(forDuration:thenDragTo:)), when XCUIDevice rotation or a fold can't be scripted, or when running xcodebuild test on the existing iPhone Duo simulator with -destination id=<UDID>, -parallel-testing-enabled NO, -only-testing, -resultBundlePath, -collect-test-diagnostics and xcresulttool."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-testing

Test an iPhone Duo app in three layers, cheapest first:

1. **Logic on the Mac.** Rules, maths and state machines in plain Swift. Seconds per run, no simulator.
2. **UI tests on the iPhone Duo simulator.** XCTest drives the real app. Minutes per run.
3. **Pose checks in Device Hub.** No API inside a test can fold the simulator. A person clicks Closed, Partially Open and Open, or, with their Accessibility permission, `duo-pose-matrix` presses the same buttons from outside the test.

Load other skills for neighbouring work: `duo-setup` (Xcode 27.1, the simulator, Device Hub), `duo-continuity` (state that must survive a fold, with a manual fold test in its `references/testing.md`), `duo-layout` (what the layouts should do).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 16 October 2026; details in [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Rules

- Put rules and calculations in files that import only Foundation. Test them on the Mac. Keep UI tests for flows that need the real app.
- Write UI tests with XCTest. Swift Testing has no UI automation and no performance API; Apple says to keep XCTest for those ([WWDC26: Migrate to Swift Testing](https://developer.apple.com/videos/play/wwdc2026/267/)).
- Prefix every `xcodebuild` and `xcrun` call with `DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer`. Never run `sudo xcode-select`.
- Every test hook is debug-only and stays off unless the launch has `-uiTesting`.
- Find elements by accessibility identifier. Read state from `accessibilityValue`. Never assert on pixels, point sizes or device names.
- Touch through elements: `element.tap()`, `element.coordinate(withNormalizedOffset:)`, `press(forDuration:thenDragTo:)` between element coordinates. Never work out points from `app.frame`.
- A UI test can't fold the simulator, and on the closed Duo simulator it couldn't rotate the app either (*measured*, below). Plan pose and rotation checks for Device Hub.
- Run UI tests on the existing "iPhone Duo" simulator, addressed by UDID, and boot it before `xcodebuild test`. Never create or clone a simulator unless the user asks: each one takes about 4-6 GB of disk.

## 1. Test the logic on the Mac

Keep the logic in its own folder of the app target, Foundation only. Mark each type `nonisolated` and `Sendable`: the Xcode 27.1 app template sets `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, so the same file is main-actor code inside the app but not in a test script or package. `nonisolated` makes both agree.

```swift
import Foundation

/// When a top-to-bottom fold crosses the grid, active or not, the count is even,
/// so the fold lands in a gap, not on a column. With no fold, every column that fits.
nonisolated struct GridPlan: Equatable, Sendable {
    var columns: Int
    var columnWidth: Double

    static func make(width: Double, minColumnWidth: Double, foldCrossesGrid: Bool, spacing: Double = 8) -> GridPlan {
        guard width > 0, minColumnWidth > 0 else { return GridPlan(columns: 1, columnWidth: max(width, 0)) }
        var count = max(1, Int((width + spacing) / (minColumnWidth + spacing)))
        if foldCrossesGrid, count > 1, count.isMultiple(of: 2) == false { count -= 1 }
        return GridPlan(columns: count, columnWidth: (width - spacing * Double(count - 1)) / Double(count))
    }
}
```

Then pick one runner. Both ran on the Mac in seconds (*measured*); full files in [references/logic-tests.md](references/logic-tests.md).

- **`swiftc` script**, when the repo is just an app. `Tools/LogicTests/main.swift` calls a small `check(_:_:)` helper and exits 1 on failure; `Tools/run-logic-tests.sh` runs `xcrun swiftc -swift-version 6 -o "$OUT" App/Logic/*.swift Tools/LogicTests/main.swift && "$OUT"`.
- **Swift package with Swift Testing**, when several targets share the logic or you want parameterized tests and coverage. Run `xcrun swift test` in the package folder.

```swift
import Testing
@testable import AppCore

@Test("A fold across the grid gives an even count", arguments: [466.0, 800, 951, 1100])
func evenWithFold(width: Double) {
    #expect(GridPlan.make(width: width, minColumnWidth: 150, foldCrossesGrid: true).columns.isMultiple(of: 2))
}

@Test func `without a fold, every column that fits`() {
    #expect(GridPlan.make(width: 466, minColumnWidth: 150, foldCrossesGrid: false).columns == 3)
}
```

In the app, read both inputs from the grid's own geometry: its width, and whether `reservedRegions(kind: .division, options: .includeInactive)` (iOS 27.1) finds a top-to-bottom fold across it, even while the phone is flat. View code: [references/logic-tests.md](references/logic-tests.md#feed-it-from-the-view). `duo-layout` and `duo-patterns` (feed reflow) use the same rule. In tests, pass any width and both fold values; never let a width stand in for a device.

## 2. Launch switches and a TestSupport type

UI tests start the app with launch arguments ([`launchArguments`](https://developer.apple.com/documentation/xcuiautomation/xcuiapplication/launcharguments)). One type reads them, and only in debug builds.

```swift
import SwiftUI

/// Launch switches for UI tests. They work only in debug builds, and only with -uiTesting.
///   -uiTesting           turn on test markers, turn off UIKit animations
///   -resetState          start like a fresh install
///   -openScreen <name>   start on one screen, skipping the taps to get there
enum TestSupport {
    static let arguments = ProcessInfo.processInfo.arguments

    #if DEBUG
    static let isUITesting = arguments.contains("-uiTesting")
    #else
    static let isUITesting = false
    #endif

    static func has(_ flag: String) -> Bool { isUITesting && arguments.contains(flag) }

    /// The word after a switch, as in `-openScreen board`.
    static func value(after flag: String) -> String? {
        guard isUITesting, let i = arguments.firstIndex(of: flag), i + 1 < arguments.count else { return nil }
        return arguments[i + 1]
    }

    static var startScreen: Screen? { value(after: "-openScreen").flatMap(Screen.init(rawValue:)) }

    /// Call once from the App's init, before any view reads stored state.
    static func configure() {
        guard isUITesting else { return }
        if has("-resetState"), let id = Bundle.main.bundleIdentifier {
            UserDefaults.standard.removePersistentDomain(forName: id)
            // Also delete files the app writes: a database, caches, downloads.
        }
        UIView.setAnimationsEnabled(false)
    }
}

/// Screens a test can open directly.
enum Screen: String, Hashable { case board }
```

Wire it in at the top of the app:

```swift
import SwiftUI

@main
struct SampleApp: App {
    init() { TestSupport.configure() }
    var body: some Scene { WindowGroup { RootView() } }
}

struct RootView: View {
    @State private var path: [Screen] = TestSupport.startScreen.map { [$0] } ?? []   // -openScreen board

    var body: some View {
        NavigationStack(path: $path) {
            List { NavigationLink("Play", value: Screen.board).testID("home.play") }
                .navigationDestination(for: Screen.self) { screen in
                    switch screen {
                    case .board: BoardView()   // your screen; the sample's is in references/ui-tests.md
                    }
                }
        }
    }
}
```

- `XCUIApplication.launch()` keeps the app's data between tests. *Measured:* a launch counter in `@AppStorage` read 2 on the second launch without `-resetState`, and 1 with it.
- Add switches for anything slow or random: `-timerSeconds 6` for a countdown, `-seed 42` for shuffles, `-skipIntro`. Read numbers with `value(after:)`.
- `UIView.setAnimationsEnabled(false)` stops UIKit animations ([Apple](https://developer.apple.com/documentation/uikit/uiview/setanimationsenabled(_:))). Apple's page says nothing about SwiftUI animations, so shorten those yourself when `TestSupport.isUITesting` is true.
- Try a switch by hand: `xcrun simctl launch <UDID> com.example.App -uiTesting -openScreen board`. *Measured:* the sample opened straight on the board.
- With `NavigationSplitView`, set the selection from `startScreen` instead of a path.
- Keep one switch type per app. Other Duology pages show their own (`TestSwitches` in `duo-shared-screen`, `ContinuityTesting` in `duo-continuity`, `LaunchOptions` in the two-player recipe). Fold them into `TestSupport`: `TestSupport.value(after: "-seating")`, `TestSupport.has("-continuityTesting")` (launch with `-uiTesting` too), and expose their state with `testMarker` values, not hidden labels.

## 3. Test markers: identifiers and state, only in tests

```swift
import SwiftUI

extension View {
    /// An identifier for a control that is already an accessibility element, such as a Button.
    @ViewBuilder
    func testID(_ id: String) -> some View {
        if TestSupport.isUITesting { accessibilityIdentifier(id) } else { self }
    }

    /// Makes any view (a shape, a cell, a piece) one element the tests can find, with an
    /// optional machine-readable value. UI tests only: VoiceOver never meets the extra
    /// element and never reads the value aloud.
    @ViewBuilder
    func testMarker(_ id: String, value: @autoclosure () -> String = "") -> some View {
        if TestSupport.isUITesting {
            accessibilityElement(children: .ignore)
                .accessibilityIdentifier(id)
                .accessibilityValue(value())
        } else {
            self
        }
    }
}
```

Use it on the views a test touches or reads:

```swift
Circle()
    .gesture(drag)
    .testMarker("board.piece", value: "placed=\(placed ? 1 : 0)|moves=\(moves)")
```

- Apple says an accessibility identifier is for testing and isn't visible to people ([`accessibilityIdentifier(_:)`](https://developer.apple.com/documentation/swiftui/view/accessibilityidentifier(_:))). `testMarker` does more: it creates an element and a value, which VoiceOver would read. That is why it is gated. Gating `testID` too keeps release builds free of test hooks.
- The `if` reads a value fixed at launch, so it never changes a view's identity while the app runs.
- Encode state as `key=value|key=value` and parse it in the test. Assert on the state, not on what the screen looks like.
- Mark drop targets too (`board.cell.3.2`), so a drag aims at an element, not at maths on frames.
- Two panes or two players: prefix every ID with the pane (`left.score`, `right.score`).
- *Measured:* without `-uiTesting`, `-openScreen` was ignored and no marker or test ID existed.

## 4. UI tests that reach SwiftUI on the Duo simulator

Copy the test class from [references/ui-tests.md](references/ui-tests.md). Its core:

```swift
import XCTest

final class BoardUITests: XCTestCase {
    override func setUpWithError() throws { continueAfterFailure = false }

    @MainActor
    func testDragPieceIntoSlot() {
        let app = XCUIApplication()
        app.launchArguments = ["-uiTesting", "-resetState", "-openScreen", "board"]
        app.launch()
        let piece = app.descendants(matching: .any).matching(identifier: "board.piece").firstMatch
        let slot = app.descendants(matching: .any).matching(identifier: "board.slot").firstMatch
        XCTAssertTrue(piece.waitForExistence(timeout: 10))

        let center = CGVector(dx: 0.5, dy: 0.5)
        piece.coordinate(withNormalizedOffset: center)
            .press(forDuration: 0.3, thenDragTo: slot.coordinate(withNormalizedOffset: center))

        XCTAssertTrue((piece.value as? String ?? "").contains("placed=1"))
    }
}
```

XCUIAutomation types are main-actor types. Mark each test method `@MainActor`, as Xcode 27.1's UI test template does, or the whole class when `tearDown` also touches them (*measured*: otherwise Swift 6 reports "sending 'self' risks causing data races").

### The two workarounds

| To do this | Use | Not |
|---|---|---|
| Tap a point inside a view | `element.coordinate(withNormalizedOffset: CGVector(dx: 0.25, dy: 0.5)).tap()` | `app.coordinate(withNormalizedOffset:)` with an offset worked out from `app.frame` |
| Drag, fast or slow | `from.coordinate(...).press(forDuration: 0.3, thenDragTo: to.coordinate(...))` | a press and drag between app-relative coordinates |

- A shipped two-player Duo app needed both. Its UI tests said taps placed relative to the app and slow drags between app-relative points didn't reach the app or SwiftUI's `DragGesture`; element-relative ones did. That suite ran on the shared simulator, most likely open on the inner display.
- *Measured, closed (outer display), portrait:* in a probe app every form worked: `element.tap()`, element-relative and app-relative taps, slow, quick and slow-velocity drags from element or app coordinates, `press(forDuration:thenDragTo:)` element to element, `swipeRight()`, and `pinch(withScale:velocity:)` on a `MagnifyGesture`.
- *Unverified:* the open pose in the probe. No API puts the simulator in a pose, so we couldn't rerun it open; [references/evidence.md](references/evidence.md) has a one-test probe to settle it. Use the element-relative forms everywhere: they worked in every case we saw.
- Hold 0.3 s by default. Apple suggests `press(forDuration:thenDragTo:)` for drags such as reordering table cells ([Apple](https://developer.apple.com/documentation/xcuiautomation/xcuielement/press(forduration:thendragto:))).

### Wait, don't sleep

- `waitForExistence(timeout:)` for an element to appear.
- `wait(for: \.label, toEqual: "Round 2", timeout: 3)` for a label to change ([Apple](https://developer.apple.com/documentation/xcuiautomation/xcuielement/wait(for:toequal:timeout:))).
- `XCTNSPredicateExpectation` with `value CONTAINS "placed=1"` for a marker's value.
- Countdowns and timers: add a launch switch that shortens them rather than `Thread.sleep`.

### Rotation, folds and the two displays

- *Measured:* on the closed Duo simulator, `XCUIDevice.shared.orientation = .landscapeLeft` changed the reported device orientation, but the app stayed 466 × 678 pt and screenshots stayed portrait. The same test rotated the app to 874 × 402 pt on an iPhone 17 Pro simulator (iOS 27.0). Rotate a Duo with Device Hub's rotate button. Open pose not measured.
- `XCUIDevice` has no hinge or pose property, and `simctl` and `devicectl` have no pose command (checked in Xcode 27.1). Outside the test, a Mac tool can press Device Hub's pose buttons through the Accessibility API, once the user gives the app that runs it Accessibility permission (see `duo-setup`). `duo-pose-matrix` is that tool: use it for screenshots of each pose between test runs. For a fold inside a test, use the manual pattern in `duo-continuity`'s `references/testing.md`: the test waits while a person presses Closed and Open and clicks rotate in Device Hub. Run it with `-parallel-testing-enabled NO`, so it waits on the simulator the person is looking at, not on a clone.
- `XCUIScreen.screens` listed two screens. Closed, `screens[0]` shot 466 × 678 pt and `screens[1]` about 669 × 951 pt (*measured*). Attach a screenshot of each display when a test fails ([`screens`](https://developer.apple.com/documentation/xcuiautomation/xcuiscreen/screens)). Don't use them for the App Store: the inner one came out 2006 × 2852 px, while `simctl io ... screenshot --display=primary-1` gave the required 2007 × 2853 px (*measured*).
- Device Hub can't send two-finger touches (Xcode 27 known issue), but `pinch(withScale:velocity:)` from a UI test reached a `MagnifyGesture` (*measured*, closed).

## 5. Run from the command line

```bash
export DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer
xcrun simctl list devices available | grep "iPhone Duo"   # reuse this one
UDID=<its UDID>
xcrun simctl bootstatus "$UDID" -b               # boot first; xcodebuild waits only 60 s
rm -rf build/UITests.xcresult                    # xcodebuild refuses an existing path
xcodebuild test \
  -project App.xcodeproj -scheme App \
  -destination "id=$UDID" \
  -parallel-testing-enabled NO \
  -derivedDataPath build/DerivedData \
  -resultBundlePath build/UITests.xcresult \
  -collect-test-diagnostics never
xcrun xcresulttool get test-results summary --path build/UITests.xcresult
```

- **Reuse the "iPhone Duo" simulator.** Don't create one for tests: each new simulator takes about 4-6 GB of disk. If none is listed, follow `duo-setup` step 3, which creates one after the user agrees.
- A UI test brings the app to the front and ends any running copy. Tell the user before you run it on their simulator, and wait if someone else is driving it.
- **A dedicated test simulator is opt-in.** Create one only when the user asks, after you warn them about the 4-6 GB, and delete it when the run ends. Commands: [references/commands.md](references/commands.md#a-dedicated-simulator-opt-in).
- Exit code 0 means every test passed; 65 means a test failed or the run couldn't start (*measured*).
- **`-parallel-testing-enabled NO` keeps the tests on the simulator you named.** When the scheme runs tests in parallel, xcodebuild runs them on a clone instead, which is one more simulator on disk. `duo-shared-screen` measured its tests running on "Clone 1 of iPhone Duo", which started closed. A clone starts in its own pose, not the one you set in Device Hub. It boots fresh, which can take minutes. It also logs `Test case ... passed on 'Clone 1 of ...'`, which the `Test Case` grep in commands.md misses.
- **xcodebuild can sit after the last test.** *Measured:* after one failed test it waited 600 s "collecting diagnostics from simulator", then timed out; the result bundle grew to 50 MB. With `-collect-test-diagnostics never` it exited the same second. Each `Test Case ... passed` or `failed` line reaches the log before that wait, so an agent can read results early.
- A freshly created Duo simulator failed with "Timed out trying to boot simulator after waiting 60.00s" (*measured*). `simctl bootstatus -b` first took about a minute, then tests ran.
- One test: `-only-testing:AppUITests/BoardUITests/testDragPieceIntoSlot`. Build once, run many: `build-for-testing`, then `test-without-building`.
- `-destination "platform=iOS Simulator,name=iPhone Duo"` resolves and builds (*measured*), but two simulators can share a name. Use the UDID.
- The iOS 27.1 simulator runtime refused every other iPhone we tried (iPhone 17, 17e, 17 Pro, Air, 18 Pro, 18 Pro Max) with "Incompatible device" (*measured*). To run the same tests on another iPhone, use the iOS 27.0 runtime and a deployment target of 27.0 or lower.

Scripts, flags, `xcresulttool` recipes and a troubleshooting table: [references/commands.md](references/commands.md).

## Checklist

- [ ] Rules and maths live in Foundation-only files, as `nonisolated` `Sendable` types, with Mac tests that pass. Fold-dependent maths takes the fold as an input, not a width.
- [ ] `TestSupport` reads `-uiTesting`, `-resetState` and `-openScreen`, inside `#if DEBUG`; release builds ignore them.
- [ ] Slow or random behaviour has a switch (timer length, seed, skip intro).
- [ ] Views that tests touch or read have `testID` or `testMarker`; state is exposed as `key=value|key=value`.
- [ ] No test computes points from `app.frame`; taps and drags use element coordinates and `press(forDuration:thenDragTo:)`.
- [ ] Tests wait with `waitForExistence`, `wait(for:toEqual:timeout:)` or predicates, not fixed sleeps.
- [ ] Rotation and pose checks are listed for Device Hub, not left to `XCUIDevice`.
- [ ] The run reuses the existing iPhone Duo simulator by UDID (a dedicated one only if the user asked, deleted afterwards), boots it first, and passes `DEVELOPER_DIR`, `-parallel-testing-enabled NO`, a fresh `-resultBundlePath` and `-collect-test-diagnostics never`.
- [ ] Results are read with `xcresulttool get test-results summary`, and failures attach a screenshot of each display.
