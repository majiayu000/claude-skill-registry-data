---
name: duo-continuity
description: Keeps app state alive when iPhone Duo, Apple's foldable, folds, unfolds, rotates or resizes between the outer display and the inner display. Use when scroll position, video or audio playback, typed text, keyboard focus, selection, form input, the selected item, the navigation stack, an upload or sign-in resets or reloads on fold or unfold, and when writing or reviewing @Observable models, @SceneStorage, NavigationPath, NavigationSplitView, ScrollPosition, AnyLayout, .id, onAppear, .task, registerForTraitChanges or viewWillTransition(to:with:).
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-continuity

Apple says your app resizes when someone opens or closes iPhone Duo ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/)). Your content moves to the other display, and the window changes size and usually its horizontal size class. State survives only if it lives above the part of the view tree that the change rebuilds. This skill tells you where to put each kind of state and how to prove it survives.

Load other skills for neighbouring work: `duo-layout` (size classes, `ArrangementView`, the even split), `duo-navigation` (bars, sidebars, sheets), `duo-testing` (test setup on the Duo simulator).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1). Fold results come from flipping the size class from code, the change a fold makes to your views, because our probes can't fold the simulator themselves; see [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Apple has no continuity API

Don't look for one. The iOS 27.1 SDK has no fold, pose or posture symbol, and the hinge APIs only report status and angle ([API index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#not-in-the-sdk)). Apple states the goal, not a tool. The [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) asks you to keep functionality and the state of elements the same on both displays. Tech Talk [111466](https://developer.apple.com/videos/play/tech-talks/111466/) says people open and close the phone often, so the app must stay predictable. Tech Talk [111463](https://developer.apple.com/videos/play/tech-talks/111463/) keeps scrolling content in place because moving it breaks continuity. You reach that goal with ordinary SwiftUI and UIKit state tools. (Apple's "Continuity" feature, Handoff between devices, is unrelated.)

## What a fold does

| Change | What your app sees |
|---|---|
| Close or open | Content moves between displays. The width changes and the horizontal size class flips: compact outside, regular inside. |
| Partially open | The window stays on the inner display. A division region (the fold) becomes active. |
| Rotate | Width and height swap. The inner display doesn't honour your supported orientations, so don't rely on them. |
| Split View, pinned Picture in Picture | The window gets narrower or shorter. |
| Combinations | Rotate, then close. Close while scrolling. Open while typing. Each step is another resize. |

- *Measured* on the simulator with Device Hub's pose buttons (v0.2): close, open, partial fold and rotation kept the root view alive, with no relaunch, no new `onAppear` and no scene disconnect, and the scene stayed `active` with no `.inactive` ([duo-transitions evidence](https://github.com/Kimeur/duology/blob/main/plugins/duology-design/skills/duo-transitions/references/evidence.md), [duo-scenes evidence](https://github.com/Kimeur/duology/blob/main/plugins/duology/skills/duo-scenes/references/evidence.md)). *Unverified:* a real iPhone Duo, and what the keyboard does when the window changes display. Still save on `.background`.

## Where state gets lost

1. **Identity changes.** An `if`/`else` or `switch` on size class, a `ViewThatFits` that picks another child, or an `.id` tied to layout gives views a new identity. SwiftUI drops their `@State`, takes keyboard focus away, runs `onAppear` again, cancels their `.task`, and closes sheets attached to them.
2. **Code reloads on resize.** A fetch in `onAppear`, a UIKit trait handler that rebuilds child view controllers, an `onDisappear` that pauses or clears.
3. **A pane leaves the screen.** When the phone closes, a split view collapses and the extra column leaves the view tree. State stored only in that column goes with it.

## What must survive, and where it lives

| State | Keep it in | Tool |
|---|---|---|
| Scroll position | the model, as an item ID | `ScrollPosition` + `scrollTargetLayout()` (iOS 18); `scrollPosition(id:anchor:)` (iOS 17) |
| Playback | one player owned by a model | `AVPlayer`, `VideoPlayer(player:)` |
| Text and selection | the model | `TextEditor(text:selection:)`, `TextSelection` (iOS 18) |
| Keyboard focus | `@FocusState` on a view whose identity never changes | `focused(_:equals:)` |
| Form input | a draft struct in the model | `@Observable`, `@Bindable` |
| Selected item, navigation stack | the model | `NavigationSplitView` selection, `NavigationPath` |
| Uploads, downloads | a service object, never a view | a `Task` the service keeps |
| Sign-in | an app-level session object, secrets in the Keychain | Keychain Services |
| Open sheet or alert | the item in the model, the modifier on a stable view | `sheet(item:onDismiss:content:)` |

## 1. Own state above every layout switch

