---
name: duo-layout
description: Core layout rules for iPhone Duo, Apple's foldable. Use when content lands in the fold, a screen breaks on the inner or outer display, or you write SwiftUI or UIKit layout for a foldable. Covers size classes instead of UIScreen.main, idiom or orientation, asymmetric safe areas and margins, reserved regions (ReservedRegion, reservedRegions(kind:options:), .division, .occlusion, .includeInactive), ArrangementView and UIArrangementViewController (split and overlay styles), an even custom split (EvenSplit) for two halves that must always show, even grid columns, and keeping controls off the fold.
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-layout

iPhone Duo has a compact outer display, a large inner display and a fold. Your app resizes every time someone opens, closes, rotates or folds it. This skill tells you how to lay out for that.

Load other skills for neighbouring work: `duo-navigation` (vertical bars, sidebars, sheets), `duo-continuity` (state that must survive a fold), `duo-patterns` (which layout pattern to pick).

Labels used below: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, fully open, held wide). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Rules

1. Choose layouts by size class. Never by device, idiom, orientation or screen size.
2. Size views from their container. No fixed widths, no "iPhone is 390 pt".
3. Treat every safe area inset and margin as independent. Left and right differ on Duo.
4. Use system containers first (`NavigationSplitView`, `TabView`, sheets, alerts). They avoid the fold on their own.
5. For your own controls, read reserved regions and move them off the fold. Scrolling content can cross it.
6. Use `ArrangementView` for two views that sit side by side or overlap. Put `NavigationStack` or `TabView` around it. Never nest it with `NavigationSplitView`.
7. When both halves must always be visible, use `EvenSplit`, not `ArrangementView`.
8. Prefer an even number of grid columns.
9. Gate the iOS 27.1 APIs when the app deploys lower. See the next section.

Apple's sources for these rules: the [HIG page](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), the [developer overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo), and Tech Talks [111461](https://developer.apple.com/videos/play/tech-talks/111461/), [111463](https://developer.apple.com/videos/play/tech-talks/111463/) and [111466](https://developer.apple.com/videos/play/tech-talks/111466/).

## Deploying below iOS 27.1

`ArrangementView` and its modifiers, reserved regions (`ReservedRegion`, `reservedRegions(kind:options:)`) and `ContentMarginGuide` with `contentMargins(for:edges:alignment:)` are new in iOS 27.1. Most apps deploy lower, and then these calls don't compile.

