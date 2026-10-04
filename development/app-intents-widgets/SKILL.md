---
name: app-intents-widgets
description: Design, implement, debug, and verify stable App Intents and WidgetKit integrations, including AppIntent, AppEntity, AppEnum, entity queries, AppShortcutsProvider, dependency injection, shared extension data, widget timelines, relevance, controls, Live Activity selection, deep links, handoff, confirmation, and privacy. Use when exposing app actions to Siri or Shortcuts, building configurable or interactive widgets, sharing state with extensions, or choosing the correct system surface for an action. Do not use for ordinary in-app buttons, generic SwiftUI layout, background scheduling without a widget or intent, SiriKit-only legacy work with no migration request, or Live Activity push-server implementation as the sole task.
---

# App Intents and Widgets

Expose a thin, testable capability to the system, then add only the surfaces that improve the user journey. Intents execute outside ordinary screen assumptions; widgets render system-scheduled snapshots rather than miniature apps.

## Inspect targets and versions first

Do not write an intent or widget before identifying the executable targets, deployment floors, and shared capabilities.

```bash
xcodebuild -version
xcrun swiftc --version
xcodebuild -list -project App.xcodeproj
xcodebuild -showBuildSettings -project App.xcodeproj -target App \
  | rg 'PRODUCT_BUNDLE_IDENTIFIER|APPLICATION_EXTENSION_API_ONLY|IPHONEOS_DEPLOYMENT_TARGET|MACOSX_DEPLOYMENT_TARGET|SWIFT_VERSION'
rg --files | rg '\.(entitlements|plist)$|Widget|Intent|Activity'
rg -n 'AppIntent|AppEntity|AppEnum|Entity(Query|StringQuery)|AppShortcutsProvider|TimelineProvider|ControlWidget|ActivityAttributes|onOpenURL|NSUserActivity'
```

Record the app, widget extension, shared framework/package, and test targets separately. Verify App Group and other entitlements in every executable that needs them. Read [architecture, execution, and privacy](references/architecture-and-privacy.md) before introducing shared state.

## Select the stable surface

| User need | Stable surface | Minimum commonly relevant OS |
|---|---|---|
| Run an app action from Siri/Shortcuts/system UI | `AppIntent` | iOS 16 |
| Resolve app-owned content | `AppEntity` + `EntityQuery`/`EntityStringQuery` | iOS 16 |
| Offer a finite semantic choice | `AppEnum` | iOS 16 |
| Ship zero-setup phrases for core actions | `AppShortcutsProvider` | iOS 16 |
| Show scheduled glanceable snapshots | WidgetKit timeline widget | iOS 14 |
| Let the user configure a widget with App Intents | `AppIntentConfiguration` | iOS 17 |
| Add buttons/toggles to a widget | Interactive widget intent | iOS 17 |
| Offer a discrete or boolean system control | `ControlWidget` | iOS 18 |
| Display an ongoing, time-bounded event | ActivityKit Live Activity | iOS 16.1 |

Use the minimum that satisfies the request. A widget is not required for an App Shortcut, a configuration intent is not required for an interactive button, and a Live Activity is not a general background refresh mechanism. Read [widgets and system-surface selection](references/widgets-and-system-surfaces.md) for the full decision flow.

## Build the intent layer from stable primitives

1. Define a Sendable domain command/result in shared code.
2. Keep storage, networking, and policy in an injected service or actor.
3. Create a small `AppEntity` projection with a stable persistent ID and only system-relevant fields.
4. Resolve IDs in `EntityQuery`; return a bounded, relevant suggestion set.
5. Use `EntityStringQuery` only when text search adds value.
6. Use `AppEnum` for small fixed choices, not database records.
7. Make `perform()` validate, authorize, call one use case, and translate the result/dialog.
8. Add 3–5 high-value App Shortcuts with natural phrases containing `\(.applicationName)`.

Do not make a persistence model conform to `AppEntity` merely to reduce code. The entity is a system-facing value projection; the query rehydrates current data by ID.

Use [the stable App Intents example](examples/AppIntentsExample.swift) for compile-checked syntax.

## Inject dependencies deliberately

