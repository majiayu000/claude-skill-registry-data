---
name: recipe-two-player-game
description: Creates a complete two-player, one-phone SwiftUI game for iPhone Duo, Apple's foldable, where each player gets half the screen in every pose (closed on the outer display, open on the inner display, upright or sideways, partly folded). Use when someone wants to start a new two-player game or shared-screen app from scratch (a new Xcode project), or runs /duo-new recipe-two-player-game. For an existing app, use duo-shared-screen instead. Covers EvenSplit (GeometryReader plus AnyLayout), per-half coordinate spaces and content shapes, face-to-face seating turned by split axis, right-to-left seats, input gating, countdown, winner screen and rematch, keeping targets off the fold with reservedRegions(kind:) (.division, .occlusion), a Foundation-only game engine tested on the Mac, and UI tests that work on the iPhone Duo simulator.
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-two-player-game

This recipe makes a new Xcode project: a two-player race for one iPhone Duo. Each player gets half the screen. Targets appear in each half; a player taps their own. A miss locks that player out for a moment. First to the goal wins, then both tap Rematch.

The game is a placeholder. The value is the frame around it: two halves that always show, touches judged in each half's own coordinates, rules you can test on the Mac in seconds, and UI tests that pass on the Duo simulator.

Labels: *measured* means we ran it, on the iPhone Duo simulator (iOS 27.1, closed, outer display) unless the line names another one. *Unverified* means we could not check it. Everything else links to Apple. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists: use `duo-layout` (EvenSplit) and `duo-shared-screen`;
- one person uses the app: start from `duo-start`.

## 1. Create the project

`/duo-new recipe-two-player-game` runs steps 1 to 5, but it launches to the home screen (no launch switches) and does not run the UI tests: run step 6 yourself. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools`, and not an Apple module name such as `SwiftUI` or `Foundation`;
   - a bundle id such as `com.example.dueltap`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-two-player-game/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-two-player-game/scripts/new-project.sh" \
     DuelTap com.example.dueltap ~/Developer/DuelTap
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths, checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65) before it creates anything.
3. Test the rules on the Mac. Expect `0 failed`:

   ```bash
   cd ~/Developer/DuelTap && Tools/run-engine-tests.sh
   ```

4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -project DuelTap.xcodeproj -scheme DuelTap \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Install, launch straight into a round, and screenshot both displays. Use the simulator's UDID, not `booted`: several simulators may be running.

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl install <UDID> build/DerivedData/Build/Products/Debug-iphonesimulator/DuelTap.app
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.dueltap -openDuel -autoReady -countdown 0
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary build/outer.png     # outer display
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary-1 build/inner.png   # inner display
   ```

   Only the display in use has content; the other screenshot is black. Look at the PNG before you report.
6. Run the UI tests: `DESTINATION="id=<UDID>" Tools/run-ui-tests.sh`. With no setting it uses the simulator named `iPhone Duo`.
7. Tell the user what passed, and that poses change only in Device Hub (step 6 of the checklist).

Set `DEVELOPER_DIR` for every `xcrun` and `xcodebuild` call when the Mac has more than one Xcode. Never run `xcode-select` for this.

## 2. What you get

| Path | What it holds |
|---|---|
| `<App>/Engine/Duel.swift` | The rules: players, ready, countdown, hits, misses, lockout, time limit, winner, rematch, seeded targets. Foundation only, `nonisolated`, `Sendable`. |
| `<App>/Engine/PlayArea.swift`, `Geometry.swift` | Where targets may go inside a half, clear of the fold and cameras. Own small geometry types, so the engine needs no CoreGraphics. |
| `<App>/Shared/EvenSplit.swift` | Two equal halves: side by side when wide, stacked when tall. Same type as the gallery's and `duo-layout`'s. |
| `<App>/Duel/DuelScreen.swift` | The split, seating and layout direction, system overlays, idle timer, the clock task, the leave dialog. |
| `<App>/Duel/PlayerHalf.swift` | One half: content shape, turn, touch surface, target, score bar, ready and result panels. |
| `<App>/Duel/DuelModel.swift` | `@Observable` wrapper: holds the `Duel`, the current time, haptic counters and the haptics switch. |
| `<App>/Duel/GeometryBridge.swift` | CGRect to engine types, and the reserved-region query. |
| `<App>/App/` | App entry, `RootView` (home or duel), launch switches. |
| `<App>UITests/` | Ten UI tests, pose-agnostic. |
| `Tools/` | `run-engine-tests.sh`, `EngineTests/main.swift`, `run-ui-tests.sh`. |

Project settings: iOS 26.0 deployment, Swift 6 language mode, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups (new files need no project edits), iPhone and iPad, a privacy manifest that declares nothing collected. The scheme turns off parallel testing so `xcodebuild` doesn't clone the simulator.

Architecture, data flow and test details: [references/architecture.md](references/architecture.md).

