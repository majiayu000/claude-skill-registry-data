---
name: recipe-camera-studio
description: "Creates a complete SwiftUI camera studio for iPhone Duo, Apple's foldable: photos and videos with the rear camera and a self-timer, and, while the phone is open, the person being filmed sees themselves on the outer display (CameraCaptureAccessory) with the countdown or the recording time. Closed or open and flat, the controls float along the bottom or trailing edge, off the fold; folded like a book, the preview takes the left page and the controls the right; in tabletop the preview sits above the fold and the controls below it. Use when someone wants to start a new camera, photo booth, self-portrait or filming app from scratch, or runs /duo-new recipe-camera-studio. Covers AVFoundation capture on an actor (photo and movie outputs, rotation coordinators, a second mirrored preview layer), a stand-in camera that makes the simulator usable (it has no camera), an in-app gallery with ShareLink and no file dates, usage strings, a privacy manifest with Mac checks, and UI tests on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-camera-studio

This recipe makes a new Xcode project: a camera studio for iPhone Duo. The photographer takes photos and videos with the rear camera, with a self-timer of 3 or 10 seconds. While the phone is open, the outer display faces the person being filmed, and the studio shows them their own picture, mirrored, with a framing guide and the countdown or the recording time. Fold the phone like a book and the controls move to the right page; set it on a table half folded and the preview sits above the fold with the controls below it, for hands-free shots. Photos and videos stay in the app's gallery until someone shares them.

**The simulator has no camera** (*measured* in `duo-camera`). So the studio has a stand-in: a moving test card that the shutter photographs and the recorder films into a real movie. With it, every pose, the timer, recording, the gallery and the subject view on the outer display work in the simulator. The real capture code typechecks against the iOS 27.1 SDK and builds with no warnings, but has not run with a camera (`device: no`). Section 5 lists what to check on a device.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 2 November 2026). *Derived* means reasoning from Apple's pages or our measurements. *Unverified* means we could not check it. Everything else links to Apple. "Book" and "tabletop" are Duology's words for Apple's "partially folded, like a book" and "seated on a table like a laptop"; no API reports them. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists and needs the camera to work on Duo: `duo-camera` (which camera faces whom, mirroring, rotation, the front cameras, flipped selfies), with `duo-scenes` for the accessory;
- the app is a video call: `duo-camera` covers the virtual front camera that follows the app between displays;
- the outer display should show something other than a camera's subject view: `duo-scenes`.

## 1. Create the project

`/duo-new recipe-camera-studio` runs steps 1 to 5. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools`, and not an Apple module name such as `SwiftUI` or `AVFoundation`;
   - a bundle id such as `com.example.sitter`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-camera-studio/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-camera-studio/scripts/new-project.sh" \
     Sitter com.example.sitter ~/Developer/Sitter
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths, checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65), before it creates anything.
3. Test the rules on the Mac. Expect `0 failed`:

   ```bash
   cd ~/Developer/Sitter && Tools/run-model-tests.sh
   ```

4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -project Sitter.xcodeproj -scheme Sitter \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Install, launch with a 10-second countdown running, and screenshot both displays. Use the UDID, not `booted`. With the phone open, the outer display (`--display=primary`) shows the subject view.

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl install <UDID> build/DerivedData/Build/Products/Debug-iphonesimulator/Sitter.app
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.sitter -timer 10 -shutter
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary build/outer.png
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary-1 build/inner.png
   ```

   Look at the PNGs before you report. The studio asks for the camera on a device; in the simulator it says "Stand-in camera".
6. Run the UI tests: `DESTINATION="id=<UDID>" Tools/run-ui-tests.sh`. A UI test brings the app to the front; tell the user first if they share the simulator.
7. Tell the user what passed, that capture needs a real iPhone Duo to check (section 5), and that poses change only in Device Hub.

Set `DEVELOPER_DIR` for every `xcrun` and `xcodebuild` call when the Mac has more than one Xcode. Never run `xcode-select`.

## 2. What you get

