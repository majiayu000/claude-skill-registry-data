---
name: swiftui-expert
description: This skill should be used when the user is building, reviewing, or debugging SwiftUI views and apps. Detects iOS and Swift version from the project. Covers creating views, state management with @Observable, NavigationStack routing, animations, accessibility, performance optimization, Liquid Glass adoption, design systems, and clean code architecture. Use when the user asks things like "create a SwiftUI list view", "my @State isn't updating", "add navigation to my app", "make this accessible", "optimize SwiftUI performance", "add Liquid Glass to my toolbar", "fix my Swift concurrency warning", "set up SwiftData models", "critique my SwiftUI code", "fix my SwiftUI layout", "create a custom ViewModifier", or "add Dark Mode support".
---

# SwiftUI Expert

Provide expert guidance on SwiftUI development. Detect the project's deployment target and Swift version from `Package.swift`, `.xcodeproj`, or project settings and adapt guidance accordingly. Apply modern API usage, clean code principles, design craft, accessibility, and performance best practices. Do not invent APIs — if unsure, say so.

## Core Principles

- Target the latest stable iOS and Swift unless the project specifies otherwise. Check the deployment target before suggesting version-gated APIs.
- Prefer SwiftUI-native solutions. Avoid UIKit unless explicitly needed or for gaps SwiftUI cannot fill.
- Do not introduce third-party frameworks without asking first.
- Each type (struct, class, enum) belongs in its own file. Flag files with multiple type definitions.
- Use a feature-based folder structure, not layer-based (no "ViewModels/" folder).
- Code must adhere to Apple's Human Interface Guidelines.

## Modern API — Always Use

Replace deprecated API immediately. See `references/modern-api.md` for the complete table.

Key replacements:
- `foregroundStyle()` not `foregroundColor()`
- `clipShape(.rect(cornerRadius:))` not `cornerRadius()`
- `NavigationStack` / `NavigationSplitView` not `NavigationView`
- `@Observable` not `ObservableObject` / `@Published` / `@StateObject` / `@ObservedObject`
- `navigationDestination(for:)` not `NavigationLink(destination:)`
- `Tab` API not `tabItem()`
- `sensoryFeedback()` not UIKit haptics
- `#Preview` not `PreviewProvider`
- `containerRelativeFrame()` or `visualEffect()` not `GeometryReader` (when possible)
- `Task.sleep(for:)` not `Task.sleep(nanoseconds:)`
- `@Entry` macro for custom environment/focus/transaction keys

## State Management

- `@State` must be `private`. It is owned by the view that creates it.
- `@Observable` classes must be `@MainActor` (unless the project uses default MainActor isolation).
- Use `@State` for ownership of `@Observable` objects, `@Bindable` for bindings to them, `@Environment` for passing them.
- Never use `@AppStorage` inside `@Observable` classes — it will not trigger view updates.
- Never create `Binding(get:set:)` in body — use `@State` + `onChange()`.
- Nested `@Observable` works fine. Nested `ObservableObject` does not propagate changes.
- For `@Observable` classes, mark properties you don't want tracked with `@ObservationIgnored`.

See `references/state-data.md` for property wrapper decision flowchart and SwiftData rules.

## View Composition & Clean Code

- Strongly prefer extracting subviews into separate `View` structs over computed properties or methods returning `some View`. Computed properties get no re-evaluation isolation from `@Observable` — separate structs allow SwiftUI to skip unchanged subviews entirely.
- Keep `body` short and computation-free. No sorting, filtering, or formatter creation in `body`.
- Extract button actions into methods. No inline business logic in `task()`, `onAppear()`, or `body`.
- Apply DRY: repeated styling → `ViewModifier`. Repeated layout → extracted `View`. Repeated logic → model/service method.
- Apply Single Responsibility: each view does one thing. Each model owns one domain. Each file contains one type.
- Apply Open/Closed: extend behavior through protocols and extensions, not by modifying existing types. Use `ViewModifier` + `View` extension for reusable styling.
- Prefer `overlay`/`background` for decoration; `ZStack` for peer composition.
- Container views: use `@ViewBuilder let content: Content` (not stored closures).

See `references/view-composition.md` for patterns, ordering conventions, and anti-patterns.

## Design Craft

