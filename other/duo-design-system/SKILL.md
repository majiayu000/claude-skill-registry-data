---
name: duo-design-system
description: "Design tokens and a drop-in SwiftUI token module for iPhone Duo, Apple's foldable, that adapt by size class instead of by device. Covers a 4-point spacing scale, system margins and gutters with a wider gap at the fold, even-column layout grids (4 compact, 8 regular) with spans, one type scale with Dynamic Type for the 5.4-inch outer and 7.6-inch inner display, Liquid Glass usage and legibility (glassEffect, GlassEffectContainer, regular vs clear, dimming, tint), ConcentricRectangle and containerShape for corners, 44 pt touch targets, and light, dark and Increase Contrast colours with a contrast check. Use when you set up spacing, grids, fonts, corners, glass or colours, build a design system, theme or tokens for an iPhone Duo app, or turn a two-frame Figma design into code."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-design-system

One set of design tokens for both iPhone Duo displays. The tokens follow the size class and Dynamic Type size of the view that reads them. They never ask which display, device or screen the app is on.

Load other skills for neighbouring work: `duo-layout` (size classes, safe areas, reserved regions, `ArrangementView`), `duo-patterns` (which layout, feed reflow), `duo-navigation` (vertical bars), `duo-design-review` (checking screenshots against the rules).

Labels: *measured* means we ran it on the iOS 27.1 simulator runtime (offscreen renders and command-line checks, or the iPhone Duo simulator in an earlier skill). *Derived* means arithmetic on measured or Apple numbers. *Duology default* means Apple gives no number and we picked one. *Unverified* means we could not confirm it. Sources: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Rules

1. Key every token to the size class or to the view's own space. Never to the device, the display, the idiom, the orientation or a screen size. Apple warns against breakpoints and metrics tied to one screen ([111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=230)).
2. Keep one type scale. System text styles, the same on both displays; the inner display shows more, not bigger.
3. Use the system margins, per side. They differ next to a vertical bar ([111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=453)).
4. Use even column counts whenever a fold crosses the grid, active or not ([111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=456)). Partly folded, the fold's frame is the middle gutter and the outer margins stay ([111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=350)).
5. Put Liquid Glass on controls only, and sparingly. Regular by default; clear only over media, with dimming ([HIG, Materials](https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass)).
6. Make corners near a display edge or inside a container concentric. Never hard-code a display radius ([111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=258)).
7. Give everything people tap a 44 × 44 pt hit region, in every pane and half ([HIG, Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)).
8. Start from system colours. Custom colours need light, dark and increased-contrast variants. Text needs 4.5:1, or 3:1 at 18 pt or bold ([HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)).

## What each display gets

