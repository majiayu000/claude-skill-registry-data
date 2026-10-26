---
name: recipe-finance-dashboard
description: "Creates a complete SwiftUI personal finance dashboard for iPhone Duo, Apple's foldable: balance and recent spending in one column on the closed outer display; balance, a Swift Charts spending chart and the transaction list side by side on the open inner display; an even 8-column grid with the fold as its middle gutter (DuoColumns and PaneFrames from duo-design-system); and list-detail for a transaction that survives fold and unfold. Use when someone wants to start a new finance, budgeting, banking, expenses or any dashboard app from scratch (a new Xcode project), or runs /duo-new recipe-finance-dashboard. For an existing app, use duo-design-system (grid) and duo-patterns (list-detail) instead. Covers FoldPanes reading the .division reserved region with includeInactive, one NavigationStack whose path comes from the selection, a delayed pop on unfold that keeps the margins right, money as whole cents, a Foundation-only model tested on the Mac, and UI tests that pass in any pose on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-finance-dashboard

This recipe makes a new Xcode project: a personal finance dashboard for one iPhone Duo. Closed, it shows the total balance, money in and out this month, a spending chart against an even pace to the budget, the newest transactions and spending by category, in one column. Open, the window becomes one even grid with the fold in its middle gutter: balance and every transaction on the leading side, the chart and categories on the trailing side. Pick a transaction and it replaces the chart, next to the list it came from.

The sample data is a placeholder (six months of realistic transactions, pinned to 20 October 2026). The value is the frame: panes that sit on the fold in every pose, a selection that survives opening and closing the phone, money maths you can test on the Mac in seconds, and UI tests that pass on the Duo simulator in any pose.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1). *Unverified* means we could not check it. Everything else links to Apple. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists: use `duo-design-system` (the grid), `duo-patterns` (list-detail) and `duo-continuity`;
- the screen is a list and a detail with no dashboard: `NavigationSplitView`, as `duo-patterns` shows, is less code.

## 1. Create the project

`/duo-new recipe-finance-dashboard` runs steps 1 to 5 without launch switches and does not run the UI tests: run step 6 yourself. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools`, and not an Apple module name such as `SwiftUI`, `Charts` or `Foundation`;
   - a bundle id such as `com.example.pocketledger`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-finance-dashboard/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-finance-dashboard/scripts/new-project.sh" \
     PocketLedger com.example.pocketledger ~/Developer/PocketLedger
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths, checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65) before it creates anything.
3. Test the money maths on the Mac. Expect `0 failed`: `cd ~/Developer/PocketLedger && Tools/run-model-tests.sh`.
4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -quiet -project PocketLedger.xcodeproj -scheme PocketLedger \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Install, launch on a transaction, and screenshot the display in use. Use the UDID, not `booted`.

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl install <UDID> build/DerivedData/Build/Products/Debug-iphonesimulator/PocketLedger.app
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.pocketledger -select 8
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary build/outer.png     # closed
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary-1 build/inner.png   # open
   ```

   Only the display in use has content; the other screenshot is black. Look at the PNG before you report.
6. Run the UI tests: `DESTINATION="id=<UDID>" Tools/run-ui-tests.sh`. With no setting it uses the simulator named `iPhone Duo`.
7. Tell the user what passed, and that poses change only in Device Hub (`duo-pose-matrix` can press its buttons).

Set `DEVELOPER_DIR` for every `xcrun` and `xcodebuild` call when the Mac has more than one Xcode. Never run `xcode-select` for this.

## 2. What you get

