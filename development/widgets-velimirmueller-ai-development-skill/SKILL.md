---
name: widgets
description: Use when building a widget extension, a timeline provider, a Lock Screen or accessory widget, a watch complication, an interactive button/toggle widget, a Control Center control, a Live Activity, or fixing a widget that won't update or render correctly in tinted mode. Writes and reviews SwiftUI…
license: MIT
metadata:
  author: Anton Novoselov
  version: '1.2'
---

Write and review SwiftUI WidgetKit code, choosing the right configuration, timeline policy, and surface so the widget renders correctly in every mode, updates within its budget, and behaves correctly across the extension/app process boundary.

Review process:

1. Establish the widget execution model (the extension process, app groups, the timeline lifecycle, the reload budget) using `references/fundamentals.md`.
1. Validate the timeline provider (`placeholder`/`snapshot`/`timeline`, reload policy, `WidgetCenter` reloads, entry relevance) using `references/timeline-provider.md`.
1. Validate the configuration and any user-configurable parameters (`StaticConfiguration`, `AppIntentConfiguration`, `WidgetConfigurationIntent`) using `references/configuration-and-intents.md`.
1. Check whether any legacy API is in use and route it to the modern equivalent (SiriKit `.intentdefinition` → App Intents, ClockKit → WidgetKit, `PreviewProvider` → `#Preview`) using `references/migration-and-deprecations.md`.
1. Validate data loading - networking, persistence, images, location - in the provider and intents using `references/data-and-networking.md`.
1. Validate family support and per-family layout (`WidgetFamily`, sizing, content margins, `ViewThatFits`) using `references/families-and-layout.md`.
1. Validate Lock Screen / accessory widgets and watch complications (`widgetLabel`, `AccessoryWidgetBackground`, the transparent-container trick, ClockKit migration) using `references/lock-screen-and-watch.md`.
1. Validate rendering across full-color, accented, tinted, and vibrant modes (`widgetRenderingMode`, `widgetAccentable`, `widgetAccentedRenderingMode`, the luminance-to-alpha trick) using `references/rendering-modes-and-tinting.md`.
1. Validate interactivity (`Button(intent:)`, `Toggle(intent:)`, the app-process boundary, `reloadTimelines`, `invalidatableContent`) using `references/interactive-widgets.md`.
1. Validate deep links and navigation into the app (`widgetURL`, `Link`, `onOpenURL`, `OpenIntent`) using `references/deep-linking-and-navigation.md`.
1. Validate animations and entry transitions (`contentTransition`, `.transition` + identity, `invalidatableContent`, what doesn't animate) using `references/animations-and-transitions.md`.
1. Validate Control Center controls (`ControlWidget`, toggle vs button, `SetValueIntent`, value providers, `ControlCenter` reloads) using `references/controls.md`.
1. Validate Live Activities and the Dynamic Island (`ActivityAttributes`, `ActivityConfiguration`, `DynamicIsland`, request/update/end, push, `supplementalActivityFamilies`) using `references/live-activities.md`.
1. Validate Smart Stack relevance (`TimelineEntryRelevance`, `relevance()` / `WidgetRelevance`, `RelevanceConfiguration`, push-based relevance) using `references/relevance-and-smart-stacks.md`.
1. Check the design and gallery presentation (glanceability, sizes, the don'ts, `configurationDisplayName`/`description`, the placeholder) using `references/design-and-gallery.md`.
1. Validate previews and the testing/debugging workflow (`#Preview(as:)`, WidgetKit developer mode, the reload budget) using `references/previews-and-testing.md`.
1. Validate platform-specific surfaces (visionOS spatial widgets, CarPlay, macOS menu bar, the availability map) using `references/platforms.md`.
1. Catch common mistakes using `references/anti-patterns.md`.

If doing partial work, load only the relevant reference files.


## Task-based routing

Match the user's goal to the read order. Load only what you need.

### "Create my first widget" / "show me a complete widget"
1. `references/fundamentals.md` - the extension, the widget bundle, the timeline lifecycle
2. `references/worked-example.md` - one widget built end to end (entry → provider → layout → links → tinting → animation → preview)
3. `references/timeline-provider.md` - `TimelineProvider`, entries, reload policy
4. `references/families-and-layout.md` - pick families, per-family layout
5. `references/previews-and-testing.md` - `#Preview(as:)` to iterate

### "Let the user configure my widget"
1. `references/configuration-and-intents.md` - `AppIntentConfiguration` + `WidgetConfigurationIntent`, dynamic options, defaults
2. `references/timeline-provider.md` - `AppIntentTimelineProvider` (the intent is the first argument)

### "Add a Lock Screen widget / watch complication"
1. `references/lock-screen-and-watch.md` - accessory families, `widgetLabel`, `AccessoryWidgetBackground`, gauges, ClockKit migration
2. `references/rendering-modes-and-tinting.md` - accessory widgets are always rendered in a tint mode

### "My widget looks wrong in tinted / dark / accented mode"
1. `references/rendering-modes-and-tinting.md` - `widgetRenderingMode`, `widgetAccentable`, `widgetAccentedRenderingMode`, the luminance-to-alpha trick, designing for the accent group
2. `references/lock-screen-and-watch.md` - the transparent `containerBackground` for accessory widgets

### "Add a button / toggle inside my widget"
1. `references/interactive-widgets.md` - `Button(intent:)` / `Toggle(intent:)`, the app-process boundary, App Group store, `reloadTimelines`, `invalidatableContent`
2. `references/configuration-and-intents.md` - `isDiscoverable = false` on helper intents

### "Add a Control Center control / Action button / Lock Screen control"
1. `references/controls.md` - `ControlWidget`, `ControlWidgetToggle` (`SetValueIntent`) vs `ControlWidgetButton` (`AppIntent`), value providers, `ControlCenter.shared.reloadControls`
2. `references/interactive-widgets.md` - the same app-process / shared-store rules apply

### "Build a Live Activity / Dynamic Island"
1. `references/live-activities.md` - `ActivityAttributes` / `ContentState`, `ActivityConfiguration`, `DynamicIsland` regions, request/update/end, staleness, push, `supplementalActivityFamilies`, the iOS-27 landscape Dynamic Island
2. `references/interactive-widgets.md` - `LiveActivityIntent` buttons

### "Keep my widget fresh from the server"
1. `references/timeline-provider.md` - reload policy, the reload budget, reload on app background
2. `references/relevance-and-smart-stacks.md` - push-updated widgets (`WidgetPushHandler`, iOS 26), and when a Live Activity is the right tool instead

### "Make my widget show up in the Smart Stack at the right time"
1. `references/relevance-and-smart-stacks.md` - `TimelineEntryRelevance`, `relevance()` + `WidgetRelevance`, `RelevanceConfiguration` (watchOS 26), `RelevantContext`

### "Fetch data / load images / use a database or location in my widget"
1. `references/data-and-networking.md` - App Group snapshot, `async` fetch in the provider, image downsampling, SwiftData/Core Data, `NSWidgetUsesLocation`
2. `references/timeline-provider.md` - where fetching fits in the lifecycle and the budget

### "Deep link / open my app from the widget"
1. `references/deep-linking-and-navigation.md` - `widgetURL` vs `Link`, per-family rules, `onOpenURL`, `OpenIntent`

### "Animate my widget / make values roll or transition"
1. `references/animations-and-transitions.md` - entry diffing, `contentTransition(.numericText)`, `.transition` + `.id`, `invalidatableContent`, what doesn't animate

### "Modernize an old widget / I'm seeing IntentConfiguration / ClockKit / PreviewProvider"
1. `references/migration-and-deprecations.md` - the old → new map, `CustomIntentMigratedAppIntent`, the ClockKit migrator, dual-path `#available`

### "Design my widget well / make it gallery-ready"
1. `references/design-and-gallery.md` - glanceable/personal/relevant, sizes & tap styles, the don'ts, the snapshot, the placeholder

### "Support visionOS / CarPlay / macOS / Apple Watch"
1. `references/platforms.md` - spatial widgets (`supportedMountingStyles`, `widgetTexture`, `levelOfDetail`), CarPlay, macOS menu bar, the availability map

### "My widget won't update / shows stale data / never appears"
1. `references/previews-and-testing.md` - the reload budget, WidgetKit developer mode, debugging
2. `references/anti-patterns.md` - the usual causes

### "I'm hitting build errors or rendering bugs"
1. `references/anti-patterns.md` - catches with before/after fixes


## Decision trees

Quick orientation when you know the task but not the right API.

### Which configuration should the widget use?

```
No user configuration, fixed behavior?
  -> StaticConfiguration(kind:provider:)

User picks parameters (account, city, repo)?
  -> AppIntentConfiguration(kind:intent:provider:) + WidgetConfigurationIntent   (iOS 17+)

Migrating an existing iOS 14-16 configurable widget?
  -> WidgetConfigurationIntent + CustomIntentMigratedAppIntent (keep intentClassName)
  -> or keep IntentConfiguration(kind:intent:provider:) with the legacy INIntent

Appears in the Smart Stack only when relevant (watchOS)?
  -> RelevanceConfiguration(kind:provider:)   (watchOS 26+)
```

### Which timeline provider?

```
StaticConfiguration?
  -> TimelineProvider           (placeholder / getSnapshot / getTimeline, completion-based)

AppIntentConfiguration?
  -> AppIntentTimelineProvider  (placeholder / snapshot(for:in:) / timeline(for:in:), async, intent FIRST)

RelevanceConfiguration (watchOS)?
  -> RelevanceEntriesProvider   (placeholder / relevance() / entry(configuration:context:), one entry per config)
```

### Which reload policy?

```
Next update time is known (countdown ends, event starts)?
  -> .after(date)

Entries cover a window and the next batch can be computed at the end?
  -> .atEnd

Content only changes from interaction / push, never on a schedule?
  -> .never   (then reload via WidgetCenter from an intent, app, or push)
```

### Which interactive element?

```
Inside a widget or Live Activity, runs an action?
  -> Button(intent:) with an AppIntent          (iOS 17+)

Inside a widget, binary on/off?
  -> Toggle(isOn:intent:) with an AppIntent      (iOS 17+)

Inside a Control Center control, binary on/off?
  -> ControlWidgetToggle(action:) with a SetValueIntent

Inside a Control Center control, runs an action / opens the app?
  -> ControlWidgetButton(action:) with an AppIntent (or OpenIntent to launch)
```

### Widget vs Live Activity vs Control?

```
Glanceable data on a schedule, lives on Home/Lock Screen?
  -> Widget (timeline)

Ongoing, time-bound event the user wants to watch live (delivery, game, workout)?
  -> Live Activity (ActivityKit) - NOT a fast-reloading widget

A quick action or state toggle from Control Center / Lock Screen / Action button?
  -> Control (ControlWidget)
```


## Core Instructions

- A widget runs in a **separate extension process**, not your app. It is **always SwiftUI**, even in a UIKit app. The system **archives your view and renders it later** - your code is not running while the widget is on screen. Share data with the app only through an **App Group** container (shared `UserDefaults(suiteName:)`, a shared file, or a shared `ModelContainer`/Core Data store) - never `UserDefaults.standard`, never in-memory singletons.
- **Never** make a widget interactive with a closure or `onTapGesture`. The only interactivity is `Button(intent:)` / `Toggle(intent:)` backed by an `AppIntent` (iOS 17+), plus `Link` / `widgetURL` for deep links. Anything else silently does nothing.
- **Always** mark the widget's background with `.containerBackground(for: .widget) { ... }` (iOS 17+). Without it the widget is blank in the gallery, can't be removed/relocated cleanly, and the system can't substitute the material background in Lock Screen / StandBy / tinted contexts. The container type is `ContainerBackgroundPlacement` (value `.widget`) - there is no `WidgetBackgroundPlacement`.
- **Never** do blocking or asynchronous work in `placeholder(in:)` - it must return synchronously with stand-in data. Do real fetching in `getSnapshot`/`getTimeline` (or the async `snapshot`/`timeline`). Use `.redacted(reason: .placeholder)` for the first-render stand-in.
- `getSnapshot` (and `snapshot(for:in:)`) is what the **widget gallery** shows - return realistic, populated sample data even when the user has none yet, never an empty/loading state.
- Treat timeline reloads as a **budgeted, opportunistic** resource, not a timer. The system gives roughly 40-70 reloads/day per widget and learns from viewing habits. **Never** assume `.after(date)` fires exactly on time. Provide multiple entries to cover a window, pick the policy that matches your data (`.atEnd` / `.after` / `.never`), and trigger a final `WidgetCenter.shared.reloadAllTimelines()` when the app **enters the background** if data changed.
- `TimelineReloadPolicy` is a **struct**; `.after(_:)` takes a **`Date`**, not a `TimeInterval`. `WidgetCenter.shared.reloadTimelines(ofKind:)` takes the widget's `kind` string - keep `kind` values as shared constants so the app and extension can't drift.
- For a configurable widget, use `AppIntentConfiguration` + a `WidgetConfigurationIntent` (iOS 17+) and an `AppIntentTimelineProvider` whose `snapshot`/`timeline` take the **intent as the first argument**. `WidgetConfigurationIntent` lives in the **AppIntents** module and needs **no** `perform()`. Provide sensible `@Parameter` defaults; never force the user to configure before the widget shows anything.
- **Never** write a *new* configurable widget with the legacy SiriKit path - `IntentConfiguration`, an `INIntent` from a `.intentdefinition` file, or `IntentTimelineProvider`. Since iOS 17 the modern path is App Intents (`AppIntentConfiguration` + `WidgetConfigurationIntent` + `AppIntentTimelineProvider`). Only keep the legacy types behind `#available` when deploying below iOS 17, and when migrating an existing one conform the new intent to `CustomIntentMigratedAppIntent` with the original `intentClassName` so saved configurations survive. Likewise build watch complications with WidgetKit (+ a `CLKComplicationWidgetMigrator`), not ClockKit, and previews with `#Preview(as:)`, not `PreviewProvider`. See `references/migration-and-deprecations.md`.
- Don't fetch data inside the widget view (no `AsyncImage`, no network at render time) - the view is an archived snapshot rendered later. Resolve data and **downsample images** during timeline generation and put them in the entry, prefer reading an App-Group snapshot the app wrote, and always complete the provider (fall back to last-good data on error). See `references/data-and-networking.md`.
- Switch on `@Environment(\.widgetFamily)` and design each supported family deliberately. List only the families you actually lay out in `supportedFamilies` - shipping a family you didn't design looks broken. Accessory families (`accessoryCircular` / `accessoryRectangular` / `accessoryInline`) are **iOS 16+**; `accessoryCorner` is **watchOS only**.
- Design for **every rendering mode**, not just full color. Read `@Environment(\.widgetRenderingMode)` (`.fullColor` / `.accented` / `.vibrant`); both `WidgetRenderingMode` and `WidgetAccentedRenderingMode` are **structs with type properties**, not enums. In `.accented` mode the system flattens your view into two tint groups by alpha - put foreground content in the accent group with `.widgetAccentable()`, and control how images flatten with `.widgetAccentedRenderingMode(.desaturated / .accented / .accentedDesaturated / .fullColor)` (the image modifier is **iOS 18+**).
- For a multicolor image or icon that the accent group would crush into a flat silhouette: on **iOS 18+** use `.widgetAccentedRenderingMode(.desaturated)` (the system maps luminance to alpha and recolors for you); on **iOS 17 and below** that modifier doesn't exist, so apply the manual `.luminanceToAlpha()` filter (bright pixels opaque, dark transparent) to preserve the shape's internal detail as a clean monochrome glyph - it also stays useful on iOS 18+ for hands-on control. Pair it with a soft gradient background and `.widgetAccentable()`. (See `references/rendering-modes-and-tinting.md`.)
- For an accessory/Lock Screen widget or watch complication that should let the watch face or wallpaper show through, give it an **empty** `.containerBackground(for: .widget) { }`. Omitting `containerBackground` entirely makes the system add an opaque default material instead of a transparent one.
- An interactive `AppIntent` runs **in the app's process** (the app is launched in the background if needed), not the widget extension - so it can write to the real data store. After it mutates data a widget displays, call `WidgetCenter.shared.reloadTimelines(ofKind:)` (or `reloadAllTimelines()`); for a control, call `ControlCenter.shared.reloadControls(ofKind:)`. Mark helper intents that only back a widget/control button with `static let isDiscoverable = false` so they don't pollute Shortcuts.
- In the **27 releases** (iOS 27): a widget button's write intent must run on `.main` (the widget extension has a **read-only** view of the shared store). Pin it with `static var allowedExecutionTargets: ExecutionTargets { .main }`, and pin display-only intents with `.widgetKitExtension`.
- A **Control** (`ControlWidget`, iOS 18; macOS/watchOS 26) uses `ControlWidgetToggle` with a **`SetValueIntent`** (its `value: Bool` is set by the system) or `ControlWidgetButton` with a plain `AppIntent` / `OpenIntent`. The status modifier is `controlWidgetStatus(_:)` - there is no `controlWidgetStatusText`. Provide a `previewValue` and an async `currentValue` in the value provider.
- A **Live Activity** is the right tool for an ongoing, time-bound event - not a widget that reloads every few seconds. Split immutable data into `ActivityAttributes` and the only-updatable half into the nested `ContentState: Codable, Hashable` (keep it under 4 KB). `ActivityConfiguration` and `DynamicIsland` live in **WidgetKit**; `Activity.request/update/end` and tokens live in **ActivityKit**. `staleDate` / `relevanceScore` are set on `ActivityContent.init`, not the configuration.
- Live Activities require `NSSupportsLiveActivities` = `YES` in the **app's** Info.plist; high-frequency push updates also need `NSSupportsLiveActivitiesFrequentUpdates`. Push-to-start uses `Activity.pushToStartToken` (iOS 17.2+) - it is **not** a `PushType` case. For mass-audience pushes use a broadcast `channel`; otherwise per-activity push tokens.
- **Never** put a `symbolEffect` animation in a Live Activity or widget - they aren't supported and silently no-op. Widget/Live Activity views are static snapshots; only `Text(_:style:)` timers/dates and the system's transition between timeline entries animate.
- `widgetAccentedRenderingMode` is **iOS 18+**; Controls are **iOS 18+** (macOS/watchOS **26+**); push-updated widgets (`WidgetPushHandler`) and `RelevanceConfiguration` are **iOS 26 / watchOS 26**; spatial-widget modifiers (`supportedMountingStyles`, `widgetTexture`, `levelOfDetail`) are **iOS/visionOS 26**; `systemExtraLargePortrait`, the landscape Dynamic Island (`isDynamicIslandLimitedInWidth`), and `allowedExecutionTargets` are part of the **27 releases**. Gate each behind the correct availability and call the WWDC 2026 cohort **"the 27 releases"**, not "iOS 19".
- Use the `#Preview(as:)` macro (iOS 17+) to iterate on widgets across families, color schemes, and rendering modes without running the host app; enable **WidgetKit developer mode** (Settings ▸ Developer) to lift the reload budget while iterating. The reload budget being exhausted - not a code bug - is the most common reason a widget "stops updating".


## Output Format

If the user asks for a review, organize findings by file. For each issue:

1. State the file and relevant line(s).
2. Name the anti-pattern being replaced.
3. Show a brief before/after code fix.

Skip files with no issues. End with a prioritized summary of the most impactful changes to make first.

If the user asks you to write or fix widget code, make the changes directly instead of returning a findings report.

Example output:

### CaffeineWidget.swift

**Line 14: `placeholder(in:)` does a synchronous disk fetch - placeholders must return instantly.**

```swift
// Before
func placeholder(in context: Context) -> Entry {
    Entry(date: .now, drinks: Store.shared.loadAllDrinks())   // blocks the render
}

// After
func placeholder(in context: Context) -> Entry {
    Entry(date: .now, drinks: .sample)   // synchronous stand-in; real data in getTimeline
}
```

**Line 41: interactive `onTapGesture` in a widget does nothing - use an App Intent.**

```swift
// Before
Image(systemName: "plus.circle").onTapGesture { addDrink() }

// After
Button(intent: AddDrinkIntent()) { Image(systemName: "plus.circle") }
// AddDrinkIntent.perform() writes to the App Group store, then:
// WidgetCenter.shared.reloadTimelines(ofKind: "CaffeineWidget")
```

### Summary

1. **Placeholder (high):** must be synchronous; move fetching to the timeline.
2. **Interactivity (high):** gestures don't work in widgets; back the tap with an `AppIntent`.

End of example.


## References

- `references/fundamentals.md` - the widget execution model: the extension process, app groups, `WidgetBundle`, the `Widget` protocol, the timeline lifecycle, `containerBackground`, content margins, deep linking, `kind`, and the "which surface" map.
- `references/timeline-provider.md` - `TimelineProvider` vs `AppIntentTimelineProvider`, `TimelineEntry`, `Timeline`, reload policies, the reload budget, `WidgetCenter` reloads, reload-on-background, `TimelineEntryRelevance`.
- `references/configuration-and-intents.md` - `StaticConfiguration`, `AppIntentConfiguration`, `WidgetConfigurationIntent`, dynamic options / entity parameters, `recommendations()`, defaults.
- `references/migration-and-deprecations.md` - the old → new map: SiriKit `.intentdefinition` / `IntentConfiguration` → App Intents, `IntentTimelineProvider` → `AppIntentTimelineProvider`, ClockKit → WidgetKit, `PreviewProvider` → `#Preview`, what's deprecated vs legacy-but-supported, `CustomIntentMigratedAppIntent`.
- `references/data-and-networking.md` - loading data for timelines: App Group snapshots, `async`/background `URLSession` fetches, image downsampling, SwiftData/Core Data in widgets, location, Lock Screen privacy.
- `references/families-and-layout.md` - `WidgetFamily` cases, sizing, `supportedFamilies`, content margins, the per-family switch, `ViewThatFits`, `ContainerRelativeShape`.
- `references/lock-screen-and-watch.md` - accessory families, watch complications, `widgetLabel`, `AccessoryWidgetBackground`, gauges, the transparent `containerBackground` trick, ClockKit → WidgetKit migration.
- `references/rendering-modes-and-tinting.md` - `widgetRenderingMode` (`.fullColor`/`.accented`/`.vibrant`), `widgetAccentable`, `widgetAccentedRenderingMode`, the luminance-to-alpha trick, designing for the tinted/clear Home Screen and accent groups.
- `references/interactive-widgets.md` - `Button(intent:)` / `Toggle(intent:)`, the app-process boundary, `@Parameter` persistence, the App Group store, `reloadTimelines`, the optimistic `ToggleStyle`, `invalidatableContent`, `isDiscoverable`, `allowedExecutionTargets` (the 27 releases).
- `references/deep-linking-and-navigation.md` - `widgetURL` vs `Link`, per-family tap rules, URL-scheme design, handling on the app side (`onOpenURL` / scene delegate), Live Activity `widgetURL`/`keylineTint`, control `OpenIntent`.
- `references/animations-and-transitions.md` - the entry-diffing animation model, `contentTransition(.numericText)`, `.transition` + `.id` identity, the optimistic `Toggle`, `invalidatableContent`, Live Activity transitions, what does not animate (`symbolEffect`, loops, video).
- `references/controls.md` - `ControlWidget`, `StaticControlConfiguration` / `AppIntentControlConfiguration`, `ControlWidgetToggle` (`SetValueIntent`) vs `ControlWidgetButton` (`AppIntent`/`OpenIntent`), value providers, `ControlCenter` reloads, status/action-hint modifiers, platforms.
- `references/live-activities.md` - `ActivityAttributes` / `ContentState`, `ActivityConfiguration`, `DynamicIsland`, `Activity.request/update/end`, `ActivityContent` staleness, push (token / channel / push-to-start), `supplementalActivityFamilies` / `activityFamily`, the landscape Dynamic Island, StandBy, `LiveActivityIntent`, entitlements.
- `references/relevance-and-smart-stacks.md` - `TimelineEntryRelevance`, `relevance()` + `WidgetRelevance` / `WidgetRelevanceAttribute` / `RelevantContext`, `RelevanceConfiguration` + `RelevanceEntriesProvider` (watchOS 26), push-updated widgets (`WidgetPushHandler`, iOS 26), Smart Stack behavior.
- `references/design-and-gallery.md` - the design rules (glanceable/relevant/personal, not a mini-app), sizes & tap styles, layout margins & type, the explicit don'ts, the gallery (`configurationDisplayName`/`description`/snapshot), the placeholder, personalization, Smart Stack etiquette.
- `references/previews-and-testing.md` - the `#Preview(as:)` macro variants, `WidgetPreviewContext`, testing rendering modes/families, WidgetKit developer mode, the reload budget, debugging "won't update".
- `references/platforms.md` - visionOS spatial widgets (`supportedMountingStyles`, `widgetTexture`, `levelOfDetail`, `systemExtraLargePortrait`), CarPlay widgets and Live Activities, macOS menu bar, watchOS, the cross-platform availability map.
- `references/worked-example.md` - one widget built end to end (a `systemMedium` Quick Actions widget): entry + provider, multi-`Link` layout, full-color-vs-tinted handling, an entry-driven `MeshGradient` animation, `contentMarginsDisabled`, and the preview - with pointers to the deeper reference for each step.
- `references/anti-patterns.md` - the consolidated smell → fix checklist, including the API-name confusions LLMs make (struct vs enum rendering modes, `ContainerBackgroundPlacement`, `pushToStartToken`, `controlWidgetStatus`).