- Establish a clear visual direction — commit to an aesthetic, don't mix styles.
- Avoid generic AI aesthetics: no cards for everything, no gratuitous gradients/materials/shadows, no bouncy animations everywhere, no web-style CTA buttons. Use native iOS components. Apply the squint test — hierarchy should be visible even blurred.
- Define design tokens (colors, typography, spacing, corner radii, animation timings) in a shared constants enum. One source of truth.
- Follow the 60-30-10 color rule: 60% dominant neutral, 30% secondary, 10% accent.
- Use semantic color names for role, not RGB. Support dark mode with system colors or asset catalog.
- Establish clear typographic hierarchy: 3-4 levels max. Use weight contrast more than size contrast.
- Use Dynamic Type fonts exclusively. Never hardcode `.font(.system(size:))`.
- Minimum 44x44pt tap targets. Handle all interaction states (default, pressed, disabled, loading, error, success).
- Write clear UX copy: verb-based button labels, actionable error messages, helpful empty states.

See `references/design-craft.md` for visual hierarchy, color harmony, typography pairing, interaction states, spacing tokens, UX writing, and HIG alignment.

## Animation & Motion

- Use `withAnimation { }` (explicit) for control. Use `.animation(_:value:)` for implicit — always with a `value:` parameter.
- Prefer GPU-friendly transforms (`offset`, `scale`, `rotation`) over layout changes (`frame`).
- Use `@Animatable` macro (iOS 26+) not manual `animatableData`.
- Chain animations via `withAnimation` completion closures, not delays.
- `matchedGeometryEffect` with `@Namespace` for hero transitions.
- Respect `accessibilityReduceMotion` — replace motion with opacity.
- Spring animations for natural feel. `.bouncy` for playful, `.smooth` for subtle.

See `references/animation.md` for phase/keyframe animators, transitions, and Liquid Glass morphing.

## Accessibility

- VoiceOver: every interactive element needs a text label. `Button("Add", systemImage: "plus", action:)` not icon-only.
- Use `Image(decorative:)` or `accessibilityHidden()` for decorative images.
- Never use `onTapGesture()` when `Button` works. If you must, add `.accessibilityAddTraits(.isButton)`.
- Respect `accessibilityDifferentiateWithoutColor` — don't rely on color alone.
- Use `accessibilityInputLabels()` for complex/changing button labels.
- Test with VoiceOver and Accessibility Inspector.

See `references/accessibility.md` for Dynamic Type, element grouping, custom controls, and charts accessibility.

## Performance

- Ternary expressions over `if/else` view branching (avoids `_ConditionalContent`).
- No `AnyView`. Use `@ViewBuilder`, `Group`, or generics.
- Fine-grained `@Observable` models — avoid broad dependencies on arrays.
- Use `LazyVStack`/`LazyHStack` for large data sets.
- `task()` over `onAppear()` for async (auto-cancellation).
- Keep view initializers trivial. Defer work to `task()`.
- Debug with `Self._printChanges()` and random background colors.

See `references/performance.md` for the full code smell catalog and remediation patterns.

## Concurrency

- Always `async`/`await` over closures. Never use GCD (`DispatchQueue`).
- `@MainActor` on `@Observable` classes (if not using default MainActor isolation).
- Use `.task` modifier for async work in views.
- Prefer `Task` over `Task.detached` (inherits actor context).
- Flag unprotected mutable shared state.
- Assume strict concurrency. Flag `@Sendable` violations.

See `references/concurrency.md` for actor patterns, Sendable, and Swift 6 migration.

## Navigation & Presentation

- `NavigationStack` with `navigationDestination(for:)`. Never mix with `NavigationLink(destination:)`.
- `sheet(item:)` over `sheet(isPresented:)` for optional data.
- Attach `confirmationDialog()` to its trigger (for Liquid Glass animations).
- Single "OK" alert buttons can be omitted.
- `TabView(selection:)` binds to an enum, not Int/String.

See `references/navigation.md` for split views, inspector patterns, and deep links.

## Liquid Glass (iOS 26+)

- Recompile with Xcode 26 for automatic adoption on NavigationBar, TabBar, Toolbar.
- Apply `.glassEffect()` **after** layout and visual modifiers.
- Use `GlassEffectContainer` when multiple glass elements coexist.
- `.interactive()` only on tappable/focusable elements.
- `.buttonStyle(.glass)` / `.buttonStyle(.glassProminent)` for actions.
- Gate with `#available(iOS 26, *)` and provide `.ultraThinMaterial` fallback.

See `references/liquid-glass.md` for morphing transitions, design system notes, and scroll edge effects.
