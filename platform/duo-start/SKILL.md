---
name: duo-start
description: Entry point for iPhone Duo, Apple's foldable with an outer display, an inner display and a fold; use it first when someone asks to get an app ready for iPhone Duo, make it work on the foldable or survive fold and unfold, or doesn't know which Duology skill to load. It detects SwiftUI or UIKit, new or existing app, the Xcode and iOS SDK the app builds with (iOS 26, 27 or 27.1 behaviour on Duo), the deployment target and the UIKit scene life cycle, runs a five-minute first pass (Xcode 27.1 build, duo-lint, closed and open on the iPhone Duo simulator in Device Hub) and routes to duo-setup, duo-layout, duo-navigation, duo-continuity, duo-scenes, duo-patterns, the design skills (duo-design-system, duo-postures, duo-transitions, duo-ergonomics, duo-accessibility), the iOS 27 feature skills in duology-features, duo-testing, duo-pose-matrix, duo-lint, the recipes and Apple's App Resizability skill (xcrun agent skills export).
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-start

Use this skill before any other Duology skill. It answers three questions about the app, runs a short first pass, and tells you which skill to load next. Don't fix anything until the first pass is reported.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 16 or 17 Oct 2026. *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline. Full list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Rules

1. Build with Xcode 27.1 through `DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer`. Never run `sudo` or `xcode-select -s`. Don't change the Mac's default Xcode.
2. Detect first, then route. Don't guess the stack from the README.
3. Never pick a layout by device model, `userInterfaceIdiom`, orientation or screen size. Use size classes and the space the view has ([Apple's prepare page](https://developer.apple.com/iphone-duo/prepare/)).
4. `simctl` and `devicectl` in Xcode 27.1 have no pose command (*measured*). Ask the user to click the pose buttons in Device Hub. A tool can press those buttons through the macOS Accessibility API, but only after the user gives the app that runs you Accessibility permission. See `duo-setup`.
5. Let Apple's App Resizability skill do the generic resizing fixes. Use Duology for the fold, the two displays and the design. Don't redo one with the other.
6. If the deployment target is below iOS 27.1, wrap every iOS 27.1 API in `if #available(iOS 27.1, *)`.

## Step 1: Answer three questions

Run the detection script in [references/detect.md](references/detect.md) from the repo's root folder. It is read-only. The short version:

```bash
# Existing app? Look three levels down: many repos keep it in ios/, App/ or apps/ios/.
find . -maxdepth 3 \( -name .git -o -name Pods -o -name .build -o -name node_modules \) -prune \
  -o \( -name '*.xcworkspace' -o -name '*.xcodeproj' \) -print -prune -o -name Package.swift -print
grep -rlE --include='*.swift' ':[[:space:]]*App[[:space:]]*\{' .  # SwiftUI App entry point
grep -rlE --include='*.swift' 'UIApplicationDelegate|UIWindowSceneDelegate' .
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
  xcodebuild -project <path/App.xcodeproj> -scheme <Scheme> \
  -destination 'generic/platform=iOS Simulator' -showBuildSettings \
  | grep -E '^ *(SDK_VERSION|IPHONEOS_DEPLOYMENT_TARGET|SWIFT_VERSION|SUPPORTS_MACCATALYST) = '
```

Use `-workspace <path/App.xcworkspace>` instead when `find` prints a workspace next to the project (CocoaPods).

### 1. New or existing?

- An `.xcodeproj` or `.xcworkspace` here or up to three levels down: an existing app. Note its folder. Run the first pass from there, or pass its path with `-project` or `-workspace`.
- Swift or Objective-C files but no project: still existing. Ask the user how they build it (a Swift package, XcodeGen or Tuist). Never treat it as new.
- No project and no source files: a new app. Go to [New app](#new-app).
- A project with only template code ("Hello, world!") counts as new too.
- Flutter (`pubspec.yaml`), React Native (`"react-native"` in `package.json`) or Capacitor (`capacitor.config.*`): Duology covers native SwiftUI and UIKit only. Point the user to [mirzaaghazadeh/iphone-duo-skills](https://github.com/mirzaaghazadeh/iphone-duo-skills), which covers those stacks.

### 2. SwiftUI or UIKit?

| Signal | Verdict | Load first |
|---|---|---|
| A `struct ...: App` entry point | SwiftUI app | SwiftUI sections of each skill |
| SwiftUI `App` plus `UIViewControllerRepresentable` | SwiftUI with UIKit parts | SwiftUI, then the UIKit notes for those parts |
| `UIApplicationDelegate` with `UIWindowSceneDelegate` | UIKit app | UIKit sections of each skill |
| UIKit plus `UIHostingController` | UIKit with SwiftUI screens | UIKit for the shell, SwiftUI for the hosted screens |
| `UIApplicationDelegate` and no scene delegate, no `UISceneConfigurations` | UIKit app **without scene life cycle** | Blocker, see below |

**Blocker: UIKit without scenes.** Apple's [scene life cycle article](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle) says that from iOS 27, an app built with the latest SDK must adopt the scene-based life cycle or it fails to launch. The [WWDC26 UIKit talk](https://developer.apple.com/videos/play/wwdc2026/278/) says the same. Fix this before anything else. Apple's App Resizability skill can do the migration (Step 4).

### 3. Which SDK does the app build with?

The SDK decides how the app looks on iPhone Duo, before you change a line of code ([prepare page](https://developer.apple.com/iphone-duo/prepare/), [Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/)):

| Built with | Open (inner display) | Closed (outer display) |
|---|---|---|
| iOS 26 SDK or earlier (Xcode 26) | Familiar iPhone size, centred, empty space around it | Content to the left of the status bar and camera |
| iOS 27 SDK (Xcode 27) | Fills most of the display, still clear of the status bar on the right edge | Apple doesn't say |
| iOS 27.1 SDK or later (Xcode 27.1) | Edge to edge; toolbars and tab bars can go vertical | Edge to edge; bars vertical |

Find the SDK the app *ships* with, not only the one on this Mac:

- `SDK_VERSION` from the build settings above, run with the Xcode the team really uses.
- The CI pin: `.xcode-version`, `xcode-version:` or `DEVELOPER_DIR` in `.github/workflows`, `fastlane`, `ci_scripts`. The script greps for these.
- A built app or archive: `plutil -extract DTSDKName raw <App>.app/Info.plist` prints, for example, `iphonesimulator27.1` (*measured*). `DTXcodeBuild` gives the Xcode build, such as `27A9275`.

Also note:

- **Deployment target.** Below 27.1, gate Duo APIs (example below). iPhone Duo ships with iOS 27.1, so the fallback is the layout the app ships today.
- **Mac Catalyst.** If `SUPPORTS_MACCATALYST = YES`, iOS 27.1-only APIs fail to compile for Catalyst. Wrap them in `#if !targetEnvironment(macCatalyst)` ([Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)).
- **`UIRequiresFullScreen`.** It doesn't stop resizing. Tech Talk 111461 says the app still resizes when the phone opens or closes, and Apple deprecated the key in iOS 26 ([TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key)).
- **App Store dates.** From April 2027, uploads need the iOS 27 SDK or later ([news](https://developer.apple.com/news/?id=k1mtkt1k)), and iPhone Duo screenshots become required ([news](https://developer.apple.com/news/?id=kkphp5qo)). Apple's pages differ on which apps the screenshot rule covers; plan for all of them.

```swift
import SwiftUI

// Gate every iOS 27.1 API when the deployment target is lower.
// The navigation container wraps the gate, so both branches keep their bar.
struct PlayerScreen: View {
    var body: some View {
        NavigationStack {
            Group {
                if #available(iOS 27.1, *) {
                    ArrangementView {
                        PlayerView()
                    } secondary: {
                        UpNextView()
                    }
                } else {
                    PlayerView()   // what the app ships today
                }
            }
            .navigationTitle("Now Playing")
        }
    }
}
```

This is the supporting-pane pattern from `duo-patterns`, shaped like `duo-layout`'s `NowPlayingScreen`. Keep navigation containers outside the arrangement, never inside it (`duo-layout`). For list-detail, use `NavigationSplitView`, not `ArrangementView` (`duo-patterns`). With the phone closed and held sideways, `ArrangementView` shows only the primary view (*measured* in `duo-layout`), so the pane needs another way in. Read `duo-patterns` and `duo-layout` before you pick a layout.

## Step 2: Route to the right skill

Duology skills. Load the one that matches the task. Full map with symptoms: [references/routing.md](references/routing.md).

| Skill | Plugin | Load it when |
|---|---|---|
| `duo-start` | duology | You don't know where to begin (this skill). |
| `duo-setup` | duology | Xcode 27.1 sits next to an older Xcode, the Duo simulator is missing, or Xcode's agent connection (`xcrun mcpbridge`) fails. |
| `duo-layout` | duology | Content lands in the fold, a screen breaks on one display, or you need size classes, safe areas, reserved regions or `ArrangementView`. |
| `duo-navigation` | duology | Toolbars and tab bars go vertical, tabs should become a sidebar, sheets sit in the wrong place, items vanish into overflow. |
| `duo-continuity` | duology | Scroll, playback, typed text, selection or navigation resets on fold, unfold, rotate or resize. |
| `duo-scenes` | duology | The app opens a second window, runs in Split View, or shows something on the outer display while the camera runs on the inner one. |
| `duo-patterns` | duology-design | You need to choose a layout: list-detail, supporting pane, two-page, dual view, extended canvas, feed reflow. |
| `duo-design-system` | duology-design | You set up spacing, grids, type, Liquid Glass, corners, colours or touch targets for both displays. |
| `duo-postures` | duology-design | A screen must work half folded: book pose, tabletop media or video call, or a hinge effect. |
| `duo-transitions` | duology-design | A screen flashes, jumps or moves its controls when the phone opens or closes. |
| `duo-ergonomics` | duology-design | You decide where primary actions and floating controls go so hands reach them. |
| `duo-accessibility` | duology-design | VoiceOver order across panes, Dynamic Type on the outer display, Reduce Motion, keyboard and contrast. |
| `duo-shared-screen` | duology-design | Two people use one phone: games, teaching, showing a customer. |
| `duo-design-review` | duology-design | You review screenshots or Figma frames against the Duo checklist. |
| `duo-intelligence` | duology-features | The app uses Foundation Models: an AI pane when open, a short summary when closed. |
| `duo-app-intents` | duology-features | Siri, Shortcuts or the Action button must open the right pane or window. |
| `duo-camera` | duology-features | The app captures photos or video, or shows a camera preview, on either display or in tabletop. |
| `duo-media` | duology-features | Video or audio must keep playing through fold and unfold; tabletop player, Picture in Picture. |
| `duo-reading` | duology-features | Books and documents: two facing pages, the reader's place kept through a fold, notes beside the text. |
| `duo-games` | duology-features | A game must fill every pose, with touch controls off the fold. |
| `duo-swiftui-27` | duology-features | The app adopts iOS 27 SwiftUI: reordering, swipe actions on any view, the `@State` macro, toolbar minimizing. |
| `duo-system-surfaces` | duology-features | Widgets, Live Activities, StandBy or Controls must look right on both displays. |
| `duo-testing` | duology-ship | You write unit or UI tests that must hold up on the Duo simulator. |
| `duo-pose-matrix` | duology-ship | You need screenshots of the app closed, open, in book pose and in tabletop. |
| `duo-lint` | duology-ship | You need to find code Apple warns against before it ships. |
| `recipe-two-player-game` | duology-recipes | You build a two-player game on one phone from scratch. |
| `recipe-finance-dashboard` | duology-recipes | You start a personal finance or dashboard app. |
| `recipe-media-player` | duology-recipes | You start a video or podcast player. |
| `recipe-reader` | duology-recipes | You start an e-book or document reader. |
| `recipe-shop` | duology-recipes | You start a shop with in-app purchases. |
| `recipe-kids-learning` | duology-recipes | You start a learning app for young children, with a parental gate and nothing tracked. |

Commands: `/duo-doctor` (check the setup), `/duo-new <recipe>` (new app from a recipe), `/duo-audit` (lint plus checklist, most serious first), `/duo-poses` (screenshot every pose), `/duo-review` (design review of screenshots by the `duo-design-reviewer` agent).

If a skill isn't installed, tell the user the plugin to add, for example `/plugin install duology-design@duology`. On other agents: `npx skills add Kimeur/duology --skill <name>`.

**Coming.** Say "coming" and use the Apple source listed in [references/routing.md](references/routing.md) until then: `duo-performance`, `/duo-ship` and the last two recipes, all planned for v1.0. For an app that ships today on an older SDK, load `duo-migrate`; for Duo screenshots and the submission, `duo-app-store` (both `duology-ship`).

## Step 3: The five-minute first pass (existing app)

Goal: a short report, not fixes. Details, logger code and the report template: [references/first-pass.md](references/first-pass.md). Run each code block below as one command, and keep its first line: agent shells often drop `export` and variables between calls, and a plain `xcrun` or `xcodebuild` would use the Mac's default Xcode.

1. **Build with Xcode 27.1.** Use the iPhone Duo simulator as the destination (*measured*: it appears as `name:iPhone Duo, OS:27.1`).

   ```bash
   export DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer
   xcodebuild -scheme <Scheme> \
     -destination 'platform=iOS Simulator,name=iPhone Duo,OS=27.1' \
     -derivedDataPath "$TMPDIR/duo-first-pass" build 2>&1 | grep -E 'error:|BUILD (SUCCEEDED|FAILED)'
   ```

   Run it from the folder that holds the project (Step 1 prints it). Use `-workspace <Name>.xcworkspace` when the app has one. Count the errors; don't fix them yet. If Xcode 27.1 or the simulator is missing, stop and load `duo-setup` (or run `/duo-doctor`).

2. **Run duo-lint.** Load the `duo-lint` skill and run it on the app's sources. If it isn't installed, run the rough grep in [references/first-pass.md](references/first-pass.md#no-duo-lint-yet). Keep the top findings.

3. **Run it on the Duo simulator.**

   ```bash
   export DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer
   APP="$TMPDIR/duo-first-pass/Build/Products/Debug-iphonesimulator/<App>.app"
   BUNDLE=$(plutil -extract CFBundleIdentifier raw "$APP/Info.plist")
   xcrun simctl boot "iPhone Duo" 2>/dev/null    # fine if it is already booted
   xcrun simctl install booted "$APP"
   xcrun simctl launch --terminate-running-process --stderr="$HOME/Library/Caches/duo-first-pass.log" booted "$BUNDLE"
   ```

   Keep the log in the home folder. *Measured:* `--stderr` into `$TMPDIR` or `/tmp` wrote nothing. The first simulator launch with Xcode 27.1 can take several minutes (a known issue in the release notes).

4. **Check open, then closed.** Screenshot both displays. The display that is off comes out solid black (*measured* with the phone open; the closed case is unverified).

   ```bash
   export DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer
   xcrun simctl io booted screenshot --display=primary   "$TMPDIR/duo-outer.png"   # outer display
   xcrun simctl io booted screenshot --display=primary-1 "$TMPDIR/duo-inner.png"   # inner display
   ```

   Then ask the user: "In Device Hub, click **Closed** (the pose buttons sit under the bezel). Tell me when it's done." Take the screenshots again. Repeat with **Partially Open** if time allows ([Device Hub article](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)). If the user asks you to script the poses and has given Accessibility permission to the app that runs you, `duo-pose set closed` from `duo-pose-matrix` presses the button instead; it refuses while UI tests share the simulator. Look for: empty space around the app, clipped or stretched content, controls in the fold, lost scroll or typing, bars that look wrong.

5. **Report and route.** Fill the template in [references/first-pass.md](references/first-pass.md#report). Map each problem to one skill from Step 2. For a deeper audit, run `/duo-audit`.

## Step 4: Use Apple's App Resizability skill for generic resizing

Xcode 27.1 ships a skill called App Resizability (it was the app modernization skill in Xcode 27). It covers SwiftUI and iPhone Duo ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/)) and fixes the generic patterns: main-screen reads, orientation and idiom checks, safe-area assumptions and the move to the UIKit scene life cycle ([WWDC26 session 278](https://developer.apple.com/videos/play/wwdc2026/278/), [prepare page](https://developer.apple.com/iphone-duo/prepare/)).

- **Inside Xcode:** ask Xcode's coding assistant to "get my app ready for iPhone Duo".
- **In Claude Code or another agent:** ask the user before you export; it changes their setup. Export to `~/xcode-skills`, the same folder `duo-setup` uses, outside any repo:

  ```bash
  DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
    xcrun agent skills export --output-dir ~/xcode-skills
  ```

  *Measured:* it opened Xcode, took about two minutes and wrote 10 skills, one folder per skill name ([references/routing.md](references/routing.md#apples-skills-in-xcode-271)). Add `--replace-existing` to overwrite an older export. Don't export into `~/.claude/skills`: that loads all 10 in every Claude Code session. To load only App Resizability in Claude Code, copy its folder once the user agrees: `cp -R ~/xcode-skills/app-resizability ~/.claude/skills/`. For another agent, point it at `~/xcode-skills/app-resizability/SKILL.md`. Never copy Apple's skill text into the app's repo.

- **Order.** App Resizability triggers on the same request as this skill (getting an app ready for iPhone Duo), and its instructions treat that request as a call to run every task on its list. If both load, this skill goes first: finish Steps 1 to 3 and report. Run App Resizability here, at Step 4, after the user has seen the report.

Apple says the skill finds most issues, not all. Run `duo-lint` after it to catch the rest.

## New app

1. Run `/duo-doctor`, or load `duo-setup`, so Xcode 27.1 and the Duo simulator are ready.
2. A two-player game, a finance dashboard, a media player, a reader, a shop or a learning app for young children: run `/duo-new <recipe>` with `recipe-two-player-game`, `recipe-finance-dashboard`, `recipe-media-player`, `recipe-reader`, `recipe-shop` or `recipe-kids-learning`.
3. Anything else: ask the user to create a SwiftUI app in Xcode 27.1 (File > New > Project > iOS App). Then load `duo-patterns` to pick a layout, `duo-layout` and `duo-navigation` to build it, `duo-continuity` to keep state, and `duo-testing` to test it.
4. Ask the user which deployment target they want. iOS 27.1 removes every availability check but drops older iPhones. A lower target keeps them and needs the gate from Step 1. From April 2027 the App Store floor is iOS 15 ([Submitting](https://developer.apple.com/app-store/submitting/)).

## Checklist

- [ ] New or existing app decided; cross-platform apps pointed to the right repo.
- [ ] SwiftUI, UIKit or mixed decided from code, not from the README.
- [ ] UIKit apps checked for the scene life cycle; a missing one reported as a blocker.
- [ ] Shipping SDK found (build settings, CI pin or `DTSDKName`) and its Duo behaviour stated.
- [ ] Deployment target noted; iOS 27.1 APIs gated if it is lower; Catalyst noted.
- [ ] Built with Xcode 27.1 for `iPhone Duo, OS=27.1`; errors counted, not fixed.
- [ ] `duo-lint` (or the rough grep) run; top findings kept.
- [ ] App checked open and closed in Device Hub, with screenshots of both displays.
- [ ] App Resizability skill offered for the generic fixes.
- [ ] Report written; each problem mapped to one skill; coming skills marked "coming".