| | Outer display, closed | Inner display, open |
|---|---|---|
| Size class | compact width ([111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=187)) | regular width |
| Window, portrait or held wide | 466 × 678 pt (*measured*) | 951 × 669 pt (*measured*) |
| Safe area | 382 × 644 pt (*measured*) | 867 × 635 pt (*measured*, bar on the right) |
| Layout columns | 4 | 8 |
| Gutter | 12 pt | 16 pt, the middle one on the fold line; partly folded, the fold's frame (40 pt, *measured*) |
| Margins | system, per side: 16 to 20 pt on iPhone ([doc](https://developer.apple.com/documentation/swiftui/contentmarginguide/container)), asymmetric next to the status bar column (gallery app: 20 pt leading, 0 pt trailing) | system, per side; asymmetric next to the vertical bar |
| Card padding, radius | 16 pt, 24 pt | 20 pt, 28 pt |
| Section spacing | 24 pt | 32 pt |
| Text | system text styles | the same sizes; lines capped at `readableWidth` |

Never copy these numbers into code. The tokens produce them.

## 1. Drop in the token module

Copy the complete file from [references/tokens.md](references/tokens.md) into the app as `DuoTokens.swift`. It adds text roles (`DuoType`), colours (`DuoColor`), `DuoCard` and the modifiers used below. If the app still has the v0.1 version of `duo-start`'s debug logger, delete it first: it declares a `struct DuoSpace`, and the build fails (v0.2 renamed it `DuoFirstPassSize`). This is its core:

```swift
import SwiftUI

/// Duology's 4-point spacing scale. The suffix is the number of 4-point steps.
nonisolated enum DuoSpace {
    static let x1: CGFloat = 4    // icon to badge, label to value
    static let x2: CGFloat = 8    // related items in a row
    static let x3: CGFloat = 12   // padding around a control with a bezel (HIG)
    static let x4: CGFloat = 16
    static let x5: CGFloat = 20
    static let x6: CGFloat = 24   // padding around a control without a bezel (HIG)
    static let x8: CGFloat = 32
    static let x10: CGFloat = 40
    static let x12: CGFloat = 48
}

/// Design tokens for one view. Read them with `@DuoMetrics`.
nonisolated struct DuoTokens: Equatable, Sendable {
    var isRegularWidth: Bool
    var isAccessibilitySize: Bool
    /// Longest comfortable line of body text, already scaled for Dynamic Type.
    var readableWidth: CGFloat

    init(widthClass: UserInterfaceSizeClass?,
         isAccessibilitySize: Bool = false,
         readableWidth: CGFloat = 600) {
        self.isRegularWidth = widthClass == .regular
        self.isAccessibilitySize = isAccessibilitySize
        self.readableWidth = readableWidth
    }

    /// Layout grid columns. Even in both size classes, so a fold never lands inside a column.
    var columns: Int { isRegularWidth ? 8 : 4 }
    var gutter: CGFloat { isRegularWidth ? DuoSpace.x4 : DuoSpace.x3 }
    var sectionSpacing: CGFloat { isRegularWidth ? DuoSpace.x8 : DuoSpace.x6 }
    var cardPadding: CGFloat { isRegularWidth ? DuoSpace.x5 : DuoSpace.x4 }
    /// Padding plus the inner radius, so nested corners stay concentric.
    var cardRadius: CGFloat { cardPadding + Self.innerRadius }

    /// Grid columns an item spans. Doubles at accessibility text sizes.
    func span(_ base: Int) -> Int { min(columns, isAccessibilitySize ? base * 2 : base) }

    static let minTouchTarget: CGFloat = 44        // HIG
    static let innerRadius: CGFloat = 8            // smallest radius, concentric fallback
    static let clearGlassDimming: Double = 0.35    // HIG, behind clear glass on bright media
}

/// Tokens for the view it sits in: `@DuoMetrics private var tokens`.
@propertyWrapper
struct DuoMetrics: DynamicProperty {
    @Environment(\.horizontalSizeClass) private var widthClass
    @Environment(\.dynamicTypeSize) private var typeSize
    @ScaledMetric(relativeTo: .body) private var readableWidth: CGFloat = 600

    init() {}

    var wrappedValue: DuoTokens {
        DuoTokens(widthClass: widthClass,
                  isAccessibilitySize: typeSize.isAccessibilitySize,
                  readableWidth: readableWidth)
    }
}
```

It builds for iOS 17 and later and typechecks with no warnings in Swift 5, Swift 6 and main actor default isolation modes. Use it in any view:

```swift
import SwiftUI

// requires: DuoTokens.swift (references/tokens.md)

struct AccountScreen: View {
    @DuoMetrics private var tokens

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: tokens.sectionSpacing) {
                Text("Account").font(DuoType.sectionTitle)
                DuoCard {
                    VStack(alignment: .leading, spacing: DuoSpace.x2) {
                        Text("Signed in").font(DuoType.itemTitle)
                        Text("Sync is on.").font(DuoType.secondary).foregroundStyle(.secondary)
                    }
                }
            }
            .duoContainerMargins()
        }
        .background(DuoColor.groupedBackground) // cards are white in light mode
    }
}
```

Every value, its source and how to change it safely: [references/tokens.md](references/tokens.md#every-value-and-where-it-comes-from).

## 2. Adapt per size class, not per device

- `@DuoMetrics` reads the size class where the view sits. Inside an `ArrangementView` half on the inner display it returns compact tokens, because that half reports compact width (*measured* in `duo-layout`).
- A custom split keeps the window's size class in each half (*measured* for `EvenSplit` in `duo-layout`: regular on the inner display). Give each half compact tokens with `.environment(\.horizontalSizeClass, .compact)` on the half.
- *Measured* offscreen: `@DuoMetrics` followed the size class and the Dynamic Type size set in the environment, and `readableWidth` scaled from 518 pt (xSmall) to 1691 pt (AX5).
- Change structure with `AnyLayout`, so views keep their state. `ViewThatFits` swaps children and resets their `@State` (*measured*); use it only for stateless labels and icons (see `duo-continuity`).

| Don't | Do |
|---|---|
| `if UIScreen.main.bounds.width > 900` | `tokens.columns`, or the view's own width |
| `userInterfaceIdiom == .pad ? 24 : 16` | `tokens.cardPadding` |
| `Font.system(size: isOpen ? 20 : 17)` | `DuoType.body`, the same everywhere |
| `cornerRadius: 55` to match the screen | `ConcentricRectangle` |
| `.padding(.horizontal, 20)` | `.duoContainerMargins()` |

## 3. Spacing, margins and gutters

- Spacing comes from `DuoSpace`: steps of 4 pt. Apple's padding advice (about 12 pt around controls with a bezel, about 24 pt around those without) sits on it ([HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)).
- Margins come from the system: `.duoContainerMargins()` uses `contentMargins(for: .container)` on iOS 27.1, which can differ on each side next to a vertical bar.
- Gutters: `tokens.gutter`, 12 pt compact and 16 pt regular (Duology default).
- The fold: flat, the middle gutter is a normal gutter centred on the fold line. Partly folded, it becomes the fold's frame, which includes the system's margin on each side of the curve (*measured*: 40 pt flat in `duo-layout`, and 40 pt partly folded in the gallery app's region overlay). Apple's Fitness example keeps the outer margins and widens only the middle ([111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=350)).

## 4. Even-column grids

Lay designed screens out on `tokens.columns` (4 or 8) and give content a span, not a width: `tokens.span(1)` for thumbnails, `span(2)` for cards, `span(4)` for wide cards. Spans double at accessibility text sizes, which gives fewer, wider columns, as Apple asks ([HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type)).

`DuoColumns` in [references/grid.md](references/grid.md#the-grid-helper) turns tokens and the fold into `LazyVGrid` columns. When a fold crosses the grid, flat or folded, it rounds to an even count, puts half the columns on each side of the fold and never lets a span cross it. If one side is too narrow (in a half of an `EvenSplit`), every column goes on the other side:

```swift
let columns = DuoColumns(width: geometry.width, count: tokens.columns,
                         gutter: tokens.gutter, fold: geometry.fold)
    .grouped(by: tokens.span(2))
// LazyVGrid(columns: columns.gridItems, spacing: tokens.gutter) { ... }
//     .padding(.leading, columns.leadingInset)
//     .frame(minWidth: 0, maxWidth: .infinity, alignment: .leading)
//     .onGeometryChange(for: DuoGridGeometry.self) { DuoGridGeometry($0) } action: { ... }
```

Measure the grid's width on that frame, never on the `LazyVGrid` itself: with fixed columns it reports their sum, so it never shrinks when the phone closes or enters Split View (*measured*). The full `CardGrid` view, the version for apps below iOS 27.1, and worked numbers for both displays are in [references/grid.md](references/grid.md). For an endless feed that should fit as many tiles as possible, use feed reflow from `duo-patterns`.

## 5. Type on both displays

- Use `DuoType` roles (system text styles). Body is 17 pt at the default size, from 14 pt (xSmall) to 53 pt (AX5) ([HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Specifications)).
- Don't change font sizes by display or size class. Apple asks Duo games to keep text and control sizes steady while resizing ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)); Duology applies that to every app.
- Cap long text with `.duoReadableWidth(tokens)` (600 pt at the default size, scaled). On the 867 pt inner display, a full-width paragraph is too long to read.
- At accessibility sizes, stack side-by-side rows and widen spans. Design the closed outer display at AX5 first: 382 × 644 pt of safe area (*measured*).
- Custom fonts: `Font.custom(_:size:relativeTo:)`.

Role table with sizes, the stacking row, and the test matrix: [references/typography.md](references/typography.md).

## 6. Liquid Glass

Liquid Glass is the controls layer (iOS 26 and later). On Duo the system already draws the vertical bar, sheets, menus and alerts in it.

- Controls only, never content. Few custom glass elements, and never glass on glass ([Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/?time=784)).
- Group neighbouring glass in one `GlassEffectContainer`; glass can't sample other glass ([WWDC25 323](https://developer.apple.com/videos/play/wwdc2025/323/?time=1196)).
- `.regular` for almost everything. `.clear` only over media, with a 35% black layer behind it when the media is bright.
- Tint only the primary action, on its background (`.buttonStyle(.glassProminent)`) ([HIG, Color](https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color)).
- No solid strip under controls; the scroll edge effect handles legibility.
- On Duo: no extra glass beside the vertical bar; custom content in the bar must read with and without its Reduce Transparency background ([111462](https://developer.apple.com/videos/play/tech-talks/111462/?time=652)); floating glass controls move off the fold like any control (`duo-layout`).

```swift
GlassEffectContainer(spacing: DuoSpace.x3) {
    HStack(spacing: DuoSpace.x3) {
        Button { } label: {
            Label("Play", systemImage: "play.fill").labelStyle(.iconOnly).duoTouchTarget()
        }
        .buttonStyle(.glassProminent)
        // More buttons with .buttonStyle(.glass)
    }
    .buttonBorderShape(.circle)
}
```

Full controls, clear glass with dimming, Reduce Transparency and UIKit: [references/liquid-glass.md](references/liquid-glass.md).

## 7. Corners

- Near a display edge, or nested in a rounded container: `ConcentricRectangle` or `.rect(corners: .concentric(minimum: .fixed(DuoTokens.innerRadius)))`. The same code follows the outer display's corners and the inner display's.
- Declare custom containers with `.containerShape(_:)`. Apply it before any `.background(_:in:)` on the same view; the other order made `concentricCornerRadii` read `nil` in our test.
- In an app that deploys below iOS 26, call it inside `if #available(iOS 26.0, *)`, as `duoContainerShape(_:)` does. Outside that check the compiler picks the iOS 15 overload, and `concentricCornerRadii` read `nil` (*measured*).
- `cardRadius = cardPadding + innerRadius`, so the first nested element lands on 8 pt. *Measured:* a child inset 16 pt in a 24 pt container resolves to 8 pt.
- Controls are capsules; near a phone's edge, give them extra margin ([WWDC25 356](https://developer.apple.com/videos/play/wwdc2025/356/?time=348)).

Code, measured radii and UIKit `cornerConfiguration`: [references/corners.md](references/corners.md).

## 8. Touch targets

- A hit region of at least 44 × 44 pt for every tappable element. In a screenshot, 44 pt is 132 px.
- Keep about 12 pt around controls with a bezel and about 24 pt around those without ([HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)).
- In small halves (closed and split, about 382 × 321 pt each, *measured* in `duo-shared-screen`), drop labels and spacing before you shrink a target.
- Keep targets out of the fold's frame when the phone is partly open.
- *Measured* offscreen: a symbol-only `Button` was 23 × 20 pt and a symbol-only `.glassProminent` circle 29 × 30 pt until we added `duoTouchTarget()` (then 44 × 44 and 58 × 58 pt). Never trust a style to reach 44 pt on its own.

```swift
Button { isFavorite.toggle() } label: {
    Image(systemName: isFavorite ? "star.fill" : "star").duoTouchTarget()
}
.accessibilityLabel(isFavorite ? "Remove Favorite" : "Add Favorite")
```

## 9. Colour and contrast

- Use `DuoColor` backgrounds and `.primary` / `.secondary` text styles. They adapt to light, dark and Increase Contrast.
- Put `DuoCard` on `DuoColor.groupedBackground`, never on `DuoColor.background`: in light mode the card and `systemBackground` are the same white (*measured*).
- *Measured* on the iOS 27.1 runtime: `label` on `systemBackground` is 21:1. `secondaryLabel` is 3.44:1 in light mode (5.97:1 with Increase Contrast) and `systemBlue`, the default tint, 3.52:1. Use those for 18 pt and up, bold text, symbols and controls; use `label` for small text people must read.
- Custom colours: `DuoColor.dynamic(light:dark:lightHighContrast:darkHighContrast:)` or an asset catalog colour with Dark and High Contrast variants.
- Check pairs in a unit test with `duoWorstContrast(text:on:)` from [references/color.md](references/color.md#check-contrast-in-code).
- Never carry meaning in colour alone.

## UIKit

Same tokens, read with `DuoTokens(traitCollection)` and re-applied on trait changes. `readableContentGuide`, `UIFontMetrics`, `cornerConfiguration` and `UIGlassEffect` replace the SwiftUI pieces. Code: [references/uikit.md](references/uikit.md).

## Deploying below iOS 27.1

The token module builds for iOS 17. Glass, `ConcentricRectangle` and `scrollEdgeEffectStyle` need iOS 26. `concentricCornerRadii` needs iOS 27.0. Container margins and the fold need iOS 27.1. Mark types `@available` and call them inside `if #available`; iPhone Duo always runs iOS 27.1.

## Test it

1. In Device Hub, check Closed, Open and Partially Open, held wide and held tall, and Split View on both sides. `simctl` can't change the pose.
2. Text sizes: Large, xxxLarge and AX5 on the closed outer display first (`xcrun simctl ui <device> content_size accessibility-extra-extra-extra-large`; set it back afterwards on a shared simulator).
3. Light and dark (`xcrun simctl ui <device> appearance dark`), Increase Contrast (`increase_contrast enabled`), and Reduce Transparency in Settings, one at a time and together. Put each setting back when you finish.
4. Measure hit regions and the middle gutter on screenshots: `xcrun simctl io booted screenshot --display=primary` (outer) and `--display=primary-1` (inner).
5. Run `duo-design-review`'s checklist, rules R5 (even grids) and R13 (touch targets) at least.

## Checklist

- [ ] `DuoTokens.swift` is in the app; no spacing, radius or font size is written as a literal in views.
- [ ] No token depends on the device, display, idiom, orientation or `UIScreen.main`.
- [ ] Custom split halves set a compact size class; arrangement halves read their own.
- [ ] Margins come from `duoContainerMargins()` (or `layoutMarginsGuide`), per side.
- [ ] Grids use 4 or 8 columns split at the fold, flat and folded; no item crosses it; the width is read from a frame that fills the offered width.
- [ ] Text uses `DuoType` roles or `Font.custom(_:size:relativeTo:)`; sizes are the same on both displays.
- [ ] Long text is capped with `duoReadableWidth`; AX5 works on the closed outer display.
- [ ] Glass is on controls only, grouped in `GlassEffectContainer`, regular unless over media; one tinted action at most.
- [ ] Corners near an edge or inside a container are concentric; `containerShape` comes before `background(_:in:)`.
- [ ] Every tappable element has a 44 × 44 pt hit region, also in the smallest half.
- [ ] Custom colours have light, dark and high-contrast variants; text pairs meet 4.5:1 (3:1 at 18 pt or bold); cards sit on `DuoColor.groupedBackground`.
- [ ] Checked closed, open, partly folded, Split View, AX5, dark, Increase Contrast and Reduce Transparency.
