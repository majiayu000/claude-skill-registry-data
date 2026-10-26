---
name: duo-reading
description: "Builds reading and document screens for iPhone Duo, Apple's foldable: one page on the closed outer display, two facing pages split at the fold when the phone is open and held wide or folded like a book, and in tabletop the page above the fold with page turns below it. Use when you build an e-reader, a long-form or PDF viewer, notes beside a document, or when a reader loses its place on fold, unfold, rotation or a Dynamic Type change. Covers TextKit 1 pagination (NSLayoutManager, NSTextContainer) that keeps the place as a character offset, PagedReader with FoldGeometry and reservedRegions(kind: .division, options: .includeInactive), notes that move between the trailing region and a sheet, Dynamic Type reflow, text selection that stays inside one page (iOS 27 Text range selection, a UITextView edit menu Add to Notes action, drag), PDFKit two-up centred on the fold, and Apple Pencil, which Apple says comes later in 2026 (what it will support is unverified)."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-reading

Reading suits iPhone Duo: one page when closed, two facing pages when open, like a book. This skill builds that, keeps the reader's place through every fold, and puts notes, selection and PDFs in the right region.

Load neighbours when the task needs them: `duo-patterns` (the two-page pattern and its measured fold frames), `duo-continuity` (state through a fold), `duo-postures` (book and tabletop), `duo-accessibility` (Dynamic Type, VoiceOver), `duo-layout` (reserved regions in depth).

Labels: *measured* means we ran it in a probe app on the iPhone Duo simulator (Xcode 27.1, iOS 27.1, 20 Oct 2026); details in [references/measurements.md](references/measurements.md). *Unverified* means we could not confirm it. Everything else links to Apple. "Book" and "tabletop" are Duology's words for Apple's "partially folded, like a book" and "seated on a table like a laptop"; no API reports them.

## Rules

1. **Scrolling text may cross the fold; paged text splits at it.** Apple says articles, feeds and documents that scroll don't need to move away from the fold ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=225), [talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=597)). A page is not scrolling content: give each page its own region.
2. **The place is a character offset, never a page number.** Page breaks change with every fold, rotation and text size. The offset of the first character on screen doesn't.
3. **Paginate again after every size or text size change, once the size settles.** Then show the page that holds the offset.
4. **Never skip unread text.** A spread starts on an even page. After any change, the page holding the offset is on screen, even if the offset falls mid-page.
5. **One page or two by the fold, not by device.** Two pages only when a top-to-bottom fold crosses the reader, or on a wide regular-width view without a fold. Use size class and `.division`, never `UIScreen.main`, idiom or orientation ([prepare page](https://developer.apple.com/iphone-duo/prepare/)).
6. **Page turns are buttons in the system bottom bar**, which stays off the fold on its own ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)). Add a VoiceOver scroll action. Never turn pages from the hinge: folds happen by accident.
7. **Notes go on the trailing side** of the fold when there is room, in a sheet otherwise. The text lives in a model, so moving it loses nothing.
8. **A selection lives inside one page.** Don't promise selection across the fold. Offer Add to Notes and drag instead.
9. **Dynamic Type reflows the pages.** Build the text at the reader's size and paginate again; the offset keeps the place.
10. **No Pencil-only features yet.** Apple has announced Apple Pencil (USB-C) for iPhone Duo later in 2026 ([Newsroom](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/)). Build markup that works with a finger.

## What the reader does in each pose

| Pose | Reader (measured, inside a `NavigationStack`) | Pages | Notes |
|---|---|---|---|
| Closed | 382 × 620 pt | one | sheet |
| Closed, sideways (tent) | not measured | one, wide | sheet |
| Open, flat, held wide | 867 × 611 pt (the bar takes 84 pt) | two, split at the fold line | trailing region |
| Book | 867 × 611 pt, fold active | two, the fold's frame between them | trailing region |
| Open, flat, held tall | 669 × 787 pt | one tall page | sheet |
| Tabletop | 669 × 835 pt, fold active across | one, above the fold; page turns below | sheet |
| Split View | not measured | one | sheet |