## 3. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| Both halves show in every pose | `Shared/EvenSplit.swift`, used in `DuelScreen` | `ArrangementView` shows only its first view when the phone is closed and held sideways (*measured*, see `duo-layout`). `AnyLayout` keeps each half's state when the axis flips ([AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout)). |
| Each half has its own coordinates | `PlayField` in `PlayerHalf.swift` | `.coordinateSpace(.named("p1.field"))` plus `SpatialTapGesture(coordinateSpace:)` ([doc](https://developer.apple.com/documentation/swiftui/spatialtapgesture)). The engine gets points in the half's own space, so top, bottom, left, right and upside down all run the same code. |
| Face to face | `Player.quarterTurns(faceToFace:sideBySide:)`, applied by `turned(_:)` in `PlayerHalf` | The phone lies flat with one player at each far edge, so each half turns until its top edge sits on the seam: stacked, player 1's half turns upside down; side by side, each half turns a quarter toward the seam. Same rule as `duo-shared-screen`. Touches still arrive in the half's own coordinates (*measured*: `testTurnedHalfStillScores` stacked on the Duo; side by side on an iPhone 17 simulator, iOS 26.2, turned to landscape). |
| Touches stay in their half | [`.contentShape(.interaction, Rectangle())`](https://developer.apple.com/documentation/swiftui/view/contentshape(_:_:eofill:)) on each half, with no gesture on it | *Measured:* a hit-testable layer that grew past player 2's half took player 1's taps until each half had this content shape; the target's accessibility frame stayed 56 × 56 pt. |
| Drawing stays in its half | `.clipped()` on each half | Clipping hides overflow. It does not limit touches (*measured*); the content shape does. |
| Right-to-left languages | `DuelScreen` pins the split to left-to-right; `PlayerHalf` gives the content the real direction; `PlayField` stays left-to-right | Player 1 keeps the top or left half in every language, as in `duo-shared-screen`. *Measured:* with the turn inside the mirrored content, each side-by-side half's top edge pointed away from the seam, so the turn sits outside it. In a mirrored field, a tap on the drawn target counted as a miss in both halves; a left-to-right field fixed it. |
| Targets stay off the fold and cameras | `FoldAvoidance.playArea(in:margin:)` and `Engine/PlayArea.swift` | Reads active `.division` and `.occlusion` regions with [`reservedRegions(kind:options:layoutDirectionBehavior:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) behind `#available(iOS 27.1, *)`, then keeps the biggest strip clear of them. Not yet run with an active fold (unverified). |
| Input gating | `Duel.canTap(_:now:)` | No taps count during the countdown, after the round, or for a player locked out after a miss. One player's lockout never blocks the other. |
| Ready and rematch per half | `ReadyPanel`, `ResultPanel`, `Duel.toggleReady` | Each player starts and restarts from their own half. A round starts only when both are ready. |
| Fill the screen, keep content safe | `.background { … .ignoresSafeArea() }` in `PlayerHalf` | Colour runs to the edges; the field and score bar stay inside the safe area. Apple asks games to fill the screen in every pose rather than letterbox ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)). |
| One shared control, in one place | `duel.leave` in player 2's score bar, with a confirmation | Player 2's score bar sits at the edge away from the seam in every seating. |
| Game survives fold, unfold, rotate | `DuelModel` lives in `RootView`, above the split | Layout changes never recreate the game. Fold and unfold with a round running are not yet checked (unverified). |
| No accidental exits mid-game | `DuelScreen` | [`persistentSystemOverlays(.hidden)`](https://developer.apple.com/documentation/swiftui/view/persistentsystemoverlays(_:)), [`defersSystemGestures(on: .all)`](https://developer.apple.com/documentation/swiftui/view/deferssystemgestures(on:)), [`isIdleTimerDisabled`](https://developer.apple.com/documentation/uikit/uiapplication/isidletimerdisabled). |
| One haptic per hit or miss, and a switch | `PlayField`, `HomeView` | [`sensoryFeedback(_:trigger:condition:)`](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:condition:)) on per-player counters, so each event plays once. The whole phone vibrates, so both players feel every haptic; the Haptics switch on the home screen turns them off (`duo-shared-screen` rule 7). |
| VoiceOver | `TargetView`, each half a labelled container | The target is a button with an [accessibility action](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(_:_:)) that counts as a tap on its centre. |

## 4. Customise the game

Change the rules first, in `Engine/Duel.swift`, and test them on the Mac before you touch a view.

- **Tune it:** change `DuelRules` defaults (goal, countdown, lockout, time limit, target size). Keep `minTargetRadius` at 22 or more, so targets stay at least 44 pt across.
- **New game, same frame:** keep `Player`, `Phase`, `toggleReady`, `tick` and `canTap`. Replace what `tap(_:at:in:now:)` does and what `spot(for:)` returns. Keep the file Foundation only and every type `nonisolated` and `Sendable`.
- **Add a test for every rule** in `Tools/EngineTests/main.swift` with `check(_:_:)`. Pass explicit dates (`at(1.5)`) instead of sleeping.
- **Looks:** `TargetView`, `ScoreBar`, `ReadyPanel` and `ResultPanel` in `Duel/PlayerHalf.swift`; player colours in `Player.tint` (`DuelScreen.swift`).
- **Drag games:** put a `DragGesture(minimumDistance:coordinateSpace:)` on the touch surface instead of the tap. Code: [architecture.md](references/architecture.md#drag-instead-of-tap).
- **Taking turns:** gate by turn in the engine. Code: [architecture.md](references/architecture.md#taking-turns).

Keep these, whatever the game:

1. `EvenSplit` for the halves, never `ArrangementView`.
2. The touch surface as a clear layer *beside* the content, never a gesture plus `.contentShape` on a container that holds a positioned accessibility element. *Measured:* with `.contentShape(Rectangle())` and the tap gesture on the field, the target's accessibility frame became the whole field (382 × 261 pt instead of 56 × 56), so UI tests tapped the middle of the field and every hit counted as a miss. VoiceOver would outline the whole field too.
3. `.contentShape(.interaction, Rectangle())` on each half, with no gesture there, so nothing that grows past a half takes the other player's taps. `.clipped()` only hides it.
4. Non-interactive overlays (target, countdown, banners) get `.allowsHitTesting(false)`, so touches reach the touch surface and the engine judges them.
5. Accessibility modifiers inside the view, then `.position`.
6. Accessibility identifiers `p1.*` and `p2.*`, so tests address a player, not a screen position.
7. A play field never mirrors: keep `PlayField` left-to-right, and give text panels the reader's direction.

## 5. Test it

**On the Mac:** `Tools/run-engine-tests.sh` builds `Engine/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`, like the app target. One check runs the engine in `Task.detached` and uses every engine type, so a type that loses `nonisolated` stops compiling (*measured* for all 13 types). Add a line to that check for each new engine type. *Measured:* 63 checks, under 10 seconds.

**On the simulator:** `Tools/run-ui-tests.sh`. The tests:

- start from launch switches (`-openDuel`, `-autoReady`, `-goal`, `-countdown`, `-lockout`, `-timeLimit`, `-seed`, `-faceToFace`); a later switch overrides an earlier one;
- find elements by identifier and tap through `element.coordinate(withNormalizedOffset:)` ([doc](https://developer.apple.com/documentation/xcuiautomation/xcuielement/coordinate(withnormalizedoffset:)));
- never depend on the pose or orientation;
- take turns, because XCUITest makes its own touches one at a time and has no call that presses two elements at once (its multi-finger calls, such as [`twoFingerTap()`](https://developer.apple.com/documentation/xcuiautomation/xcuielement/twofingertap()), act on one element). Device Hub can't send a two-finger touch either ([Xcode 27 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes)).

The script passes `-parallel-testing-enabled NO` (otherwise `xcodebuild` may clone the Duo simulator, and a fresh clone can take minutes to boot) and `-collect-test-diagnostics never` (*measured:* a failing run took 720 s with diagnostics on and 138 s with them off, for about 120 s of tests). For a simulator on an older iOS runtime, pass `DESTINATION="id=<UDID>"`.

*Measured:* all ten pass on the closed Duo simulator (iOS 27.1). On an iPhone 17 simulator on iOS 26.2, which runs the pre-27.1 branch of the reserved-region check, a rotation check turned the app: the fields went side by side, the score survived the turn, and face to face each half turned a quarter toward the seam and scored, left-to-right and right-to-left.

*Measured on the closed Duo simulator:* setting `XCUIDevice.shared.orientation` reported the new orientation, but the app did not turn. Set pose and rotation in Device Hub, then run `testBothHalvesShowInThisPose` once per pose:

```bash
Tools/run-ui-tests.sh -only-testing:DuelTapUITests/DuelTapUITests/testBothHalvesShowInThisPose
```

It checks the split follows the window's long side, the two play fields match, and the target's frame is the circle. It saves a screenshot of each display to the result bundle; the display not in use is black.

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-engine-tests.sh` prints `0 failed`.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] The app launched on the Duo simulator; you looked at the screenshot of the display in use.
- [ ] `Tools/run-ui-tests.sh` passes.
- [ ] In Device Hub, for Closed, Partially Open and Open, upright and sideways: both halves show, no target sits on the fold, `testBothHalvesShowInThisPose` and `testTurnedHalfStillScores` pass.
- [ ] Right to left: launch with `-AppleTextDirection YES -NSForceRightToLeftWritingDirection YES`; player 1 keeps the top or left half, text reads right to left, and hits still count.
- [ ] Every new rule has a check in `Tools/EngineTests/main.swift`.
- [ ] Touch surface beside the content; overlays don't take hits; targets keep their own accessibility frame.
- [ ] Two real people played it on a device, both touching at once (the simulator can't).