| Path | What it holds |
|---|---|
| `<App>/Model/` | `StudioLayout` (the regions from the size and the fold), the self-timer (`TimerSetting`, `Countdown`), `RecordingClock`, `CameraAccess`, the gallery's index (`Capture`, `CaptureLibrary`), the stand-in's picture (`StandInFrame`), app facts. Foundation, CoreGraphics and ImageIO only, every type `nonisolated` and `Sendable`. |
| `<App>/Capture/` | `CaptureService`: an actor that owns the `AVCaptureSession`, the photo and movie outputs, the microphone, the rotation coordinators and the subject preview's mirroring. `CameraPreview` (the preview layer in SwiftUI), `StandInPreview`, `StandInRecorder` (writes the stand-in's movie with `AVAssetWriter`), `Poster`. |
| `<App>/Studio/` | `StudioScreen` (preview and controls), `StudioControls` and `ShutterButton`, `SubjectView` and the accessory registration, `GalleryScreen`. |
| `<App>/Shared/` | `StudioSplit` (the two regions), `onFoldChange` (from `recipe-reader`), test markers. |
| `<App>/App/` | App entry, `RootView` (the screen and the gallery sheet), `StudioStore`, launch switches. |
| `<App>/PrivacyInfo.xcprivacy` | No tracking, no domains, no data collected, no required-reason API. |
| `<App>UITests/` | Eight UI tests, pose-agnostic, on the stand-in camera. |
| `Tools/` | `run-model-tests.sh`, `ModelTests/main.swift`, `run-ui-tests.sh`. |

Project settings match the other recipes: iOS 26.0 deployment, Swift 6, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups, iPhone and iPad, a scheme with parallel testing off. This one is `public.app-category.photography` and sets the camera, microphone and photo-library-add usage strings.

Architecture, the capture paths and the stand-in: [references/architecture.md](references/architecture.md). What to check on a device: [references/device-checks.md](references/device-checks.md).

## 3. How it behaves in each pose

| Pose | Studio screen (inside the safe area) | Preview | Controls | Outer display |
|---|---|---|---|---|
| Closed (outer display) | 382 × 644 pt (*measured*) | the whole screen | float along the bottom, a 132 pt bar; shutter 76 pt, the others 52 pt high (*measured*) | it is the screen in use |
| Closed, held sideways | wider than tall | the whole screen | float along the trailing edge | the same |
| Open, flat, held wide | 867 × 635 pt, fold's frame at x 455.5 to 495.5 (*measured*) | the whole screen; it may cross the flat fold | float along the trailing edge, 132 pt, x 735 to 867, off the fold (*measured*) | the subject view (*measured*, no capture session) |
| Book | the same size; the fold turns active (*measured*) | the left page, 455.5 pt wide (*measured*) | a column on the right page, 371.5 pt wide (*measured*) | the subject view (*measured*, no capture session) |
| Tabletop | 669 × 835 pt, fold's frame at y 373.5 to 413.5 (*measured*) | above the fold, 373.5 pt high (*measured*) | a row below it, 421.5 pt high (*measured*) | the subject view (*measured*, no capture session) |
| Open, held tall, flat | as tabletop's size; the fold is inactive | the whole screen | float along the bottom, off the fold | the subject view (*unverified*) |

*Measured* on 2 November 2026: each pose set with `duo-pose`, then `testStudioLayoutInThisPose`, which fails if a control sits on the fold, is under 44 pt or leaves the controls' region, or if the shutter is under 76 pt, and attaches the real frames and a screenshot of each display with a countdown running; it passed in each pose, and every frame matched the table. Flat and folded differ on purpose, like Apple's `ArrangementView` with the overlay style (`duo-camera` measured it): flat, the preview keeps the whole screen; folded, the controls take their own half. The preview's view keeps its identity through every change, because one `StudioSplit` places it in every pose. The closed phone held sideways and the open phone held tall are *unverified*: their rows come from the Mac tests.