Register Sendable dependencies with `AppDependencyManager` in every executable context that can run the intent, then use `@Dependency` in the intent/query. Prefer actors or immutable Sendable services. Do not reach through a global UI singleton or construct a production database inside `perform()`.

The app and widget extension are separate processes. Share durable values through an App Group container or another supported cross-process store; dependency injection alone does not share in-memory state. Make the shared schema/version explicit, protect sensitive files, and tolerate missing or stale data.

## Define execution, confirmation, and privacy

- Use the least permissive `authenticationPolicy` that matches the action and exposed data.
- `requiresAuthentication` can accept authentication on the originating trusted device; use `requiresLocalDeviceAuthentication` when protected data or services require the device executing the intent to be unlocked.
- Request confirmation before destructive, expensive, externally visible, or difficult-to-reverse actions.
- Revalidate authorization and current state inside `perform()`; a resolved entity can become stale.
- Return the minimum result/dialog needed. Do not leak secrets through entity display representations, suggestions, widget snapshots, or lock-screen surfaces.
- Keep background execution independent of UIApplication/UI state.
- On an iOS 26 deployment, use stable `supportedModes` to describe background/foreground behavior. For older deployment floors, preserve the supported pre-26 path and test both rather than assuming a runtime availability check changes protocol metadata.

Confirmation is not a substitute for authorization. Authentication policy is not a substitute for checking whether the current account may mutate the selected object.

## Design the continuation path

When the action needs richer UI, return or invoke a stable app route rather than duplicating the workflow in an intent or widget.

- Give every entity/action a stable URL or route identifier where appropriate.
- Handle the route in the app's `onOpenURL`, scene routing, or equivalent coordinator.
- Donate `NSUserActivity` for handoff/current-content continuity when another device or system experience should resume the same context.
- Preserve a fallback that opens the app to a safe landing page when the entity no longer exists, the user is signed out, or the requested feature is unavailable.
- Never encode credentials or private payloads in a URL.

## Build widgets as snapshots

Create timeline entries that already contain everything the SwiftUI view needs. Perform reads/network work in the provider or main app, never in widget `body`. Return placeholder, snapshot, and timeline content quickly, and let WidgetKit schedule reloads. Call `WidgetCenter` reload APIs only after meaningful app-driven data changes; repeated reload requests are not guaranteed refresh timers.

Use an App Group for shared files/defaults/databases and configure it in both targets. Version shared data and handle a fresh/missing container. See [the stable timeline example](examples/WidgetTimelineExample.swift).

Treat entity display representations, suggestions, and widget snapshots as system-visible or cacheable metadata. Use a deliberately safe alias when names are private, keep placeholders generic, and mark sensitive widget content with SwiftUI privacy/redaction behavior appropriate to the supported families.

Use relevance only when time, location, or activity context genuinely predicts usefulness. Use a Control Widget only for a fast discrete/boolean action with a reliable current value and fallback. Use a Live Activity only for an ongoing event with a clear start, changing state, and end; always provide stale/end behavior. Do not add all three surfaces by default.

## Verify system behavior

Compile the shared types in every consuming target. Test direct intent execution with injected fakes, then test Shortcuts discovery, suggested entities, authentication, confirmation, cancellation, and stale IDs on device.

For widgets, test placeholder/snapshot/timeline generation, every supported family, missing shared data, app-driven reload, offline state, and actual-device scheduling. For controls and Live Activities, test only on supported OS/device surfaces and verify a stable fallback.

## OS 27 beta boundary

Stable Xcode 26.6 is the compilation source of truth for this skill. Treat OS 27-cycle App Intents schemas, testing frameworks, or other new symbols as beta. Do not mix their declarations into stable examples. Read [the OS 27 beta boundary](references/os-27-beta-boundary.md) before responding to an explicit beta request.

## Resources

- [Architecture, execution, and privacy](references/architecture-and-privacy.md)
- [Widgets and system-surface selection](references/widgets-and-system-surfaces.md)
- [OS 27 beta boundary and stable fallbacks](references/os-27-beta-boundary.md)
- [Stable App Intents example](examples/AppIntentsExample.swift)
- [Stable WidgetKit timeline example](examples/WidgetTimelineExample.swift)
- [Positive and negative prompt scenarios](examples/prompts.md)
