---
name: duo-navigation
description: Gets toolbars, navigation bars, tab bars, split views and sheets right on iPhone Duo, Apple's foldable, where bars move into one vertical bar on the side of the outer display and of the inner display in landscape. Use it when bars go vertical, items overflow or vanish, an app draws its own custom bottom bar (UIToolbar, or a SwiftUI row in safeAreaInset or an overlay), toolbar or Menu buttons are icon-only, tabs should become a sidebar on the inner display, a sheet should sit to one side or off the fold, or code touches toolbarVerticalBehavior, toolbarVerticalEdge, axisBehavior, visibilityPriority, topBarPinnedTrailing, ToolbarOverflowMenu, toolbarVerticalCompressionBehavior, defaultTabBarPlacement, presentationPlacement, NavigationSplitView, preferredVerticalBarBehavior, verticalBarEdge, pinnedTrailingGroup, additionalOverflowItems, UITabBarController.Sidebar.preferredPlacement or UISheetPresentationController.preferredPlacement.
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-navigation

On iPhone Duo the system can merge the navigation bar, the toolbar and the tab bar into one vertical bar on the side of the display. You get this for free when you build with the iOS 27.1 SDK and use the bars that system containers own. Your job is to keep those bars, give each item what it needs to move, rank items for overflow, and opt out only where horizontal bars serve a screen better.

Load other skills for neighbouring work: `duo-layout` (safe areas, margins, the fold in your own content), `duo-continuity` (state that must survive a fold), `duo-patterns` (which layout to pick).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, inner display, fully open, held wide). *Unverified* means we could not confirm it. Everything else comes from Apple, linked inline. Sources: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Where the bars go

| Context | Bars |
|---|---|
| Outer display (closed), portrait or landscape | One vertical bar on the side |
| Inner display, landscape (held wide) | One vertical bar on the side (*measured*: trailing edge) |
| Inner display, portrait (held tall) | Normal top and bottom bars |
| Split View multitasking on the inner display | Each app puts its bar on its own outer edge |
| `NavigationSplitView` / `UISplitViewController` showing columns | Detail column vertical; sidebar and content columns horizontal (*measured* in SwiftUI) |
| Inspector | Horizontal |
| Sheet on the outer display | Vertical |
| Sheet on the inner display, centred (default) or leading | Horizontal (*measured* in SwiftUI) |
| Sheet on the inner display, trailing | Vertical (*measured* in SwiftUI) |

