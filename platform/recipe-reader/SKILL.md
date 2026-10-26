---
name: recipe-reader
description: "Creates a complete SwiftUI reading app for iPhone Duo, Apple's foldable: a library shelf, then one page on the closed outer display, two facing pages split at the fold when the phone is open and held wide or folded like a book, and in tabletop the page above the fold with the page turns below it. Use when someone wants to start a new e-reader, book, story, essay or long-form reading app from scratch, or runs /duo-new recipe-reader. For an existing reader, use duo-reading instead. Covers the reading place kept as a chapter and character offset in a store above the navigation stack, TextKit 1 pagination that runs again after every fold, rotation and Dynamic Type change, ReaderLayout reading the .division reserved region, an even-column shelf split at the fold, an in-app text size menu, swipe and VoiceOver page turns, three sample books written for the template, a Foundation-only model tested on the Mac (the paginator too, through AppKit), and UI tests that work on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-reader

This recipe makes a new Xcode project: a reading app for iPhone Duo. The library shows a shelf of books and the one you were reading. A book opens on one page when the phone is closed and on two facing pages when it opens, split at the fold like a paper book. Set the phone on a table half folded and the page sits above the fold, with big page turns below it. Close it, open it, fold it, turn it or change the text size: the words you were reading stay on screen.

The books are sample content. The value is the frame around them: a place that no layout change can lose, pages that always break where the page ends, rules you can test on the Mac in seconds, and UI tests that pass on the Duo simulator.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 20 October 2026). *Unverified* means we could not check it. Everything else links to Apple. "Book" and "tabletop" are Duology's words for Apple's "partially folded, like a book" and "seated on a table like a laptop"; no API reports them. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists: use `duo-reading` (the same pagination and reader, as code to add) and `duo-continuity`;
- the app plays video or audio: use `recipe-media-player`.

## 1. Create the project

