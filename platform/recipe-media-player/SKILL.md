---
name: recipe-media-player
description: "Creates a complete SwiftUI video and podcast player for iPhone Duo, Apple's foldable: a library list-detail, a full-screen player whose playback survives every fold, unfold and rotation, a tabletop layout (video above the fold, the same controls below), a book layout (video leading, controls trailing), Picture in Picture, an up next card, a mini player and background audio. Use when someone wants to start a new video, podcast, course or streaming app from scratch, or runs /duo-new recipe-media-player. For an existing player, use duo-postures (tabletop media) and duo-continuity instead. Covers one AVPlayer, AVPlayerLayer and AVPictureInPictureController owned above the layout switch, FoldRegionsLayout reading the .division reserved region, NavigationSplitView selection kept in a model, an up next card inside the controls so it never sits in the fold, a Foundation-only model tested on the Mac, bundled sample clips made with ffmpeg, and UI tests that work on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-media-player

This recipe makes a new Xcode project: a video podcast app for iPhone Duo. The library lists shows and episodes. An episode plays full screen. Close the phone, open it, fold it like a book or set it on a table half folded, and the video keeps playing from the same frame. Near the end of an episode, an "up next" card offers the next one.

The shows are sample content. The value is the frame around them: one player that no layout change can restart, one set of controls that moves to the right place in every pose, rules you can test on the Mac in seconds, and UI tests that pass on the Duo simulator.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 20 October 2026). *Unverified* means we could not check it. Everything else links to Apple. "Book" and "tabletop" are Duology's words for Apple's "partially folded, like a book" and "seated on a table like a laptop"; no API reports them. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists: use `duo-postures` (its tabletop media recipe) and `duo-continuity` (playback through a fold);
- the app is a reader with pages: use `recipe-reader`.

## 1. Create the project

`/duo-new recipe-media-player` runs steps 1 to 5. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools`, and not an Apple module name such as `SwiftUI` or `AVFoundation`;
   - a bundle id such as `com.example.fieldcast`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-media-player/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-media-player/scripts/new-project.sh" \
     FieldCast com.example.fieldcast ~/Developer/FieldCast
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths (the video clips are left alone), checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65), before it creates anything.
3. Test the rules on the Mac. Expect `0 failed`:

   ```bash
   cd ~/Developer/FieldCast && Tools/run-model-tests.sh
   ```

4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -project FieldCast.xcodeproj -scheme FieldCast \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Install, launch straight into the player, and screenshot the display in use. Use the UDID, not `booted`.

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl install <UDID> build/DerivedData/Build/Products/Debug-iphonesimulator/FieldCast.app
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.fieldcast -play small-repairs-1 -paused -start 4
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary build/outer.png     # closed
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary-1 build/inner.png   # open
   ```

   Only the display in use has content. Look at the PNG before you report.
6. Run the UI tests: `DESTINATION="id=<UDID>" Tools/run-ui-tests.sh`. A UI test brings the app to the front; tell the user first if they share the simulator.
7. Tell the user what passed, and that poses change only in Device Hub (the checklist below).

Set `DEVELOPER_DIR` for every `xcrun` and `xcodebuild` call when the Mac has more than one Xcode. Never run `xcode-select`.

## 2. What you get

| Path | What it holds |
|---|---|
| `<App>/Model/` | Catalogue, queue, up next policy, resume points, fold geometry, player regions, time text. Foundation and CoreGraphics only, every type `nonisolated` and `Sendable`. |
| `<App>/Player/PlayerModel.swift` | `@Observable` owner of the one `AVPlayer`, its `AVPlayerLayer` and the Picture in Picture controller. Time observer, end of episode, background audio, saving. |
| `<App>/Player/PlayerScreen.swift`, `PlayerControls.swift` | The player: `FoldRegionsLayout` with the video first and the controls second; the up next card inside the controls. |
| `<App>/Player/VideoSurface.swift` | A `UIViewRepresentable` that shows the model's layer and never makes its own; the AirPlay button. |
| `<App>/Library/` | `NavigationSplitView` of shows and episodes, the episode detail, the mini player, drawn artwork. |
| `<App>/Shared/` | `FoldRegionsLayout`, `onFoldChange`, test markers. |
| `<App>/Media/` | `Catalog.json` and six 12-second clips, 640 × 360, about 110 KB each. |
| `<App>/Info.plist` | Only `UIBackgroundModes` = `audio`; Xcode generates the rest. |
| `<App>UITests/` | Twelve UI tests, pose-agnostic. |
| `Tools/` | `run-model-tests.sh`, `ModelTests/main.swift`, `run-ui-tests.sh`. |

