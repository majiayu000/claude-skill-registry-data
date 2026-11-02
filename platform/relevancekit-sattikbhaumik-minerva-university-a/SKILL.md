---
name: relevancekit
description: "Increase widget visibility on Apple Watch using RelevanceKit. Use when providing contextual relevance signals for watchOS widgets, declaring time-based or location-based relevance, combining multiple relevance providers, or helping the system surface the right widget at the right time on watchOS 26."
---

# RelevanceKit

Provide on-device contextual clues that increase a widget's visibility in the
Smart Stack on Apple Watch. RelevanceKit tells the system *when* a widget is
relevant -- by time, location, fitness state, sleep schedule, or connected
hardware -- so the Smart Stack can surface the right widget at the right moment.
Targets Swift 6.3 / watchOS 26+.

> **Beta-sensitive.** RelevanceKit shipped with watchOS 26. Re-check Apple
> documentation before making strong claims about API availability or behavior.

See [references/relevancekit-patterns.md](references/relevancekit-patterns.md) for complete code patterns including
relevant widgets, timeline provider integration, grouping, previews, and
permission handling.

## Contents

- [Overview](#overview)
- [Setup](#setup)
- [Relevance Providers](#relevance-providers)
- [Time-Based Relevance](#time-based-relevance)
- [Location-Based Relevance](#location-based-relevance)
- [Fitness and Sleep Relevance](#fitness-and-sleep-relevance)
- [Hardware Relevance](#hardware-relevance)
- [Combining Signals](#combining-signals)
- [Widget Integration](#widget-integration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Overview

watchOS uses two mechanisms to determine widget relevance in the Smart Stack:

1. **Timeline provider relevance** -- implement `relevance()` on an existing
   `AppIntentTimelineProvider` to attach `RelevantContext` clues to timeline
   entries. Available across platforms; only watchOS acts on the data.
2. **Relevant widget** -- use `RelevanceConfiguration` with a
   `RelevanceEntriesProvider` to build a widget driven entirely by relevance
   clues. The system creates individual Smart Stack cards per relevant entry.
   watchOS 26+ only.

Choose a timeline provider when the widget always has data to show and relevance
is supplementary. Choose a relevant widget when the widget should *only* appear
when conditions match, or when multiple cards should appear simultaneously (e.g.,
several upcoming calendar events).

### Key Types

| Type | Module | Role |
|---|---|---|
| `RelevantContext` | RelevanceKit | A contextual clue (date, location, fitness, sleep, hardware) |
| `WidgetRelevance` | WidgetKit | Collection of relevance attributes for a widget kind |
| `WidgetRelevanceAttribute` | WidgetKit | Pairs a widget configuration with a `RelevantContext` |
| `WidgetRelevanceGroup` | WidgetKit | Controls grouping behavior in the Smart Stack |
| `RelevanceConfiguration` | WidgetKit | Widget configuration driven by relevance clues (watchOS 26+) |
| `RelevanceEntriesProvider` | WidgetKit | Provides entries for a relevance-configured widget (watchOS 26+) |
| `RelevanceEntry` | WidgetKit | Data needed to render one relevant widget card (watchOS 26+) |

## Setup

### Import

```swift
import RelevanceKit
import WidgetKit
```

### Platform Availability

`RelevantContext` is declared across platforms (iOS 17+, watchOS 10+), but
**RelevanceKit functionality only takes effect on watchOS**. Calling the API on
other platforms has no effect. `RelevanceConfiguration`, `RelevanceEntriesProvider`,
and `RelevanceEntry` are watchOS 26+ only.

### Permissions

Certain relevance clues require the user to grant permission to both the app
and the widget extension:

| Clue | Required Permission |
|---|---|
| `.location(inferred:)` | Location access |
| `.location(_:)` (CLRegion) | Location access |
| `.location(category:)` | Location access |
| `.fitness(_:)` | HealthKit workout/activity rings permission |
| `.sleep(_:)` | HealthKit `sleepAnalysis` permission |
| `.hardware(headphones:)` | None |
| `.date(...)` | None |

Request permissions in both the main app target and the widget extension target.

## Relevance Providers

### Option 1: Timeline Provider with Relevance

Add a `relevance()` method to an existing `AppIntentTimelineProvider`. This
approach shares code across iOS and watchOS while adding watchOS Smart Stack
intelligence.

```swift
struct MyProvider: AppIntentTimelineProvider {
    // ... snapshot, timeline, placeholder ...

    func relevance() async -> WidgetRelevance<MyWidgetIntent> {
        let attributes = events.map { event in
            let context = RelevantContext.date(
                from: event.startDate,
                to: event.endDate
            )
            return WidgetRelevanceAttribute(
                configuration: MyWidgetIntent(event: event),
                context: context
            )
        }
        return WidgetRelevance(attributes)
    }
}
```

### Option 2: RelevanceEntriesProvider (watchOS 26+)

Build a widget that only appears when conditions match. The system calls
`relevance()` to learn *when* the widget matters, then calls `entry()` with
the matching configuration to get render data.

```swift
struct MyRelevanceProvider: RelevanceEntriesProvider {
    func relevance() async -> WidgetRelevance<MyWidgetIntent> {
        let attributes = events.map { event in
            WidgetRelevanceAttribute(
                configuration: MyWidgetIntent(event: event),
                context: RelevantContext.date(event.date, kind: .scheduled)
            )
        }
        return WidgetRelevance(attributes)
    }

    func entry(
        configuration: MyWidgetIntent,
        context: Context
    ) async throws -> MyRelevanceEntry {
        if context.isPreview {
            return .preview
        }
        return MyRelevanceEntry(event: configuration.event)
    }

    func placeholder(context: Context) -> MyRelevanceEntry {
        .placeholder
    }
}
```

## Time-Based Relevance

Time clues tell the system a widget matters at or around a specific moment.

### Single Date

```swift
RelevantContext.date(eventDate)
```

### Date with Kind

`DateKind` provides an additional hint about the nature of the time relevance:

| Kind | Use |
|---|---|
| `.default` | General time relevance |
| `.scheduled` | A scheduled event (meeting, flight) |
| `.informational` | Information relevant around a time (weather forecast) |

```swift
RelevantContext.date(meetingStart, kind: .scheduled)
```

### Date Range

```swift
// Using from/to
RelevantContext.date(from: startDate, to: endDate)

// Using DateInterval
RelevantContext.date(interval: dateInterval, kind: .scheduled)

// Using ClosedRange
RelevantContext.date(range: startDate...endDate, kind: .default)
```

## Location-Based Relevance

### Inferred Locations

The system infers certain locations from a person's routine. No coordinates
needed.

```swift
RelevantContext.location(inferred: .home)
RelevantContext.location(inferred: .work)
RelevantContext.location(inferred: .school)
RelevantContext.location(inferred: .commute)
```

Requires location permission in both the app and widget extension.

### Specific Region

```swift
import CoreLocation

let region = CLCircularRegion(
    center: CLLocationCoordinate2D(latitude: 37.3349, longitude: -122.0090),
    radius: 500,
    identifier: "apple-park"
)
RelevantContext.location(region)
```

### Point-of-Interest Category (watchOS 26+)

Indicate relevance near any location of a given category. Returns `nil` if the
category is unsupported.

```swift
import MapKit

if let context = RelevantContext.location(category: .beach) {
    // Widget is relevant whenever the person is near a beach
}
```

## Fitness and Sleep Relevance

### Fitness

```swift
// Relevant when activity rings are incomplete
RelevantContext.fitness(.activityRingsIncomplete)

// Relevant during an active workout
RelevantContext.fitness(.workoutActive)
```

Requires HealthKit workout/activity permission.

### Sleep

```swift
// Relevant around bedtime
RelevantContext.sleep(.bedtime)

// Relevant around wakeup
RelevantContext.sleep(.wakeup)
```

Requires HealthKit `sleepAnalysis` permission.

## Hardware Relevance

```swift
// Relevant when headphones are connected
RelevantContext.hardware(headphones: .connected)
```

No special permission required.

## Combining Signals

Return multiple `WidgetRelevanceAttribute` values in the `WidgetRelevance`
array to make a widget relevant under several different conditions.

```swift
func relevance() async -> WidgetRelevance<MyIntent> {
    var attributes: [WidgetRelevanceAttribute<MyIntent>] = []

    // Relevant during morning commute
    attributes.append(
        WidgetRelevanceAttribute(
            configuration: MyIntent(mode: .commute),
            context: .location(inferred: .commute)
        )
    )

    // Relevant at work
    attributes.append(
        WidgetRelevanceAttribute(
            configuration: MyIntent(mode: .work),
            context: .location(inferred: .work)
        )
    )

    // Relevant around a scheduled event
    for event in upcomingEvents {
        attributes.append(
            WidgetRelevanceAttribute(
                configuration: MyIntent(eventID: event.id),
                context: .date(event.date, kind: .scheduled)
            )
        )
    }

    return WidgetRelevance(attributes)
}
```

**Order matters.** Return relevance attributes ordered by priority. The system
may use only a subset of the provided relevances.

## Widget Integration

### Relevant Widget with RelevanceConfiguration

```swift
@available(watchOS 26, *)
struct MyRelevantWidget: Widget {
    var body: some WidgetConfiguration {
        RelevanceConfiguration(
            kind: "com.example.relevant-events",
            provider: MyRelevanceProvider()
        ) { entry in
            EventWidgetView(entry: entry)
        }
        .configurationDisplayName("Events")
        .description("Shows upcoming events when relevant")
    }
}
```

### Associating with a Timeline Widget

When both a timeline widget and a relevant widget show the same data, use
`associatedKind` to prevent duplicate cards. The system replaces the timeline
widget card with relevant widget cards when they are suggested.

```swift
RelevanceConfiguration(
    kind: "com.example.relevant-events",
    provider: MyRelevanceProvider()
) { entry in
    EventWidgetView(entry: entry)
}
.associatedKind("com.example.timeline-events")
```

### Grouping

`WidgetRelevanceGroup` controls how the system groups widgets in the Smart Stack.

```swift
// Opt out of default per-app grouping so each card appears independently
WidgetRelevanceAttribute(
    configuration: intent,
    group: .ungrouped
)

// Named group -- only one widget from the group appears at a time
WidgetRelevanceAttribute(
    configuration: intent,
    group: .named("weather-alerts")
)

// Default system grouping
WidgetRelevanceAttribute(
    configuration: intent,
    group: .automatic
)
```

### RelevantIntent (Timeline Provider Path)

When using a timeline provider, also update `RelevantIntentManager` so the
system has relevance data between timeline refreshes.

```swift
import AppIntents

func updateRelevantIntents() async {
    let intents = events.map { event in
        RelevantIntent(
            MyWidgetIntent(event: event),
            widgetKind: "com.example.events",
            relevance: RelevantContext.date(from: event.start, to: event.end)
        )
    }
    try? await RelevantIntentManager.shared.updateRelevantIntents(intents)
}
```

Call this whenever relevance data changes -- not only during timeline refreshes.

### Previewing Relevant Widgets

Use Xcode previews to verify appearance without simulating real conditions.

```swift
// Preview with sample entries
#Preview("Events", widget: MyRelevantWidget.self, relevanceEntries: {
    [EventEntry(event: .surfing), EventEntry(event: .meditation)]
})

// Preview with relevance configurations
#Preview("Relevance", widget: MyRelevantWidget.self, relevance: {
    WidgetRelevance([
        WidgetRelevanceAttribute(configuration: MyIntent(event: .surfing),
                                 context: .date(Date(), kind: .scheduled))
    ])
})

// Preview with the full provider
#Preview("Provider", widget: MyRelevantWidget.self,
         relevanceProvider: MyRelevanceProvider())
```

### Testing

Enable **WidgetKit Developer Mode** in Settings > Developer on the watch to
bypass Smart Stack rotation limits during development.

## Common Mistakes

- **Ignoring return order.** The system may only use a subset of relevance
  attributes. Return them sorted by priority (most important first).
- **Missing permissions in widget extension.** Location, fitness, and sleep
  clues require permission in *both* the app and the widget extension. If only
  the app has permission, the clues are silently ignored.
- **Using RelevanceKit API expecting iOS behavior.** The API compiles on all
  platforms but only has effect on watchOS.
- **Duplicate Smart Stack cards.** When offering both a timeline widget and a
  relevant widget for the same data, use `.associatedKind(_:)` to prevent
  duplication.
- **Forgetting placeholder and preview entries.** `RelevanceEntriesProvider`
  requires both `placeholder(context:)` and a preview branch in
  `entry(configuration:context:)` when `context.isPreview` is true.
- **Not calling `updateRelevantIntents`.** When using timeline providers,
  calling this only inside `timeline()` means the system has stale relevance
  data between refreshes. Update whenever data changes.
- **Ignoring nil from `location(category:)`.** This factory returns an optional.
  Not all `MKPointOfInterestCategory` values are supported.

## Review Checklist

- [ ] `import RelevanceKit` is present alongside `import WidgetKit`
- [ ] `RelevantContext` clues match the app's actual data model
- [ ] Relevance attributes are ordered by priority
- [ ] Permissions requested in both app target and widget extension for location/fitness/sleep clues
- [ ] `RelevanceEntriesProvider` implements `entry`, `placeholder`, and `relevance`
- [ ] `context.isPreview` handled in `entry(configuration:context:)` to return preview data
- [ ] `.associatedKind(_:)` used when a timeline widget and relevant widget show the same data
- [ ] `RelevantIntentManager.updateRelevantIntents` called when data changes (timeline provider path)
- [ ] `location(category:)` nil return handled
- [ ] WidgetKit Developer Mode used for testing
- [ ] Widget previews verify appearance across display sizes

## References

- [references/relevancekit-patterns.md](references/relevancekit-patterns.md) -- extended patterns, full provider
  implementations, permission handling, and grouping strategies
- [RelevanceKit documentation](https://sosumi.ai/documentation/relevancekit)
- [RelevantContext](https://sosumi.ai/documentation/relevancekit/relevantcontext)
- [Increasing the visibility of widgets in Smart Stacks](https://sosumi.ai/documentation/widgetkit/widget-suggestions-in-smart-stacks)
- [RelevanceConfiguration](https://sosumi.ai/documentation/widgetkit/relevanceconfiguration)
- [RelevanceEntriesProvider](https://sosumi.ai/documentation/widgetkit/relevanceentriesprovider)
- [What's new in watchOS 26 (WWDC25 session 334)](https://sosumi.ai/videos/play/wwdc2025/334/)
