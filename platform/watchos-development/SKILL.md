---
name: watchos-development
description: Use when building or reviewing a watchOS app or WatchKit extension — app structure and independent-app configuration, Watch Connectivity / companion-app sync, complications and Smart Stack widgets, controls or Live Activities on watch, background refresh and networking limits, watchOS-specific SwiftUI design conventions, or modernizing an older WatchKit/ClockKit project.
---

# watchOS Development

Guidance for building watchOS apps that behave the way the platform expects: independent by default, SwiftUI-first, glanceable, and resilient to a paired iPhone that may not be nearby.

## Agent behavior contract (follow these rules)

1. Determine the project's shape before proposing changes: watch-only, paired companion, or independent+companion. Default recommendation for new work is **independent + companion** — it's the only shape that degrades gracefully on Family Setup watches and unpaired watches.
2. Never let Watch Connectivity become the primary data path. It is an opportunistic optimization on top of a network/CloudKit fetch, not a substitute for one — see `references/watch-connectivity.md`.
3. Default new app entry points to the SwiftUI `App` protocol (`@main`, `WindowGroup`, `NavigationStack`) — see `references/platform-basics.md` for entry-point structure and `references/design-for-watchos.md` for how these primitives handle watchOS-specific navigation. Only add a `WKApplicationDelegate` via `@WKApplicationDelegateAdaptor` for the specific callbacks SwiftUI doesn't expose (workout recovery, Now Playing, extended runtime, remote-notification registration) — never as a precaution.
4. Route all networking through `URLSession`. Low-level networking (`NWConnection`, raw sockets, `URLSessionStreamTask`/`WebSocketTask`) is blocked by the OS on watchOS except for audio-streaming, VoIP+CallKit, and tvOS-pairing apps — see `references/background-and-networking.md`.
5. Every `WKRefreshBackgroundTask` (including `WKWatchConnectivityRefreshBackgroundTask` and `WKURLSessionRefreshBackgroundTask`) must reach `setTaskCompletedWithSnapshot(_:)` exactly once. Missing this drains the background budget and produces a delayed `SIGKILL` that looks unrelated to its cause.
6. When migrating ClockKit complications to WidgetKit, insist on migrating every complication in the same release. The instant one WidgetKit complication is offered, the system stops calling ClockKit entirely — a partial migration silently breaks the rest on every user's device.
7. For SwiftUI content, only cover what's genuinely different on watchOS (navigation primitives, toolbar placement, Always On, containerBackground). General SwiftUI state management, layout, and animation belong to the `swiftui-expert-skill` and `swiftui-liquid-glass` skills — don't re-explain those here.
8. For workouts and HealthKit specifics (HKWorkoutSession, HKLiveWorkoutBuilder, recovery), defer to the `healthkit` skill; this skill only covers how workout data affects Smart Stack suggestions.

## First 60 seconds (triage template)

- **Clarify the goal**: new feature, crash/bugfix, design review, or WatchKit/ClockKit migration?
- **Collect minimal facts**:
  - Project shape (watch-only / paired companion / independent+companion) and whether it's SwiftUI or still has storyboards
  - Deployment target and whether the watchOS 26 SDK / ARM64 submission gate (April 2026) applies
  - Is a paired iPhone assumed to be reachable, or must the app work standalone?
  - Exact crash signature or error, if debugging
- **Branch immediately**:
  - Background wake crash (`SIGKILL` after a refresh) → background-task completion audit — `references/background-and-networking.md` and/or `references/watch-connectivity.md`
  - Complication/widget not updating → check for a partial ClockKit→WidgetKit migration first — `references/modernization.md`
  - Data not arriving on watch → check Watch Connectivity is *not* the only path — `references/watch-connectivity.md`
  - Navigation/layout looks wrong → check the navigation primitive matches the content shape — `references/design-for-watchos.md`

## Routing map (pick the right reference fast)

- **App structure, independent apps, entry point, Info.plist keys, submission requirements, Foundation Models on watch** → `references/platform-basics.md`
- **Navigation (`TabView`/`NavigationSplitView`/`NavigationStack`), toolbar placement, `containerBackground`, Always On design** → `references/design-for-watchos.md`
- **Complications, Smart Stack widgets, RelevanceKit, configurable widgets, APNs widget push** → `references/smart-stack-and-complications.md`
- **Controls (Control Center / Action button / Double Tap), Live Activities on watch** → `references/controls-and-live-activities.md`
- **`WCSession`, paired-device data transfer, Family Setup, background-task completion for WC wakes** → `references/watch-connectivity.md`
- **Background tasks, `BGTaskScheduler`, URLSession background transfers, TN3135 networking limits** → `references/background-and-networking.md`
- **WatchKit storyboards → SwiftUI, dual-target → single-target, ClockKit → WidgetKit, watch-only → +companion** → `references/modernization.md`

## Common symptoms → next best move

- **`EXC_CRASH (SIGKILL)` shortly after a background wake** → `references/background-and-networking.md` and/or `references/watch-connectivity.md` (audit every `WKRefreshBackgroundTask` branch for a missing completion call)
- **`NWConnection` stuck in `.waiting` with `ENETDOWN`, works fine in the simulator** → `references/background-and-networking.md` (low-level networking is policy-blocked on device; switch to `URLSession`)
- **ClockKit complications silently stop updating after a release** → `references/modernization.md` (a WidgetKit complication was shipped without migrating the rest)
- **App shows empty/stale data on Family Setup or an unpaired watch** → `references/watch-connectivity.md` + `references/platform-basics.md` (Watch Connectivity was used as the primary path instead of URLSession/CloudKit)
- **Control doesn't appear in the watch controls gallery** → `references/controls-and-live-activities.md` (its intent likely foregrounds the iPhone app — watch placement filters those out)
- **Two Smart Stack cards for the same event** → `references/smart-stack-and-complications.md` (missing `associatedKind(_:)` between a timeline and a relevant widget)
- **Tabs never activate, or `NavigationSplitView` detail selection is stuck** → `references/design-for-watchos.md` (`List` unwraps `Optional` selection, `TabView` doesn't)
- **`'BGTaskScheduler' is unavailable in watchOS` compile error** → `references/background-and-networking.md` (needs the Xcode 27 SDK, even though the API is annotated back to watchOS 26)

## Reference files

- `references/platform-basics.md`
- `references/design-for-watchos.md`
- `references/smart-stack-and-complications.md`
- `references/controls-and-live-activities.md`
- `references/watch-connectivity.md`
- `references/background-and-networking.md`
- `references/modernization.md`

Source: [CharlesWiltgen/Axiom](https://github.com/CharlesWiltgen/Axiom) (axiom-watchos discipline skill), adapted — not copied verbatim.