The fold frame stays put when the phone folds; only `isActive` changes ([`duo-patterns` two-page measurements](https://github.com/Kimeur/duology/blob/main/plugins/duology-design/skills/duo-patterns/references/two-page.md#what-we-measured)). So flat and book get the same pages, and folding doesn't paginate again (*measured*).

## Paginate by character offset

`PageBreaks` holds character ranges, one per page. `Paginator` fills page-sized TextKit 1 containers until the text runs out. Pages render with the same engine, so a page never overflows ([`NSLayoutManager`](https://developer.apple.com/documentation/uikit/nslayoutmanager), [`NSTextContainer`](https://developer.apple.com/documentation/uikit/nstextcontainer)).

```swift
import SwiftUI
import UIKit

/// Where each page starts and ends, as character ranges in the chapter.
/// A place in the text is a character offset, so it survives any new page size.
nonisolated struct PageBreaks: Equatable, Sendable {
    var ranges: [NSRange] = []

    /// The page that holds a character offset (the last page if the offset is past the end).
    func page(containing offset: Int) -> Int {
        ranges.firstIndex { NSMaxRange($0) > offset } ?? max(ranges.count - 1, 0)
    }
}

enum Paginator {
    /// Lays the text out in page-sized containers until it runs out (TextKit 1).
    static func pageBreaks(for text: NSAttributedString, pageSize: CGSize) -> PageBreaks {
        guard text.length > 0, pageSize.width >= 44, pageSize.height >= 44 else { return PageBreaks() }
        let storage = NSTextStorage(attributedString: text)
        let layout = NSLayoutManager()
        storage.addLayoutManager(layout)
        var ranges: [NSRange] = []
        while NSMaxRange(ranges.last ?? NSRange()) < text.length {
            let container = NSTextContainer(size: pageSize)
            container.lineFragmentPadding = 0          // PageTextView uses the same value
            layout.addTextContainer(container)
            let glyphs = layout.glyphRange(for: container)
            let characters = layout.characterRange(forGlyphRange: glyphs, actualGlyphRange: nil)
            guard characters.length > 0 else { break } // not even one line fits
            ranges.append(characters)
        }
        return PageBreaks(ranges: ranges)
    }

    /// Body text at the reader's Dynamic Type size. Rebuild it when the size changes.
    static func styledText(_ plain: String, size: DynamicTypeSize) -> NSAttributedString {
        let traits = UITraitCollection(preferredContentSizeCategory: UIContentSizeCategory(size))
        let paragraph = NSMutableParagraphStyle()
        paragraph.lineSpacing = 3
        paragraph.paragraphSpacing = 10
        paragraph.hyphenationFactor = 0.7
        return NSAttributedString(string: plain, attributes: [
            .font: UIFont.preferredFont(forTextStyle: .body, compatibleWith: traits),
            .foregroundColor: UIColor.label,
            .paragraphStyle: paragraph,
        ])
    }
}
```

- *Measured:* with the place at character 20,000 of a 44,500-character chapter, the page on screen held it in every pose: closed page 22 of 48, open and book pages 23 and 24 of 50, tabletop page 22 of 48.
- *Measured:* a 44,500-character chapter took 0.04 to 0.15 s to paginate on the simulator; 558,000 characters (a long novel) took 1.1 to 3.1 s in four runs. The simulator runs on the Mac's CPU. Paginate one chapter at a time. Device speed is unverified.
- Spreads lose at most one page of position: after closing, the reader sees the leading page of the last spread. That is the price of never skipping text.

## The reader

`PagedReader` renders pages with `PageTextView`, a non-scrolling TextKit 1 `UITextView`. Full code, with the tabletop layout and every pitfall: [references/paged-reader.md](references/paged-reader.md). It needs `FoldGeometry` from [references/fold-geometry.md](references/fold-geometry.md).

```swift
import SwiftUI

// requires: Chapter, PagedReader (references/paged-reader.md)

@available(iOS 27.1, *)
struct BookScreen: View {
    let chapter: Chapter
    // The place, saved per window. It also comes back after the system ends the app.
    @SceneStorage("reader.offset") private var offset = 0

    var body: some View {
        NavigationStack {
            PagedReader(chapter: chapter, offset: $offset)
                .navigationTitle(chapter.id)
                .navigationBarTitleDisplayMode(.inline)
        }
    }
}
```

What the reader does, and why:

- **Splits at the fold, not the middle.** Held wide, the reader is 867 pt wide and the fold is at x = 455.5, 22 pt right of the reader's middle (*measured*).
- **Gives both pages the narrower region's size**, so one pagination serves both sides.
- **Tabletop: the page above the fold, page turns below.** A single tall page put text lines inside the active fold band (*measured* before the fix). Apple suggests content on top and controls on the stable base below when the phone sits on a table ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=263)). The bottom bar hides there and the same buttons move into the bottom region.
- **Measures its size with `.frame(minWidth: 0, maxWidth: .infinity, minHeight: 0, maxHeight: .infinity)`.** With only `maxWidth: .infinity`, the frame grew to fit its fixed-width pages and the measured size fed back into the page widths: once it measured 951 pt, the reader stayed 951 pt wide in tabletop and on the closed phone, and pages ran off both edges (*measured*).
- **Waits 200 ms for the size to settle.** Opening the phone sent seven sizes in 0.2 s, and the reader paginated once, after the last (*measured*). `task(id:)` cancels the wait when a newer size arrives.

## Document and notes side by side

Open, the notes take the facing page's place on the trailing side of the fold. Closed, held tall or in tabletop, they open in a sheet. Code: [references/notes-beside.md](references/notes-beside.md).

- *Measured:* notes open on the closed phone showed as a sheet. Opening the phone dismissed the sheet and the notes appeared beside a single page in the leading region (455.5 pt wide). Closing it again brought the sheet back.
- Trailing is where Apple moves alerts in book pose, because that is where they sit once the phone closes ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=249)).
- Keep the notes text, the open state and the reader's offset in one `@Observable` model above the layout. The sheet and the pane are two different editors, so keyboard focus doesn't move with the notes; the text does.
- Where the keyboard appears in book pose and in tabletop is unverified. Check that the notes field stays visible.

