---
name: duo-migrate
description: "Moves an existing iOS app that already ships onto iPhone Duo, Apple's foldable, step by step: from an app built with Xcode 26 (iOS 26 SDK) or Xcode 27.0 to a build with Xcode 27.1 and the iOS 27.1 SDK. Use when an app shows up centred with empty space around it on the open iPhone Duo, when a UIKit app built with the new SDK crashes at launch because it has no scene life cycle (no UIApplicationSceneManifest, no configurationForConnecting, UIWindow(frame:) in didFinishLaunching), when replacing UIScreen.main, device orientation, userInterfaceIdiom, regular width treated as iPad, hard-coded device sizes or UIRequiresFullScreen, when toolbars and tab bars turn vertical after the rebuild, when moving CI off an older Xcode, or when planning for the April 2027 App Store rules (iOS 27 SDK or later, iOS 15 or later)."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-migrate

Take an app that ships today and make it right on iPhone Duo, in an order where each step can be checked before the next: where the app stands, what stops it launching, the rebuild, the code Apple warns against, what the new SDK changes on its own, and the proof.

Load other skills for the detail of each fix: `duo-start` (it detects the SDK, the stack and the deployment target; run it first), `duo-lint` (finds the patterns), `duo-layout` (sizes, the fold), `duo-navigation` (vertical bars), `duo-continuity` (state through a fold), `duo-scenes` (windows, Split View), `duo-testing` and `duo-pose-matrix` (the proof).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 23 October 2026; details in [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline.

## What people see today

The SDK an app is built with decides how it looks on iPhone Duo, before any code change ([prepare page](https://developer.apple.com/iphone-duo/prepare/), [Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/)):

| Built with | Open (inner display) | Closed (outer display) |
|---|---|---|
| iOS 26 SDK or older (Xcode 26) | An iPhone-sized window in the middle, empty space around it | Content beside the status bar and camera |
| iOS 27 SDK (Xcode 27.0) | Fills most of the display, but keeps clear of the status bar on the right edge | Apple doesn't say |
| iOS 27.1 SDK (Xcode 27.1) | Edge to edge; toolbars and tab bars can turn vertical below the status bar | Edge to edge |

So the first visible win is the rebuild. The rebuild also changes layout with no code change (the vertical bars), which is why Apple asks you to check content against vertical bars before shipping a 27.1 build.

## Rules

- One change at a time: the SDK first, then the code. Build, run and lint after each step, so a regression has one cause.
- Never switch the Mac's default Xcode. Prefix commands with `DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer`, and never run `sudo xcode-select`.
- Keep the deployment target the user ships with. Wrap iOS 27.1 APIs in `if #available(iOS 27.1, *)`. Raising the target is the user's call.
- Removing `UIRequiresFullScreen` is not the fix by itself. The app resizes on iPhone Duo with or without it; the fix is a layout that resizes.
- Silence a duo-lint finding only for code that is not layout, with a reason. Never to get a clean run.
- Report before and after in the user's words: what people saw, what they see now, what you could not check.

## Step 1. Know where the app stands

Run duo-start's detection script (`duo-start`, `references/detect.md`). Write down five things before touching anything:

1. **The SDK it ships with**: the CI pin first, then `DTSDKName` in the last build, then the default Xcode.
2. **The deployment target** (`IPHONEOS_DEPLOYMENT_TARGET`).
3. **The life cycle**: a SwiftUI `App`, a UIKit app with a scene delegate, or a UIKit app with no scenes.
4. **`UIRequiresFullScreen`**, in the Info.plist or as `INFOPLIST_KEY_UIRequiresFullScreen`.
5. **Mac Catalyst** (`SUPPORTS_MACCATALYST`), because some iOS 27.1 APIs need a compile-time guard there.

Then tell the user which row of the table above their users see today.

## Step 2. Make it launch on the new SDK

From iOS 27, a UIKit app built with the latest SDK must adopt the scene life cycle, or it fails to launch ([Transitioning to the UIKit scene-based life cycle](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle)). Two signs it hasn't: no `UIApplicationSceneManifest` with a configuration in the Info.plist, and no `application(_:configurationForConnecting:options:)` in the app delegate. Older systems already log a console message for such apps (from iOS 18.4, reworded in iOS 26). SwiftUI apps that use the `App` protocol already have scenes; skip to Step 3.

*Measured:* a UIKit app with no scene manifest and no `configurationForConnecting`, built with Xcode 27.1, stopped 3.8 s after launch on the iPhone Duo simulator: `EXC_BREAKPOINT`, raised inside UIKit's check for apps that have not adopted scenes. The same app with a scene delegate launched and kept running.

The move, in short (full code and the mapping of app-delegate callbacks in [references/fixes.md](references/fixes.md#adopt-the-scene-life-cycle)):

1. Add a scene manifest (`UIApplicationSceneManifest`) to the Info.plist, or let Xcode generate it (`INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES`).
2. Name your scene delegate class: in the manifest's scene configuration, or by returning a `UISceneConfiguration` from `application(_:configurationForConnecting:options:)`.
3. Move the window from `application(_:didFinishLaunchingWithOptions:)` to `scene(_:willConnectTo:options:)`, created with `UIWindow(windowScene:)`. `UIWindow(frame:)` is deprecated since iOS 26.
4. Move foreground and background work from the app delegate to the scene delegate (`sceneDidBecomeActive(_:)`, `sceneDidEnterBackground(_:)` and the rest). Once the app has scenes, UIKit stops calling the app delegate's versions. For the state of the whole app, across scenes, observe `UIApplication` notifications such as `willEnterForegroundNotification`.

Apple's App Resizability skill in Xcode 27.1 can do this conversion; `duo-start` (`references/routing.md`, "Apple's skills in Xcode 27.1") says how to run it next to Duology.

## Step 3. Rebuild with Xcode 27.1

Build locally first, on the shared iPhone Duo simulator:

```bash
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
  xcodebuild -project MyApp.xcodeproj -scheme MyApp \
  -destination "id=<UDID of the iPhone Duo simulator>" build
```

- Fix new errors before anything else. Don't count on warnings to find the rest: Xcode 27.1 flags `UIScreen.main` and `UIWindow(frame:)` as deprecated only when the deployment target is iOS 26 or later. With an iOS 16 target, the same code built without a warning (*measured*). duo-lint finds them at any target (Step 4).
- Then move the CI to the same Xcode. The detection script names the file that pins the old one (`.xcode-version`, a workflow's `DEVELOPER_DIR` or `xcode-version`, fastlane). The path of Xcode 27.1 on a hosted runner depends on its image; read the runner's list of installed Xcodes rather than guessing. Xcode Cloud picks its Xcode in the workflow settings, not in the repo.
- Open the app on the iPhone Duo simulator, closed and open, before changing code. Note what moved: that is what the SDK changed by itself.

## Step 4. Find the patterns

Apple groups what to remove into a few patterns ([prepare page](https://developer.apple.com/iphone-duo/prepare/)). Two tools find them: Apple's App Resizability skill, which Apple says finds most issues but not all, and `duo-lint`, which flags them in seconds without the model reading the codebase:

| Apple's pattern | duo-lint | Where the fix lives |
|---|---|---|
| Sizing from the main screen | DUO001 | [fixes.md](references/fixes.md#size-from-the-window-not-the-screen), `duo-layout` |
| Layout from device orientation | DUO002, DUO003 | [fixes.md](references/fixes.md#shape-not-orientation) |
| Idiom or size class as a device check | DUO004, DUO005 | [fixes.md](references/fixes.md#space-not-device), `duo-layout` |
| Checks for known device sizes | DUO006, DUO007, DUO009 | [fixes.md](references/fixes.md#space-not-device), `duo-layout` |
| `UIRequiresFullScreen` | DUO008 | [fixes.md](references/fixes.md#uirequiresfullscreen) |
| Full-bleed images and video cropped on wide windows | not linted: search for `.scaleAspectFill` and `contentMode: .fill` | [fixes.md](references/fixes.md#full-bleed-media) |

Run duo-lint from the app's folder (`duo-lint`) and keep its report as the list for Step 5.

## Step 5. Fix, in this order

1. **Launch blockers** (Step 2), if any are left.
2. **duo-lint errors**: deprecated APIs. Each one is a crash or a wrong size waiting for a fold.
3. **duo-lint warnings**: one rule at a time, build and re-run duo-lint after each rule.
4. **Full-bleed media** found by the search above.

Use the size of the view or window you are in, never the screen's, and read it again whenever it changes: a fold changes it while the app runs. The before-and-after code for each pattern, UIKit and SwiftUI, is in [references/fixes.md](references/fixes.md).

## Step 6. What the new SDK changes on its own

These need no lint finding to break; check them on the rebuilt app:

- **Vertical bars.** Toolbars and tab bars can move to the side under the status bar. Content and custom controls must leave room for them (`duo-navigation`).
- **State through a fold.** A fold resizes the window while the app runs. Anything a layout switch rebuilds loses its state (`duo-continuity`). Pushing a screen when the phone is closed and popping it during the unfold animation left stale insets in our recipes (*measured* there; `duo-continuity`, `references/swiftui.md`).
- **Split View and windows.** Every app takes part in Split View on the inner display, and only the inner display can open a new window (`duo-scenes`).
- **Regular width on a phone.** Open, iPhone Duo reports regular width and regular height. Code that meant "iPad" by "regular" now runs on a phone.

## Step 7. Prove it

- `duo-lint` reports 0 findings, or only findings silenced with a reason.
- The app builds and its tests pass on the iPhone Duo simulator (`duo-testing`).
- Screenshots closed, open, in book pose and in tabletop (`/duo-poses`, `duo-pose-matrix`), compared with the screenshots from Step 3.
- Apple also suggests resizing tests in Device Hub's resizable simulator and in iPhone Mirroring on macOS 27, at extreme sizes both ways ([prepare page](https://developer.apple.com/iphone-duo/prepare/)).
- On a real iPhone Duo: the hinge, 120 Hz resizing and the camera. Say so if no device was available (*unverified* here).

## Deployment target and the App Store

- iPhone Duo always runs iOS 27.1 or later, so iOS 27.1 APIs behind `#available` are safe on it, and the fallback serves older iPhones.
- From April 2027, App Store uploads must be built with the iOS 27 SDK or later and target iOS 15 or later ([Submitting](https://developer.apple.com/app-store/submitting/)). That floor gives the iOS 27 behaviour in the table above, not the full 27.1 layout.
- iPhone Duo screenshots in App Store Connect add a badge to the product page saying the app is optimized for iPhone Duo ([prepare page](https://developer.apple.com/iphone-duo/prepare/)). Apple's news of 5 October 2026 says Duo screenshots will be required from April 2027 ([news](https://developer.apple.com/news/?id=kkphp5qo)).

## Report to the user

```text
Before: built with <SDK>, so on iPhone Duo people saw <row of the table>.
Launch: <scene life cycle adopted | already had scenes>.
Rebuild: Xcode 27.1 locally and in CI (<file changed>).
Fixed: <n> duo-lint findings (<rules>), <media fixes>. Silenced: <finding, reason> or none.
Checked: <build, tests, poses, Split View>. Not checked: <real device, …>.
Deployment target: <unchanged | changed, at the user's request>.
```

## Checklist

- [ ] The SDK, deployment target, life cycle, `UIRequiresFullScreen` and Catalyst are written down before any change.
- [ ] A UIKit app has a scene manifest, a scene delegate and `UIWindow(windowScene:)`; it launches on the iPhone Duo simulator.
- [ ] The app builds with Xcode 27.1 locally and in CI; the old Xcode pin is gone.
- [ ] duo-lint reports 0 findings, or each one left is silenced with a reason.
- [ ] Full-bleed images and video were checked on the wide inner display.
- [ ] Vertical bars, state through a fold and Split View were checked on the rebuilt app.
- [ ] Screenshots in each pose, before and after, are in the report.
- [ ] The deployment target is unchanged unless the user asked.
