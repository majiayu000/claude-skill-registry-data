---
name: duo-swiftui-27
description: "The iOS 27 SwiftUI changes that matter on iPhone Duo, Apple's foldable, where every fold, unfold and rotation resizes the app. Use it when building with Xcode 27.1 breaks a view (@State macro, ContentBuilder, TN3211), when a grid or list that reflows between the outer and inner display needs drag to reorder or swipe actions, or when you adopt the new tab, toolbar, dialog or AsyncImage APIs in a Duo app. Covers the @State macro through a fold and its source breaks, reorderable() and reorderContainer(for:isEnabled:move:) in a 2 or 4 column grid and across the fold, swipeActionsContainer() outside List, Tab(role: .prominent) at the foot of the vertical tab bar, toolbarMinimizationBehavior(_:for:) (the talk's toolbarMinimizeBehavior is not in the SDK), visibilityPriority, ToolbarOverflowMenu, topBarPinnedTrailing, alert and confirmationDialog with item:, AsyncImage HTTP caching and asyncImageURLSession(_:), and resizable iPhone apps. Points to Apple's swiftui-whats-new-27 Xcode skill for the rest."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-swiftui-27

Every app that builds with Xcode 27 gets the iOS 27 SwiftUI changes. On iPhone Duo they show up more, because the app resizes each time someone opens, closes, rotates or folds the phone. This skill covers what that changes. For the rest of iOS 27 SwiftUI, use Apple's own skill (below).

Load neighbours when the task needs them: `duo-navigation` (vertical bars, ranking toolbar items), `duo-continuity` (state through a fold), `duo-patterns` (grids and two-pane layouts), `duo-system-surfaces` (the Dynamic Island that shares the side column with your bars).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 20 October 2026) with a probe app that logged its own size and fold. *Unverified* means we could not confirm it. Everything else links to Apple. Runs and logs: [references/evidence.md](references/evidence.md). Sources: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Start with Apple's skill

