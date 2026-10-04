---
description: |
    Use when building, reviewing, debugging, or refactoring SwiftUI on Apple platforms, especially for state management, layout, navigation, component patterns, animation, accessibility, or performance. Also use for SwiftUI-specific architecture questions, app scaffolding, deep links, and runtime performance issues such as janky scrolling, excessive view updates, layout thrash, or Instruments-guided audits.
metadata:
    targets:
        - codex
name: SwiftUI Mastery
tags:
    - swiftui
    - ios
    - macos
    - watchos
    - tvos
    - ui
    - layout
    - state-management
    - navigation
    - animation
    - performance
    - accessibility
---

<!-- Merged from: apple-swiftui-mastery, swiftui-expert-skill, swiftui-ui-patterns (2026-03-30) -->
<!-- Merged from: swiftui-performance-audit (2026-03-31) -->

# SwiftUI Mastery

Expert guidance for building, reviewing, and architecting SwiftUI UIs on all Apple platforms. Covers state management, layout, navigation, animations, accessibility, performance, and component patterns.

## Operating Rules

- Consult `references/latest-apis.md` at the start of every task to check for deprecated APIs
- Prefer native SwiftUI APIs over UIKit/AppKit bridging unless bridging is explicitly needed
- Use `#available` gating with sensible fallbacks for version-specific APIs (iOS 16+, iOS 17+, iOS 26+)
- Separate business logic from views for testability — without mandating a specific architecture
- Follow Apple's Human Interface Guidelines
- Only adopt Liquid Glass when explicitly requested (see the `liquid-glass` skill)
- `@State` properties should always be `private`

## Task Workflow

### Review existing SwiftUI code
- Identify which topics apply (state management, layout, navigation, performance, accessibility)
- Flag deprecated APIs using `references/latest-apis.md`
- Check `#available` gating and fallback paths for iOS 26+ features
- Validate the Correctness Checklist below

### Improve existing SwiftUI code
- Audit against the Topic Router
- Replace deprecated APIs with modern equivalents from `references/latest-apis.md`
- Refactor hot paths to reduce unnecessary state updates
- Extract complex view bodies into separate subviews
- Suggest image downsampling when `UIImage(data:)` is encountered (see `references/image-optimization.md`)

### Implement a new SwiftUI feature
- Design data flow first: identify owned vs injected state
- Structure views for optimal diffing — extract subviews early
- Apply correct animation patterns (implicit vs explicit, transitions)
- Use `Button` for all tappable elements; add accessibility grouping and labels
- Gate version-specific APIs with `#available` and provide fallbacks

### Scaffold a new project or screen
- Start with `references/app-wiring.md` to wire TabView + NavigationStack + sheets
- Add a minimal `AppTab` enum and per-tab router
- Choose component references from `references/components-index.md` based on UI needs
- Expand route and sheet enums as new screens are added

## Topic Router

Consult the reference file for each topic relevant to the current task:

| Topic | Reference |
|-------|-----------|
| Deprecated → modern API lookup | `references/latest-apis.md` — **Read first every task** |
| State management & @Observable | `references/state-management.md` |
| View composition & extraction | `references/view-structure.md` |
| Performance & update control | `references/performance-patterns.md` |
| Performance audit (Instruments guide) | `references/optimizing-swiftui-performance-instruments.md` |
| Performance audit (understanding & improving) | `references/understanding-improving-swiftui-performance.md` |
| Performance audit (hangs) | `references/understanding-hangs-in-your-app.md` |
| Performance audit (WWDC23 deep dive) | `references/demystify-swiftui-performance-wwdc23.md` |
| Lists, ForEach & Table | `references/list-patterns.md` |
| Layout & GeometryReader alternatives | `references/layout-best-practices.md` |
| Sheets & navigation | `references/sheet-navigation-patterns.md` |
| ScrollView patterns | `references/scroll-patterns.md` |
| Animations (basics) | `references/animation-basics.md` |
| Animations (transitions) | `references/animation-transitions.md` |
| Animations (advanced / iOS 17+) | `references/animation-advanced.md` |
| Accessibility & Dynamic Type | `references/accessibility-patterns.md` |
| Swift Charts | `references/charts.md` |
| Charts accessibility | `references/charts-accessibility.md` |
| Image optimization | `references/image-optimization.md` |
| macOS scenes & windows | `references/macos-scenes.md` |
| macOS window styling | `references/macos-window-styling.md` |
| macOS-specific views | `references/macos-views.md` |
| App shell / tab + nav wiring | `references/app-wiring.md` |
| Component patterns index | `references/components-index.md` |
| Component: TabView | `references/tabview.md` |
| Component: NavigationStack | `references/navigationstack.md` |
| Component: Sheets | `references/sheets.md` |
| Component: List | `references/list.md` |
| Component: ScrollView | `references/scrollview.md` |
| Component: Grids | `references/grids.md` |
| Component: Forms | `references/form.md` |
| Component: Controls | `references/controls.md` |
| Component: Overlays | `references/overlay.md` |
| Component: Split views | `references/split-views.md` |
| Component: Searchable | `references/searchable.md` |
| Component: Focus | `references/focus.md` |
| Component: Haptics | `references/haptics.md` |
| Component: Media | `references/media.md` |
| Component: Loading/Placeholders | `references/loading-placeholders.md` |
| Component: Input toolbar | `references/input-toolbar.md` |
| Component: Matched transitions | `references/matched-transitions.md` |
| Component: Theming | `references/theming.md` |
| Component: Top bar | `references/top-bar.md` |
| Component: Title menus | `references/title-menus.md` |
| Component: Menu bar (macOS) | `references/menu-bar.md` |
| Component: macOS Settings | `references/macos-settings.md` |
| Component: Deep links | `references/deeplinks.md` |
| Component: Lightweight clients | `references/lightweight-clients.md` |

