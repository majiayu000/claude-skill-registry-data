---
name: duo-system-surfaces
description: "Widgets, Live Activities, StandBy and Controls for apps on iPhone Duo, Apple's foldable. Use it when you build or check a widget extension, a Live Activity, a Dynamic Island presentation, a StandBy layout or a Control Center or Lock Screen control, and the app runs on iPhone Duo. Covers the redesigned Dynamic Island in the side column of the outer and inner display, which grows down that column as Live Activities arrive and takes room from the app's own vertical bars (measured: about 84 pt closed, 94 pt open); isDynamicIslandLimitedInWidth (iOS 27, names iPhone Duo) for narrow compact and minimal views that fit a 28 pt circle; StandBy on either display, even when not charging; two Home Screen pages and Today View; widget families, including the new systemExtraLargePortrait, where Apple's pages disagree; controls with no Action button on Duo; deep links that work closed and open. Says what Apple has not published, what the simulator cannot run (StandBy, most app extensions) and what to test on a device."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-system-surfaces

The system draws your widgets, Live Activities and controls, not your app. On iPhone Duo it draws them in new places: a Dynamic Island in the side column of both displays, two Home Screen pages with Today View, StandBy on either display. You can't lay these places out. Your job is to give each presentation content that still reads when the system makes it narrower, taller or bigger, and to check on a device what the simulator can't show.