| Path | What it holds |
|---|---|
| `<App>/Model/Money.swift` | `Money`: whole cents, exact sums, literals such as `-8.40`. |
| `<App>/Model/Ledger.swift` | Every number on screen: balance, month to date, money in and out, budget pace, daily totals for the chart, categories, activity by day, merchant history. Takes `now`; never reads the clock. |
| `<App>/Model/LedgerEntry.swift`, `SampleLedger.swift` | Accounts, transactions, categories, and six months of sample data. |
| `<App>/Model/DuoColumns.swift` | `DuoFold`, `DuoColumns` (duo-design-system's grid) and `PaneFrames`: two panes of half the grid each, the fold as the middle gutter. Foundation only. |
| `<App>/Shared/FoldPanes.swift` | Reads the fold from `GeometryProxy` and lays out one pane or two. |
| `<App>/Shared/DuoTokens.swift` | duo-design-system's tokens: 4 or 8 columns, gutters, card padding, type, colours. |
| `<App>/Dashboard/` | The dashboard, balance card, spending chart (Swift Charts), category grid, activity list. |
| `<App>/Detail/TransactionDetail.swift` | One transaction: category picker, facts, what the merchant cost each month (a bar chart). |
| `<App>/App/` | App entry, `FinanceModel` (selection, filter, panes), `RootView` (the stack), launch switches. |
| `<App>UITests/` | Six UI tests, pose-agnostic. |
| `Tools/` | `run-model-tests.sh`, `ModelTests/main.swift`, `run-ui-tests.sh`. |

Project settings: iOS 26.0 deployment, Swift 6 language mode, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups (new files need no project edits), iPhone and iPad, a privacy manifest that declares nothing collected. The scheme turns off parallel testing so `xcodebuild` doesn't clone the simulator.

Architecture, data flow and test details: [references/architecture.md](references/architecture.md).

## 3. How it behaves in each pose

| Pose | Width class | Layout |
|---|---|---|
| Closed (outer display) | compact | One column: balance, money in and out, chart, the six newest transactions and "Show all", categories. A transaction pushes onto the stack. |
| Open, flat, held wide | regular | Two panes from an 8-column grid. Leading: balance, money in and out, every transaction. Trailing: chart and categories, or the picked transaction. The gap between the panes is one 16 pt gutter centred on the fold line (*measured*: leading pane x 20 to 467.7 pt, trailing from 483.7 pt). |
| Partly folded like a book | regular | The same panes. Only the gap grows, to the fold's frame, so nothing sits in it (*measured*: leading pane ends at 455.7 pt, trailing starts at 495.7 pt; each edge moved 12 pt). |
| Open, held tall, or set on a table like a laptop | regular | The fold runs across the window, so `DuoFold` is nil and the panes split the width evenly. The fold falls between rows of scrolling content (unverified on this recipe). |
| Narrow Split View window | compact | Same as closed (unverified). |

Fold and unfold: the selection lives in `FinanceModel`, above the stack. Closed on a transaction, then opened: it moves to the trailing pane (*measured* with `-select 8`). Closed again: it is pushed (*measured* in `recipe-shop`, which shares this code).

## 4. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| The fold as the grid's middle gutter | `PaneFrames` in `Model/DuoColumns.swift`, used by `DashboardScreen` | Apple asks for an even column count whenever a division region exists, active or not, and for the outer margins to stay while the gap at the hinge widens ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)). Same helper as `duo-design-system`'s grid.md. |
| Read the fold even when flat | `DuoFold.init?(_:)` in `Shared/FoldPanes.swift` | [`reservedRegions(kind: .division, options: .includeInactive)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) behind `#available(iOS 27.1, *)`, so the panes sit in the same place flat and folded. A fold that only touches the view's edge, or runs across it, is ignored. |
| Each pane lays out for a half | `FoldPanes` sets `.environment(\.horizontalSizeClass, .compact)` on the panes | A custom split keeps the window's regular class (*measured* in `duo-layout`), so without it each half would ask for 8 columns. |
| Re-measure only when it matters | `onPaneGeometryChange` keeps width and the fold's x values only | `onGeometryChange` fires on scroll otherwise; the fold's y changes as content scrolls. |
| One source of truth for list-detail | `FinanceModel.path` is computed from `selection` and `isTwoPane` | Closed, the selection is pushed; open, the path is empty and the trailing pane shows it. Nothing to sync. |
| Unfolding on a pushed transaction | `RootView` waits 600 ms before it switches to two panes | *Measured:* when the stack popped during the unfold, the dashboard came back 2 pt left of the window edge with the closed phone's right inset (42 pt instead of 84) and no margins, and stayed so; popped after the animation, it matched a fresh launch. See [architecture.md](references/architecture.md#unfolding-on-a-pushed-screen). |
| Width class, never the device | `RootView` reads `horizontalSizeClass` | Apple: size classes and the view's space, not the device or orientation ([D1](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)). |
| Margins next to the vertical bar | `duoContainerMargins()` in `DuoTokens.swift` | `contentMargins(for: .container, edges: .horizontal)` on iOS 27.1 gives asymmetric margins (*measured*: 20 pt leading, 0 pt next to the bar). |
| A chart that never crosses the fold | `SpendingCard` lives in one pane | Its height grows with Dynamic Type (`@ScaledMetric`), its width is the pane's. [Swift Charts](https://developer.apple.com/documentation/charts): `AreaMark`, `LineMark`, `PointMark`, `BarMark`, `RuleMark`. |
| Controls off the fold | Filter in the toolbar; Close at the trailing pane's top trailing corner | The system moves bar items off the fold; the close button sits inside the trailing pane in every pose. |
| VoiceOver follows the detail | `@AccessibilityFocusState` on the transaction's name | Open, the detail appears beside the row; focus moves to it instead of staying on the row. |
| Exact money | `Money` (cents), `Decimal` for formatting | Doubles only for chart axes. |

## 5. Customise

Change the data first, in `Model/`, and test it on the Mac before you touch a view.

- **Real data:** build a `Ledger` from your source in `LaunchOptions.makeModel()` and pass `Date()` as `now`. Keep amounts as `Money`.
- **New numbers:** add a function to `Ledger` that takes `now`, add a check for it in `Tools/ModelTests/main.swift`, then show it.
- **New tile or card:** give it a span (`tokens.span(2)` for a tile, `span(4)` for a wide card), never a width. Spans double at accessibility text sizes.
- **Another pane layout:** keep `PaneFrames` for the split; put what you like in each pane.
- **Currency and locale:** `Ledger.currencyCode` sets the currency; formatting follows the person's locale.

Keep these, whatever the app:

1. Even columns, with the fold as the middle gutter; `.includeInactive`, so nothing jumps when the phone folds.
2. One selection in the model, above the stack; the path computed from it.
3. The 600 ms wait before popping on unfold, until a device run says otherwise.
4. Model types `nonisolated` and `Sendable`, Foundation only, so `Tools/run-model-tests.sh` keeps them honest.
5. Accessibility identifiers on rows (`txn.<id>`), panes (`pane.leading`, `pane.trailing`) and controls, so tests find them in any pose.

## 6. Test it

**On the Mac:** `Tools/run-model-tests.sh` builds `Model/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`, like the app target. *Measured:* 60 checks pass in a few seconds; one check runs the model in `Task.detached`, and removing `nonisolated` from any of the 15 model types stops the build.

**On the simulator:** `Tools/run-ui-tests.sh`. The six tests start from launch switches (`-select N`, `-filter NAME`, `-uiTesting`), find elements by identifier, and pass in any pose: closed, a transaction is pushed; open, it sits in the trailing pane. *Measured:* all six pass closed and open, and `testLayoutInThisPose` passes partly folded (iPhone Duo simulator, iOS 27.1, 20 Oct 2026).

Duo simulator notes for UI tests (*measured*):

- Closed, the back button sits in the vertical bar, which XCUITest reports as a toolbar: find it by its identifier, `BackButton`.
- A coordinate tap doesn't scroll. Scroll the element into view before tapping it, or the tap lands off screen and does nothing.
- `XCUIScreen.main` is the outer display, black while the phone is open. `XCUIScreen.screens` lists both displays; `testLayoutInThisPose` attaches a screenshot of each.

Run `testLayoutInThisPose` once per pose in Device Hub. It checks the balance sits in the leading pane, the gap between panes is a gutter or the fold (at most 60 pt), the detail opens in the trailing pane with a 44 pt close button, and it saves the pane frames and screenshots to the result bundle.

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-model-tests.sh` prints `0 failed`.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] `python3 duo-lint.py --strict <project>` reports no findings.
- [ ] The app launched on the Duo simulator; you looked at the screenshot of the display in use.
- [ ] `Tools/run-ui-tests.sh` passes closed and open.
- [ ] In Device Hub, Closed, Open and Partially Open: closed shows one column; open shows two panes; partly open, nothing sits in the fold.
- [ ] Pick a transaction, close the phone, open it: the transaction stays on screen, beside the list when open, and the list keeps its margins.
- [ ] Largest accessibility text size: tiles stack, rows put the amount under the name.
- [ ] Every new number has a check in `Tools/ModelTests/main.swift`.
- [ ] Checked on a real iPhone Duo before release (the simulator can't show the fold's feel or 120 Hz).
