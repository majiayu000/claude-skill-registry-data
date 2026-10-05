---
name: macos-development
description: Use when building or debugging a macOS app and the request involves — (1) AppKit/SwiftUI interop or modernizing AppKit code, (2) App Sandbox / file-access entitlement errors, especially "works in Xcode, fails in TestFlight", (3) menu bar commands, keyboard shortcuts, or a menu item stuck disabled, (4) multi-window scenes (WindowGroup, Window, MenuBarExtra, openWindow), (5) the Settings/Preferences scene, (6) ScreenCaptureKit screen recording or sharing, (7) SwiftUI-on-macOS behavior that differs from iOS (Table, Inspector, NavigationSplitView, focus), or (8) notarized Developer ID distribution outside the App Store.
---

# macOS Development

Platform mechanics for macOS apps — windows, menus, sandboxing, AppKit bridging,
ScreenCaptureKit, and where SwiftUI on macOS diverges from iOS. This complements
narrower macOS skills already in this profile: `macos-ci-recipes` (CI-only) and
`release-macos-spm-packaging` (SwiftPM scaffolding/build/packaging, no Xcode
project). For visual/HIG conventions ("does this look like a real Mac app"),
see the third-party `mac-assed-mac-app-skill` — that skill covers appearance,
this one covers the platform APIs underneath it.

Note the name collision with FlowDeck's own "macOS development" guide
(`resources/macos-development.md` in the `flowdeck` skill): that one is about
*driving* a running macOS app (clicks, keystrokes, accessibility automation —
see `flowdeck ui mac`), not the platform APIs a macOS app is built from. Same
name, different subject — for build/run/UI-automation tasks use `flowdeck`
directly rather than this skill.

## Agent behavior contract

1. Identify which of macOS's three structural differences from iOS is in play
   before proposing a fix: **multi-window** (state is per-scene, not global),
   **focus-driven** (the menu bar routes through the focused window, not a
   singleton), **keyboard-first** (every action needs a menu-bar path, not
   just a toolbar button). Most "this doesn't feel like a real Mac app" bugs
   trace back to one of these three.
2. Before recommending file access code, confirm whether the app is sandboxed
   (App Store) or Developer-ID direct-distributed — sandbox entitlements and
   security-scoped bookmarks only apply to the former, but debug builds don't
   sandbox by default either way, so "works in Xcode" proves nothing.
3. When bridging AppKit and SwiftUI, determine the host/guest direction first
   (which framework owns the view hierarchy) — the bridging type differs by
   direction, not just by "which framework's API do I need."
4. For distribution questions, first determine whether the project has an
   `.xcodeproj`/`.xcworkspace` or is pure SwiftPM — `release-macos-spm-packaging`
   already owns the SwiftPM scaffold/build/package/notarize pipeline end to
   end; only add net-new distribution guidance here (see
   `references/direct-distribution.md`) rather than duplicating it.
5. Prefer this skill's `references/` over recalling WWDC session content from
   memory — API availability and gotchas below are the source of truth.

## Triage template

- **Clarify the goal**: new feature, porting an iOS view to macOS, a crash/violation to diagnose, or a distribution/packaging question?
- **Collect minimal facts**: deployment target, sandboxed or Developer-ID direct-distributed, SwiftUI-only or mixing AppKit, Xcode project or SwiftPM.
- **Branch immediately**:
  - "works in Xcode, fails in TestFlight/release" → almost always sandbox (debug builds aren't sandboxed) — `references/sandbox-and-file-access.md`
  - menu item stays disabled / wrong window responds → focused-value routing — `references/menus-and-commands.md`
  - "feels like a ported iPad app" → `references/swiftui-differences.md`
  - Gatekeeper/notarization/codesign failure → `references/direct-distribution.md`

## Routing map

| Topic | Reference |
|---|---|
| WindowGroup, Window, UtilityWindow, MenuBarExtra, DocumentGroup, openWindow/dismissWindow, defaultSize | `references/windows.md` |
| Menu bar commands, CommandMenu/CommandGroup, keyboard shortcuts, context menus, focusedSceneValue routing | `references/menus-and-commands.md` |
| Table vs List, NavigationSplitView, Inspector, macOS focus/keyboard APIs, toolbars, SwiftUI-on-macOS gaps that force an AppKit escape hatch | `references/swiftui-differences.md` |
| The Settings scene (⌘,), tabbed preferences, SettingsLink, @AppStorage keys, iOS system-Settings adjacency | `references/settings.md` |
| App Sandbox model, `.fileImporter`/`NSOpenPanel`, security-scoped bookmarks, entitlements, sandbox-violation diagnosis | `references/sandbox-and-file-access.md` |
| Developer ID code signing, notarytool, packaging (dmg/zip/pkg), Sparkle auto-updates, Gatekeeper troubleshooting | `references/direct-distribution.md` |
| NSViewRepresentable/NSViewControllerRepresentable, NSHostingController/NSHostingView, `@Observable` in AppKit, NSHostingMenu, NSToolbar bridging | `references/appkit-interop.md` |
| Replacing `mouseDown` overrides, NSControl.Events, status-item expanded interface sessions, window state restoration, concentric corners/Liquid Glass, touch input | `references/appkit-modernization.md` |
| Screen recording/sharing/screenshots via ScreenCaptureKit, SCStream/SCContentFilter API surface | `references/screencapturekit.md` |

## Common errors → next best move

- **"Operation not permitted" / sandbox violation only outside Xcode** → `references/sandbox-and-file-access.md` (debug builds skip the sandbox)
- **Menu item permanently disabled** → `references/menus-and-commands.md` (missing `.focusedSceneValue` publisher)
- **`SCShareableContent` returns nothing** → `references/screencapturekit.md` (Screen Recording TCC not granted)
- **Notarization rejects with "hardened runtime" or "secure timestamp" error** → `references/direct-distribution.md`
- **`updateNSView` resets the caret / selection while typing** → `references/appkit-interop.md` (guard property writes; use `NSTextView.scrollableTextView()`)
- **Settings window compiles on macOS, fails on iOS** → `references/settings.md` (`Settings { }` needs `#if os(macOS)`)

## Out of scope, deliberately

Cross-platform SwiftUI fundamentals (state, navigation basics, animation),
Swift Concurrency, and Core Data/CloudKit aren't macOS-specific — use
`swiftui-expert-skill`, `swift-concurrency`, and `core-data-expert`
respectively. iOS screen recording is ReplayKit, not ScreenCaptureKit — not
covered here.
