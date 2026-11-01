---
name: recipe-notes-ai
description: "Creates a complete SwiftUI notes app for iPhone Duo, Apple's foldable, with summaries from Apple's on-device model (Foundation Models): a headline, key points and to-dos per note, streamed in. Closed, the note fills the screen and the summary is one line with Details; open, flat or like a book, the note takes the left page and the summary pane the right; in tabletop the note sits above the fold and the summary below it. Use when someone wants to start a new notes, journal or writing app with AI summaries from scratch, or runs /duo-new recipe-notes-ai. Covers a @Generable result streamed into a window-owned service so a fold never restarts it, a simple summary without AI whenever the model is unavailable or fails (it fails on the simulator), Stop and labels that say what is AI, a prompt budget for the 4,096-token context, notes that never leave the device (no network, no Private Cloud Compute) with a privacy manifest and Mac checks that say so, and UI tests on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-notes-ai

This recipe makes a new Xcode project: a notes app for iPhone Duo in which each note can be summarized by Apple's on-device model. A summary is a one-line headline, up to four key points and the note's to-dos. Closed, the note fills the screen and the summary is one line at the bottom, with Details for the rest. Open, the note takes the left page and the summary pane the right, like a notebook with notes in the margin. Set the phone on a table half folded and the note sits above the fold with the summary below it, where the buttons are. A summary still streaming in keeps going through every fold.

Summaries come from Foundation Models on the device. When the model can't run (Apple Intelligence off or not supported, the model still downloading, the simulator) or a request fails, the app makes a simple summary from the note's own sentences instead, labelled as not from AI. The notes never leave the device: no network, no Private Cloud Compute, no tracking, and the privacy manifest says so.

The sample notes are placeholders. The value is the frame: a request that no fold can restart, a fallback for every failure, panes read from the fold and never from the device, privacy checks that fail the Mac tests if the note could leave the phone, and UI tests that pass on the Duo simulator.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 29 October 2026). *Unverified* means we could not check it. Everything else links to Apple. "Book" and "tabletop" are Duology's words for Apple's "partially folded, like a book" and "seated on a table like a laptop"; no API reports them. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists and needs an AI pane: use `duo-intelligence` (it also covers Private Cloud Compute, tools and images), with `duo-continuity`;
- the app shows long text to read rather than write: start from `recipe-reader`;
- the summary must come from a server: this recipe's privacy promise no longer holds; see `duo-intelligence` and App Review guideline 5.1.2(i) below.

## 1. Create the project

`/duo-new recipe-notes-ai` runs steps 1 to 5. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools`, and not an Apple module name such as `SwiftUI` or `FoundationModels`;
   - a bundle id such as `com.example.margins`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-notes-ai/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-notes-ai/scripts/new-project.sh" \
     Margins com.example.margins ~/Developer/Margins
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths, checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65), before it creates anything.
3. Test the rules on the Mac. Expect `0 failed`:

   ```bash
   cd ~/Developer/Margins && Tools/run-model-tests.sh
   ```

4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -project Margins.xcodeproj -scheme Margins \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Install, launch straight into a note with its summary starting, and screenshot the display in use. Use the UDID, not `booted`. `-summarizer standin` streams a stand-in, because the real model fails on the simulator (section 5).

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl install <UDID> build/DerivedData/Build/Products/Debug-iphonesimulator/Margins.app
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.margins -open sample.offsite -summarize -summarizer standin
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary build/outer.png     # closed
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary-1 build/inner.png   # open
   ```

   Only the display in use has content. Look at the PNG before you report.
6. Run the UI tests: `DESTINATION="id=<UDID>" Tools/run-ui-tests.sh`. A UI test brings the app to the front; tell the user first if they share the simulator.
7. Tell the user what passed, that AI summaries need a device with Apple Intelligence to judge, and that poses change only in Device Hub.

Set `DEVELOPER_DIR` for every `xcrun` and `xcodebuild` call when the Mac has more than one Xcode. Never run `xcode-select`.

## 2. What you get