**The subject view.** The simulator showed it on the outer display open and flat, in book and in tabletop, and not closed (*measured*, `subjectAvailable` in the `studio.state` marker). There was no capture session: the simulator shows camera capture accessories without one, a known issue in the [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes). Apple's conditions say fully open with the camera running ([guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo)), so book and tabletop may differ on a device (*unverified*). That is why the countdown also shows large on the main preview, and nothing the photographer needs lives on the outer display. In the screenshots the subject view showed the stand-in mirrored (the bars ran the other way and the corner tag sat on the other side), the thirds guide and the countdown, upright and in portrait for the person facing the outer display. With the phone open, `simctl io … screenshot --display=primary` returns that display as a 2034 × 1398 image with the view on its side; turn it a quarter turn counterclockwise to read it (*measured*).

## 4. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| A countdown or a recording survives every fold | `StudioStore`, `@State` in `RootView` | The timer's task and the recording live above every layout switch (`duo-continuity`). `SubjectView` holds no state: the system builds a new accessory scene each time the phone opens (*measured* in `duo-scenes`). |
| One layout in every pose | `StudioSplit` placing `StudioLayout`'s regions | No `if` on the pose around the preview, so its UIView, its layer and its coordinators stay ([`Layout`](https://developer.apple.com/documentation/swiftui/layout)). |
| Folded, the regions meet at the fold | `StudioLayout`, fed by `onFoldChange` | [`reservedRegions(kind:options:layoutDirectionBehavior:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) with `.division` and `.includeInactive`, read on the `StudioSplit` itself. |
| Tabletop: watch above, tap below | `StudioLayout` mode `foldTopBottom` | Apple singles out the phone on a table as good for hands-free use: what people watch in the top region, what they tap in the bottom one, with the same controls as every other pose ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=283), [talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=263)). |
| No control on the fold | Every control lives in `controls`; flat, the floating bar or column sits at the edge, away from the fold | Nothing interactive in an active fold ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)). The UI test compares every control with a marker element at the fold's frame. |
| The subject sees themselves | `SubjectView` in a `CameraCaptureAccessory`, a second preview layer on the same session | [Registering a camera capture accessory](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo), [talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=300). The photographer can turn it off (`isEnabled`); the system decides when it can show. |
| The subject's picture is mirrored | `CaptureService.attachSubjectPreview(_:mirrored:)` | From the outer display the rear camera faces the subject, so its preview should look like a mirror ([choosing a camera by the direction it faces](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces), `duo-camera`). *Derived*; the stand-in shows it mirrored in the simulator. |
| Upright on both displays | `AVCaptureDevice.RotationCoordinator`, one per preview layer | Its angles also change when the app moves between displays ([rotation coordinator](https://developer.apple.com/documentation/avfoundation/avcapturedevice/rotationcoordinator), [talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=488)). *Unverified* on a device. |
| Width and fold, never the device | `StudioLayout(size:fold:controlsThickness:)` | Same rule as every Duology skill; `duo-lint --strict` finds nothing. |

## 5. Capture, the stand-in, and what to check on a device

- **Capture runs on an actor.** `CaptureService` owns the session; every configuration call and `startRunning()` (which blocks) run there. The photo and movie delegates hand results back through continuations. Two preview layers share the session: the photographer's and the subject's.
- **Which camera.** The rear wide camera (`.builtInWideAngleCamera`, `.back`) films the subject. Switch Camera picks the front camera every app asks for, which on iPhone Duo is the virtual front camera that follows the app between displays (`duo-camera`). With the front camera the subject view shows no picture: the thirds, "Look here" and the countdown.
- **No camera.** `CaptureService.hasCamera` is false in the simulator (*measured*: `AVCaptureDevice.default(for: .video)` returns `nil`), so the store uses the stand-in. `-standIn` forces it on a device too. Every camera lookup is optional; nothing force-unwraps a device.
- **The stand-in.** `StandInFrame` draws 75 % colour bars, a moving dot and a corner tag. The preview draws it 30 times a second, letterboxed to 4:3 like `.resizeAspect`; the shutter renders it as a 1200 × 900 JPEG; the recorder writes a 640 × 480 H.264 movie at 15 frames a second with `AVAssetWriter` (*measured*: a recording saved one H.264 track at 640 × 480 and 15 frames a second, its length matched the gallery's index, and its poster came out upright; playback in the gallery wasn't checked).
- **Permissions.** The project sets `NSCameraUsageDescription`, `NSMicrophoneUsageDescription` (video sound) and `NSPhotoLibraryAddUsageDescription` (Save Image from the share sheet); a Mac test fails if one is missing. Camera access denied: the preview says so and offers Open Settings. The microphone is asked for only when switching to video.
- **Privacy.** Photos and videos stay in the app's Documents folder. The gallery keeps its own dates in an index file, so it reads no file dates and the privacy manifest declares no required-reason API. The Mac tests fail if networking, tracking, CloudKit, `PHPhotoLibrary`, a web address or a required-reason API appears in the app's sources ([privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)).

On a real iPhone Duo, nothing in this list has run yet. [references/device-checks.md](references/device-checks.md) lists each check and what to expect: capture in each pose, the second preview layer, mirroring, rotation on both displays, the accessory's conditions in book and tabletop, interruptions in Split View, and the movie's sound.

## 6. Customise

- **Looks:** `StudioControls`, `ShutterButton`, `SubjectView`. Keep every control inside the controls' region and at least 44 pt.
- **The subject view:** keep it free of controls the photographer needs. Show what the subject needs: their picture, the countdown, a script, a "smile" cue.
- **More modes** (portrait, slow motion): add them to `CaptureMode` and `CaptureService.configure`, and to the mode button.
- **Saving to Photos directly:** add a `PHPhotoLibrary` save with add-only access, then update the privacy line in the usage strings, the manifest and the Mac checks together.
- **Add a model rule:** write it in `Model/`, keep it `nonisolated` and `Sendable`, add a check in `Tools/ModelTests/main.swift` and a line to its off-main-actor check.

Keep these, whatever the app:

1. The store above every layout switch; the accessory view reads it and keeps nothing.
2. One `StudioSplit` for every pose; regions from the fold's frame, never from half the width.
3. No control on the fold, flat or folded, and the countdown on the main preview as well as the outer display.
4. A stand-in for the simulator, so every pose and flow can be tested without a camera.
5. Capture on the actor, never on the main actor.

## 7. Test it

**On the Mac:** `Tools/run-model-tests.sh` builds `Model/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`, like the app target. It checks the layout in every pose at sizes measured on the Duo simulator, the self-timer and the clock, camera access messages, the gallery's index (order, deletes, missing files, the current file format), the stand-in's frames (pixels, size, JPEG without alpha), the privacy scan of the sources, the manifest and the usage strings, and that every model type works off the main actor. *Measured:* 82 checks pass in a few seconds, in the template and in a freshly generated project.

**On the simulator:** `Tools/run-ui-tests.sh`. The tests use the stand-in camera (`-standIn`), start from launch switches (`-timer`, `-mode`, `-shutter`, `-resetState`), find elements by identifier and read the `studio.state` and `gallery.state` markers, so they never depend on the pose. *Measured:* all eight passed on the closed Duo simulator, in a freshly generated project, in two runs of 113 s and about 270 s. The first runs found two problems, now fixed and described in [references/architecture.md](references/architecture.md#the-ui-tests).

```bash
Tools/run-ui-tests.sh -only-testing:SitterUITests/SitterUITests/testStudioLayoutInThisPose
```

Set the pose in Device Hub (or with `duo-pose`), then run that test once per pose. With `duo-pose-matrix` (needs the user's Accessibility permission):

```bash
duo-pose-matrix com.example.sitter --case "studio=-uiTesting -resetState -standIn -timer 10 -shutter"
```

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-model-tests.sh` prints `0 failed`, privacy and usage-string checks included.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] `python3 duo-lint.py --strict <project>` reports no findings.
- [ ] `Tools/run-ui-tests.sh` passes.
- [ ] Closed: the preview fills the screen, the controls along the bottom, the shutter 76 pt.
- [ ] Open and flat: the controls along the trailing edge, off the fold. Book: the preview left of the fold, the controls right of it.
- [ ] Tabletop: the preview above the fold; the shutter, timer and mode below it.
- [ ] Open, with the self-timer running: the outer display shows the subject view with the countdown.
- [ ] Start a countdown or a recording, then close, open and fold: it carries on.
- [ ] On a real iPhone Duo: every check in references/device-checks.md.
- [ ] Usage strings, privacy manifest and App Store Connect answers agree.
