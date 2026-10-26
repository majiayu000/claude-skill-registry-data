---
name: recipe-kids-learning
description: "Creates a complete SwiftUI early-learning app for young children on iPhone Duo, Apple's foldable: counting, first letters and shapes, one question at a time with a spoken prompt and big answer buttons. Closed, the picture sits above the answers; open and held wide or folded like a book, the question takes the left page and the answers the right; in tabletop the picture sits above the fold and the answers below it. Use when someone wants to start a new kids, preschool or early-learning quiz app from scratch, or runs /duo-new recipe-kids-learning. Covers a parental gate (a seeded multiplication on a number pad) in front of a grown-ups area with reset and the privacy policy link, App Review guidelines 1.3 and 5.1.4 for the Kids Category, a privacy manifest with no tracking and no data collected, no networking with a Mac check that fails if it appears, AVSpeechSynthesizer prompts, VoiceOver, progress that survives folds and relaunch, a model tested on the Mac, and UI tests on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-kids-learning

This recipe makes a new Xcode project: an early-learning app for children aged about 3 to 8 on iPhone Duo. Three activities (counting, first letters, shapes) ask one question at a time. Each question has a picture, a line of text and a big speaker button that reads it aloud for children who can't read yet. The answers are big buttons; a wrong one is set aside with a kind word, a right one earns a star. Nothing is timed and nothing is taken away. Closed, the picture sits above the answers. Open, the question takes the left page and the answers the right, like a picture book. Set the phone on a table half folded and the picture sits above the fold with the answers below it, on the half that rests on the table.

A Grown-ups button opens a parental gate. Behind it are Reset Progress, the speech setting, what the app does with data, and the privacy policy link. The app has no networking, no ads, no analytics, no purchases and no tracking, and its privacy manifest says so.