- Mark each type that uses them `@available(iOS 27.1, *)`. The snippets in this skill already are.
- Call those types inside `if #available(iOS 27.1, *)`. iPhone Duo ships with iOS 27.1, so the `else` branch only runs on other iPhones. Keep today's layout there: a stack or `EvenSplit` instead of an arrangement, plain padding instead of container margins, no fold handling.
- Examples: the margins helper in section 2, and [references/arrangement-view.md](references/arrangement-view.md#deploying-below-ios-271). `duo-start` Step 1 shows how to read the deployment target.

## 1. Size classes, not devices

| Where | Width class | Height class |
|---|---|---|
| Outer display, portrait | compact | regular |
| Outer display, landscape | compact | compact |
| Inner display | regular | regular (*measured* fully open, held wide) |
| One half of a side-by-side `ArrangementView` on the inner display | compact (*measured*) | regular (*measured*) |
| One half of an `EvenSplit` | the window's class (*measured*: regular on the inner display) | the window's class |

Source: [Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=166). The inner display ignores your supported orientations, so orientation tells you nothing useful there.

Switch layouts with `AnyLayout`. The views keep their identity and state when the layout changes ([AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout)).

```swift
import SwiftUI

struct LibraryScreen: View {
    @Environment(\.horizontalSizeClass) private var widthClass

    var body: some View {
        let layout = widthClass == .regular
            ? AnyLayout(HStackLayout(alignment: .top, spacing: 16))
            : AnyLayout(VStackLayout(alignment: .leading, spacing: 12))
        layout {
            AlbumHeader()
            TrackList()
        }
    }
}
```

Replace these on sight:

| Don't | Do |
|---|---|
| `UIScreen.main.bounds`, `UIScreen.main.scale` (deprecated since iOS 26) | the view's or scene's size; `traitCollection.displayScale` or `@Environment(\.displayScale)` |
| `UIDevice.current.userInterfaceIdiom == .pad` | `horizontalSizeClass == .regular` |
| `UIDevice.current.orientation`, `interfaceOrientation` | size classes, or the view's own width and height |
| `.frame(width: 390)`, `if height == 844` | flexible frames, `containerRelativeFrame`, `GeometryReader` |
| a global screen | `view.window?.windowScene?.screen`, only when you truly need the screen |

## 2. Asymmetric safe areas and margins

Bars sit on the side on Duo. The bar edge can be left or right, for example in Split View. So the inset on one side says nothing about the other ([HIG: account for asymmetry](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)).

- Keep controls and text inside the safe area. SwiftUI does this by default.
- Let backgrounds extend with `.ignoresSafeArea()`.
- Use the system margins. On Duo, `ContentMarginGuide.container` (iOS 27.1) can differ on each side next to a vertical bar ([doc](https://developer.apple.com/documentation/swiftui/contentmarginguide/container)).

```swift
import SwiftUI

struct ArticleScreen: View {
    var body: some View {
        ScrollView {
            ArticleBody()
                .duoContainerMargins()
        }
        .background {
            HeroImage().ignoresSafeArea()
        }
    }
}

extension View {
    /// The system container margins, which can differ per side on iPhone Duo.
    /// Plain horizontal padding before iOS 27.1.
    @ViewBuilder
    func duoContainerMargins() -> some View {
        if #available(iOS 27.1, *) {
            contentMargins(for: .container, edges: .horizontal)
        } else {
            padding(.horizontal)
        }
    }
}
```

Never compute one inset and double it. In UIKit, inset by the real insets: `view.bounds.inset(by: view.safeAreaInsets)`. See [references/uikit.md](references/uikit.md).

## 3. Reserved regions: the fold and the cameras

A reserved region is part of your view that hardware or system UI claims ([ReservedRegion](https://developer.apple.com/documentation/swiftui/reservedregion)).

| Kind | What it is | Active when |
|---|---|---|
| `.division` | The fold. It splits the inner display into two usable areas. | The phone is partly folded. Flat, it is inactive and zero width. |
| `.occlusion` | Something covering content: a camera, or other system UI (Apple lists the Dynamic Island and window controls). *Measured:* an active region also sits where the status bar is, on both displays (our reading; Apple doesn't label it). | Inner camera: while it runs. Outer camera: always. |

Facts you need:

- *Measured:* a query with no options returned only active regions. Add `.includeInactive` to get the flat fold. Apple's `ReservedRegion` page says the opposite; the talk and our probe agree with each other. Filter on `isActive` anyway, so your code works either way.
- *Measured:* flat, the inactive division was 40 pt wide: a zero-width line at the centre plus 20 pt of `margins` on each side. `frame` includes the margins.
- *Measured:* the first layout pass returned no regions at all. Regions arrived on the next pass. React to changes; don't read once in `onAppear`.
- Frames are in the view's own coordinate space. SwiftUI mirrors them for right-to-left by default; pass `layoutDirectionBehavior: .fixed` to stop that.

Move a control off the fold (Apple calls this displacement, [111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=146)):

```swift
import SwiftUI

@available(iOS 27.1, *)
struct FoldAvoidingControls<Controls: View>: View {
    @ViewBuilder var controls: Controls

    var body: some View {
        GeometryReader { proxy in
            let area = Self.controlArea(in: proxy)
            controls
                .frame(width: area.width, height: area.height)
                .position(x: area.midX, y: area.midY)
        }
    }

    /// The whole view when flat. When folded, the side after the fold:
    /// trailing for a top-to-bottom fold, bottom for a side-to-side fold.
    static func controlArea(in proxy: GeometryProxy) -> CGRect {
        let bounds = CGRect(origin: .zero, size: proxy.size)
        let folds = proxy.reservedRegions(kind: .division).filter(\.isActive)
        guard let fold = folds.first?.frame, fold.intersects(bounds) else { return bounds }
        if fold.height >= fold.width {
            return CGRect(x: fold.maxX, y: 0, width: bounds.maxX - fold.maxX, height: bounds.height)
        }
        return CGRect(x: 0, y: fold.maxY, width: bounds.width, height: bounds.maxY - fold.maxY)
    }
}
```

Grids: use an even number of columns when a division exists, so the fold falls between cells. Count with `.includeInactive`, so the column count doesn't jump when someone folds ([111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=456)). Code: [references/reserved-regions.md](references/reserved-regions.md#even-grid-columns).

More (measured values, occlusions, a player for both fold directions, UIKit): [references/reserved-regions.md](references/reserved-regions.md).

## 4. ArrangementView

A layout container for a primary and a secondary view. It adapts to size, size class and the fold ([ArrangementView](https://developer.apple.com/documentation/swiftui/arrangementview)).

- `.split` (the default, also what `.automatic` resolves to): side by side or stacked. Use it where you would write `HStack` or `VStack`.
- `.overlay`: primary on top of secondary; side by side when folded. Use it where you would write `ZStack`, such as controls over a video.
- Limit axes with `.split.axes(.horizontal)`. If it can't split on an allowed axis, it shows only the primary view.

```swift
import SwiftUI

@available(iOS 27.1, *)
struct NowPlayingScreen: View {
    var body: some View {
        NavigationStack {
            ArrangementView {
                PlayerView()
            } secondary: {
                UpNextView()
            }
            .arrangementViewStyle(.split)
            .navigationTitle("Now Playing")
        }
    }
}
```

Rules:

- Put `NavigationStack` and `TabView` around the arrangement, never inside it ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Arrangement-views), [111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=969)).
- Keep `NavigationSplitView` and arrangements apart. No split view inside an arrangement ([111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=975)), and no arrangement inside a split view or one of its columns ([overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)). The HIG's wording allows a split view around an arrangement; Duology follows the overview and the talk, as `duo-patterns` does.
- Don't put an arrangement inside a `List` or `ScrollView` ([overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)).
- *Measured:* with compact width and compact height (the closed phone held sideways), `.automatic` and `.split` show only the primary view. The secondary is never drawn, though its `onAppear` still runs. With compact width and regular height (closed, portrait) they stack the two views.
- *Measured:* read `splitArrangementAxis`, `overlayArrangementZIndex` and size classes in a view nested inside the half (for example inside a `ZStack`). The view you pass directly read the default values in our probe.

Details, the behaviour table and the UIKit `UIArrangementViewController`: [references/arrangement-view.md](references/arrangement-view.md).

## 5. When both halves must always show: EvenSplit

Two players, a game board and its tray, a teacher and a student: these need both halves in every pose, including closed and sideways. `ArrangementView` hides one there. Use an even split you control. The same type ships in the gallery app at [`samples/DuologyGallery/DuologyGallery/Shared/EvenSplit.swift`](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Shared/EvenSplit.swift).

```swift
import SwiftUI

/// Two equal halves that always show. Side by side when the view is wider
/// than tall, stacked otherwise. AnyLayout keeps each half's state when the
/// axis flips.
struct EvenSplit<Primary: View, Secondary: View>: View {
    var spacing: CGFloat = 0
    @ViewBuilder var primary: () -> Primary
    @ViewBuilder var secondary: () -> Secondary

    var body: some View {
        GeometryReader { proxy in
            let wide = proxy.size.width >= proxy.size.height
            let half = wide
                ? CGSize(width: max(0, (proxy.size.width - spacing) / 2), height: proxy.size.height)
                : CGSize(width: proxy.size.width, height: max(0, (proxy.size.height - spacing) / 2))
            let layout = wide
                ? AnyLayout(HStackLayout(spacing: spacing))
                : AnyLayout(VStackLayout(spacing: spacing))
            layout {
                primary().frame(width: half.width, height: half.height)
                secondary().frame(width: half.width, height: half.height)
            }
        }
    }
}
```

```swift
import SwiftUI

struct DuelScreen: View {
    var body: some View {
        EvenSplit(spacing: 2) {
            PlayerHalf(player: 1)
        } secondary: {
            PlayerHalf(player: 2)
        }
        .background(Color.secondary)
    }
}
```

Fit content to its half, not to the device:

- **Try both arrangements, keep the bigger.** Inside a half, compute the layout two ways (tray below, tray beside) and keep the one whose smallest important element is larger. Code: [references/custom-split.md](references/custom-split.md#try-both-arrangements-keep-the-bigger).
- **Thresholds for small halves.** Closed and portrait, each stacked half gets about 382 × 321 pt inside the safe area (*measured* in `duo-shared-screen` and `duo-design-review`: the safe area is 382 × 644 pt of a 466 × 678 pt window, with 84 pt trailing and 34 pt at the bottom). A split that ignores the safe area gets 466 × 339 pt halves. Held sideways, plan for two halves of at most about 339 × 466 pt side by side (*derived*, not measured). Drop labels, then shrink spacing, before you shrink touch targets. `ViewThatFits` code: [references/custom-split.md](references/custom-split.md#thresholds-for-small-halves).

`EvenSplit` always puts its seam at the middle of its own frame. If a vertical bar narrows the view, that middle is not the fold. To put the seam on an active fold, use `FoldSplitLayout` in [references/custom-split.md](references/custom-split.md#put-the-seam-on-the-fold).

An `EvenSplit` half keeps the window's size classes, so on the inner display a 338 pt half still reads regular width (*measured*). Inside a half, lay out by the half's size, as above, not by its size class.

## 6. Keep controls off the fold

- Buttons, sliders, text fields and drag handles: keep them out of the division frame when it is active ([111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)).
- Scrolling content (feeds, articles, lists, grids in a `ScrollView`) may cross the fold. Don't displace it.
- System sheets, alerts, menus and toolbar buttons already move off the fold. Use them instead of custom ones.
- Move only what you must. Keep moved items near the content they belong to ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)).
- Don't drive layout from the hinge angle. Use size classes, arrangements and reserved regions; the hinge is for effects.

## UIKit

Same rules: `traitCollection` size classes, `safeAreaInsets` per side, `view.reservedRegions(kind:options:)`, `UIArrangementViewController`, and a `UIStackView` with `.fillEqually` for an even split. Code: [references/uikit.md](references/uikit.md).

## Test it

1. Run on the iPhone Duo simulator in Xcode 27.1. In Device Hub, use Closed, Partially Open and Open under the bezel, and rotate in each pose. Option-drag the slider for other angles ([Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)).
2. Test Split View: on the inner display, drag your app by the home indicator to one side, then the other. Bars then sit on your app's outer edge.
3. Screenshots: `xcrun simctl io booted screenshot --display=primary outer.png` (outer) and `xcrun simctl io booted screenshot --display=primary-1 inner.png` (inner).
4. In the scheme, set App Language to Right-to-Left Pseudolanguage and check anything you placed by hand.
5. `simctl` cannot change the pose (*measured*). Pose changes happen in Device Hub only.

## Checklist

- [ ] No `UIScreen.main`, `userInterfaceIdiom`, device orientation or fixed device sizes drive layout.
- [ ] Layout switches on `horizontalSizeClass` / `verticalSizeClass`, with `AnyLayout` where the same views change axis.
- [ ] Each safe area inset is handled on its own; backgrounds ignore the safe area, controls don't.
- [ ] Custom controls near the centre read `.division` regions and move when the fold is active.
- [ ] Region code filters on `isActive` and handles an empty first pass.
- [ ] Grids use an even column count when a division exists, active or not.
- [ ] Any `ArrangementView` sits inside `NavigationStack` or `TabView` only: no `NavigationSplitView` inside or around it, and no `List` or `ScrollView` around it.
- [ ] Below an iOS 27.1 deployment target, arrangements, regions and container margins are behind `@available` and `if #available`.
- [ ] Arrangement values are read in a nested view, not in the view passed in.
- [ ] Two halves that must always show use `EvenSplit` (or `FoldSplitLayout`), checked closed and sideways.
- [ ] Small halves drop labels before they shrink touch targets.
- [ ] Checked closed, open, partly open, rotated, Split View on both sides, and right-to-left.
