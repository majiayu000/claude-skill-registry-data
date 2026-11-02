---
name: swiftui-performance
description: "Audit and improve SwiftUI runtime performance. Use when diagnosing slow rendering, janky scrolling, high CPU, memory usage, excessive view updates, layout thrash, body evaluation cost, identity churn, view lifetime issues, lazy loading, Instruments profiling guidance, and performance audit requests."
---

# SwiftUI Performance

Audit SwiftUI view performance end-to-end, from instrumentation and baselining to root-cause analysis and concrete remediation steps.

## Contents

- [Workflow Decision Tree](#workflow-decision-tree)
- [1. Code-First Review](#1-code-first-review)
- [2. Guide the User to Profile](#2-guide-the-user-to-profile)
- [3. Analyze and Diagnose](#3-analyze-and-diagnose)
- [4. Remediate](#4-remediate)
- [Common Code Smells (and Fixes)](#common-code-smells-and-fixes)
- [5. Verify](#5-verify)
- [Outputs](#outputs)
- [Instruments Profiling](#instruments-profiling)
- [Identity and Lifetime](#identity-and-lifetime)
- [Lazy Loading Patterns](#lazy-loading-patterns)
- [State and Observation Optimization](#state-and-observation-optimization)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Workflow Decision Tree

- If the user provides code, start with "Code-First Review."
- If the user only describes symptoms, ask for minimal code/context, then do "Code-First Review."
- If code review is inconclusive, go to "Guide the User to Profile" and ask for a trace or screenshots.

## 1. Code-First Review

Collect:
- Target view/feature code.
- Data flow: state, environment, observable models.
- Symptoms and reproduction steps.

Focus on:
- View invalidation storms from broad state changes.
- Unstable identity in lists (`id` churn, `UUID()` per render).
- Top-level conditional view swapping (`if/else` returning different root branches).
- Heavy work in `body` (formatting, sorting, image decoding).
- Layout thrash (deep stacks, `GeometryReader`, preference chains).
- Large images without downsampling or resizing.
- Over-animated hierarchies (implicit animations on large trees).

Provide:
- Likely root causes with code references.
- Suggested fixes and refactors.
- If needed, a minimal repro or instrumentation suggestion.

## 2. Guide the User to Profile

Explain how to collect data with Instruments:
- Use the SwiftUI template in Instruments.
- Profile a **Release build** on a real device when possible.
- Reproduce the exact interaction (scroll, navigation, animation).
- Capture SwiftUI timeline and Time Profiler.
- Export or screenshot the relevant lanes and the call tree.

Ask for:
- Trace export or screenshots of SwiftUI lanes + Time Profiler call tree.
- Device/OS/build configuration.

## 3. Analyze and Diagnose

Prioritize likely SwiftUI culprits:
- View invalidation storms from broad state changes.
- Unstable identity in lists (`id` churn, `UUID()` per render).
- Top-level conditional view swapping (`if/else` returning different root branches).
- Heavy work in `body` (formatting, sorting, image decoding).
- Layout thrash (deep stacks, `GeometryReader`, preference chains).
- Large images without downsampling or resizing.
- Over-animated hierarchies (implicit animations on large trees).

Summarize findings with evidence from traces/logs.

## 4. Remediate

Apply targeted fixes:
- Narrow state scope (`@State`/`@Observable` closer to leaf views).
- Stabilize identities for `ForEach` and lists.
- Move heavy work out of `body` (precompute, cache, `@State`).
- Use `equatable()` or value wrappers for expensive subtrees.
- Downsample images before rendering.
- Reduce layout complexity or use fixed sizing where possible.

## Common Code Smells (and Fixes)

Look for these patterns during code review.

### Expensive formatters in `body`

```swift
var body: some View {
    let number = NumberFormatter() // slow allocation
    let measure = MeasurementFormatter() // slow allocation
    Text(measure.string(from: .init(value: meters, unit: .meters)))
}
```

Prefer cached formatters in a model or a dedicated helper:

```swift
final class DistanceFormatter {
    static let shared = DistanceFormatter()
    let number = NumberFormatter()
    let measure = MeasurementFormatter()
}
```

### Computed properties that do heavy work

```swift
var filtered: [Item] {
    items.filter { $0.isEnabled } // runs on every body eval
}
```

Prefer precompute or cache on change:

```swift
@State private var filtered: [Item] = []
// update filtered when inputs change
```

### Sorting/filtering in `body` or `ForEach`

```swift
// DON'T: sorts or filters on every body evaluation
ForEach(items.sorted(by: sortRule)) { item in Row(item) }
ForEach(items.filter { $0.isEnabled }) { item in Row(item) }
```

Prefer precomputed, cached collections with stable identity. Update on input change, not in `body`.

### Unstable identity

```swift
ForEach(items, id: \.self) { item in
    Row(item)
}
```

Avoid `id: \.self` for non-stable values; use a stable ID.

### Top-level conditional view swapping

```swift
var content: some View {
    if isEditing {
        editingView
    } else {
        readOnlyView
    }
}
```

Prefer one stable base view and localize conditions to sections/modifiers (for example inside `toolbar`, row content, `overlay`, or `disabled`). This reduces root identity churn and helps SwiftUI diffing stay efficient.

### Image decoding on the main thread

```swift
Image(uiImage: UIImage(data: data)!)
```

Prefer decode/downsample off the main thread and store the result.

### Broad dependencies in observable models

```swift
@Observable class Model {
    var items: [Item] = []
}

var body: some View {
    Row(isFavorite: model.items.contains(item))
}
```

Prefer granular view models or per-item state to reduce update fan-out.

## 5. Verify

Ask the user to re-run the same capture and compare with baseline metrics.
Summarize the delta (CPU, frame drops, memory peak) if provided.

## Outputs

Provide:
- A short metrics table (before/after if available).
- Top issues (ordered by impact).
- Proposed fixes with estimated effort.

## Instruments Profiling

Use the **SwiftUI instrument template** in Xcode (Cmd+I to profile). Key instruments: SwiftUI View Body (body evaluation counts), SwiftUI View Properties (state change tracking), Time Profiler, and Hangs.

Add `Self._printChanges()` in debug builds to log which property triggered a view update:

```swift
var body: some View {
    #if DEBUG
    let _ = Self._printChanges()  // "MyView: @self, _count changed."
    #endif
    Text("Count: \(count)")
}
```

See [references/optimizing-swiftui-performance-instruments.md](references/optimizing-swiftui-performance-instruments.md) for the full profiling workflow.

## Identity and Lifetime

### Structural Identity vs Explicit Identity

SwiftUI assigns every view an **identity** used to track its lifetime, state, and animations.

- **Structural identity** (default): determined by the view's position in the view hierarchy. SwiftUI uses the call-site location in `body` to distinguish views.
- **Explicit identity**: you assign with `.id(_:)` modifier or `ForEach(items, id: \.stableID)`.

```swift
// Structural identity: SwiftUI knows these are different views by position
VStack {
    Text("First")   // position 0
    Text("Second")  // position 1
}
```

### How Identity Tracks View Lifetime

When a view's identity changes, SwiftUI treats it as a **new view**:

- All `@State` is reset.
- `onAppear` fires again.
- Animations may restart.
- Transition animations play (if defined).

When identity stays the same, SwiftUI updates the **existing view** in place, preserving state and providing smooth transitions.

### AnyView and Identity Reset

`AnyView` erases type information, forcing SwiftUI to fall back to less efficient diffing:

```swift
// DON'T: AnyView destroys type identity
func makeView(for item: Item) -> AnyView {
    if item.isPremium {
        return AnyView(PremiumRow(item: item))
    } else {
        return AnyView(StandardRow(item: item))
    }
}

// DO: use @ViewBuilder to preserve structural identity
@ViewBuilder
func makeView(for item: Item) -> some View {
    if item.isPremium {
        PremiumRow(item: item)
    } else {
        StandardRow(item: item)
    }
}
```

`AnyView` also prevents SwiftUI from detecting which branch changed, causing full subtree replacement instead of targeted updates.

### Ternary Modifiers Preserve Structural Identity

`if`/`else` in a view builder creates `_ConditionalContent` — two separate view branches with distinct identities. When the condition changes, SwiftUI destroys one branch and creates the other, resetting all `@State`.

For toggling **modifiers** on the same view, use a ternary expression instead:

```swift
// DON'T: if/else creates two separate Text views with different identities
if isHighlighted {
    Text(title).foregroundStyle(.yellow)
} else {
    Text(title).foregroundStyle(.primary)
}

// DO: ternary keeps one Text view, just changes the modifier value
Text(title)
    .foregroundStyle(isHighlighted ? .yellow : .primary)
```

This preserves the view's identity (and its state) across the condition change, and SwiftUI can animate the transition smoothly.

Use `if`/`else` when the **view type itself** differs between branches. Use ternary when only a **property or modifier** changes.

### id() Modifier Impacts

The `.id()` modifier assigns explicit identity. Changing the value **destroys and recreates** the view:

```swift
// DON'T: UUID() changes every render, destroying and recreating the view each time
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            Row(item: item)
                .id(UUID())  // kills performance -- new identity every render
        }
    }
}

// DO: use a stable identifier
ForEach(items) { item in
    Row(item: item)
        .id(item.stableID)  // identity only changes when the item actually changes
}
```

Intentional `.id()` change is useful for **resetting state** (e.g., `.id(selectedTab)` to reset a scroll position when switching tabs).

## Lazy Loading Patterns

### LazyVStack and LazyHStack

Lazy stacks only create views for items currently visible on screen. Off-screen items are not evaluated until scrolled into view.

```swift
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}
```

Key behaviors:
- Views are created lazily but **not destroyed** when scrolled off screen (they remain in memory).
- `onAppear` fires when the view first enters the visible area.
- `onDisappear` fires when it leaves, but the view is still alive.

### LazyVGrid and LazyHGrid

Use lazy grids for multi-column layouts:

```swift
// Adaptive: as many columns as fit with minimum width
let columns = [GridItem(.adaptive(minimum: 150))]

ScrollView {
    LazyVGrid(columns: columns) {
        ForEach(photos) { photo in
            PhotoThumbnail(photo: photo)
        }
    }
}

// Fixed: exact number of equal columns
let fixedColumns = [
    GridItem(.flexible()),
    GridItem(.flexible()),
    GridItem(.flexible()),
]
```

### When to Use Lazy vs Eager Stacks

| Scenario | Use |
|----------|-----|
| < 50 items | `VStack` / `HStack` (eager is fine) |
| 50-100 items | Either works; prefer `Lazy` if items are complex |
| > 100 items | `LazyVStack` / `LazyHStack` (required for performance) |
| Always-visible content | `VStack` (no benefit to lazy) |
| Scrollable lists | `LazyVStack` inside `ScrollView`, or `List` |

**Important:** Do not nest `GeometryReader` inside lazy containers. It forces eager measurement and defeats lazy loading. Use `.onGeometryChange` (iOS 16+) instead.

## State and Observation Optimization

### @Observable Granular Tracking

`@Observable` (Observation framework, iOS 17+) tracks property access at the **per-property level**. A view only re-evaluates when properties it actually read in `body` change:

```swift
@Observable class UserProfile {
    var name: String = ""
    var avatarURL: URL?
    var biography: String = ""
}

// This view ONLY re-renders when `name` changes -- not when
// biography or avatarURL change, because it only reads `name`
struct NameLabel: View {
    let profile: UserProfile
    var body: some View {
        Text(profile.name)
    }
}
```

This is a significant improvement over `ObservableObject` + `@Published`, which invalidates all observing views when **any** published property changes.

### Avoiding Observation Scope Pollution

If a view reads many properties from an `@Observable` model in `body`, it re-renders when **any** of those properties change. Push reads into child views to narrow the scope:

```swift
// DON'T: reads name, email, avatar, and settings in one body
struct ProfileView: View {
    let model: ProfileModel
    var body: some View {
        VStack {
            Text(model.name)           // tracks name
            Text(model.email)          // tracks email
            AsyncImage(url: model.avatar) // tracks avatar
            SettingsForm(model.settings)  // tracks settings
        }
    }
}

// DO: split into child views so each only tracks what it reads
struct ProfileView: View {
    let model: ProfileModel
    var body: some View {
        VStack {
            NameRow(model: model)      // only tracks name
            EmailRow(model: model)     // only tracks email
            AvatarView(model: model)   // only tracks avatar
            SettingsForm(model: model) // only tracks settings
        }
    }
}
```

### Computed Properties for Derived State

Use computed properties on `@Observable` models to derive state without introducing extra stored properties that widen observation scope:

```swift
@Observable class ShoppingCart {
    var items: [CartItem] = []

    // Views reading `total` only re-render when `items` changes
    var total: Decimal {
        items.reduce(0) { $0 + $1.price * Decimal($1.quantity) }
    }
}
```

## Common Mistakes

1. **Profiling Debug builds.** Debug builds include extra runtime checks and disable optimizations, producing misleading perf data. Profile Release builds on a real device.
2. **Observing an entire model when only one property is needed.** Break large `@Observable` models into focused ones, or use computed properties/closures to narrow observation scope.
3. **Using `GeometryReader` inside ScrollView items.** GeometryReader forces eager sizing and defeats lazy loading. Prefer `.onGeometryChange` (iOS 16+) or measure outside the lazy container.
4. **Calling `DateFormatter()` or `NumberFormatter()` inside `body`.** These are expensive to create. Make them static or move them outside the view.
5. **Animating non-equatable state.** If SwiftUI cannot determine equality, it redraws every frame. Conform state to `Equatable`, then use `.animation(_:value:)` for simple value-bound changes or `.animation(_:body:)` for narrower modifier-scoped implicit animation.
6. **Large flat `List` without identifiers.** Use `id:` or make items `Identifiable` so SwiftUI can diff efficiently instead of rebuilding the entire list.
7. **Unnecessary `@State` wrapper objects.** Wrapping a simple value type in a class for `@State` defeats value semantics. Use plain `@State` with structs.
8. **Blocking `MainActor` with synchronous I/O.** File reads, JSON parsing of large payloads, and image decoding should happen off the main actor. Use `Task.detached` or a custom actor.

## Review Checklist

- [ ] No `DateFormatter`/`NumberFormatter` allocations inside `body`
- [ ] Large lists use `Identifiable` items or explicit `id:`
- [ ] `@Observable` models expose only the properties views actually read
- [ ] Heavy computation is off `MainActor` (image processing, parsing)
- [ ] `GeometryReader` is not inside a `LazyVStack`/`LazyHStack`/`List`
- [ ] Implicit animations use `.animation(_:value:)` for value-bound changes or `.animation(_:body:)` for narrower modifier scope
- [ ] No synchronous network/file I/O on the main thread
- [ ] Profiling done on Release build, real device
- [ ] `@Observable` view models are `@MainActor`-isolated; types crossing concurrency boundaries are `Sendable`

## References

- Demystify SwiftUI performance (WWDC23): [references/demystify-swiftui-performance-wwdc23.md](references/demystify-swiftui-performance-wwdc23.md)
- Optimizing SwiftUI performance with Instruments: [references/optimizing-swiftui-performance-instruments.md](references/optimizing-swiftui-performance-instruments.md)
- Understanding hangs in your app: [references/understanding-hangs-in-your-app.md](references/understanding-hangs-in-your-app.md)
- Understanding and improving SwiftUI performance: [references/understanding-improving-swiftui-performance.md](references/understanding-improving-swiftui-performance.md)
- WWDC transcript sources: [references/wwdc-session-sources.md](references/wwdc-session-sources.md)