## Dynamic Type

- Build fonts from the environment's `dynamicTypeSize` with `UIFont.preferredFont(forTextStyle:compatibleWith:)` and `UIContentSizeCategory(_:)`. Don't let `UITextView` adjust fonts on its own (`adjustsFontForContentSizeCategory = false`): the pages would grow but the breaks wouldn't.
- Put the type size in the pagination key, next to the page size and the chapter. The offset stays.
- *Measured* at the largest accessibility size: the place held in every pose, and a closed page held about 100 characters instead of about 900 at Large. Keep two pages in book pose anyway: each region is still about as wide as the closed page (331.5 pt against 342 pt, *measured*). Apple's typography guidance at large sizes is fewer columns, not text across the fold ([HIG: Typography](https://developer.apple.com/design/human-interface-guidelines/typography)).

## Text selection across panes

Two pages are two text views, and a selection stays inside one of them. Details and code: [references/selection-and-pencil.md](references/selection-and-pencil.md).

- In iOS 27, a SwiftUI `Text` with `textSelection(.enabled)` shows selection handles and selects a range. In iOS 26 and earlier it offered a menu for the whole text ([`textSelection(_:)`](https://developer.apple.com/documentation/swiftui/view/textselection(_:))).
- `PageTextView` adds **Add to Notes** to the edit menu with `textView(_:editMenuForTextInRanges:suggestedActions:)` (iOS 26). *Measured* by UI test: a touch and hold on a page selected a word, and Add to Notes put the quote in the notes: beside the page in book, in the sheet closed and in tabletop. Put the action first; appended last, it sat on the menu's second page.
- Drag works too. *Measured:* `UIDragInteraction.isEnabledByDefault` and a new `UITextView`'s `textDragInteraction?.isEnabled` were both `true` on the iPhone Duo simulator. `PageTextView` sets it anyway. Dropping text into a SwiftUI `TextEditor` on a device is unverified.
- For long highlights, offer a scroll layout of the chapter in one text view.

## PDFs and fixed layouts

PDF pages don't reflow, so the place is a page index. `PDFView` in `.twoUp` centres the spread in its own frame, so give it a frame centred on the fold (*measured*: the pages then met at the fold's centre). Turn `displaysAsBook` off: on, the cover sat alone across the fold (*measured*). Code and the UIKit version of the reader: [references/pdf-and-uikit.md](references/pdf-and-uikit.md).

## Apple Pencil (coming)

- Apple says iPhone Duo will support Apple Pencil (USB-C) later in 2026, for notes, sketches and markup on either display ([Newsroom](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/)). Which Pencil features work on iPhone Duo is unverified.
- On iPad, that model has tilt and hover but no pressure, double tap or squeeze ([Apple Pencil](https://www.apple.com/apple-pencil/)). Don't depend on them.
- Use PencilKit with `drawingPolicy = .anyInput` so fingers draw today ([`PKCanvasView`](https://developer.apple.com/documentation/pencilkit/pkcanvasview)).
- Never anchor ink to points on reflowing text: every fold moves the words. Store highlights as text ranges; keep ink for fixed pages such as PDFs and images.

## UIKit

Use the same `Paginator`. Lay out two `UITextView(usingTextLayoutManager: false)` pages in `layoutSubviews` from `reservedRegions(kind: .division, options: .includeInactive)`; UIKit runs it again when the fold turns active or inactive (*measured* in `duo-postures`). `SpreadView` in [references/pdf-and-uikit.md](references/pdf-and-uikit.md). Don't choose a `UIPageViewController` spine from the interface orientation: the inner display ignores your supported orientations ([talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=222)).

## Test it

In Device Hub: Closed, Open, Partially Open, and Rotate Right for tabletop ([Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)).

1. Turn to a page in the middle of a chapter. Close, open, fold, rotate, close again. The same paragraph must be on screen each time.
2. Book: no line of text and no button inside the fold frame.
3. Tabletop: the page ends above the fold; page turns sit below it.
4. Change Dynamic Type from the smallest size to AX5 (Xcode's Environment Overrides, or launch with `-UIPreferredContentSizeCategoryName UICTContentSizeCategoryAccessibilityXXXL`). The place holds.
5. Open notes closed, then open the phone: notes move beside the page, text intact.
6. Select text on a page, pick Add to Notes in every pose.
7. VoiceOver: a three-finger swipe turns the page.

## Checklist

- [ ] The place is a character offset in a model or `@SceneStorage`, never a page index or scroll offset.
- [ ] Pages paginate again after size, chapter and Dynamic Type changes, after the size settles.
- [ ] One page closed; two pages only with a top-to-bottom fold or a wide regular-width view; split at the fold frame.
- [ ] Tabletop: the page sits above the fold and the page turns below it.
- [ ] The reader's frame uses `minWidth: 0` and `minHeight: 0`, so its measured size can't feed back.
- [ ] Spreads start on an even page; nothing unread is skipped after a fold.
- [ ] Page turns are system bar buttons with labels, plus a VoiceOver scroll action; no hinge page turns.
- [ ] Notes sit on the trailing side when open and in a sheet otherwise; their text lives in a model.
- [ ] Selection offers Add to Notes; nothing promises selection across the fold.
- [ ] PDF two-up is centred on the fold; ink is stored per fixed page, never on reflowing text.
- [ ] iOS 27.1 APIs are behind `@available` or `if #available` when the app deploys lower.
- [ ] Checked in Device Hub: Closed, Open wide and tall, book, tabletop, AX5 text size, right-to-left.