Xcode 27 ships two SwiftUI agent skills: `swiftui-whats-new-27` (the new APIs) and `swiftui-specialist` (best practices) ([What's new in SwiftUI](https://developer.apple.com/videos/play/wwdc2026/269/?time=1600), WWDC26 session 269). Export them with `xcrun agent skills export --output-dir <folder>` and load `swiftui-whats-new-27` when you adopt any API below. Duology links to it and never copies it.

One name differs. The talk and Apple's skill call the scroll-minimizing modifier `toolbarMinimizeBehavior`. The iOS 27.1 SDK has no such symbol. Write `toolbarMinimizationBehavior(_:for:)` with `ToolbarMinimizationBehavior` ([doc](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationbehavior(_:for:))).

## Rules

1. Build with Xcode 27.1 and fix each TN3211 break by its shape. When `init` sets a `@State` value, remove the inline default.
2. Keep reference-type models in `@State`. Never do once-only work in a view's `init`: a fold runs it again.
3. Give grids that reflow between the displays the new reorder and swipe containers, not hand-made drag code. Keep even column counts.
4. One reorder container can hold a collection on each side of the fold. In a MainActor-default target, mark its collection ID type `nonisolated`.
5. Use one `.prominent` tab, for the action that isn't a place (cart, compose). It sits apart at the foot of the vertical tab bar.
6. Rank toolbar items with `visibilityPriority(_:)`. The Dynamic Island grows in the same side column.
7. Gate the iOS 27.0 APIs with `if #available(iOS 27.0, *)` when the app deploys lower. iPhone Duo runs iOS 27.1, so the fallback runs only on other iPhones.
8. Check views that have `@State` and an `init` with a real build or `swiftc -emit-sil`. `-typecheck` misses the TN3211 initialization error (*measured*).

## Deploying below iOS 27

| Needs iOS 27.0 | Builds for any target with Xcode 27 |
|---|---|
| `reorderable()`, `reorderable(collectionID:)`, `reorderContainer(for:...)`, `swipeActionsContainer()`, `swipeActions(edge:allowsFullSwipe:content:onPresentationChanged:)`, `TabRole.prominent`, `toolbarMinimizationBehavior(_:for:)`, `visibilityPriority(_:)`, `ToolbarOverflowMenu`, `topBarPinnedTrailing`, `AsyncImage(request:...)`, `asyncImageURLSession(_:)` | the `@State` macro, `ContentBuilder`, `alert(_:item:actions:)`, `confirmationDialog(_:item:titleVisibility:actions:)` (inlined into your app; *measured*: they typecheck at an iOS 15 target) |

Availability comes from the iOS 27.1 SDK interfaces; see the [API index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#ios-27-swiftui-wwdc26).

## 1. The @State macro through a fold

`@State` is now a macro. A class you store in it is created once per view, not on every `init` of the view struct ([TN3211](https://developer.apple.com/documentation/technotes/tn3211-resolving-swiftui-source-incompatibilities-for-state-and-contentbuilder), [session 269](https://developer.apple.com/videos/play/wwdc2026/269/?time=1377)).

*Measured*: through one unfold and one fold, a parent that reads its size rebuilt its children four times, passing through 466 × 562 pt and 951 × 553 pt on the way. A class held with `@State` was created once. The same class built with `State(wrappedValue:)` in the declaration, which is the old timing, was created five times.

```swift
import SwiftUI

@Observable
final class LibraryModel {
    var books: [String] = []
}

struct LibraryScreen: View {
    @State private var model = LibraryModel()   // created once, however often the phone folds

    var body: some View {
        List(model.books, id: \.self) { Text($0) }
            .task { /* load once here, not in init */ }
    }
}
```

Source breaks, by shape:

- `@State var page = 0` plus `self.page = startPage` in `init`, before another stored property: "variable ... used before being initialized", but only in a real build. If the assignment comes last, it compiles and the default wins at run time (*measured*: the view showed page 0, not 42). Remove the default.
- Another property wrapper on a `@State` property, or a memberwise `init` called from an extension: errors whose wording in Xcode 27.1 differs from TN3211's.
- `.overlay(Color.blue.opacity(0.7))`, a constraint that spells `TupleView`, or an empty `Group { }` with MapKit visible: `ContentBuilder` ambiguity errors.

Fixes, the exact messages we saw and the probe code: [references/state-and-builders.md](references/state-and-builders.md).

## 2. Drag to reorder in a grid that reflows

`reorderable()` on a `ForEach` and `reorderContainer(for:isEnabled:move:)` on its stack, grid or layout add the system drag, placeholder and animation to any container, not only `List` ([doc](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:isenabled:move:))). The `move` closure hands you a `ReorderDifference`; you apply it to your data.

```swift
import SwiftUI

// requires: Book, BookCover, applyReorder (references/reorder-and-swipe.md)

@available(iOS 27.0, *)
struct ShelfGrid: View {
    @Binding var books: [Book]
    @Environment(\.horizontalSizeClass) private var widthClass

    var body: some View {
        // Even column counts, so the fold falls between columns on the inner display.
        let count = widthClass == .regular ? 4 : 2
        ScrollView {
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 12), count: count), spacing: 12) {
                ForEach(books) { book in
                    BookCover(book: book)
                }
                .reorderable()
            }
            .reorderContainer(for: Book.self) { difference in
                books.applyReorder(difference)
            }
            .padding()
        }
    }
}
```

*Measured* with a UI test in three poses: closed (2 columns), open with the fold inactive (4 columns), and in book pose with the fold active (4 columns). A drag from the first tile onto the fourth reordered the grid every time; open and in book it crossed the middle of the display, where the fold is. Two collections in one container, one on each side of the fold, also worked in all three poses: a card dropped on the other list moved there. That suits book pose (later and today, library and playlist).

- Put both collections in one container with `reorderContainer(for:in:isEnabled:move:)` and tag each `ForEach` with `reorderable(collectionID:)`.
- In a target with MainActor default isolation (the Xcode 27 template), declare the collection ID `nonisolated enum Lane: Hashable, Sendable`. Otherwise the build fails (*measured*; message in the reference).
- A reorder container accepts only moves inside itself. To take items from another window or app in Split View, add your own drop destination ([session 271](https://developer.apple.com/videos/play/wwdc2026/271/?time=703)).

Full code (apply helper, two lanes, UI tests that reach the drag): [references/reorder-and-swipe.md](references/reorder-and-swipe.md).

## 3. Swipe actions outside List

`swipeActions` now works on rows in a `ScrollView`, `LazyVStack` or grid. Add `swipeActionsContainer()` to the container so only one row stays open, and scrolling or a tap elsewhere closes it ([doc](https://developer.apple.com/documentation/swiftui/view/swipeactionscontainer())). That matters on the inner display, where a custom two-column inbox can't be a `List`.

```swift
import SwiftUI

// requires: Message (references/reorder-and-swipe.md)

@available(iOS 27.0, *)
struct InboxColumn: View {
    @Binding var messages: [Message]
    @State private var openRows = 0

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 0) {
                ForEach(messages) { message in
                    Text(message.subject)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding()
                        .background(.background)
                        .swipeActions(edge: .trailing) {
                            Button("Delete", systemImage: "trash", role: .destructive) {
                                messages.removeAll { $0.id == message.id }
                            }
                        } onPresentationChanged: { isShown in
                            openRows += isShown ? 1 : -1
                        }
                }
            }
        }
        .swipeActionsContainer()
    }
}
```

*Measured* closed, open and in book pose: `swipeLeft()` on a row revealed Delete and `onPresentationChanged` reported it open. The action sits at the row's trailing edge. In a row that spans the inner display, that edge is beside the vertical bar, not near the fold. In UI tests the revealed button's label was "Delete, Delete" (symbol and title), so `app.buttons["Delete"]` found nothing; match with `BEGINSWITH`.

## 4. The prominent tab

`Tab(role: .prominent)` sets one tab apart ([doc](https://developer.apple.com/documentation/swiftui/tabrole/prominent), [session 269](https://developer.apple.com/videos/play/wwdc2026/269/?time=307)). Only one tab gets it; without one, a `.search` tab may take the look.

```swift
import SwiftUI

// requires: ShopScreen, PacksScreen, SavedScreen, CartScreen (your screens)

@available(iOS 27.0, *)
struct StoreRoot: View {
    var body: some View {
        TabView {
            Tab("Shop", systemImage: "bag") { ShopScreen() }
            Tab("Packs", systemImage: "square.stack") { PacksScreen() }
            Tab("Saved", systemImage: "heart") { SavedScreen() }
            Tab("Cart", systemImage: "cart", role: .prominent) { CartScreen() }
        }
    }
}
```

*Measured*: closed, and open held wide, the tab bar is vertical on the trailing side and the prominent tab is a separate round button at its foot. Held tall on the inner display, the bar is horizontal at the bottom and the prominent tab sits at its trailing end. The vertical bar shows no titles, so give the tab a symbol that reads alone.

## 5. Toolbars in the side column

`visibilityPriority(_:)`, `ToolbarOverflowMenu` and `topBarPinnedTrailing` decide what stays in a crowded bar ([session 269](https://developer.apple.com/videos/play/wwdc2026/269/?time=366)). On Duo the crowding is vertical: your bar shares the side column with the status bar and the Dynamic Island, which grows as Live Activities arrive, and app items collapse into the overflow menu when room runs out ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=336)). How to order and rank items for the vertical bar: `duo-navigation`.

`toolbarMinimizationBehavior(.onScrollDown, for: .navigationBar)` shrinks the navigation bar as people scroll. Only `.navigationBar` supports it ([doc](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationbehavior(_:for:))). *Measured* on Duo: the title area at the top shrank (the top inset went from 82 to 24 pt) while the buttons in the side column stayed where they were, closed, open and in book pose. Details and the companion modifiers: [references/toolbars-tabs-dialogs.md](references/toolbars-tabs-dialogs.md).

## 6. Dialogs from an optional item

`alert(_:item:actions:)` and `confirmationDialog(_:item:titleVisibility:actions:)` present while the binding is non-nil and pass the value to the actions, like `sheet(item:)` ([session 269](https://developer.apple.com/videos/play/wwdc2026/269/?time=1151)).

```swift
import SwiftUI

// requires: Draft with a static `samples` list (your model)

struct DraftsList: View {
    @State private var pendingDelete: Draft?

    var body: some View {
        List(Draft.samples) { draft in
            Button(draft.title) { pendingDelete = draft }
        }
        .confirmationDialog("Delete draft?", item: $pendingDelete) { draft in
            Button("Delete \(draft.title)", role: .destructive) { delete(draft) }
        }
    }

    private func delete(_ draft: Draft) {}
}
```

Keep the item in state above the layout switch, so a fold doesn't lose it. *Measured*: a dialog opened closed stayed up through unfolding and folding into book pose, and moved beside its button, off the fold. System sheets, alerts and menus move out of the fold by themselves ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)). Don't position them yourself.

## 7. AsyncImage through a fold

In iOS 27, `AsyncImage` keeps downloaded images in an HTTP cache that follows the server's cache headers, with no code change ([doc](https://developer.apple.com/documentation/swiftui/asyncimage), [session 269](https://developer.apple.com/videos/play/wwdc2026/269/?time=1254)). On Duo it matters when a fold rebuilds your image views.

*Measured* with a local server that sends `Cache-Control: max-age=3600`, through closed, open, closed, open:

- A `LazyVGrid` that only changes from 2 to 4 columns kept its loaded images through every fold, with or without the cache. No refetch either way.
- A screen that swaps containers (a `List` closed, a grid open) rebuilds every image view. With the cache bypassed it refetched 7 or 8 images on each fold and unfold. With the default cache it fetched 8 images in all, and none after the first unfold.

Numbers and the probe: [references/async-image.md](references/async-image.md).

```swift
import SwiftUI

@available(iOS 27.0, *)
struct CoverWall: View {
    let urls: [URL]

    // One session for the whole wall, with room for a few hundred covers.
    private static let session: URLSession = {
        let configuration = URLSessionConfiguration.default
        configuration.urlCache = URLCache(memoryCapacity: 32_000_000, diskCapacity: 256_000_000)
        return URLSession(configuration: configuration)
    }()

    var body: some View {
        LazyVGrid(columns: [GridItem(.adaptive(minimum: 140))]) {
            ForEach(urls, id: \.self) { url in
                AsyncImage(url: url) { $0.resizable().scaledToFill() } placeholder: { Color.secondary.opacity(0.2) }
                    .frame(height: 180)
                    .clipped()
            }
        }
        .asyncImageURLSession(Self.session)
    }
}
```

The server's headers decide what the cache keeps. If covers never change, send a long `max-age` rather than forcing a cache policy in the app.

## 8. Resizable iPhone apps

In iOS 27 iPhone apps resize: in iPhone Mirroring on the Mac and as an iPhone app on iPad ([session 269](https://developer.apple.com/videos/play/wwdc2026/269/?time=236)). Opening and closing iPhone Duo works the same way ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=135)). An app that resizes well there is most of the way to Duo.

- Drag the resize handles in Xcode 27 previews to watch a view resize live (session 269).
- In Xcode 27.1, the canvas overrides picker has a Display group that previews the device's other display ([release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)).
- For layout code, use Xcode 27.1's App Resizability skill, which now covers SwiftUI and iPhone Duo ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=559)). Duo specifics are in `duo-layout`.

## Test it

1. Build with Xcode 27.1. For views with `@State` and an `init`, run `swiftc -emit-sil -o /dev/null` or a full build.
2. On the iPhone Duo simulator, fold and unfold with a grid on screen: reorder still works, swipe rows close when you scroll, and images come back without a new download (watch your server log).
3. Drag across the fold in book pose (Device Hub: Partially Open). In UI tests, drag between element coordinates with `press(forDuration:thenDragTo:withVelocity:thenHoldForDuration:)` (`duo-testing`).
4. Check the prominent tab and toolbar overflow closed and open, held wide and tall.

## Checklist

- [ ] Builds with Xcode 27.1 with no TN3211 errors; no `@State` property has both an inline default and an assignment in `init`.
- [ ] No once-only work in view initializers; models live in `@State` or above the layout switch.
- [ ] Reorderable grids use `reorderable()` and `reorderContainer`, with even column counts; collection ID types are `nonisolated`.
- [ ] Custom scrolling lists with swipe actions have `swipeActionsContainer()`.
- [ ] At most one `.prominent` tab, with a symbol that reads without its title.
- [ ] Toolbar items carry visibility priorities; rare actions sit in `ToolbarOverflowMenu`.
- [ ] Minimizing bars use `toolbarMinimizationBehavior(_:for:)`, the SDK name.
- [ ] Dialogs that act on an item use the `item:` form, with the item stored above the layout switch.
- [ ] Remote images come from `AsyncImage` with cacheable server headers, not hand-made reload code.
- [ ] iOS 27.0 APIs are gated when the deployment target is lower.
- [ ] Checked closed, open, book and tabletop in Device Hub.