## Correctness Checklist

Violations are always bugs — check these on every review:

- [ ] `@State` properties are `private`
- [ ] `@Binding` only where a child modifies parent state
- [ ] Values passed in from parent are never declared as `@State` or `@StateObject` (they ignore updates)
- [ ] `@StateObject` for view-owned objects; `@ObservedObject` for injected objects
- [ ] iOS 17+: use `@State` with `@Observable`; use `@Bindable` for injected observables needing bindings
- [ ] `ForEach` uses stable identity — never `.indices` for dynamic content
- [ ] Constant number of views per `ForEach` element
- [ ] `.animation(_:value:)` always includes the `value` parameter
- [ ] iOS 26+ APIs gated with `#available(iOS 26, *)` and a fallback provided
- [ ] `import Charts` present in files using chart types

## State Management Summary

SwiftUI provides several property wrappers — choose based on who owns the state:

- **`@State`** — simple value types owned by a single view; expose to children as `@Binding`
- **`@Binding`** — two-way reference into parent state; use `$` prefix to derive from `@State`
- **`@StateObject`** — creates and owns an `ObservableObject`; persists across view re-creations
- **`@ObservedObject`** — subscribes to an `ObservableObject` injected from a parent; does NOT persist
- **`@EnvironmentObject`** — shared model injected into the hierarchy; use for global app state
- **`@Environment`** — read system values (colorScheme, dynamicTypeSize) or custom `EnvironmentKey`s
- **`@Observable` (iOS 17+)** — marks a class for automatic observation; combine with `@State` or `@Environment`; no need for `@Published`

For edge cases including computed bindings, combining wrappers, and avoiding value type mutation pitfalls: see `references/state-management.md`.

## Layout Key Points

- Use `HStack`, `VStack`, `ZStack` for standard composition; `LazyVGrid`/`LazyHGrid`/`Grid` for collections
- **`Layout` protocol** (iOS 16+): implement `sizeThatFits` and `placeSubviews` for fully custom layouts
- **`GeometryReader`**: takes all available space unless constrained — wrap in a `frame` or use as overlay/background; prefer `Layout` protocol or `ViewThatFits` over `GeometryReader` where possible
- **`PreferenceKey`**: lets child views send information up the hierarchy — essential for measuring sizes or aligning siblings
- For complex layout patterns (flow, tag cloud, flexible grid): see `references/layout-best-practices.md`

## Navigation Patterns

- Use `NavigationStack` (iOS 16+) with `NavigationPath` for programmatic navigation; conform data to `Hashable` and use `.navigationDestination(for:)`
- Use `NavigationSplitView` for two- or three-column layouts on iPad and macOS
- Present secondary content with `.sheet` or `.fullScreenCover`; use `.presentationDetents` (iOS 16+) for medium/large/custom heights
- For deep linking: decode URLs into path elements; see `references/sheet-navigation-patterns.md`

## Sheet Patterns

### Item-driven sheet (preferred over isPresented)

```swift
@State private var selectedItem: Item?

.sheet(item: $selectedItem) { item in
    EditItemSheet(item: item)
}
```

### Sheet owns its actions

```swift
struct EditItemSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(Store.self) private var store
    let item: Item
    @State private var isSaving = false

    var body: some View {
        Button(isSaving ? "Saving…" : "Save") {
            Task { await save() }
        }
    }

    private func save() async {
        isSaving = true
        await store.save(item)
        dismiss()
    }
}
```

Prefer `.sheet(item:)` when state represents a selected model. Sheets should call `dismiss()` internally — avoid forwarding `onCancel`/`onConfirm` closures to the parent.

## Animations Summary

- Wrap state mutations in `withAnimation { }` for automatic animation; use `.animation(_:value:)` on individual views for targeted control
- Use `.transition()` for appear/disappear effects: `.opacity`, `.slide`, `.scale`, `.move`
- `matchedGeometryEffect(id:in:isSource:)` synchronises geometry across views for hero transitions
- iOS 17+: phase animators and keyframe animations for complex sequenced motion
- iOS 26+: `@Animatable` macro for custom animatable properties
- For advanced spring curves, keyframe examples: see `references/animation-advanced.md`

## Performance Anti-Patterns

Avoid these — each is a class of bug or performance issue:

- Performing network requests or heavy work inside `body` — use `.task` or separate model layers
- Overusing `GeometryReader` — prefer `Layout` protocol or `LayoutPriority`
- Creating new objects or closures every `body` evaluation (memory churn) — use `@StateObject` or constants
- Using `.onAppear` for repeating timers — use `TimelineView` for scheduled updates
- Modifying state inside a view's `init()` — causes unpredictable behavior
- Excessive global state through `@EnvironmentObject` — obscures data flow

## Performance Audit Workflow

Use this structured workflow when diagnosing slow rendering, janky scrolling, high CPU/memory, excessive view updates, or layout thrash.

**Decision tree:**
- If the user provides code → start with Code-First Review
- If the user only describes symptoms → ask for minimal code/context, then do Code-First Review
- If code review is inconclusive → Guide Profiling with Instruments

### 1. Code-First Review

Collect: target view/feature code, data flow (state, environment, observable models), symptoms and reproduction steps.

Focus on:
- View invalidation storms from broad state changes
- Unstable identity in lists (`id` churn, `UUID()` per render)
- Top-level conditional view swapping (`if/else` returning different root branches)
- Heavy work in `body` (formatting, sorting, image decoding)
- Layout thrash (deep stacks, `GeometryReader`, preference chains)
- Large images without downsampling or resizing
- Over-animated hierarchies (implicit animations on large trees)

### 2. Guide Profiling with Instruments

When code review is inconclusive, ask the user to:
- Open Instruments → SwiftUI template (use a **Release** build)
- Reproduce the exact interaction (scroll, navigation, animation)
- Capture the SwiftUI timeline and Time Profiler call tree
- Export or screenshot the relevant lanes

Ask for: trace export or screenshots of SwiftUI lanes + Time Profiler, device/OS/build configuration.

See `references/optimizing-swiftui-performance-instruments.md` and `references/demystify-swiftui-performance-wwdc23.md` for guidance on reading traces.

### 3. Diagnose

Prioritize the culprits listed in step 1. Summarize findings with evidence from traces/logs.

### 4. Remediate

Apply targeted fixes:
- Narrow state scope (`@State`/`@Observable` closer to leaf views)
- Stabilize identities for `ForEach` and lists
- Move heavy work out of `body` (precompute, cache, `@State`)
- Use `equatable()` or value wrappers for expensive subtrees
- Downsample images before rendering
- Reduce layout complexity or use fixed sizing where possible

### 5. Verify

Ask the user to re-run the same capture and compare with baseline. Summarize the delta (CPU, frame drops, memory peak) if provided. Provide: short metrics table (before/after), top issues ordered by impact, proposed fixes with estimated effort.

### Common Code Smells

**Expensive formatters in `body`** — allocating `NumberFormatter`/`MeasurementFormatter` each evaluation. Fix: cache in a shared helper or model.

**Computed properties doing heavy work** — `var filtered: [Item] { items.filter { ... } }` runs on every `body` eval. Fix: precompute and cache using `@State` updated on change.

**Sorting/filtering inside `ForEach`** — `ForEach(items.sorted(by:))` re-sorts every render. Fix: sort once before view updates.

**Unstable identity** — `ForEach(items, id: \.self)` on non-stable values. Fix: use a stable ID (e.g., a persistent `UUID` stored on the model).

**Top-level conditional view swapping** — `if isEditing { editingView } else { readOnlyView }` causes root identity churn. Fix: one stable base view; localize conditions to toolbar, overlays, or modifiers.

**Image decoding on the main thread** — `UIImage(data: data)`. Fix: decode/downsample off the main thread and store the result (see `references/image-optimization.md`).

**Broad dependencies in observable models** — a view reading `model.items.contains(item)` re-renders on any items change. Fix: granular view models or per-item state to reduce update fan-out.

## Workflow for a New View

1. Define the view's state and where it lives (local, parent-owned, environment)
2. Identify dependencies to inject via `@Environment`
3. Sketch the view hierarchy; extract repeated parts into subviews
4. Implement async loading with `.task` and an explicit loading/error state enum
5. Add accessibility labels for all interactive elements
6. Validate with a build; update callsites as needed

## iOS 26+ Notable APIs

- `Grid` for fully automatic grid layouts
- `FlowLayout` for wrapping content
- Improved sheet detents and `presentationCompactMode`
- `@Animatable` macro for custom animatable properties
- `Chart3D` for 3D charting (see `references/charts.md`)
- Liquid Glass design language — see the dedicated `liquid-glass` skill

## Reference Files

All reference files live in `references/`. Read only the ones relevant to your current task.

**Always read first:** `references/latest-apis.md` — deprecated-to-modern API transitions (iOS 15 through iOS 26+)

For component-specific guidance, use `references/components-index.md` as the entry point — it lists intent, best-fit scenarios, pitfalls, and links for each component.

**Performance audit references:** `references/optimizing-swiftui-performance-instruments.md`, `references/understanding-improving-swiftui-performance.md`, `references/understanding-hangs-in-your-app.md`, `references/demystify-swiftui-performance-wwdc23.md`