Sources: [HIG, Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls), [Optimize bars for vertical presentation](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Optimize-bars-for-vertical-presentation), [Tech Talk 111462](https://developer.apple.com/videos/play/tech-talks/111462/).

- The bar stays on the same hardware edge in right-to-left languages.
- Top-bar items go to the top of the vertical bar, bottom-bar items to the bottom, the tab bar at the very bottom. The system puts a gap between the two item sets.
- A vertical bar adds a leading or trailing safe-area inset instead of top and bottom ones. *Measured:* the content margin next to the bar drops to 0 while the far side keeps its usual margin. Never assume both sides match.
- Bars go vertical only in builds made with the iOS 27.1 SDK or later ([prepare page](https://developer.apple.com/iphone-duo/prepare/)).

Details, container rules and probe results: [references/bar-rules.md](references/bar-rules.md).

## Use the bars that containers own

- SwiftUI: attach `.toolbar` to content inside `NavigationStack`, `NavigationSplitView` or a `TabView` tab.
- UIKit: set `navigationItem` and `toolbarItems` on a view controller inside `UINavigationController` or `UITabBarController`.
- A hand-built bar never joins the vertical bar. In UIKit that is a `UIToolbar`, `UINavigationBar` or `UITabBar` you create yourself. In SwiftUI it is a row of buttons in `safeAreaInset(edge: .bottom)` (or `.top`) or in `.overlay(alignment: .bottom)`. That row is your own content, so the system never moves it.
- Move each action of a SwiftUI row into `.toolbar`: a bottom row into `ToolbarItemGroup(placement: .bottomBar)`, a top row into `.primaryAction` items. Drop the `Spacer()`s. A lone floating button may stay; put it on the bar's side, near the thumb and clear of the bar's items (see "Adapt custom views to the bar" and `duo-ergonomics`). Recipe: [references/swiftui.md](references/swiftui.md#replace-a-hand-drawn-bar).
- Give icon-only labels a title, `Menu` labels included. Replace `label: { Image(systemName: "…") }` with `Button("Sort", systemImage: "…")`, `Menu("Sort", systemImage: "…") { … }` or a `Label("Sort", systemImage: "…")` label.

Run both searches from the project root and review every hit. Keep the `--include` pattern quoted: unquoted, zsh stops with "no matches found" and exits 1, the same code grep gives for "no hits". No output and no error means no hits.

```bash
# Hand-built bars: UIKit bar views, SwiftUI rows pinned to the top or bottom edge.
grep -rnE 'UIToolbar\(|UINavigationBar\(|UITabBar\(|safeAreaInset\(edge: *\.(top|bottom)|overlay\(alignment: *\.(top|bottom)' --include='*.swift' .
# Icon-only labels: a bare Image on the `label: {` line or the line after it.
grep -rnE -A1 'label: *\{' --include='*.swift' . | grep -E 'Image\(systemName'
```

## Order, label and rank items

```swift
import SwiftUI

struct NoteEditor: View {
    @Environment(\.dismiss) private var dismiss
    @State private var text = ""

    var body: some View {
        NavigationStack {
            TextEditor(text: $text)
                .navigationTitle("Note")
                .toolbar {
                    // First in the vertical bar: the way out.
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Close", systemImage: "xmark", role: .close) { dismiss() }
                    }
                    // Second: the prominent action. Pinned items stay out of overflow.
                    ToolbarItem(placement: .topBarPinnedTrailing) {
                        Button("Done", systemImage: "checkmark", role: .confirm) { dismiss() }
                    }
                    // A group with symbols and titles, kept visible longer.
                    ToolbarItemGroup(placement: .bottomBar) {
                        Button("Checklist", systemImage: "checklist") {}
                        Button("Attach", systemImage: "paperclip") {}
                    }
                    .visibilityPriority(.high)
                    // Rare and destructive: first to overflow.
                    ToolbarItem(placement: .bottomBar) {
                        Button("Delete", systemImage: "trash", role: .destructive) {}
                    }
                    .visibilityPriority(.low)
                    // Always in the system overflow menu.
                    ToolbarOverflowMenu {
                        Button("Duplicate", systemImage: "plus.square.on.square") {}
                        Button("Print", systemImage: "printer") {}
                    }
                }
        }
    }
}
```

*Measured* with a toolbar built the same way: Close, then Done, then the overflow button at the top of the vertical bar, and the bottom group at its foot.

- Back or Close goes first. A navigation stack adds Back for you. For your own Close use `.cancellationAction`, or `navigationItem.leadingItemGroups` in UIKit with `leftItemsSupplementBackButton` left at `false` ([hub](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)).
- The prominent action (Done, Send) goes next with `.topBarPinnedTrailing` or `navigationItem.pinnedTrailingGroup`. A pinned SwiftUI item overflows only while search is active and space runs out ([doc](https://developer.apple.com/documentation/swiftui/toolbaritemplacement/topbarpinnedtrailing)).
- Give every item a symbol and a title. The vertical bar shows the symbol; the overflow menu shows both. An item with only a title, or a custom view, stays horizontal. *Measured (UIKit):* so did a symbol item in the same group as a text-only item, so give text-only items their own group.
- Turn text that only repeats the symbol into a badge: `.badge(7)` or `UIBarButtonItem.badge = .count(7)`. Keep text that carries facts, like a price, in the horizontal bar.
- Keep your groups (`ToolbarItemGroup`, `UIBarButtonItemGroup`). Add no spacers, fixed or flexible: Apple asks apps not to add their own spacing on either axis. In the vertical bar fixed spacers keep their size and flexible ones shrink to zero ([Tech Talk 111462](https://developer.apple.com/videos/play/tech-talks/111462/)).
- Items overflow from the bottom of the bar upward. Raise frequent actions and badged items with `.high`; lower rare ones with `.low`. Rank whole groups first, then single items ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)).
- Move your own "More" menu into `ToolbarOverflowMenu` or `navigationItem.additionalOverflowItems`. Keep the ellipsis symbol for that menu only.

## Pick the axis for special items

| `axisBehavior` value | Use for |
|---|---|
| `.automatic` (default) | Symbol items go on either axis. Text items and custom views stay horizontal. |
| `.horizontalOnly` | An item that swaps a symbol for text, like Select and Done. The item hides when no horizontal bar exists. |
| `.verticalPreferred` | A custom view that fits the bar's fixed width, like a compass. |

```swift
import SwiftUI

struct PhotoGrid: View {
    @State private var isSelecting = false

    var body: some View {
        NavigationStack {
            Text("Photos")
                .navigationTitle("Library")
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        if isSelecting {
                            Button("Done") { isSelecting = false }
                        } else {
                            Button("Select", systemImage: "checkmark.circle") { isSelecting = true }
                        }
                    }
                    .axisBehavior(.horizontalOnly)
                }
        }
    }
}
```

The system `EditButton` already stays horizontal. *Measured:* a `.horizontalOnly` item showed in the top bar next to the title.

## Opt out only where horizontal bars win

Apple names three cases: a single screen with a bottom-heavy layout that doesn't scroll (Calculator), a full-screen video player with toolbar controls, and a sheet whose only item is Close ([Tech Talk 111462](https://developer.apple.com/videos/play/tech-talks/111462/), [doc](https://developer.apple.com/documentation/swiftui/view/toolbarverticalbehavior(_:))).

```swift
import SwiftUI

struct CalculatorScreen: View {
    var body: some View {
        NavigationStack {
            Text("0")
                .font(.largeTitle)
                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottomTrailing)
                .toolbarVerticalBehavior(.disabled)
        }
    }
}

struct RecentsTab: View {
    var body: some View {
        TabView {
            Tab("Recents", systemImage: "clock") {
                NavigationStack {
                    Text("Files")
                        .toolbar {
                            Button("Up", systemImage: "chevron.up") {}
                            Button("Down", systemImage: "chevron.down") {}
                        }
                        // Task view: let the tab bar shrink before these items.
                        .toolbarVerticalCompressionBehavior(.prefersToolbarItems)
                }
            }
        }
    }
}
```

- Treat `.disabled` as a fixed choice per screen. Never toggle it from view state. To hide bars, use `toolbarVisibility(_:for:)` ([doc](https://developer.apple.com/documentation/swiftui/view/toolbarverticalbehavior(_:))).
- Where to put it: a `NavigationStack` reads its top view, a `TabView` its selected tab, a `NavigationSplitView` its trailing column, a sheet its own content.
- UIKit: override `preferredVerticalBarBehavior` to return `.disabled`, and call `setNeedsUpdateOfVerticalBarConfiguration()` when the answer changes. Navigation and tab bar controllers forward to their visible child; a custom container overrides `childForPreferredVerticalBarBehavior`.
- Compression: the default keeps the tab bar and overflows toolbar items. Use `.prefersToolbarItems` (SwiftUI) or `.prefersBarItems` (UIKit `navigationItem.verticalBarCompressionBehavior`) for task screens.

## Adapt custom views to the bar

```swift
import SwiftUI

struct CanvasScreen: View {
    @Environment(\.toolbarVerticalEdge) private var barEdge

    var body: some View {
        ZStack {
            Color.clear
            // On the bar's side, near the thumb (Apple's toolbarVerticalEdge example); no bar: trailing.
            Text("Palette")
                .padding().background(.thinMaterial, in: .capsule)
                .padding([.horizontal, .bottom], 16)  // the margin next to the bar is 0 pt
                .frame(maxWidth: .infinity, maxHeight: .infinity,
                       alignment: barEdge == .leading ? .bottomLeading : .bottomTrailing)
                .contentMargins(for: .container)
        }
    }
}
```

- `toolbarVerticalEdge` is `nil` where the system never places a vertical bar. *Measured:* it also reads `nil` inside a centred or leading sheet and under `.toolbarVerticalBehavior(.disabled)`. UIKit's `traitCollection.verticalBarEdge` reads `.unspecified` (*measured* after opting out). Observe it with `registerForTraitChanges(UITraitCollection.systemTraitsAffectingVerticalBarEdge)`.
- Extend hero art under the bar with `.backgroundExtensionEffect()` or `UIBackgroundExtensionView`.

## Tabs to a sidebar on the inner display

Offer a sidebar for information-dense apps, not for every app ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/)).

```swift
import SwiftUI

struct HealthRoot: View {
    var body: some View {
        TabView {
            Tab("Summary", systemImage: "heart") { SummaryScreen() }
            Tab("Sharing", systemImage: "person.2") { Text("Sharing") }
            Tab("Browse", systemImage: "square.grid.2x2") { Text("Browse") }
        }
        .tabViewStyle(.sidebarAdaptable)   // defaultTabBarPlacement only applies to this style
        .defaultTabBarPlacement(.sidebar)
    }
}

struct SummaryScreen: View {
    @Environment(\.isTabViewSidebarAvailable) private var hasSidebar

    var body: some View {
        Text(hasSidebar ? "Sidebar layout" : "Tab bar layout")
    }
}
```

- *Measured:* on the inner display this shows a sidebar and `isTabViewSidebarAvailable` is `true`. The `tabBarPlacement` environment value still said `bottomBar`, so gate on `isTabViewSidebarAvailable`, never on `tabBarPlacement` or size class.
- UIKit: set `tabBarController.mode = .tabSidebar` and `tabBarController.sidebar.preferredPlacement = .sidebar`. *Measured:* `preferredPlacement` alone gave no sidebar. Read `sidebar.isAvailable` and implement `tabBarController(_:sidebarAvailabilityDidChange:)`.
- *Unverified:* that the outer display keeps a tab bar with this setting. Apple implies it; check in Device Hub.

## Split views

- Use `NavigationSplitView` or `UISplitViewController`. Closed, they collapse to one stack. Open, they show columns. Partially folded, they even out the columns around the fold ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/), [Tech Talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/)). Switching panes yourself? Opening on a pushed screen pops it: see [references/swiftui.md](references/swiftui.md#a-stack-that-pops-when-the-phone-opens).
- Put actions for the open item on the detail column; they join the vertical bar. Keep actions for the list on the list column, where they stay horizontal above it ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)).
- Put an `ArrangementView` inside a `NavigationStack` or a `TabView` tab. Never put a navigation container inside an arrangement, and never put an arrangement inside a `List` or `ScrollView` ([Tech Talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/)).
- Keep arrangements out of `NavigationSplitView` columns too. Apple's pages disagree here: the [hub](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Arrange-views-in-different-poses) advises against it, while the [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Arrangement-views) shows split views around arrangements. The stricter rule is the safe default.

## Sheets and other presentations

```swift
import SwiftUI

struct MapScreen: View {
    @State private var showsPlace = false

    var body: some View {
        Button("Show place") { showsPlace = true }
            .sheet(isPresented: $showsPlace) {
                NavigationStack {
                    Text("Place details")
                        .toolbar {
                            Button("Close", systemImage: "xmark", role: .close) { showsPlace = false }
                            Button("Share", systemImage: "square.and.arrow.up") {}
                        }
                }
                .presentationDetents([.medium, .large])
                .presentationPlacement(.trailing)   // keeps the content behind in view; gets a vertical bar
            }
    }
}
```

- Sheets, alerts, menus and popovers move off the fold by themselves when the phone is partially folded. Don't reposition them ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/)).
- Pick `.leading`, `.center` or `.trailing` to keep the content behind the sheet in view, as Apple's map example does ([doc](https://developer.apple.com/documentation/swiftui/view/presentationplacement(_:))). Only sheets read `presentationPlacement(_:)`.
- UIKit: set `sheetPresentationController?.preferredPlacement` before you present. It is ignored when `sourceView` is set (`UISheetPresentationController.h`).
- For a sheet whose only item is Close, add `.toolbarVerticalBehavior(.disabled)` inside the sheet. On the outer display the sheet then stops short of the front camera ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/)).

## UIKit and older deployment targets

Full UIKit code: [references/uikit.md](references/uikit.md). More SwiftUI: [references/swiftui.md](references/swiftui.md). iPhone Duo always runs iOS 27.1 or later, so gate these APIs with `if #available` (versions in [references/bar-rules.md](references/bar-rules.md#availability)); the fallback runs only on other iPhones.

## Check it

Build with Xcode 27.1 and run on the iPhone Duo simulator. In Device Hub, try Closed, Open (held wide and held tall), Partially Open, and Split View on each side; `simctl` cannot change poses. Find the Duo's UDID with `xcrun simctl list devices booted` (more in `duo-setup`); `booted` is ambiguous when several simulators run. Screenshot the outer display with `xcrun simctl io <UDID> screenshot --display=primary outer.png` and the inner one with `xcrun simctl io <UDID> screenshot --display=primary-1 inner.png`. Then tick:

- [ ] Built with the iOS 27.1 SDK; no hand-built `UIToolbar`, `UINavigationBar` or `UITabBar`, no SwiftUI button rows in `safeAreaInset` or an edge overlay, and no icon-only `label: { Image(systemName:) }` in bars or `Menu` labels.
- [ ] Back or Close is first; the prominent action is pinned second.
- [ ] Every non-text item has a symbol and a title; text-only items are few and grouped apart; no spacers, fixed or flexible.
- [ ] Groups and items carry a visibility priority (frequent and badged items rank high); own "More" menus moved into the system overflow menu.
- [ ] Task screens set `.prefersToolbarItems` / `.prefersBarItems`.
- [ ] Vertical bars disabled only on calculator-like, full-screen video or single-Close sheet screens, never toggled by state.
- [ ] Custom floating UI reads `toolbarVerticalEdge` / `verticalBarEdge` and uses margins, not fixed insets.
- [ ] Sidebar opt-in uses `.sidebarAdaptable` + `.defaultTabBarPlacement(.sidebar)`, or `mode = .tabSidebar` + `preferredPlacement = .sidebar`.
- [ ] Split views are system split views with detail actions on the detail column; sheet placement only keeps content visible, with no manual fold avoidance.
- [ ] Checked closed, open wide, open tall, partially open and Split View in Device Hub.