The questions are sample content. The value is the frame: a gate that follows App Review's rules, progress that no fold can lose, layouts read from the fold and never from the device, privacy checks that fail the build's tests if networking appears, and UI tests that pass on the Duo simulator.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 25 October 2026). *Unverified* means we could not check it. Everything else links to Apple. "Book" and "tabletop" are Duology's words for Apple's "partially folded, like a book" and "seated on a table like a laptop"; no API reports them. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists: use `duo-postures` (tabletop and book layouts), `duo-continuity` (state through a fold) and `duo-accessibility`;
- two children play at once on one phone: use `recipe-two-player-game` and `duo-shared-screen`;
- the app sells something: start from `recipe-shop`, and in a Kids Category app put every purchase behind a parental gate like this one ([guideline 1.3](https://developer.apple.com/app-store/review/guidelines/)).

## 1. Create the project

`/duo-new recipe-kids-learning` runs steps 1 to 5. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools`, and not an Apple module name such as `SwiftUI` or `AVFoundation`;
   - a bundle id such as `com.example.littlesteps`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-kids-learning/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-kids-learning/scripts/new-project.sh" \
     LittleSteps com.example.littlesteps ~/Developer/LittleSteps
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths, checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65), before it creates anything.
3. Test the rules on the Mac. Expect `0 failed`:

   ```bash
   cd ~/Developer/LittleSteps && Tools/run-model-tests.sh
   ```

4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -project LittleSteps.xcodeproj -scheme LittleSteps \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Install, launch straight into an activity, and screenshot the display in use. Use the UDID, not `booted`. `-uiTesting` mutes the speech, which otherwise plays through the Mac's speakers.

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl install <UDID> build/DerivedData/Build/Products/Debug-iphonesimulator/LittleSteps.app
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.littlesteps -uiTesting -open counting
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary build/outer.png     # closed
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary-1 build/inner.png   # open
   ```

   Only the display in use has content. Look at the PNG before you report.
6. Run the UI tests: `DESTINATION="id=<UDID>" Tools/run-ui-tests.sh`. A UI test brings the app to the front; tell the user first if they share the simulator.
7. Tell the user what passed, what they must set in App Store Connect (section 5), and that poses change only in Device Hub.

Set `DEVELOPER_DIR` for every `xcrun` and `xcodebuild` call when the Mac has more than one Xcode. Never run `xcode-select`.

## 2. What you get

| Path | What it holds |
|---|---|
| `<App>/Model/` | Activities and the sample questions, progress, the parental gate, the two-pane layout, the answer grid, fold geometry, app facts (privacy policy address, speech language). Foundation and CoreGraphics only, every type `nonisolated` and `Sendable`. |
| `<App>/Learn/` | `HomeScreen` (welcome and activity cards), `LessonScreen` (question pane and answers pane), `BigButton` (tiles, the press style, the tile grid). |
| `<App>/Grownups/` | `GateScreen` (the gate in a sheet) and `GrownupsScreen` (the area behind it). The only file that opens a link. |
| `<App>/Shared/` | `PaneSplit` (the two-pane `Layout`), `onFoldChange` (from `recipe-reader`), `ArtView`, `Speaker`, test markers. |
| `<App>/App/` | App entry, `RootView` (the stack and the sheet), `LearningStore`, launch switches. |
| `<App>/PrivacyInfo.xcprivacy` | No tracking, no domains, no data collected; UserDefaults with reason CA92.1. |
| `<App>UITests/` | Nine UI tests, pose-agnostic. |
| `Tools/` | `run-model-tests.sh`, `ModelTests/main.swift`, `run-ui-tests.sh`. |

Project settings match the other recipes: iOS 26.0 deployment, Swift 6, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups, iPhone and iPad, `public.app-category.education`, and a scheme with parallel testing off.

Architecture, state ownership, the gate and test details: [references/architecture.md](references/architecture.md). App Review's kids rules, the privacy manifest and what the owner sets: [references/kids-rules.md](references/kids-rules.md).

## 3. How it behaves in each pose

| Pose | Lesson (inside the navigation stack) | Question pane | Answers pane | Home |
|---|---|---|---|---|
| Closed (outer display) | 382 × 562 pt (*measured*) | top half, 382 × 273 pt | below it: three answers in one row, 106 × 220 pt each; Next 350 × 88 pt (*measured*) | welcome above, three cards of 350 × 104 pt (*measured*) |
| Closed, held sideways | wider than tall | left half | right half | the same split |
| Open, flat, held wide | 867 × 553 pt, fold's frame at x 455.5 to 495.5 (*measured*) | left page, 455.5 pt wide | right page, 371.5 pt: three answers in one column, 339 × 163 pt (*measured*) | welcome left, cards right (*measured*) |
| Book | the same pages; only the fold turns active (*measured*) | the same | the same | the same |
| Tabletop | 669 × 835 pt, fold's frame at y 373.5 to 413.5 (*measured*) | above the fold, 373.5 pt high | below it, 421.5 pt: three answers in a row, 201 × 220 pt (*measured*) | welcome above, cards below (*measured*) |
| Open, held tall, flat | as tabletop; the fold is inactive | the same | the same | the same |

*Measured* on 25 October 2026. Closed: all nine UI tests, the frames above, and the largest accessibility text size. Open (flat, held wide), book and tabletop: each pose set with `duo-pose`, then `testLessonLayoutInThisPose` and `testHomeAndGateInThisPose`, which fail if a button lands on the fold or under 88 pt and attach the real frames; both passed in each pose, every frame matched the table, and every answer sat wholly on one side of the fold. The read-aloud button measured 88 × 88 pt and the gate's keys 125 × 64 pt in every pose. The closed phone held sideways and the open phone held tall are *unverified*: their rows come from the Mac tests (`LessonLayout`, `AnswerGrid`).

## 4. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| Progress survives every fold | `Progress` in `LearningStore`, `@State` in `RootView` | State above a layout switch survives it (`duo-continuity`). Saved to UserDefaults on every change, so it survives quitting too. *Measured* here: a relaunch. Progress through a real fold: *unverified* for this app (the pose tests set each pose from a fresh launch). |
| One layout in every pose | `PaneSplit` placing `LessonLayout`'s two rectangles | No `if` on the pose around the panes, so neither is rebuilt ([`Layout`](https://developer.apple.com/documentation/swiftui/layout)). |
| The pages meet at the fold, not the middle | `LessonLayout`, fed by `onFoldChange` | [`reservedRegions(kind:options:layoutDirectionBehavior:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) with `.division` and `.includeInactive`, read on the `PaneSplit` itself. Flat and folded give the same panes, so folding moves nothing. |
| Tabletop: look above, touch below | `LessonLayout` mode `foldTopBottom` | Apple's optional per-pose layout: what people watch in the top region, what they touch in the stable bottom one, with the same controls ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=276)). For a small child, the bottom half resting on the table doesn't wobble under a tap. |
| No button on the fold | Answers, Next and Play Again live only in the second pane; the fold's frame is the gap | Nothing interactive in an active fold ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)). The UI tests compare every button with a marker element at the fold's frame. |
| Big buttons | `AnswerGrid`, 88 pt minimum | Our choice: twice the 44 pt Apple asks for, for small fingers. Tidy grids only: one row, one column, or two by two. |
| No size feedback | `.frame(minWidth: 0, maxWidth: .infinity, minHeight: 0, maxHeight: .infinity)` on every measured pane | *Measured:* without `minWidth: 0` the closed phone's answers stayed 434 pt wide in a 382 pt screen. |
| Width and fold, never the device | `LessonLayout(size:fold:)` | Same rule as every Duology skill; `duo-lint --strict` finds nothing. |
| Spoken prompts | `Speaker` (`AVSpeechSynthesizer`), `.task(id: question?.id)` | A new question is read aloud; a fold keeps the ID, so it never repeats. VoiceOver users get announcements instead ([`AccessibilityNotification.Announcement`](https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement)). |
| VoiceOver | Each pane a container (`accessibilityElement(children: .contain)`); things to count read one by one | A child using VoiceOver can count the stars by swiping (`duo-accessibility`). |
| Sheets survive folds | `.sheet` on `RootView` | The gate and a half-typed answer stay through a fold (`duo-continuity`). |

## 5. Kids rules, privacy, and what the owner sets

Read [references/kids-rules.md](references/kids-rules.md) before you submit. In short, in our words:

- **Guideline 1.3 (Kids Category):** links out of the app, purchases and other distractions belong only in an area behind a parental gate; avoid third-party analytics and ads; never send personal or device data to third parties. The template's only link and its Reset Progress sit behind the gate, and a Mac test fails if a link appears anywhere else ([guidelines](https://developer.apple.com/app-store/review/guidelines/)).
- **Guideline 5.1.4 (Kids):** care with children's data under laws such as COPPA and GDPR; a privacy policy is needed; a parental gate is not parental consent. The template collects nothing.
- **The gate:** Apple's [kids apps page](https://developer.apple.com/app-store/kids-apps/) describes an adult-level task, such as a maths problem or a question, and suggests a spoken prompt for children who can't read. The template asks a multiplication (6 to 9 times 4 to 9) on a number pad, says aloud that this part is for grown-ups, closes on a wrong answer, and asks something new next time.
- **Privacy manifest:** `NSPrivacyTracking` false, no tracking domains, no collected data types, `NSPrivacyAccessedAPICategoryUserDefaults` with `CA92.1` (defaults only the app reads and writes), the same file as `recipe-reader`. A Mac test fails if networking or tracking APIs appear in the app's sources, or if the manifest and the sources disagree.

Only the app's owner can do these, in App Store Connect:

1. **Kids Category and age band:** App Information, Age Ratings: choose Made for Kids and an age range (5 and under, 6 to 8, 9 to 11). The rating must come out 4+ or 9+, and the choice can't be changed after approval ([help](https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/)).
2. **Privacy answers:** App Privacy: "No, we do not collect data from this app", if that is still true of your build ([help](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy/), [what counts as collecting](https://developer.apple.com/app-store/app-privacy-details/)).
3. **Privacy policy URL:** required; replace `https://example.com/privacy` in `AppFacts.swift` with the same page.
4. **Store text:** no "For Kids" or "For Children" outside the Kids Category (guidelines 2.3.8 and 5.1.4).

## 6. Customise

Change the content first, then the look.

- **Your questions:** edit `Model/SampleActivities.swift`. Keep question IDs stable once children have stars for them. `Tools/run-model-tests.sh` checks every activity: 2 to 4 answers, the right one among them, unique IDs, every SF Symbol present, and the sample's own sense checks (the counting answer equals the things shown). A new activity:

  ```swift
  import Foundation

  // requires: Activity, Question, Answer (Model/Activity.swift), SampleActivities

  extension SampleActivities {
      /// Add it to `all` to show its card on the home screen.
      static let animals = Activity(
          id: "animals", title: "Animals", symbol: "pawprint.fill", tint: .blue,
          questions: [
              Question(
                  id: "animals.fly", text: "Which one can fly?", spoken: "Which animal can fly in the sky?",
                  art: .symbol("cloud.fill", .blue), artLabel: "The sky",
                  answers: [
                      Answer(id: "fish", label: "Fish", art: .symbol("fish.fill", .orange)),
                      Answer(id: "bird", label: "Bird", art: .symbol("bird.fill", .blue)),
                      Answer(id: "tortoise", label: "Tortoise", art: .symbol("tortoise.fill", .green)),
                  ],
                  correct: "bird"),
          ])
  }
  ```

- **Another language:** translate the content, set `AppFacts.speechLanguage` (a BCP 47 code such as `fr-FR`), and translate the spoken prompts in `AppFacts`.
- **Looks:** `BigTile`, `ArtView`, the home cards. Keep `AnswerGrid.minimumTarget` at 88 pt or more.
- **Add a model rule:** write it in `Model/`, keep it `nonisolated` and `Sendable`, add a check in `Tools/ModelTests/main.swift` and a line to its off-main-actor check.

Keep these, whatever the app:

1. Progress in a store above the navigation stack, saved on the device on every change.
2. One `PaneSplit` for every pose; panes from the fold's frame, never from half the width.
3. Every button in the second pane, so none can land on the fold.
4. Links out, purchases and destructive settings only behind the gate.
5. No networking or tracking code; keep the privacy checks in `Tools/ModelTests/main.swift`, and update the manifest, the grown-ups text and the App Store Connect answers together if that ever changes.

## 7. Test it

**On the Mac:** `Tools/run-model-tests.sh` builds `Model/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`, like the app target. It checks the sample content and its SF Symbols, progress (stars once, no penalty, save and load, an old file format), the gate (seeds, ranges, digits, attempts, a new question every time), the layouts at screen sizes measured on the Duo simulator (closed for this app; open and tabletop for `recipe-reader`'s reader), the answer grid, the privacy scan of the app's sources and manifest, and that every model type works off the main actor. *Measured:* 164 checks pass in a few seconds, in the template and in a freshly generated project.

**On the simulator:** `Tools/run-ui-tests.sh`. The tests start from launch switches (`-open`, `-question`, `-gateSeed`, `-resetState`), find elements by identifier, and read the `lesson.state`, `home.state`, `gate.state` and `grownups.state` markers. They never depend on the pose. *Measured:* all nine passed on the closed Duo simulator, about 160 s. The first runs found three problems, now fixed and described in [references/architecture.md](references/architecture.md#the-ui-tests): the answers pane growing to fit its buttons, taps lost when other apps on the shared simulator took the foreground, and a frame read while a pressed button was still shrunk. Open, book and tabletop are *unverified* (section 3).

```bash
Tools/run-ui-tests.sh -only-testing:LittleStepsUITests/LittleStepsUITests/testLessonLayoutInThisPose
```

Set the pose in Device Hub (or with `duo-pose`), then run that test and `testHomeAndGateInThisPose` once per pose. To check each pose by hand, or with `duo-pose-matrix` (needs the user's Accessibility permission):

```bash
duo-pose-matrix com.example.littlesteps --case "lesson=-uiTesting -resetState -open counting"
```

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-model-tests.sh` prints `0 failed`, privacy checks included.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] `python3 duo-lint.py --strict <project>` reports no findings.
- [ ] `Tools/run-ui-tests.sh` passes.
- [ ] Closed: the picture above three answers in a row, each at least 88 pt.
- [ ] Open, flat and like a book: the question left of the fold, the answers right of it, nothing in the fold's frame.
- [ ] Tabletop: the picture above the fold; the answers, Next and Play Again below it.
- [ ] Answer a question, then close, open and fold: the stars, the question and Next stay; quit and relaunch: the same.
- [ ] VoiceOver reads the question pane, then the answers; the stars to count are read one by one; feedback is announced.
- [ ] The gate: a wrong answer closes it, the next question differs, the right one opens the grown-ups area; Done locks it again.
- [ ] The privacy policy address in `AppFacts.swift` is yours, and the grown-ups text is still true.
- [ ] App Store Connect: Kids Category and age band chosen, privacy answers given, privacy policy URL set (the owner's decisions).