Put screen state in an `@Observable` model ([Observation](https://developer.apple.com/documentation/observation)). Create one per window in the window's root view, which never changes identity, and pass it down with `.environment`. Section 3 shows that root. Keep `@State` for values you are happy to lose, such as a press highlight. Data shared by every window (a store, the signed-in user) goes one level up, in the `App`. The snippets below use this model.

```swift
import SwiftUI
import Observation

struct Item: Identifiable, Hashable, Codable, Sendable {
    let id: Int
    var title: String
}

@MainActor @Observable
final class LibraryModel {
    var items: [Item] = []
    var selection: Item.ID?                              // drives the detail column
    var path = NavigationPath()                          // pushed screens in the detail
    var scroll = ScrollPosition(idType: Item.ID.self)    // where the feed is
    var draft = ""                                       // text being typed
    var draftSelection: TextSelection?                   // the selection in that text
    var sheetItem: Item?                                 // the open sheet, if any
    private var didLoad = false

    func loadIfNeeded() async {
        guard !didLoad else { return }                   // a fold never refetches
        didLoad = true
        items = (1...200).map { Item(id: $0, title: "Item \($0)") } // your fetch here
    }
}
```

## 2. Keep view identity stable

Don't branch between containers on size class. Pick a layout and keep the same children ([AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout) changes the layout without destroying the subviews' state).

```swift
import SwiftUI

struct CommentsPane: View {
    @State private var reply = ""      // lost on every fold in the bad version
    var body: some View { TextField("Reply", text: $reply) }
}

// Bad: each branch is a different identity, so a fold resets CommentsPane.
struct ArticleScreenBad: View {
    @Environment(\.horizontalSizeClass) private var sizeClass
    var body: some View {
        if sizeClass == .compact {
            VStack { Text("Article"); CommentsPane() }
        } else {
            HStack { Text("Article"); CommentsPane() }
        }
    }
}

// Good: one identity, two layouts.
struct ArticleScreen: View {
    @Environment(\.horizontalSizeClass) private var sizeClass
    var body: some View {
        let layout = sizeClass == .compact ? AnyLayout(VStackLayout()) : AnyLayout(HStackLayout())
        layout {
            Text("Article")
            CommentsPane()
        }
    }
}
```

- *Measured:* with the `if`/`else`, every flip gave the child a new `@State`, ran `onAppear` again and cancelled its `.task`. With `AnyLayout`, the child appeared once for the whole run.
- Use `.id(_:)` only for data identity, such as `.id(item.id)` to reset a detail on purpose. Changing the value resets the view's state ([id(_:)](https://developer.apple.com/documentation/swiftui/view/id(_:))). Never `.id(sizeClass)`, `.id(proxy.size)` or `.id(UUID())`.
- [ViewThatFits](https://developer.apple.com/documentation/swiftui/viewthatfits) shows a different child when space changes; keep its children free of state. Never swap `NavigationStack` for `NavigationSplitView` by size class. The split view collapses to a stack on its own.
- For two panes around the fold, use `ArrangementView` or the even split from `duo-layout`. Both take each pane once, with no branch. A split `ArrangementView` can hide its secondary view when it can't split (see `duo-layout`), so keep that view's state in the model.

## 3. Selection and navigation stack

Keep the selection and the path in the model. `NavigationSplitView` collapses to one stack when the phone closes and shows the detail when something is selected ([NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview)). If you switch panes yourself and opening the phone pops a pushed screen, pop it after the unfold animation ([references/swiftui.md](references/swiftui.md#popping-a-stack-while-the-phone-opens)).

```swift
import SwiftUI

struct LibrarySplitView: View {
    @Environment(LibraryModel.self) private var model

    var body: some View {
        @Bindable var model = model
        NavigationSplitView {
            List(model.items, selection: $model.selection) { item in
                Text(item.title)
            }
        } detail: {
            NavigationStack(path: $model.path) {
                if let item = model.items.first(where: { $0.id == model.selection }) {
                    NavigationLink("Related", value: item.id + 1)
                        .navigationTitle(item.title)
                        .navigationDestination(for: Item.ID.self) { Text("Item \($0)") }
                }
            }
        }
    }
}

struct WindowRoot: View {
    @State private var model = LibraryModel()    // one per window, lives as long as the window

    var body: some View {
        LibrarySplitView()
            .environment(model)
            .task { await model.loadIfNeeded() } // WindowRoot never changes identity
    }
}
```

- *Measured:* with the size class flipped to compact, the split view collapsed, kept the selection, and brought the sidebar list back at the same scroll offset on expand.
- `init(preferredCompactColumn:sidebar:detail:)` (iOS 17) is a hint for the column shown after the collapse. Keep that binding in the model too. *Measured:* with an item selected, the collapse hid the sidebar although the binding said `.sidebar`. Check what you get in Device Hub.
- A fold does not need `@SceneStorage`. Use it so the window comes back after the system ends the app: save the selection and `path.codable` when the scene goes to the background ([NavigationPath](https://developer.apple.com/documentation/swiftui/navigationpath), [SceneStorage](https://developer.apple.com/documentation/swiftui/scenestorage)). Keep it small and never store secrets in it. Code: [references/swiftui.md](references/swiftui.md#restore-after-a-relaunch).

## 4. Scroll position by item ID, never by offset

```swift
import SwiftUI

struct FeedView: View {
    @Environment(LibraryModel.self) private var model
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        @Bindable var model = model
        let count = sizeClass == .compact ? 2 : 4        // even column counts
        ScrollView {
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: count)) {
                ForEach(model.items) { Text($0.title) }
            }
            .scrollTargetLayout()
        }
        .scrollPosition($model.scroll, anchor: .top)
    }
}
```

- Apple's [ScrollPosition](https://developer.apple.com/documentation/swiftui/scrollposition) page says SwiftUI tries to keep the view with that ID visible when the scroll view's size changes. A point position gets no such help.
- *Measured:* item 150 stayed at the top through 4 → 1 → 4 columns; a point position showed rows 31 to 33 instead. `scrollPosition(id:)` did not move a `List`. Use `ScrollViewReader` for a `List`, or a `ScrollView` with a lazy stack when you need ID positions. One exception, *measured* in the gallery: long text that reflows while the system margins arrive late lost its paragraph with `ScrollPosition`; a `ScrollViewReader.scrollTo` by the saved ID after the width settles kept it ([gallery README](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/README.md#the-v02-screens)).

## 5. No reloads, and no work tied to a view's life

- Load once, in the model (`loadIfNeeded()`), from a view that never changes identity. Or use `.task(id:)` keyed on the data, such as `item.id`, never on layout.
- SwiftUI cancels a `.task` when its view goes away or changes identity ([task](https://developer.apple.com/documentation/swiftui/view/task(name:priority:file:line:_:))). Never start an upload, a download or a payment from `.task` or `onAppear` inside a layout branch. Start it from a button action in a service object. Code: [references/swiftui.md](references/swiftui.md#uploads-and-downloads).
- Never pause, clear or sign out in `onDisappear`. A fold can trigger it.

## 6. Text, focus and selection

```swift
import SwiftUI

struct NoteEditor: View {
    @Bindable var model: LibraryModel
    @FocusState private var isFocused: Bool       // lives in this view, so keep its identity stable
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        let layout = sizeClass == .compact ? AnyLayout(VStackLayout()) : AnyLayout(HStackLayout())
        layout {
            TextEditor(text: $model.draft, selection: $model.draftSelection)
                .focused($isFocused)
            Text("\(model.draft.count) characters")
        }
    }
}
```

- *Measured:* a field with stable identity kept focus through two size-class flips. The same field inside an `if`/`else` lost it: its `@FocusState` became `nil`.
- Form drafts work the same way: a struct in the model, fields bound with `$model.form.name` ([references/swiftui.md](references/swiftui.md#form-input)).

## 7. Playback

- Create the `AVPlayer` once, in a model owned by the window root. Views only show it: `VideoPlayer(player: playback.player)`. *Measured:* a model-owned `AVPlayer` kept playing while `VideoPlayer` was torn down and rebuilt on each flip.
- Never write `@State private var player = AVPlayer(url:)` in a view below a layout switch. A fold starts a new player from zero.
- Code for SwiftUI and `AVPlayerViewController`: [references/swiftui.md](references/swiftui.md#playback), [references/uikit.md](references/uikit.md#players).

## 8. Sheets, alerts and sign-in

- Attach `.sheet`, `.fullScreenCover`, `.alert` and `.confirmationDialog` to a view that never changes identity, usually the window root. Drive them from the model. *Measured:* a sheet attached inside an `if`/`else` closed when the size class flipped, and its `isPresented` binding stayed `true`. The model and the screen disagreed. The same sheet on the root stayed up.
- Keep the session in an app-level object and secrets in the Keychain. Let the root decide between signed-in and signed-out content. Never start sign-in from `onAppear` below a layout switch; a fold would start it again. *Unverified:* whether a web sign-in sheet in flight survives a fold. Start it from the root to be safe.

## 9. UIKit

Keep the same view controllers and views. Change layout in place; don't rebuild. Keep the top item in view when the column count changes.

```swift
import UIKit

// Give it a compositional layout that reads the size class; see references/uikit.md.
final class FeedViewController: UICollectionViewController {
    private var pendingAnchor: IndexPath?

    override func viewDidLoad() {
        super.viewDidLoad()
        registerForTraitChanges([UITraitHorizontalSizeClass.self]) { (self: Self, _: UITraitCollection) in
            self.pendingAnchor = self.pendingAnchor ?? self.collectionView.indexPathsForVisibleItems.min()
        }
    }

    override func viewWillTransition(to size: CGSize, with coordinator: any UIViewControllerTransitionCoordinator) {
        pendingAnchor = pendingAnchor ?? collectionView.indexPathsForVisibleItems.min()   // before the resize
        super.viewWillTransition(to: size, with: coordinator)
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        guard let anchor = pendingAnchor else { return }
        pendingAnchor = nil
        collectionView.scrollToItem(at: anchor, at: .top, animated: false)   // after the new layout
    }
}
```

- *Measured:* with no restore, a 4 → 2 column change put item 74 at the top instead of item 148. Scrolling inside the trait handler didn't stick; scrolling after the next layout pass kept item 148.
- [registerForTraitChanges(_:handler:)](https://developer.apple.com/documentation/uikit/uitraitchangeobservable-67e94/registerfortraitchanges(_:handler:)) replaces `traitCollectionDidChange(_:)`, deprecated in iOS 17 ([Adapting your app when traits change](https://developer.apple.com/documentation/uikit/adapting-your-app-when-traits-change)). [viewWillTransition(to:with:)](https://developer.apple.com/documentation/uikit/uicontentcontainer/viewwilltransition(to:with:)) runs before the size changes; always call `super`. *Unverified:* the size-transition path, because the open simulator refused a rotation request from code.
- Never call `reloadData()` or replace child view controllers in either handler.
- Split view, compositional layout, text views, players and state restoration: [references/uikit.md](references/uikit.md).

## 10. How to test

1. **By hand in Device Hub.** Run on the iPhone Duo simulator. Build up state: scroll halfway, select an item, push a screen, type and select text, start playback, start an upload, open a sheet. Then press Closed, Open and Partially Open under the bezel, rotate, and try the combinations ([Interacting with your app in Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)). Check every row of the table above after each step.
2. **Automatic UI test.** A debug-only launch switch adds a button that flips the size class at the root and hidden labels that report a state summary. The test records the summary, flips there and back, and compares. *Measured:* it passed on the closed Duo simulator. Don't rotate in it: *measured*, setting `XCUIDevice.shared.orientation` on the closed Duo did not resize the app (open: *unverified*).
3. **Real fold and rotation in a UI test.** A test can't fold the simulator: `XCUIDevice` has no fold control, and `simctl` and `devicectl` have no pose command. So a test, skipped by default, waits while you press the pose buttons and the rotate button in Device Hub, then compares the summary. Steps, matrix and full test code: [references/testing.md](references/testing.md).

## Red flags in review

- `if sizeClass == .compact { A } else { B }` where A and B hold the same stateful views
- `.id(UUID())`, `.id(sizeClass)`, `.id(geometry.size)` or any `.id` fed by layout
- `.onAppear { load() }` or `.task { await upload() }` below a layout switch; `onDisappear { player.pause() }` or a form cleared in `onDisappear`
- `@State private var player = AVPlayer(...)` in a leaf view
- `NavigationStack` in one branch and `NavigationSplitView` in the other; `.sheet` or `.alert` attached inside a size-class branch
- UIKit: `traitCollectionDidChange(_:)`, `reloadData()` or new child view controllers on a trait change; restoring a saved `contentOffset` after a layout change

## Checklist

- [ ] Screen state lives in an `@Observable` model created once per window in a root view that never changes identity.
- [ ] Layout switches use `AnyLayout`, `ArrangementView` or one container. No `if`/`else` between containers, and no `.id` fed by size, size class or a fresh `UUID`.
- [ ] Selection and navigation path live in the model; one `NavigationSplitView` handles open and closed; `@SceneStorage` restores them after a relaunch and holds no secrets.
- [ ] Scroll position is stored as an item ID, not an offset.
- [ ] Loading runs once in the model. Uploads, downloads and payments run in a service object, never in `.task` or `onAppear`.
- [ ] Draft text, selection and form input live in the model; focused fields keep their identity.
- [ ] One `AVPlayer`, owned by a model above the layout switch; no pause in `onDisappear`.
- [ ] Sheets and alerts attach to the window root and read their item from the model. Sign-in state lives above every window; secrets are in the Keychain.
- [ ] UIKit: same view controllers through trait changes; the top item is remembered before the change and restored after the next layout pass.
- [ ] Tested in Device Hub (Closed, Open, Partially Open, rotate, Split View, rotate-then-close) with every state in the table; a UI test flips the size class and checks the state summary.