| Path | What it holds |
|---|---|
| `<App>/Model/` | `Note` and `Notebook` (the saved file), `Digest` and `DigestDraft`, `SimpleSummary` (no AI), `PromptBudget`, `SummaryEngine` and the stand-in stream, `NoteLayout` and `NoteColumns`, fold geometry, sample notes, app facts (the model's instructions, the labels). Foundation and CoreGraphics only, every type `nonisolated` and `Sendable`. |
| `<App>/AI/` | `OnDeviceSummarizer`: the `@Generable` result, availability in words, the streamed request. The only file that talks to the model. `SummaryService`: one summary at a time, Stop, and the fallback. |
| `<App>/Notes/` | `NotesListScreen` and `NoteCard`, `NoteScreen` with `EditorPane`, and `SummaryPane`, `SummaryBar`, `SummarySheet`. |
| `<App>/Shared/` | `PaneSplit` (the note and its summary) and `ColumnsRow` (the list), `onFoldChange` (from `recipe-reader`), test markers. |
| `<App>/App/` | App entry, `RootView` (the stack and the sheet), `NotesStore`, launch switches. |
| `<App>/PrivacyInfo.xcprivacy` | No tracking, no domains, no data collected, no required-reason API. |
| `<App>UITests/` | Eleven UI tests, pose-agnostic. |
| `Tools/` | `run-model-tests.sh`, `ModelTests/main.swift`, `run-ui-tests.sh`. |

Project settings match the other recipes: iOS 26.0 deployment (the first with Foundation Models), Swift 6, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups, iPhone and iPad, `public.app-category.productivity`, and a scheme with parallel testing off.

Architecture, the request's life and test details: [references/architecture.md](references/architecture.md).

## 3. How it behaves in each pose

| Pose | Note screen (inside the navigation stack) | The note | The summary | The list |
|---|---|---|---|---|
| Closed (outer display) | 382 × 562 pt (*measured*) | 382 × 498 pt (*measured*) | a 64 pt bar at the bottom; Details opens the full summary in a sheet (*measured*) | one column of cards, 350 pt (*measured*) |
| Closed, held sideways | wider than tall, under 700 pt | the same | the same bar | two columns |
| Open, flat, held wide | 867 × 553 pt, fold's frame at x 455.5 to 495.5 (*measured*) | left page, 455.5 pt wide (*measured*) | right page, 371.5 pt; Summarize Again and Clear side by side, 198 × 51 and 105 × 50 pt (*measured*) | two columns that meet at the fold's frame, 434 and 349 pt (*measured*) |
| Book | the same pages; only the fold turns active (*measured*) | the same | the same | the same |
| Tabletop | 669 × 835 pt, fold's frame at y 373.5 to 413.5 (*measured*) | above the fold, 373.5 pt high (*measured*) | below it, 421.5 pt, buttons at the bottom (*measured*) | two columns; the list scrolls across the fold |
| Open, held tall, flat | as tabletop; the fold is inactive | the same | the same | the same |

*Measured* on 29 October 2026: each pose set with `duo-pose`, then `testNoteLayoutInThisPose` and `testListInThisPose`, which fail if a region crosses the fold or a summary button is under 44 pt or on the fold, and attach the real frames; all passed in each pose and the frames matched the table. The closed phone held sideways and the open phone held tall are *unverified*: their rows come from the Mac tests (`NoteLayout`, `NoteColumns`).

## 4. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| A summary survives every fold | `SummaryService` in `NotesStore`, `@State` in `RootView` | The request's task lives above every layout switch, so a fold only changes where its text shows (`duo-continuity`). Never start a request in `onAppear` or `.task` below a layout switch. *Measured:* a stand-in summary went from closed to open, book and closed again while streaming; it only grew and never restarted (`testStreamKeepsGoingThroughFolds`); the result is saved once, when the task ends. |
| One layout in every pose | `PaneSplit` placing `NoteLayout`'s two regions | No `if` on the pose around the editor, so the text field, the cursor and the scroll position stay ([`Layout`](https://developer.apple.com/documentation/swiftui/layout)). |
| The pages meet at the fold, not the middle | `NoteLayout`, fed by `onFoldChange` | [`reservedRegions(kind:options:layoutDirectionBehavior:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) with `.division` and `.includeInactive`, read on the `PaneSplit` itself. Flat and folded give the same regions. |
| Open adds the pane; closed keeps the feature | `SummaryPane` in two-pane modes, `SummaryBar` and `SummarySheet` in single mode | Apple lets the open phone add one level of detail, and keeps the same features on both displays ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)). The sheet closes by itself when the pane fits beside. |
| Tabletop: read above, touch below | `NoteLayout` mode `foldTopBottom` | Content in the top region, controls in the stable bottom one ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=276)). The keyboard covers the summary there instead of squeezing both regions (*unverified* with a software keyboard on a device). |
| No button on the fold | Every summary button lives in the summary's region; the fold's frame is the gap | Nothing interactive in an active fold ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)). The list's columns meet at the fold for the same reason. |
| Headline first | `GeneratedDigest` declares `headline` first | The model writes properties in the order declared ([guided generation](https://developer.apple.com/documentation/foundationmodels/generating-swift-data-structures-with-guided-generation)), so the closed phone's bar fills in before the points. |
| Width and fold, never the device | `NoteLayout(size:fold:barHeight:)` | Same rule as every Duology skill; `duo-lint --strict` finds nothing. |
| No size feedback | `.frame(minWidth: 0, maxWidth: .infinity, minHeight: 0, maxHeight: .infinity)` on each region | A region that grows to fit its content never shrinks back (*measured* in `recipe-kids-learning`). |

## 5. The model, the fallback and privacy

- **Availability:** `OnDeviceSummarizer.unavailableReason` turns `SystemLanguageModel.default.availability` and `supportsLocale()` into a sentence for the pane: device not eligible, Apple Intelligence off, model not ready, language not supported ([generating content](https://developer.apple.com/documentation/foundationmodels/generating-content-and-performing-tasks-with-foundation-models)). When it isn't available the pane says why and Summarize makes the simple summary.
- **Failure:** every request that throws ends in `SimpleSummary`, labelled, with the reason and Summarize Again. The final `catch` is untyped: *measured*, the simulator's failure arrives as a plain `NSError` (domain `FoundationModels.LanguageModelError`, code -1). The app logs the error's domain and code; its description stays private.
- **The simulator:** *measured* on 29 October 2026, with the model forced (`-summarizer ai`), every request failed within seconds. The underlying error from the guardrail's text sanitizer reads "Simulator is not supported". So the simulator can't test summary quality; the stand-in engines test everything around it. Judge the summaries on a device with Apple Intelligence (*unverified* here).
- **Stop and Summarize Again:** Stop cancels the task and keeps the note's previous summary. A new request replaces one still running. People can always stop, redo or clear a summary, and the pane says which summaries are AI ([HIG: Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai)).
- **The context window:** the on-device model holds 4,096 tokens for instructions, schema, prompt and answer together ([managing the context window](https://developer.apple.com/documentation/foundationmodels/managing-the-context-window)). `PromptBudget` sends at most 6,000 characters, cut at a sentence end, and the summary then says it covers the start. A note in a script that uses more tokens per character can still overflow; that fails like any request and falls back.
- **Prompt injection:** the note goes in the prompt; the instructions are the constant `AppFacts.summaryInstructions`. A Mac test fails if anything else reaches `instructions:` ([safety](https://developer.apple.com/documentation/foundationmodels/improving-the-safety-of-generative-model-output)).
- **The note never leaves the device:** on-device requests stay on the phone. The Mac tests fail if `PrivateCloudComputeLanguageModel`, networking, CloudKit or tracking APIs appear in the app's sources, or if the manifest declares anything. The privacy manifest has no tracking, no domains, no collected data and no required-reason API: notes go to a JSON file in Application Support, and the app reads no file dates ([privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)).

Only the app's owner can do these:

1. **App Privacy answers** in App Store Connect: "Data Not Collected" stays true while nothing leaves the device ([app privacy details](https://developer.apple.com/app-store/app-privacy-details/)).
2. **Before adding a server or a third-party model:** guideline 5.1.2(i) asks apps to say clearly when personal data goes to third parties, "including with third-party AI", and to get explicit permission first ([App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/), checked 29 October 2026). Change the privacy line, the manifest, the Mac checks and the App Privacy answers together.
3. **Judge the summaries** on a device with Apple Intelligence, in each language you support.

## 6. Customise

- **Your notes:** edit `Model/SampleNotes.swift`, or return none. Keep the IDs if UI tests open them.
- **What a summary holds:** change `GeneratedDigest` (the model's fields, with `@Guide` limits), `Digest` and `DigestDraft` (what's saved and shown), and `SimpleSummary` (the fallback) together. Put the field the closed phone shows first.
- **The instructions:** `AppFacts.summaryInstructions`. Keep it a constant.
- **Looks:** `NoteCard`, `SummaryPane`, `SummaryBar`. Keep the summary's buttons inside its region.
- **Add a model rule:** write it in `Model/`, keep it `nonisolated` and `Sendable`, add a check in `Tools/ModelTests/main.swift` and a line to its off-main-actor check.

Keep these, whatever the app:

1. The request in a service owned above the navigation stack; views only read it.
2. One `PaneSplit` for every pose; regions from the fold's frame, never from half the width.
3. A non-AI path for every failure, and a label on every summary saying where it came from.
4. The note in the prompt, never in the instructions.
5. The privacy checks in `Tools/ModelTests/main.swift`; if the note ever leaves the device, update the privacy line, the manifest and the App Store Connect answers together.

## 7. Test it

**On the Mac:** `Tools/run-model-tests.sh` builds `Model/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`, like the app target. It checks the sample notes, the notebook (edits, empty notes dropped, save and load, the current file format), fingerprints, tidying the model's lines, the simple summary, the prompt budget, the stand-in stream, the layouts and columns at sizes measured on the Duo simulator, the privacy scan of the app's sources and manifest, and that every model type works off the main actor. *Measured:* 119 checks pass in a few seconds, in the template and in a freshly generated project.

**On the simulator:** `Tools/run-ui-tests.sh`. The tests start from launch switches (`-open`, `-summarizer`, `-standInPace`, `-resetState`), find elements by identifier, and read the `list.state` and `note.state` markers. The summary's buttons have the same identifiers in the bar and in the pane, so the tests never depend on the pose. *Measured:* all eleven passed on the closed Duo simulator in about 210 s, in a freshly generated project. The first runs found three problems, now fixed and described in [references/architecture.md](references/architecture.md#the-ui-tests). Open, book and tabletop: the pose tests in section 3.

```bash
Tools/run-ui-tests.sh -only-testing:MarginsUITests/MarginsUITests/testNoteLayoutInThisPose
```

Set the pose in Device Hub (or with `duo-pose`), then run that test and `testListInThisPose` once per pose. Run `testStreamKeepsGoingThroughFolds` and press Open, Partially Open and Closed while it streams. With `duo-pose-matrix` (needs the user's Accessibility permission):

```bash
duo-pose-matrix com.example.margins --case "note=-uiTesting -resetState -open sample.offsite -summarize -summarizer simple"
```

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-model-tests.sh` prints `0 failed`, privacy checks included.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] `python3 duo-lint.py --strict <project>` reports no findings.
- [ ] `Tools/run-ui-tests.sh` passes.
- [ ] Closed: the note above a one-line summary bar; Details opens the full summary.
- [ ] Open, flat and like a book: the note left of the fold, the summary right of it, nothing in the fold's frame.
- [ ] Tabletop: the note above the fold; the summary and its buttons below it.
- [ ] Start a summary, then close, open and fold: it keeps streaming, never restarts, and is saved once.
- [ ] With the model unavailable or failing, a simple summary appears, labelled, with the reason.
- [ ] Every summary says whether it is AI; Stop, Summarize Again and Clear work.
- [ ] Summaries judged on a device with Apple Intelligence, in each language you support.
- [ ] Privacy line, manifest and App Store Connect answers agree.
