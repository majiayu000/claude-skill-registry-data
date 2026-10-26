---
name: duo-patterns
description: Picks and builds layout patterns for iPhone Duo, Apple's foldable iPhone, in SwiftUI - list-detail, supporting pane, two-page, dual view, extended canvas, feed reflow with even columns, tabs to sidebar, and displacement off the fold. Use it when you design or fix a screen for the outer display and the inner display, when content or buttons land in the fold, or when choosing between NavigationSplitView, inspector, ArrangementView (split and overlay styles), TabView with sidebarAdaptable and defaultTabBarPlacement, and reserved regions (division, occlusion, includeInactive).
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# Duo layout patterns

Use this skill to choose a layout pattern for a screen on iPhone Duo, then build it. Every pattern has a reference file with when to use it, closed and open behaviour, the Apple APIs, rules, pitfalls, a SwiftUI recipe that typechecks against the iOS 27.1 SDK, and a screen in the Duology gallery app.

Read the reference for the pattern you pick before you write code. For bars and toolbars, load `duo-navigation`. For size classes, safe areas and UIKit layout depth, load `duo-layout`. For keeping state through a fold, load `duo-continuity`.

## Ground rules for every pattern

1. **Design for two size classes, not for poses.** Compact width for the outer display, regular width for the inner display. Let the layout grow; don't design one layout per way of holding the phone ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Device-poses), [talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=222)).
2. **One app on both displays.** Same features and same state closed and open. Open may add one level of hierarchy, as Mail adds the message beside the list ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)).
3. **System containers first.** `NavigationSplitView`, `TabView`, `NavigationStack`, sheets, alerts, menus and toolbar buttons already adapt to the fold ([hub](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo), [talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=519)).
4. **Nothing interactive in the fold.** Scrolling content may cross it ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)).
5. **Even columns** whenever a fold crosses a grid, active or not ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions), [talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=470)).
6. **Small moves.** Move only what must move. Don't swap in a different view tree when the window resizes; you lose scroll position, selection and typing ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)).
7. **Arrangement placement.** Navigation outside, content inside. Put an `ArrangementView` inside a `NavigationStack` or a tab. Never put a navigation container inside an arrangement, and never put an arrangement inside a `List` or `ScrollView`. Don't nest it with a `NavigationSplitView` either way; Apple's pages disagree on that case, so see [Combining patterns](#combining-patterns) ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=969), [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Arrangement-views), [hub](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)).
8. **No posture API exists.** Lay out with size classes, the view's own size, arrangements and reserved regions. Use the hinge (`onHingeChange`) for effects only ([talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/)).
9. **No device checks.** Never lay out from `UIScreen.main`, `userInterfaceIdiom`, interface orientation or fixed sizes ([prepare page](https://developer.apple.com/iphone-duo/prepare/)).

## What a layout can read

| Input | API | Use it for |
|---|---|---|
| Width class | `@Environment(\.horizontalSizeClass)` | One pane or two |
| The view's own size and shape | [`onGeometryChange(for:of:action:)`](https://developer.apple.com/documentation/swiftui/view/ongeometrychange(for:of:action:)) | Wide or tall, column count |
| The fold | [`reservedRegions(kind: .division, options:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) (iOS 27.1) | Where to split, where controls may not go |
| Cameras and the status bar corner | `reservedRegions(kind: .occlusion, options:)` | Keeping controls clear |
| System margins, per side | [`contentMargins(for: .container, edges:)`](https://developer.apple.com/documentation/swiftui/view/contentmargins(for:edges:alignment:)) (iOS 27.1) | Asymmetric margins next to a vertical bar |
| Is a tab sidebar available | [`isTabViewSidebarAvailable`](https://developer.apple.com/documentation/swiftui/environmentvalues/istabviewsidebaravailable) (iOS 27.0) | Hiding shortcuts the sidebar repeats |

## Pick a pattern

Answer in order. The first yes is the screen's main pattern. If a later question is also a yes, read [Combining patterns](#combining-patterns).

1. Many top-level sections, information-dense? **Tabs to sidebar**, then pick a pattern for each tab.
2. Two halves that must both show in every pose (two players, a before and after), or two people sharing the screen? None of these patterns: use `EvenSplit` or `FoldSplitLayout` from `duo-layout`, and `duo-shared-screen`. A split arrangement can drop to its primary view alone, for example on the closed phone held sideways.
3. Items, each with its own detail that makes sense alone? **List-detail.**
4. A second view that only makes sense next to the main one (comments, transcript, tools)? **Supporting pane.**
5. The same data shown two ways (list and map, source and preview)? **Dual view.**
6. Content made of pages (book, slides, document)? **Two-page.**
7. Many equivalent items in a scrolling grid? **Feed reflow.**
8. One continuous surface to pan or draw on (map, canvas, timeline)? **Extended canvas.**
9. Any screen with a control you place yourself near the middle: add **displacement** to whatever you picked.

## Catalog

"Partly folded" means folded like a book, the fold running top to bottom.

| Pattern | Closed (outer) | Open, flat | Partly folded | Build with | Reference | Gallery screen |
|---|---|---|---|---|---|---|
| List-detail | List, then detail | Both, list narrower | 50/50 at the fold, by the system, while `columnVisibility` is `.all` | `NavigationSplitView` with `columnVisibility` | [list-detail.md](references/list-detail.md) | [ListDetailView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/ListDetailView.swift) |
| Supporting pane | Main content; pane in a sheet | Main plus a narrower pane | One per side | `ArrangementView`, `.split.axes(.horizontal)` | [supporting-pane.md](references/supporting-pane.md) | [SupportingPaneView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/SupportingPaneView.swift) |
| Two-page | One page | Two pages, gap on the fold line | One page per side | Custom split from the `.division` region | [two-page.md](references/two-page.md) | [TwoPageView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/TwoPageView.swift) |
| Dual view | One view and a switch | Both views, in sync | One per side | `ArrangementView` split, shared model | [dual-view.md](references/dual-view.md) | [DualView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/DualView.swift) |
| Extended canvas | Canvas | Canvas across the fold | Canvas across; tools move to one side | Full-size view, tools placed from `.division` | [extended-canvas.md](references/extended-canvas.md) | [ExtendedCanvasView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/ExtendedCanvasView.swift) |
| Feed reflow | As many columns as fit | Even column count | Half the columns per side, fold as the gap | `LazyVGrid`, `.division` with `.includeInactive` | [feed-reflow.md](references/feed-reflow.md) | [FeedReflowView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/FeedReflowView.swift) |
| Tabs to sidebar | Tab bar on the side | Sidebar | Sidebar (not measured folded) | `TabView`, `.sidebarAdaptable`, `.defaultTabBarPlacement(.sidebar)` | [tabs-to-sidebar.md](references/tabs-to-sidebar.md) | [TabsToSidebarView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/TabsToSidebarView.swift) |
| Displacement | Unchanged | Unchanged | Controls move to the trailing region; content stays | `.division` region, active only | [displacement.md](references/displacement.md) | [DisplacementView](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/DisplacementView.swift) |

Folded across instead (the phone held tall and set on a table like a laptop), the regions are top and bottom: content to look at goes up, controls go down ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=240)).

## Combining patterns

Most screens need one pattern. When two questions above get a yes, combine them like this:

| Screen | Build it like this |
|---|---|
| Tabs plus any pattern | The pattern goes inside each tab. Prefer a `NavigationStack` in a tab; a `NavigationSplitView` there adds a second leading column ([tabs-to-sidebar.md](references/tabs-to-sidebar.md#pitfalls)). |
| List-detail plus a side pane (a notes list, the note, a summary pane) | `NavigationSplitView`, with [`inspector(isPresented:content:)`](https://developer.apple.com/documentation/swiftui/view/inspector(ispresented:content:)) on the detail column. Recipe below. |
| Supporting pane or dual view with navigation | `NavigationStack { ArrangementView { … } }`, also inside a tab. The recipes in [supporting-pane.md](references/supporting-pane.md) and [dual-view.md](references/dual-view.md) already do this. |
| Any pattern plus your own centred controls | Add [displacement](references/displacement.md) to those controls only. |

Split views and arrangements: the talk and the HIG say navigation containers, split views included, go around an arrangement, not inside it. The hub says to avoid an arrangement inside a navigation split view, because part of it can become unreachable. Follow the stricter hub rule, as `duo-navigation` does: never nest an `ArrangementView` with a `NavigationSplitView` in either direction. For a pane beside list-detail, use an inspector. It is a system container, so it needs no arrangement.

```swift
import SwiftUI

// requires: Note, NoteDetail (references/list-detail.md)

struct NotesWithSummary: View {
    let notes: [Note]
    @SceneStorage("notes.selection") private var selection: Note.ID?
    @SceneStorage("notes.showsSummary") private var showsSummary = false
    // Same rule as list-detail.md: both columns when wide, the note alone when tall.
    @State private var columnVisibility = NavigationSplitViewVisibility.all
    @State private var isWide = true

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            List(notes, selection: $selection) { Text($0.title) }
                .navigationTitle("Notes")
        } detail: {
            if let note = notes.first(where: { $0.id == selection }) {
                NoteDetail(note: note)
                    .toolbar {
                        ToolbarItem {
                            Button("Summary", systemImage: "sparkles") { showsSummary.toggle() }
                        }
                    }
                    // Open: a trailing column. Closed: a sheet. Same view, same state.
                    .inspector(isPresented: $showsSummary) {
                        Text("Summary of \(note.title)")
                            .inspectorColumnWidth(min: 240, ideal: 300, max: 360)
                    }
            } else {
                ContentUnavailableView("No Note Selected", systemImage: "note.text")
            }
        }
        .onGeometryChange(for: Bool.self) { $0.size.width > $0.size.height } action: {
            isWide = $0
            columnVisibility = isWide || selection == nil ? .all : .detailOnly
        }
        .onChange(of: selection) {
            columnVisibility = isWide || selection == nil ? .all : .detailOnly
        }
    }
}
```

Apple's inspector doc promises a trailing column at regular width and a sheet at compact width. Measured on the closed simulator (382 pt wide, compact): the pane came up at 374 × 636 pt over a full-width detail, whether the inspector sat on the detail column or on the whole split view. Open, the list, the note and the pane share the inner display; check in Device Hub that the note keeps a usable width. (unverified open and folded)

## Shared helper: FoldGeometry

Three recipes (two-page, extended canvas, displacement) use this helper. Add it to the app once. It typechecks against the iOS 27.1 simulator SDK in Swift 5 and Swift 6 mode, with an iOS 26 deployment target, and with a new Xcode 27.1 app's settings (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency). Keep `nonisolated`: without it, that setting makes the struct's `Equatable` conformance main-actor isolated, and `onGeometryChange` rejects it.

```swift
import SwiftUI

/// Where the fold crosses a view, read from the view's reserved regions.
/// Layout input only. Never drive layout from the hinge angle.
@available(iOS 27.1, *)
nonisolated struct FoldGeometry: Equatable, Sendable {
    /// The fold's frame in this view's space, margins included. Nil when no fold crosses the view.
    var frame: CGRect?
    /// True while the phone is partly folded. False when it lies flat.
    var isActive = false

    /// True when the fold runs top to bottom, so the view has a left half and a right half.
    var isVertical: Bool {
        guard let frame else { return false }
        return frame.height > frame.width
    }

    init(frame: CGRect? = nil, isActive: Bool = false) {
        self.frame = frame
        self.isActive = isActive
    }

    init(_ proxy: GeometryProxy) {
        // The default query returns active regions only. Ask for inactive ones too,
        // so a flat inner display still tells you where its fold is. Keep only a
        // fold with part of this view on each side of it.
        let size = proxy.size
        let folds = proxy.reservedRegions(kind: .division, options: .includeInactive)
            .filter { Self.liesInside($0.frame, of: size) }
        if let fold = folds.first(where: \.isActive) ?? folds.first {
            frame = fold.frame
            isActive = fold.isActive
        }
    }

    /// True when a fold frame splits a view of `size` into two non-empty parts.
    /// A region query can return regions that lie outside the view (`duo-postures`).
    static func liesInside(_ frame: CGRect, of size: CGSize) -> Bool {
        if frame.height > frame.width {
            return frame.minX > 0 && frame.maxX < size.width
        }
        return frame.minY > 0 && frame.maxY < size.height
    }
}

@available(iOS 27.1, *)
extension View {
    /// Calls `action` with the fold geometry now and every time it changes.
    func onFoldChange(_ action: @escaping (FoldGeometry) -> Void) -> some View {
        onGeometryChange(for: FoldGeometry.self) { proxy in
            FoldGeometry(proxy)
        } action: { fold in
            action(fold)
        }
    }
}
```

Use it: `@State private var fold = FoldGeometry()`, then `.onFoldChange { fold = $0 }` on the view whose space you lay out in. Region frames come back in that view's coordinates, mirrored for right-to-left by default. Don't attach it inside a scroll view's content unless you store only x values; see [feed-reflow.md](references/feed-reflow.md).

### Measured on the simulator

iOS 27.1 iPhone Duo simulator, open, flat, held wide (951 × 669 pt), Xcode 27.1, 16 Oct 2026:

- The default `.division` query returned nothing. With `.includeInactive` it returned one inactive fold: a 40 pt frame, centred, full height, with 20 pt margins each side. Talk 111463 says the default is "active only"; Apple's `ReservedRegion` page says the opposite. The simulator agrees with the talk.
- The default `.occlusion` query returned one active 84 × 124 pt region in the top trailing corner, where the status bar sits. `.includeInactive` added a 58 × 37 pt inactive one, likely the inner camera (our reading).
- The first read in `onAppear` was empty. Values came with the next geometry update.
- Partly folded like a book (18 Oct 2026, gallery screenshots with the region overlay): the same `.division` region turned active and stayed in place, 40 × 669 pt at (455, 0), top to bottom. Partly folded and held tall (tabletop), it ran across: active, 669 × 40 pt at (0, 455). The overlay prints y = 17 held wide because its own view starts 17 pt above the display. Details in [two-page.md](references/two-page.md#what-we-measured).

## Arrangement facts

From Apple's [hub](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo), [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Arrangement-views), [`ArrangementView`](https://developer.apple.com/documentation/swiftui/arrangementview) and [talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=560):

- The default style, `.automatic`, resolves to `.split`.
- **Split** puts the two views side by side when the arrangement is wider than tall, and stacks them when taller than wide. Size class and active divisions are inputs too. `.split.axes(.horizontal)` forbids stacking; if it can't split, it shows only the primary.
- **Overlay** layers the primary over the secondary while no division is active (closed, or open flat). Partly open, it puts the primary in the trailing or bottom part and the secondary in the leading or top part.
- Pick split for main-detail content where neither may be covered (HStack or VStack today). Pick overlay for foreground over background (ZStack today), such as controls over video.
- Size split views with `splitArrangementLayoutRatio` or `splitArrangementLayoutSize`, never fixed widths.

Measured on the simulator, open and flat:

- `.split.axes(.horizontal)` in a frame taller than wide showed only the primary. The secondary still ran `onAppear` and got the full size. No API told us it was hidden.
- A primary shorter than the overlay sat at the top edge, over the secondary.
- `splitArrangementAxis` read `nil` and `overlayArrangementZIndex` read `0` in the views passed to the arrangement, full screen and in frames: those views get the defaults. Read both one view down (`duo-layout`). There, `overlayArrangementZIndex` in the primary read `1` closed and open flat and `0` in book and tabletop (*measured* in `duo-media`). `splitArrangementAxis` folded is unverified.

## UIKit

| Pattern | UIKit |
|---|---|
| List-detail | `UISplitViewController` |
| Supporting pane, dual view | `UIArrangementViewController`, `setViewController(_:for:)`, `updateArrangement(.split.axes(.horizontal))` |
| Tabs to sidebar | `tabBarController.mode = .tabSidebar` plus `tabBarController.sidebar.preferredPlacement = .sidebar` (iOS 27.0). *Measured:* `preferredPlacement` alone gave no sidebar. |
| Two-page, extended canvas, feed reflow, displacement | `UIView.reservedRegions(kind:options:)` with `.division` and `.includeInactive` (iOS 27.1) |

We found no change callback for reserved regions in the UIKit headers. Re-query them in `layoutSubviews` and check in Device Hub that a fold triggers it. (unverified)

## Prior art

Duology's pattern names come from earlier foldables. Their guidance describes other hardware: treat it as ideas to test, not rules for iPhone Duo.

- Microsoft Surface Duo: [extended canvas](https://learn.microsoft.com/en-us/previous-versions/dual-screen/design/extended-canvas), [list-detail](https://learn.microsoft.com/en-us/previous-versions/dual-screen/design/list-detail), [two-page](https://learn.microsoft.com/en-us/previous-versions/dual-screen/design/two-page), [dual view](https://learn.microsoft.com/en-us/previous-versions/dual-screen/design/dual-view), [companion pane](https://learn.microsoft.com/en-us/previous-versions/dual-screen/design/companion-pane) (our supporting pane).
- Android (Material) [canonical layouts](https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts): list-detail, supporting pane, feed.
- Samsung [Flex mode](https://developer.samsung.com/galaxy-z/flex-mode.html): content up, controls down when half folded on a table.
- Displacement and arrangements are Apple's own, from talk 111463.

Every source with its check date: [`reference/sources.md`](https://github.com/Kimeur/duology/blob/main/reference/sources.md). Every API with its availability: [`reference/api-index.md`](https://github.com/Kimeur/duology/blob/main/reference/api-index.md).

## Checklist

- [ ] Picked the pattern with the list above and read its reference file.
- [ ] Layout decisions use size class, the view's size, arrangements or reserved regions. No idiom, orientation, `UIScreen.main`, hinge angle or fixed screen sizes.
- [ ] Same features and same state closed and open; open adds at most one level of hierarchy.
- [ ] No button, slider or text field sits in the fold when partly folded.
- [ ] Scrolling content is never displaced.
- [ ] Grids use an even column count when a fold crosses them.
- [ ] No `ArrangementView` inside a `List`, a `ScrollView` or a `NavigationSplitView` column, and no navigation container inside an arrangement. A pane beside list-detail is an `inspector`.
- [ ] Types passed to `onGeometryChange` are `nonisolated` when the target uses main actor default isolation.
- [ ] iOS 27.0 and 27.1 APIs are behind `@available` or `if #available` when the app supports iOS 26.
- [ ] Selection, scroll position and drafts survive close, open, Partially Open, rotation and Split View.
- [ ] Checked in Device Hub: Closed, Open, Partially Open, held wide and held tall, and Split View on the inner display.
