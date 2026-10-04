---
name: mobile-navigation
category: mobile
description: Use when adding a screen, a tab, a deep link, or back-navigation handling - the per-stack navigation APIs, state preservation, auth-boundary resets, and how to verify a deep link actually opens the right screen.
---
# Mobile Navigation

## Overview

Navigation bugs rarely show up in a widget test — they show up as a stale back stack, a deep link that opens the wrong screen, or state from a previous session leaking past login. Use the platform's own navigation stack, not a hand-rolled one, and verify a deep link by actually following it, not by reading the routing table.

## Per-stack APIs

- **Flutter:** `go_router` (declarative routing — see `flutter-setup-declarative-routing` if the repo is adopting it) for stack + deep-link handling. `PopScope`, not the deprecated `WillPopScope`, to intercept back.
- **SwiftUI:** `NavigationStack(path:)` + `.navigationDestination(for:)` for a programmatic, type-safe stack; the `Tab` API for top-level tab navigation.
- **Compose:** Navigation 3 with type-safe routes; `NavigationSuiteScaffold` to switch a bottom nav bar to a nav rail at the ≥600dp breakpoint (see `android-compose-patterns`).

## Rules

- **Pass IDs, not whole objects,** through navigation params — the destination screen re-fetches or reads from the shared state/cache by ID. An object passed by reference goes stale the moment the source list refreshes.
- **Preserve per-tab state** across tab switches (scroll position, in-progress form) unless the task says otherwise — switching tabs is not meant to reset a screen.
- **Reset navigation state intentionally at auth boundaries:** after logout, clear every stack back to the entry point; after completing a flow (checkout, onboarding), pop back to where it makes sense to land, not back through the flow's own screens.
- **Stack navigators for drill-in flows, tab navigators for top-level sections.** Don't nest navigators deeper than the user can reason about (three levels is usually the practical ceiling).
- **Don't hide the tab bar on push on iOS** unless the task explicitly asks — losing the tab bar mid-flow disorients the user about where they are in the app.
- **Hardware/predictive back does what the visible back affordance does** — never let them diverge (see `android-compose-patterns`'s predictive-back section for why `onBackPressed` alone is no longer reliable at targetSdk 36).

## Verifying a deep link

Don't trust the routing table — follow the link on the device and look at what opened:

```
# Android
adb shell am start -W -a android.intent.action.VIEW -d "<uri>" <package>

# iOS simulator
xcrun simctl openurl booted "<uri>"
```

Then `mobile_screenshot` to confirm the right screen rendered with the right data, not just that nothing crashed.

## Common Mistakes

- Passing a full object (e.g. a `Task`) as a route argument instead of its ID.
- A tab switch that resets scroll position or an in-progress form.
- Logout leaving a previous user's screen reachable via back.
- `WillPopScope`/raw `onBackPressed` overrides that stop working once predictive back is the default.
- Claiming a deep link works from reading the route definition, without actually opening it on a device.

## Red Flags

- A navigation param typed as the full domain model instead of an ID.
- Back button behavior that differs from the system/predictive back gesture.
- A deep link task closed with no `adb`/`simctl` verification step in the diff or the closing message.