`/duo-new recipe-reader` runs steps 1 to 5. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools`, and not an Apple module name such as `SwiftUI` or `UIKit`;
   - a bundle id such as `com.example.shelfie`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-reader/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-reader/scripts/new-project.sh" \
     Shelfie com.example.shelfie ~/Developer/Shelfie
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths, checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65), before it creates anything.
3. Test the rules on the Mac. Expect `0 failed`:

   ```bash
   cd ~/Developer/Shelfie && Tools/run-model-tests.sh
   ```

4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -project Shelfie.xcodeproj -scheme Shelfie \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Install, launch straight into a book, and screenshot the display in use. Use the UDID, not `booted`.

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl install <UDID> build/DerivedData/Build/Products/Debug-iphonesimulator/Shelfie.app
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.shelfie -open keeper -chapter 0 -offset 2400
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
| `<App>/Model/` | Library, chapter text, reading places, page breaks and turns, the reader's layout, the shelf's columns, fold geometry. Foundation and CoreGraphics only, every type `nonisolated` and `Sendable`. |
| `<App>/Text/Paginator.swift` | TextKit 1 page breaks. UIKit in the app, AppKit in the Mac tests. |
| `<App>/Reader/` | `ReaderScreen` (layout, pagination, turns, menus, tabletop controls), `PageView` with a TextKit 1 `UITextView`, `TextStyle` (serif body at the reader's Dynamic Type size). |
| `<App>/Library/` | The shelf (`ShelfLayout`), book tiles, the Continue Reading card, drawn covers. |
| `<App>/App/` | App entry, `RootView` (the navigation stack), `LibraryStore` (places, saved as JSON), launch switches. |
| `<App>/Shared/` | `onFoldChange` and the test marker. |
| `<App>/Books/` | `Library.json` and eight chapters in three books, written for this template (about 6,400 words). |
| `<App>UITests/` | Nine UI tests, pose-agnostic. |
| `Tools/` | `run-model-tests.sh`, `ModelTests/main.swift`, `run-ui-tests.sh`. |

Project settings: iOS 26.0 deployment, Swift 6 language mode, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups (new files need no project edits), iPhone and iPad, a privacy manifest that declares UserDefaults (reason CA92.1) for the saved places. The scheme turns off parallel testing so `xcodebuild` doesn't clone the simulator.

Architecture, data flow and test details: [references/architecture.md](references/architecture.md). Your own books, typography, Dynamic Type and what we measured in each pose: [references/books-and-text.md](references/books-and-text.md).

## 3. How it behaves in each pose

| Pose | Reader (*measured*, inside the navigation stack) | Pages | Page turns | Shelf |
|---|---|---|---|---|
| Closed (outer display) | 382 × 562 pt | one | vertical bar on the side | two columns |
| Open, flat, held wide | 867 × 553 pt, fold flat | two, either side of the fold line | vertical bar | two columns each side of the fold line |
| Book | 867 × 553 pt, fold active | the same two, so no new pagination | vertical bar | the same columns |
| Tabletop | 669 × 835 pt, fold active across | one, above the fold | below the fold, with Contents and Text Size | four in a row; the shelf scrolls across the fold |

*Measured* with Device Hub's pose buttons pressed by `duo-pose`, one app process through closed, open and book and another through tabletop and closed: at character 2,400 of the first chapter, the page on screen held it in every pose (closed page 4 of 7, open and book pages 3 and 4 of 8, tabletop page 4 of 7). Details: [references/books-and-text.md](references/books-and-text.md#what-we-measured).

## 4. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| The place survives every fold | `ReadingLog` in `LibraryStore`, `@State` in `RootView` | State above a layout switch survives it (`duo-continuity`). The place is two numbers, saved on every change. |
| The place is an offset, never a page | `ReadingPosition`, `PageBreaks.page(containing:)` | Page breaks change with every fold, rotation and text size; the first character on screen doesn't ([duo-reading](https://github.com/Kimeur/duology/blob/main/plugins/duology-features/skills/duo-reading/SKILL.md)). |
| Never skip unread text | `PageBreaks.firstPage(showing:perSpread:)` | A spread starts on an even page, so the page holding the offset is always on screen, leading or trailing. |
| Pages split at the fold, not the middle | `ReaderLayout`, fed by `onFoldChange` | [`reservedRegions(kind:options:layoutDirectionBehavior:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) with `.division` and `.includeInactive`, on the reader's own frame. *Measured:* the fold's frame started at x 455.5 in an 867 pt reader, 22 pt right of its middle. |
| Folding doesn't paginate again | `PaginationKey` | Flat and book give the same page size, so the key doesn't change when the fold turns active. |
| Tabletop: read above, turn below | `ReaderLayout` mode `.tabletop`, `tabletopControls` | Apple's optional per-pose layout: content in the top half, controls in the stable bottom half, the same controls as every other pose ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=276)). |
| Page turns stay off the fold | System bars; tabletop controls in their own region | Toolbars move off the fold on their own ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)). |
| Dynamic Type reflows the pages | `TextStyle.attributed(_:size:)`, the type size in `PaginationKey` | The text is built at the reader's size and paginated again; the offset keeps the place. The in-app Text Size menu moves the system size by steps. |
| Pages never overflow | `Paginator` and `PageTextView` | Both TextKit 1 ([`NSLayoutManager`](https://developer.apple.com/documentation/uikit/nslayoutmanager), [`NSTextContainer`](https://developer.apple.com/documentation/uikit/nstextcontainer)) with the same padding; [`UITextView(usingTextLayoutManager: false)`](https://developer.apple.com/documentation/uikit/uitextview/init(usingtextlayoutmanager:)). |
| No size feedback | `.frame(minWidth: 0, maxWidth: .infinity, minHeight: 0, maxHeight: .infinity)` on the reader | The pages' sizes come from the measured size; a frame that grows to fit them would never shrink (`duo-reading`). |
| An even shelf | `ShelfColumns`, `ShelfLayout` | When a fold crosses a grid, flat or folded, use an even column count with the fold in a gutter ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=456)). |
| VoiceOver page turns | `accessibilityScrollAction` on the reader | A three-finger swipe turns the page ([`accessibilityScrollAction(_:)`](https://developer.apple.com/documentation/swiftui/view/accessibilityscrollaction(_:))). |

## 5. Customise

Change the books and the rules first, then the look.

- **Your books:** add them to `Books/Library.json`, one `.txt` file per chapter; blank lines separate paragraphs. File names must be unique across books. Run `Tools/run-model-tests.sh`: it checks every file is there and has text. More, including long books and EPUB: [references/books-and-text.md](references/books-and-text.md#your-own-books).
- **Typography:** `TextStyle` (font, line height, paragraph spacing, hyphenation) and `PageInsets` (margins, running head, page number, longest line). Paginator and pages share them, so change them in one place.
- **Looks:** `BookCover`, `BookTile`, `ContinueCard`, `PageView`.
- **Add a model rule:** write it in `Model/`, keep it `nonisolated` and `Sendable`, add a check in `Tools/ModelTests/main.swift` and a line to its off-main-actor check.

Keep these, whatever the app:

1. The place is a chapter and a character offset, in a store above the navigation stack.
2. Paginate again for a new page size, text size or chapter; show the page that holds the offset.
3. One `ReaderScreen` for every pose; the first page is the same view in every mode. Never an `if` on the pose around the pages.
4. Page regions from the fold's frame, never from half the width.
5. The same controls in every pose. Tabletop moves them below the fold; it never adds or removes one.
6. Paginator and page view on the same text engine, with the same padding and insets.

## 6. Test it

**On the Mac:** `Tools/run-model-tests.sh` builds `Model/*.swift` and `Text/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`, like the app target. It reads the real `Library.json` and every chapter, paginates the first chapter through AppKit and checks every character lands on exactly one page and the place stays on screen at three page sizes. The layout checks use the reader sizes and fold frames measured on the Duo simulator. *Measured:* 147 checks, under 10 seconds with the build.

**On the simulator:** `Tools/run-ui-tests.sh`. The tests start from launch switches (`-open`, `-chapter`, `-offset`, `-textStep`, `-resetState`), find elements by identifier, tap through `element.coordinate(withNormalizedOffset:)`, and read the reader through the `reader.state` marker (`book=keeper|chapter=0|offset=2400|first=2|pages=8|mode=spread|shown=1261-2546|step=0|ready=1|`). Every test that moves the place checks the saved offset is inside `shown`. They never depend on the pose.

*Measured:* all nine passed on the Duo simulator open and held wide, about 115 s of tests, and `testReaderLayoutInThisPose` passed closed, in book pose and in tabletop. Set the pose in Device Hub (or with `duo-pose`), then run that test once per pose:

```bash
Tools/run-ui-tests.sh -only-testing:ShelfieUITests/ShelfieUITests/testReaderLayoutInThisPose
```

Then check each pose by hand in Device Hub, or with `duo-pose-matrix` (needs the user's Accessibility permission):

```bash
duo-pose-matrix com.example.shelfie --case "reader=-resetState -open keeper -chapter 0 -offset 2400"
```

To see the place survive the poses, pass `--no-relaunch`. For the shelf, launch once with `-open bread -chapter 1 -offset 900` so Continue Reading has a book, then run the matrix with `--case "library="` (no switches: the saved place stays).

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-model-tests.sh` prints `0 failed`.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] The app launched on the Duo simulator; you looked at the screenshot of the display in use.
- [ ] `Tools/run-ui-tests.sh` passes.
- [ ] Closed: one page. Open and held wide, flat or like a book: two pages, no text inside the fold's frame.
- [ ] Tabletop: the page ends above the fold; Previous, Next, Contents and Text Size sit below it.
- [ ] Read to the middle of a chapter, then close, open, fold, rotate and close again: the same paragraph is on screen each time.
- [ ] Text size from the smallest to AX5 (the reader's menu, or Settings): the pages reflow and the place holds.
- [ ] The shelf: an even number of columns on the open phone, no cover on the fold, Continue Reading on the leading side.
- [ ] VoiceOver reads the page and a three-finger swipe turns it, in every pose.