Project settings: iOS 26.0 deployment, Swift 6 language mode, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups with one exception (`Info.plist` is not a resource), iPhone and iPad, a privacy manifest that declares UserDefaults (reason CA92.1) for resume points. The scheme turns off parallel testing so `xcodebuild` doesn't clone the simulator.

Architecture, data flow and test details: [references/architecture.md](references/architecture.md). Sample clips, streams, Picture in Picture and background audio: [references/media.md](references/media.md).

## 3. How it behaves in each pose

| Pose | Library | Player | Up next card | Mini player |
|---|---|---|---|---|
| Closed (outer display) | Collapsed to one stack; side bars | Controls float at the bottom; the video moves up into the space above them | Inside the controls, button on its own row | Full width, bottom |
| Open, flat, held wide | Sidebar and detail | Controls float over the video, bottom centre | Inside the controls | Trailing side of the fold line |
| Book | The system evens the columns out at the fold | Video in the leading region, controls in the trailing region | Trailing, with the controls | Trailing region |
| Tabletop | Detail, sidebar behind its button | Video above the fold, the same controls below it | Below the fold | Full width, bottom region |

*Measured* for the player and the library in every row, with Device Hub's pose buttons pressed by `duo-pose`, and with one app process kept through closed, open, book, tabletop and closed again.

