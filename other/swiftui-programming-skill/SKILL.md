---
name: SwiftUI Programming Skill
description: Use when work involves SwiftUI view composition, state and Observation ownership, navigation, adaptive layout, toolbars, forms, SF Symbols, accessibility, previews, or SwiftUI-specific performance. Do not use for UIKit/AppKit-only work, general Swift language questions, or architecture and performance work that does not involve SwiftUI.
---

# SwiftUI Programming Skill

Build SwiftUI interfaces that are correct for the user's declared platforms and deployment targets. Ask for those targets when an API choice depends on them; never assume the newest SDK is deployable.

## Supported baseline

The primary examples use Xcode 15, Swift 5.9, and iOS/iPadOS 17 or macOS 14. SwiftUI itself supports older systems, but newer APIs need explicit availability handling:

| Need | Preferred API | Minimum | Compatibility path |
|---|---|---|---|
| Stack navigation | `NavigationStack` | iOS 16, macOS 13, tvOS 16, watchOS 9 | `NavigationView` remains valid for earlier targets |
| Observation | `@Observable` | iOS 17, macOS 14, tvOS 17, watchOS 10 | `ObservableObject` and `@StateObject` remain supported |
| Toolbars | `.toolbar` | iOS 14, macOS 11, tvOS 14, watchOS 7 | Put controls in the view hierarchy on earlier targets |
| Modern change handling | zero- or two-parameter `onChange` | iOS 17, macOS 14, tvOS 17, watchOS 10 | Use the one-parameter overload on earlier targets |

APIs from the OS 27 development cycle are beta material relative to the stable Xcode 26.6 toolchain. Discuss them only when explicitly requested, label them beta, and provide stable fallbacks plus `#available` gates.

## Workflow

1. Record Swift, Xcode, and every platform minimum.
2. Choose semantic system controls before custom controls.
3. Define state ownership and a stable identity model.
4. Choose navigation and layout from capabilities, not device-name guesses.
5. Add accessibility and Dynamic Type while composing the view.
6. Compile at the oldest supported targets; test large accessibility sizes and relevant input methods.
7. Profile before adding performance-specific wrappers or caches.

## State and Observation

- Use `@State` for view-owned value state.
- For a view-owned `@Observable` reference, store it in `@State` so SwiftUI owns its lifetime.
- Pass an injected observable model as a plain property when the view only reads it. Create `@Bindable` locally when the view needs bindings.
- Use `@Environment` for dependencies intentionally shared through a subtree.
- Keep UI-observed mutable models on `@MainActor` unless their isolation is deliberately designed otherwise.
- Do not copy derived state into another mutable property. Prefer a computed property.

```swift
import Observation
import SwiftUI

@MainActor
@Observable
final class ProfileModel {
    var displayName = ""
}

struct ProfileEditor: View {
    @State private var model = ProfileModel()

    var body: some View {
        @Bindable var model = model
        TextField("Display name", text: $model.displayName)
    }
}
```

For iOS 16 and earlier, use `ObservableObject` with `@StateObject` for view ownership and `@ObservedObject` for injection. That is a compatibility decision, not an anti-pattern.

## Composition and layout

- Extract subviews around meaningful responsibility, reuse, or independent state—not to force a presumed redraw boundary.
- Prefer flexible frames, stacks, grids, `ViewThatFits`, and size classes. Use `GeometryReader` only when the child genuinely needs the proposed size.
- Respect safe areas unless the visual treatment deliberately extends under system UI.
- Use semantic colors and text styles; avoid fixed text heights and one-line truncation for user content.
- Treat iPad multitasking, macOS window resizing, tvOS focus, watchOS glanceability, and visionOS volumes as distinct capabilities.

## Navigation and toolbars

- Model destinations with stable, `Hashable` route data when navigation is state-driven.
- Prefer `NavigationStack` at its supported minimum. Use `NavigationSplitView` for genuinely multi-column interfaces, with a compact fallback.
- Keep destination construction consistent: every destination receives the selected value it requires.
- Use semantic toolbar placements such as `.primaryAction`, `.confirmationAction`, and `.cancellationAction` where they express intent across platforms.
- Do not use iOS-only placements or modifiers in an ungated all-platform view.

See [the complete toolbar example](examples/example_toolbar.swift) and [prompt scenarios](examples/prompts.md).

## Accessibility and Dynamic Type

- Prefer `Button`, `Toggle`, `TextField`, `Label`, and other semantic controls.
- Label icon-only controls with their purpose. Hints describe the result of an action, not the gesture.
- Keep separate interactive controls as separate accessibility elements.
- Use semantic fonts (`.body`, `.headline`) or `@ScaledMetric`; do not claim that a fixed `.system(size:)` font scales.
- Preserve alternatives to color, adequate interactive sizes and spacing, Reduce Motion, and Differentiate Without Color.

## Performance

- First measure with Instruments on a release build and representative hardware.
- Give collection elements stable IDs. Never use array offsets as identity for mutable collections.
- `List` already creates rows lazily. Use `ScrollView` plus `LazyVStack` for layout/interaction behavior that `List` cannot provide, not as a blanket speed upgrade.
- A parent body evaluation does not mean every descendant is redrawn on screen. Keep `body` inexpensive, but do not promise that extracting a view creates an independent render boundary.
- Use SwiftUI's `.equatable()` or `EquatableView` only after measurement and only when equality fully represents visible output.
- Cancel asynchronous work when its owning view disappears or its input changes. `.task(id:)` is usually the clearest view-lifetime tool.

## SF Symbols

- Verify each symbol exists for the deployment target and choose a fallback for newer symbols.
- Use rendering modes and symbol effects only at their documented availability.
- Give decorative symbols no separate accessibility focus; label icon-only controls at the control level.

## Copy-ready examples

- [State-driven toggle](examples/example_toggle.swift)
- [Navigation and semantic toolbar actions](examples/example_toolbar.swift)
- [Example prompts](examples/prompts.md)

When a requested example spans architecture, accessibility, performance, or platform-specific behavior, keep this skill focused on the SwiftUI layer and route the other concerns to their dedicated guidance.
