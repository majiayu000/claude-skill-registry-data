---
name: Cross-Platform App Development Skill
description: Use when one Swift/SwiftUI product intentionally targets two or more of iOS, iPadOS, Mac Catalyst, macOS, watchOS, tvOS, or visionOS and needs shared-domain design, adaptive UI, capability boundaries, navigation, input, scenes, storage, or conditional compilation. Do not use for a single-platform feature or for non-Apple cross-platform frameworks.
---

# Cross-Platform App Development Skill

Share product behavior and domain logic while preserving each platform's interaction model. “Compiles everywhere” is a starting point, not proof of a good multi-platform experience.

## Stable baseline

Primary examples use Xcode 15 and Swift 5.9 with these deployment targets:

- iOS/iPadOS/Mac Catalyst 17
- macOS 14
- watchOS 10
- tvOS 17
- visionOS 1

The same architecture can support older systems, but APIs must be checked and gated at the real minimum. `NavigationStack`, `NavigationSplitView`, and `ViewThatFits` begin with the iOS 16/macOS 13/tvOS 16/watchOS 9 generation; visionOS starts at 1.0. OS 27-cycle APIs are beta relative to stable Xcode 26.6 and require explicit user intent, beta labeling, a stable fallback, and availability checks.

## Start with a target matrix

Record this before generating code:

| Target | Minimum | Window model | Primary input | Navigation | Persistence/sync | Key capabilities |
|---|---:|---|---|---|---|---|
| iPhone/iPad | project-specific | scenes, multitasking | touch, pencil, keyboard | stack or split | local and/or cloud | cameras, sensors, share extensions |
| Mac Catalyst | project-specific | UIKit scenes/windows | pointer, keyboard | split/window-aware | iOS-compatible stores | Catalyst availability gaps |
| macOS | project-specific | multiwindow, documents, menus | pointer, keyboard | split, tables, windows | sandbox-aware | commands, files, services |
| watchOS | project-specific | glanceable scenes | touch, Crown, gestures | shallow stack | paired/cloud strategy | complications, workouts |
| tvOS | project-specific | full-screen scenes | focus, remote | focus-driven stack | cloud-first; local caches are purgeable | media playback |
| visionOS | project-specific | windows, volumes, immersive spaces | eyes, hands, pointer | spatially appropriate | local and/or cloud | ornaments, immersion |

Do not infer capability from screen width alone, and do not infer iPad from a regular size class. Windows resize, multitasking changes size classes, and macOS may report no horizontal size class.

## Architecture boundary

Prefer this dependency direction:

1. Shared domain models and pure business rules.
2. Shared protocols for capabilities such as sharing, file selection, haptics, or playback.
3. Platform implementations in their target modules.
4. SwiftUI features that consume capabilities through initializers or environment values.
5. Thin platform scenes, commands, menus, and lifecycle adapters.

Use a Swift package for truly shared code when its platform declarations and dependencies match every consumer. Keep UIKit, AppKit, WatchKit, TVUIKit, and RealityKit imports out of the shared domain target.

## Adaptation tools

Use them in this order:

1. Semantic SwiftUI controls that adapt automatically.
2. Flexible layout, `ViewThatFits`, grids, and environment values for runtime conditions.
3. Capability protocols when behavior differs but the feature contract is shared.
4. `#available` when an API differs by OS version.
5. `#if os(...)` or `#if targetEnvironment(macCatalyst)` only when code truly cannot compile for another target.

Compile-time checks cannot represent runtime states such as compact windows, pointer availability, Reduce Motion, or current scene phase.

See [the adaptive layout](examples/example_adaptive_layout.swift) and [platform-specific implementation](examples/example_platform_specific.swift).

## Navigation

- Use `NavigationSplitView` for iPad, Mac Catalyst, macOS, and visionOS experiences that genuinely have sidebar/content/detail structure.
- Let the split view collapse on compact iOS instead of maintaining a separate device-name branch when the workflow is the same.
- Use `NavigationStack` for watchOS, tvOS, and shallow or linear flows.
- Pass the selected value to the destination. Do not construct `DetailView()` when its initializer requires an item.
- Keep `.sidebar` and other platform-specific styles inside supported branches.
- Model routes and selections with stable `Hashable` values so deep links and restoration can be tested.

See [the complete adaptive navigation example](examples/example_adaptive_navigation.swift).

## Platform experience checklist

### iOS, iPadOS, and Catalyst

- Test rotation, Stage Manager, Split View, external keyboards, pointer use, drag and drop, and multiple scenes when supported.
- Treat Catalyst as its own target environment for availability and UX; an iPad layout is not automatically a Mac experience.

### macOS

- Design window sizes, commands, menus, keyboard shortcuts, focus, tables/inspectors, file access, sandboxing, and restoration.
- Prefer macOS scenes and commands over placing every action in an iOS-style toolbar.

### watchOS

- Keep tasks glanceable and navigation shallow. Test Digital Crown focus, Always On behavior, background limits, complications, and Watch Connectivity failure modes.

### tvOS

- Test Focus Engine movement and remote input on every screen. Avoid touch-only gestures and hover assumptions.
- Treat local files as a cache, not the sole durable copy of user data.

### visionOS

- Choose windows, volumes, and immersive spaces deliberately. Preserve comfort, accessibility, and a non-immersive route to essential tasks.

## State, storage, and sync

- Share domain state only when semantics match; keep presentation and navigation state local to each scene.
- Define the source of truth, offline behavior, merge policy, account changes, and conflict UX before sharing a store.
- Check each persistence framework and model feature on every target. “Swift code” does not imply identical framework availability.
- Use App Groups only for processes that need shared containers and configure entitlements per target.
- Test schema migration and downgrade/rollback scenarios with real prior stores.

## Input, focus, and accessibility

- Every essential action needs an appropriate path for touch, pointer, keyboard, focus engine, Digital Crown, and spatial input on its target.
- Use semantic controls so VoiceOver and other assistive technologies inherit roles and actions.
- Test Dynamic Type, focus order, reduced motion, contrast, and platform-specific accessibility features separately on each target.
- Do not hide platform-critical controls solely to maximize source sharing.

## Scenes, commands, and lifecycle

- Handle `scenePhase`, background work, restoration, and external events per target.
- Model macOS menus/commands and multiwindow behavior outside a phone-first root view.
- Keep watch complications, widgets, Live Activities, and spatial immersive scenes in target-specific modules with shared domain inputs.

## Validation matrix

For every supported target:

1. Compile at the declared minimum with warnings treated seriously.
2. Run unit tests for the shared domain package.
3. Run navigation and restoration tests for target-specific shells.
4. Exercise narrow and wide windows plus relevant input devices.
5. Test offline, sync conflict, background/foreground, memory pressure, and accessibility states.

Do not claim cross-platform readiness when only one SDK target compiled.

## Resources

- [Adaptive layout example](examples/example_adaptive_layout.swift)
- [Conditional platform implementation](examples/example_platform_specific.swift)
- [Adaptive navigation example](examples/example_adaptive_navigation.swift)
- [Cross-platform prompt scenarios](examples/prompts.md)
