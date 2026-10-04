---
name: macos-app-lifecycle-bridge
description: Use when a macOS AppKit or SwiftUI app needs lifecycle, activation, window, panel, menu/status-item, event-monitor, reopen, ownership, or teardown work.
license: "MIT"
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# macOS App Lifecycle Bridge

Define one owner for every AppKit resource and one decision point for every user-visible transition.

## Route the Work

1. Inspect the app entry point, delegate/adaptor, SwiftUI scenes, activation-policy changes, windows, panels, hosting, status items, menus, event monitors, reopen, and shutdown paths.
2. Choose a primary lifecycle: SwiftUI scenes with delegate-only integration, or an AppKit coordinator that retains controllers and hosts SwiftUI. Never let both own the same surface or command.
3. Read [ownership-and-transitions.md](references/ownership-and-transitions.md) to assign owners and model launch, headless, active/inactive, reopen, close, hide, and termination transitions.
4. Read [windows-menus-and-monitors.md](references/windows-menus-and-monitors.md) when implementing a window, panel, hosting shell, menu/status item, or event monitor.
5. If Xcode MCP is available, run `DocumentationSearch`; use [apple-documentation.md](references/apple-documentation.md) as the dated API index.

## Preserve These Invariants

- Keep lifecycle coordinators, AppKit resources, and their cleanup on the main actor.
- Give each persistent window identity, panel, status item, menu target, and monitor token one retained owner. Views request actions; SwiftUI recomputation must not recreate shells.
- Model activation policy, app activity, visibility, key/main status, and background readiness separately.
- Treat show, activate, make-key, order-front, close, and release as different operations.
- Make reopen, repeated show, start, stop, and teardown idempotent.
- Pair every observer, timer, task, delegate, callback, status item, and monitor with explicit cleanup; avoid owner/callback retain cycles.
- Local event monitors may alter this app's events; global monitors only observe other apps and may require Accessibility trust. Remove each token exactly once.
- Keep menu tracking bounded and perform expensive work before the menu opens.

## Complete the Task

Separate transition decisions from AppKit effects where tests benefit. Verify actual activation, focus, panel/menu behavior, repeated presentation, and teardown—not only compilation. Report the ownership graph, transition behavior, cleanup guarantees, and runtime evidence.

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

Scope/evidence: AppKit and SwiftUI lifecycle ownership, activation, windows, panels, menus, event monitors, reopen, and teardown guidance was checked with Xcode MCP `DocumentationSearch`.

[Apple documentation evidence](references/apple-documentation.md)