## 4. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| Playback survives every fold | `PlayerModel` is `@State` in `RootView`; the player screen is a `fullScreenCover` attached there | State below a layout switch is rebuilt; state above it isn't (`duo-continuity`). `RootView` never changes identity. |
| The video layer is never rebuilt | `PlayerModel.playerLayer`; `VideoSurface` only hosts it | A new layer would flash black. The `surfaces` test marker counts views made: *measured* 1 through a full pose sweep. |
| One layout for every pose | `FoldRegionsLayout` in `PlayerScreen`, geometry in `Model/FoldRegions.swift` | One `Layout` type, so both children keep their identity ([Layout](https://developer.apple.com/documentation/swiftui/layout)). An `if` on the fold would rebuild them. |
| Reading the fold | `onFoldChange` on the layout itself; `FoldGeometry(candidates:in:)` | [`reservedRegions(kind:options:layoutDirectionBehavior:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) with `.division` and `.includeInactive`, read in `onGeometryChange` because the first layout pass has no regions. There is no posture API ([api-index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#not-in-the-sdk)). |
| Tabletop: watch above, touch below | `FoldRegions.split` | Apple's one optional per-pose layout: media in the top half, the same controls in the bottom half ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=276)). |
| Nothing interactive in the fold | The up next card lives inside `PlayerControls` | It moves with the controls, so it is never on the fold's 40 pt frame. |
| The mini player avoids the fold | `FoldRegions.floatingBarSpan` | A bar across the open phone would put its buttons on the fold line. It reads the fold even while flat, so folding doesn't move it. |
| Library keeps its selection | `LibraryModel.selection`, one `NavigationSplitView` | The split view collapses closed and evens out at the fold on its own ([NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview)). Never swap it for a stack by size class. |
| Picture in Picture | `PlayerModel` creates `AVPictureInPictureController` from its own layer | The system pins the floating video to the top, and stretches it to half the screen when the phone is partly folded; the app below must cope with a shorter window ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=201)). |
| Sound in the background | `sceneMovedToBackground(_:)`, `Info.plist`, the playback category | iOS pauses a video whose layer is on screen; the model takes the player off its layer in the background ([media playback setup](https://developer.apple.com/documentation/avfoundation/configuring-your-app-for-media-playback)). |
| No autoplay on fold, no pause on fold | Nothing in the views starts or stops playback | Folding is not a request to play. No `onAppear` or `onDisappear` touches the player. |
| Screen stays on only while watching | `RootView` | [`isIdleTimerDisabled`](https://developer.apple.com/documentation/uikit/uiapplication/isidletimerdisabled) follows "playing and on screen". |

## 5. Customise

Change the catalogue and the rules first, then the look.

- **Your shows:** edit `Media/Catalog.json`. `media` is a bundled file name or an `https` URL (an HLS playlist works the same way). Run `Tools/run-model-tests.sh`: it checks every bundled file exists, IDs are unique and episodes are numbered.
- **Up next:** `UpNextPolicy.lead` (default 10 s, never more than half an episode) and `autoplay`. The library's options menu has the autoplay switch.
- **Looks:** `PlayerControls` (the glass panel), `Artwork` (swap for `AsyncImage` when you have image URLs), `EpisodeDetailView`.
- **Audio-only podcasts:** the item has no video track; show `Artwork` in `VideoFrame` instead of the surface. Code: [references/media.md](references/media.md#audio-only-episodes).
- **Lock Screen and Control Center:** publish Now Playing information and handle remote commands with the MediaPlayer framework ([MPNowPlayingInfoCenter](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter)). The template doesn't yet.
- **Add a model rule:** write it in `Model/`, keep it `nonisolated` and `Sendable`, add a check in `Tools/ModelTests/main.swift` and a line to its off-main-actor check.

Keep these, whatever the app:

1. One `AVPlayer`, one `AVPlayerLayer`, one Picture in Picture controller, owned by a model above every layout switch.
2. One `FoldRegionsLayout` for the player: video first, controls second. Never an `if` on the pose.
3. Every control in every pose. Tabletop moves the controls; it never adds or removes one.
4. Nothing that starts, pauses or reloads in `onAppear`, `onDisappear` or `.task` below the root.
5. Interactive overlays (the up next card) inside the controls view, never floating over the video on their own.
6. Icon buttons with a title and a 44 × 44 pt hit region (`IconButton`).

## 6. Test it

**On the Mac:** `Tools/run-model-tests.sh` builds `Model/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`, like the app target. It reads the real `Catalog.json` and checks each clip. The fold checks use the frames measured on the Duo simulator (book: a 40 × 669 pt fold at x 455 in 951 × 669 pt; tabletop: 669 × 40 pt at y 455). *Measured:* 103 checks, under 10 seconds with the build.

**On the simulator:** `Tools/run-ui-tests.sh`. The tests start from launch switches (`-play`, `-paused`, `-start`, `-select`, `-upNextLead`, `-autoplay 0`, `-loop`, `-resetState`), find elements by identifier, tap through `element.coordinate(withNormalizedOffset:)`, and read the player through the `player.state` marker (`item=…|playing=1|time=4|upNext=counting|pip=0|surfaces=1|presented=1|`). They never depend on the pose. Tests that need time start paused or stop at the end instead of racing a 12-second clip.

*Measured:* 11 passed and 1 skipped on the closed Duo simulator, about 140 s of tests; `testPlayerLayoutInThisPose` also passed in book pose and in tabletop. Picture in Picture is not supported on the iPhone Duo simulator (`isPictureInPictureSupported()` returned `false`), so the player hides its button there and `testPictureInPictureStarts` skips. Check Picture in Picture on a device.

Then check each pose by hand in Device Hub, or with `duo-pose-matrix` (needs the user's Accessibility permission):

```bash
duo-pose-matrix com.example.fieldcast \
  --case "library=-resetState -select small-repairs-2" \
  --case "player=-resetState -play small-repairs-1 -paused -start 4"
```

To see playback survive the poses, launch with `-play night-sky-notes-1 -loop` and pass `--no-relaunch`.

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-model-tests.sh` prints `0 failed`.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] The app launched on the Duo simulator; you looked at the screenshot of the display in use.
- [ ] `Tools/run-ui-tests.sh` passes (Picture in Picture skips on the simulator).
- [ ] Closed and open: the controls float over the video, every control visible.
- [ ] Book: video leading, controls trailing, nothing in the fold. Tabletop: video above the fold, the same controls below.
- [ ] Play, then fold, unfold and rotate: the video keeps playing from the same frame, with no black flash.
- [ ] The up next card appears near the end and never sits in the fold; Cancel stops at the end; Play Now moves on.
- [ ] Close the player: the mini player shows and the sound goes on; it sits clear of the fold line on the open phone.
- [ ] On a device: Picture in Picture starts from the button and on going home, pins to the top, and comes back to the player.
- [ ] VoiceOver reads every control's title in every pose.