Load neighbours when the task needs them: `duo-navigation` (your app's bars, which share the side column with the island), `duo-continuity` (opening the right screen from a tap), `duo-swiftui-27` (`visibilityPriority` and the other iOS 27 toolbar APIs).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 20 October 2026). *Unverified* means we could not confirm it. *Not published* means Apple has said nothing about it as of 20 October 2026. Everything else links to Apple. Runs: [references/evidence.md](references/evidence.md). Sources: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## What Apple has said about iPhone Duo

| Claim | Source |
|---|---|
| The side column of both displays holds the status bar and the Dynamic Island. The island is redesigned to fit vertically there and expands to show Live Activities and alerts. | [Newsroom](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/), [Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=94), [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) |
| On the outer display the island grows out of the front camera's region, which is always present. | [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) |
| App bars share that column with Live Activities and the status bar. When room runs out, app items collapse into the overflow menu. | [Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=336) |
| The system draws compact and minimal Live Activity views narrower on iPhone Duo (and on iPhone held sideways). Read `isDynamicIslandLimitedInWidth` (iOS 27.0). | [doc](https://developer.apple.com/documentation/swiftui/environmentvalues/isdynamicislandlimitedinwidth) |
| Where width is limited (which the doc above says includes iPhone Duo), compact and minimal views should fit a 28 pt circle. A leading view alone is fine; the system then hides the trailing one. | [HIG: Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities) (updated 13 Oct 2026) |
| Open, the display shows two Home Screen pages, with Today View (a scrolling list of widgets) on the left. The Dock and Lock Screen controls sit on the side. | [Newsroom](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/) |
| Set down, iPhone Duo enters StandBy on the outer or the inner display, even when it isn't charging. | [Newsroom](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/) |
| iOS 27 adds the `systemExtraLargePortrait` widget family to iOS. | [doc](https://developer.apple.com/documentation/widgetkit/widgetfamily/systemextralargeportrait), [WWDC26 session 277](https://developer.apple.com/videos/play/wwdc2026/277/?time=711) |
| The spec page lists volume buttons, Camera Control and the side button, and no Action button. | [Specs](https://www.apple.com/iphone-duo/specs/) |

## What Apple has not published

- Widget sizes in points on either display. The HIG's iOS widget table has no iPhone Duo row ([HIG: Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets#Specifications)).
- Which families each Home Screen offers. The HIG's family table says iPhone supports neither extra-large family; the API doc and session 277 say `systemExtraLargePortrait` comes to iOS 27. Whether Duo offers it is unverified.
- How compact, minimal and expanded views are laid out in a vertical island, how several activities stack there, and their sizes. The HIG's Live Activity table lists two iPhone screen sizes only.
- StandBy on Duo: sizes, which faces go on which display, how a widget or Live Activity looks there.
- Anything about controls on Duo. The HIG's Controls page has not changed since June 2024.
- An iOS 27 entry on the [WidgetKit](https://developer.apple.com/documentation/updates/widgetkit) or [ActivityKit](https://developer.apple.com/documentation/updates/activitykit) updates pages. The two iOS 27 additions above (`isDynamicIslandLimitedInWidth`, `systemExtraLargePortrait`) appear only in the SDK and the symbol docs. The ActivityKit interface in the iOS 27.1 SDK has no iOS 27 symbols.

## What the simulator can and can't show

Xcode 27.1's release notes list two limits of the iPhone Duo simulator: StandBy is unavailable, and most app extensions can't run or be debugged ([release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)). Widgets, Live Activity views and controls are app extensions.

*Measured*:

- `Activity.request` succeeded from the app, and the activity reported `.active`.
- With the app in front, its own activity took no room in the side column.
- With Settings in front, the island's content never appeared in screenshots, but the side column made room for it. The status bar's clock moved down from 87 to 171 pt closed (about 84 pt) and from 34 to 128 pt open, held wide (about 94 pt).
- Closed, the Home Screen put the Dock and the search button in the side column. The widget gallery opened on the outer display and listed the app's widget.

Use Xcode Previews for each widget family and island presentation, and a real iPhone Duo for StandBy and the vertical island. Details: [references/evidence.md](references/evidence.md).

## Rules

1. Never hard-code a widget, island or StandBy size. Apple says widget sizes vary by device ([WidgetFamily](https://developer.apple.com/documentation/widgetkit/widgetfamily)) and publishes none for Duo.
2. Give every compact and minimal view a limited-width form. On Duo it is the normal case, not an edge case.
3. Make the Lock Screen view work scaled up and without its background, for StandBy on either display.
4. Offer several widget families. Add `systemExtraLargePortrait` behind `if #available(iOS 27.0, *)`, with content that grows by rows, not by a fixed height.
5. Rank your toolbar items. A running Live Activity takes height from the column your vertical bar uses.
6. Route every tap to state that both layouts read. The app may open closed or open.
7. Don't promise an Action button on Duo. Offer controls for Control Center and the Lock Screen.

## 1. Live Activities in the side column

Write the narrow form first. `isDynamicIslandLimitedInWidth` is iOS 27 only and read-only, so wrap it when the extension deploys lower. iPhone Duo always runs iOS 27.1, so the fallback runs only on other iPhones.

```swift
import SwiftUI
import WidgetKit

// requires: MinutesLeftLabel (references/live-activities.md)

/// Narrow on iPhone Duo and on iPhone held sideways.
struct MinutesLeft: View {
    let minutes: Int

    var body: some View {
        if #available(iOS 27.0, *) {
            LimitedAware(minutes: minutes)
        } else {
            MinutesLeftLabel(minutes: minutes, limited: false)
        }
    }

    @available(iOS 27.0, *)
    private struct LimitedAware: View {
        let minutes: Int
        @Environment(\.isDynamicIslandLimitedInWidth) private var isLimited

        var body: some View {
            MinutesLeftLabel(minutes: minutes, limited: isLimited)   // the number alone when limited
        }
    }
}
```

- Use it for `compactTrailing` and `minimal`. Keep `compactLeading` to one symbol, or drop the trailing view when no short form makes sense ([HIG](https://developer.apple.com/design/human-interface-guidelines/live-activities)).
- Keep the expanded view's elements in the same places as the compact ones. Its layout in the vertical island is not published; test it on a device.
- End the activity when the task ends. While it runs, it takes height in the side column that other apps' vertical bars use (section 5).
- Full `ActivityConfiguration`, previews, the StandBy background and the deep link: [references/live-activities.md](references/live-activities.md).

## 2. StandBy on either display

On iPhone, StandBy shows a Live Activity as its minimal view; a tap shows the Lock Screen view scaled up 2x. Widgets in StandBy are the small family, scaled up, without their background ([HIG: Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities#StandBy), [HIG: Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets#StandBy-and-CarPlay)). On Duo that can happen on the 5.4-inch outer display or the 7.6-inch inner display. Apple publishes no StandBy sizes for either.

- Draw the Lock Screen view's background only when `showsWidgetContainerBackground` is `true`. Set `activityBackgroundTint(_:)` so StandBy fills the screen with your colour ([session 223](https://developer.apple.com/videos/play/wwdc2026/223/?time=679)).
- Keep the widget background removable (the default), or the widget can't appear in StandBy.
- Use large type and few elements; people read StandBy from across a room.
- In low light, StandBy tints widgets red. Don't carry meaning in colour alone.
- StandBy is unavailable in the iPhone Duo simulator. Test it on a device, on both displays.

## 3. Widgets on two Home Screens

Closed, your widget sits on the outer display's Home Screen. Open, it can sit on either Home Screen page or in Today View. Apple has not published the sizes, so lay out by family and let content grow or shrink.

```swift
import SwiftUI
import WidgetKit

// requires: ShelfProvider, ShelfWidgetView (references/widgets-and-controls.md)

struct ShelfWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "shelf", provider: ShelfProvider()) { entry in
            ShelfWidgetView(entry: entry)          // ViewThatFits: more rows where there is room
                .containerBackground(.fill.tertiary, for: .widget)
                .widgetURL(URL(string: "reader://shelf"))
        }
        .configurationDisplayName("Reading shelf")
        .supportedFamilies(Self.families)
    }

    static var families: [WidgetFamily] {
        var list: [WidgetFamily] = [.systemSmall, .systemMedium, .systemLarge, .accessoryRectangular]
        if #available(iOS 27.0, *) {
            list.append(.systemExtraLargePortrait)   // new tall family; whether Duo offers it is unverified
        }
        return list
    }
}
```

- Design one widget for both displays. The same family can appear on either, and nothing in WidgetKit tells a widget which display it is on.
- A tap opens the app on the display in use. Route `widgetURL(_:)` to state that the compact and the regular layout both read, not to a screen that exists in one of them (`duo-continuity`). Code: [references/live-activities.md](references/live-activities.md#opening-the-app).

## 4. Controls

Controls (`ControlWidgetButton`, `ControlWidgetToggle`) appear in Control Center and on the Lock Screen ([HIG: Controls](https://developer.apple.com/design/human-interface-guidelines/controls)). On Duo, Lock Screen controls sit on the side ([Newsroom](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/)), and the spec page lists no Action button. Build controls as on any iPhone. Don't write help text that tells Duo owners to put one on the Action button. Example: [references/widgets-and-controls.md](references/widgets-and-controls.md#controls).

## 5. Your bars share the column with the island

Your vertical toolbar and tab bar live in the same column as the island and the status bar. A Live Activity from any app can take height from your bar while your app runs. *Measured*: one activity pushed the status bar down by about 84 pt closed and 94 pt open. Rank items so the important ones stay:

- `.visibilityPriority(.high)` on the actions people use most; `.low` on rare ones; `ToolbarOverflowMenu` for actions that always belong in the menu (`duo-swiftui-27`, `duo-navigation`).
- Give every item a symbol and a title, so it reads well in the overflow menu.
- Check it with a Live Activity from another app running, closed and open held wide, on a device. *Unverified*: we did not see an app's own bars next to another app's activity in the simulator.

## Test it

1. Previews: one `#Preview(as: .systemSmall)` (and one per family) per widget, and `#Preview(as: .dynamicIsland(.compact), using:)` plus `.dynamicIsland(.minimal)`, `.dynamicIsland(.expanded)` and `.content` per Live Activity. Preview the limited-width form on its own at 28 pt.
2. Simulator: start the Live Activity from your app, bring another app forward, and check that the activity reports active. Check your deep links closed and open.
3. Device: StandBy on the outer and the inner display, the vertical island closed and open, several activities at once, widgets on both Home Screen pages and in Today View, controls in Control Center and on the Lock Screen.

## Checklist

- [ ] No fixed widget, island or StandBy sizes anywhere in the extension.
- [ ] `compactTrailing` and `minimal` have a limited-width form behind `isDynamicIslandLimitedInWidth`, gated for iOS 27.
- [ ] The limited form fits a 28 pt circle; the leading view alone still makes sense.
- [ ] The Lock Screen view draws its background only when `showsWidgetContainerBackground` is `true`, and sets `activityBackgroundTint(_:)`.
- [ ] Widget backgrounds stay removable; StandBy content uses large type and doesn't rely on colour.
- [ ] Widgets support several families; `systemExtraLargePortrait` only behind `#available(iOS 27.0, *)`.
- [ ] Widget views grow by rows with `ViewThatFits`, not by fixed heights.
- [ ] Taps from widgets and Live Activities route to state that works closed and open.
- [ ] Toolbar items carry visibility priorities, so a growing island overflows the right ones.
- [ ] Live Activities end when the task ends.
- [ ] No help text assumes an Action button.
- [ ] Previews checked for every family and island presentation; StandBy and the vertical island checked on a device, or marked untested.
