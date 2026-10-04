---
description: |
    Use for Apple Liquid Glass work on iOS 26+, iPadOS 26+, and related SwiftUI/UIKit interfaces. Covers native glassEffect APIs, GlassEffectContainer, glassEffectID, glass button styles, tab/search accessories, safe-area bars, background extension, AI chat composers, floating controls, canvas overlays, morphing, motion polish, accessibility, performance, dependency review, and migration from older Material UI. Do not use for generic CSS glassmorphism, Android imitation, static mockups, or non-Apple UI unless the user explicitly asks for inspiration only.
license: MIT
metadata:
    targets:
        - codex
name: liquid-glass_KM
---
# Liquid Glass

Use this skill to implement, review, or refactor Apple-native Liquid Glass UI. Prefer real SwiftUI/UIKit code and current SDK behavior over visual imitation.

## Activation

Use when the request mentions Liquid Glass, iOS 26 UI, glassEffect, frosted Apple controls, agent composers, floating toolbars, native tab/search accessories, canvas/media overlays, or migration from older SwiftUI Materials.

Stay out of scope for web CSS glassmorphism, Android, generic mockups, or legacy-only backports. If older OS support is required, keep the iOS 26 native path primary and add a minimal fallback.

## Workflow

1. Identify the surface: system navigation, custom control group, composer, sheet/popover, canvas overlay, or migration.
2. Choose the smallest native API that fits before custom drawing.
3. Keep content readable; put glass around controls and transient chrome, not dense text bodies.
4. Add motion only when it clarifies state, navigation, or direct manipulation.
5. Respect Reduce Transparency, Reduce Motion, Dynamic Type, VoiceOver labels, hit targets, and contrast.
6. Verify against the active SDK when a symbol is new, beta-sensitive, or absent from the project.

## Native API Priority

Use standard SwiftUI/UIKit components first:

- Native `NavigationStack`, `TabView`, sheets, popovers, menus, toolbar items, and `.searchable`.
- `Tab(role: .search)`, `tabViewBottomAccessory`, and `tabBarMinimizeBehavior` for tab/search flows.
- `safeAreaBar` for iOS 26 custom bars when the active SDK exposes the needed behavior; otherwise use `safeAreaInset`.
- `backgroundExtensionEffect()` for media/header imagery continuing under sidebars or inspectors.
- `.buttonStyle(.glass)` and `.buttonStyle(.glassProminent)` before custom button backgrounds.
- `glassEffect(_:in:)` for custom glass controls, compact overlays, pills, bars, and floating surfaces.
- `GlassEffectContainer(spacing:)` when multiple glass elements need coherent blending, performance, or morphing.
- `glassEffectID(_:in:)` for state or hierarchy changes that should morph instead of fade.
- `NavigationTransition.zoom` with `matchedTransitionSource` for list/grid/card to detail continuity.
- `.contentTransition(.symbolEffect(.replace))` for send/stop, play/pause, expand/collapse, and mic/waveform swaps.
- UIKit public APIs such as `UIGlassEffect`, `UIGlassContainerEffect`, `UIButton.Configuration.glass()`, and standard tab/navigation/sheet behavior.

Use `glassEffectUnion` only after verifying the active Xcode 26 SDK exposes the needed overload and the design truly needs separated elements to read as one connected glass group. Prefer `GlassEffectContainer` plus stable IDs as the generated default.

Never use private APIs such as `_UILiquidLensView`, KVC on private backdrop layers, or hidden UIKit hierarchy assumptions in production code.

## Design Rules

Liquid Glass is a functional material for controls, navigation, overlays, and transient surfaces. It should preserve context while protecting legibility.

Use one main glass slab or morph domain per local control group. Avoid glass-on-glass, busy nested blur, full-screen decorative glare, and blanket tint. Tint should mean something: selected, primary, destructive, recording, streaming, or status.

For AI chat and agent apps, favor:

- A glass bottom composer with plain readable messages above it.
- Floating tool controls, attachment chips, status chips, and canvas/media controls.
- Collapsible agent metadata and reasoning controls, with plain text bodies.
- Native tab/search accessories for global active-agent or queue state.

For visual polish, read `references/animation-visual-patterns.md`. Keep motion short, interruptible, and useful. Prefer morphing, symbol replacement, small scale/opacity changes, and direct manipulation over ornamental shimmer.

## Accessibility And Performance

In reusable components, read:

```swift
@Environment(\.accessibilityReduceTransparency) private var reduceTransparency
@Environment(\.accessibilityReduceMotion) private var reduceMotion
@Environment(\.colorSchemeContrast) private var contrast
```

When transparency is reduced, replace glass with an opaque system background plus a subtle border. When motion is reduced, replace morphing and springy transitions with opacity or short ease animations.

Keep hit targets around 44 points or larger. Give icon-only controls useful accessibility labels. Avoid glass behind dense text, tiny labels, or busy media unless you add a dimming or contrast layer.

Control GPU cost by avoiding stacked blur, many independent full-width glass rows, display-link-driven effects, and shader overlays for ordinary controls. Use `GlassEffectContainer` around related elements to help rendering and morphing.

## Code Generation Rules

- Generate real Swift code before design commentary.
- Use `@available(iOS 26.0, *)` on reusable components that call iOS 26-only APIs.
- Match the existing project architecture and naming when editing a project.
- Keep snippets self-contained with sample state and `#Preview` when practical.
- Put related controls inside one `GlassEffectContainer`.
- Use stable IDs with `glassEffectID` for morphing between compact and expanded states.
- Use native tab/search/sheet APIs before recreating system chrome.
- For drag interactions, use gesture translation and predicted end translation to choose the final state.
- For visual examples, use real app surfaces: composers, toolbars, panels, canvases, media headers, command palettes, and tab accessories.

## Quick Patterns

### Composer group

```swift
GlassEffectContainer(spacing: 10) {
    HStack(spacing: 10) {
        Button("Tools", systemImage: toolsExpanded ? "xmark" : "plus") {
            withAnimation(animation) { toolsExpanded.toggle() }
        }
        .buttonStyle(.glass)
        .contentTransition(.symbolEffect(.replace))

        TextField("Ask, search, or delegate", text: $prompt, axis: .vertical)
            .textFieldStyle(.plain)
            .padding(.horizontal, 14)
            .padding(.vertical, 12)
            .glassEffect(.regular.interactive(), in: Capsule())

        Button(isStreaming ? "Stop" : "Send", systemImage: isStreaming ? "stop.fill" : "arrow.up") {
            submitOrStop()
        }
        .buttonStyle(.glassProminent)
        .contentTransition(.symbolEffect(.replace))
    }
}
```

### Reduced transparency fallback

```swift
@ViewBuilder
func adaptiveGlassBackground<S: InsettableShape>(_ shape: S) -> some View {
    if reduceTransparency {
        shape
            .fill(.background)
            .overlay(shape.stroke(.separator.opacity(0.6), lineWidth: 0.5))
    } else {
        shape.glassEffect(.regular, in: shape)
    }
}
```

### Morphing cluster

```swift
@Namespace private var glassNamespace

GlassEffectContainer(spacing: 8) {
    if isExpanded {
        expandedPanel
            .glassEffect(.regular, in: .rect(cornerRadius: 24))
            .glassEffectID("agent-tools", in: glassNamespace)
    } else {
        compactButton
            .glassEffect(.regular.interactive(), in: Capsule())
            .glassEffectID("agent-tools", in: glassNamespace)
    }
}
```

## Verified gotchas (selection morph)

These rules are SDK-verified against `iPhoneSimulator26.4.sdk/.../SwiftUICore.framework/.../SwiftUICore.swiftmodule/arm64-apple-ios-simulator.swiftinterface`:

```swift
public struct Glass : Swift.Equatable, Swift.Sendable {
  public static var regular: Glass { get }
  public static var clear: Glass { get }
  public static var identity: Glass { get }            // ← REAL — frequently misdocumented
  public func tint(_ color: Color?) -> Glass
  public func interactive(_ isEnabled: Bool = true) -> Glass
}
```

1. **`Glass.identity` IS a real Glass variant.** It renders no visible effect but keeps the view in the morph graph. Use it for the inactive state when you want `GlassEffectContainer` to morph the selection between cells. Many third-party docs and AI agents claim `.identity` doesn't exist — they are wrong; the SDK header above proves it.

2. **Conditional rendering breaks the morph.** `.background { if isSelected { GlassView() } }` makes the container see view-destroyed + view-created, not a morph. Render the glass view for **every** cell at all times: `.identity` when inactive, `.regular.tint(...)` when active. Same `glassEffectID` + namespace across cells.

3. **Don't nest `.glassEffect()` inside another `.glassEffect()` within the same `GlassEffectContainer`.** Two glass surfaces in one container mute each other — the inner tinted glass collapses to a flat color overlay, and foreground text on the inner pill can render invisibly even with `.white` or `.tint`. Use `.ultraThinMaterial` or a regular `.background` for the OUTER rail, and `.glassEffect()` ONLY on the moving inner element.

4. **State-bound animation goes OUTSIDE the `GlassEffectContainer`.** `.animation(_:value:)` on or outside the container is correct (matches the Apple Music tab bar pattern). DON'T wrap state changes in `withAnimation` in the tap handler — it captures stale state on rapid taps and can desync the morph.

### Bonus subtleties

- `GlassEffectContainer(spacing:)` controls how far glass blobs can flow between siblings. 20–24 is typical for a cross-cell selection morph; set to 0 if you specifically want to PREVENT merging.
- The text-invisibility symptom in #3 is a vibrancy interaction between outer-rail glass and inner-pill glass. Switching the outer rail to Material removes it.

### Canonical morphing-selection pattern

Use this for filter pills, tab bars, segmented controls, any "selection slides between cells" UX:

```swift
// 1. Render the selection glass for every cell, ALL the time.
// 2. Use Glass.identity for inactive cells, .regular.tint(...).interactive() for active.
// 3. Shared @Namespace + same glassEffectID across all cells.
// 4. Wrap the cell row in GlassEffectContainer with spacing >= the visual gap between cells.
// 5. Outer container = .ultraThinMaterial (NOT .glassEffect) so cell glass doesn't nest into rail glass.
// 6. Animation is state-bound on or outside the container, NOT withAnimation in the tap handler.

@Namespace private var ns
@State private var selection: Item.ID = ...

GlassEffectContainer(spacing: 24) {
    HStack(spacing: 6) {
        ForEach(items) { item in
            Button { selection = item.id } label: { ItemLabel(item) }
                .frame(maxWidth: .infinity)
                .background {
                    Capsule()
                        .fill(.clear)
                        .glassEffect(
                            selection == item.id
                                ? .regular.tint(.accentColor).interactive()
                                : .identity,
                            in: Capsule()
                        )
                        .glassEffectID("selection", in: ns)
                }
        }
    }
}
.background(.ultraThinMaterial, in: Capsule())   // NOT another glassEffect!
.animation(.spring(response: 0.34, dampingFraction: 0.82), value: selection)
```

## Read As Needed

- `references/api-map.md` for exact API selection.
- `references/design-principles.md` for Apple-aligned visual rules.
- `references/animation-visual-patterns.md` for motion, morphing, and visual polish.
- `references/performance-accessibility.md` for guardrails.
- `references/component-taxonomy.md` for choosing surfaces.
- `references/library-evaluation.md` before recommending dependencies.
- `references/source-evaluation.md` when integrating community research.
- `recipes/ChatComposerRecipe.swift` for AI composer patterns.
- `recipes/NativeSearchAccessoryRecipe.swift` for native tab/search/accessory patterns.
- `snippets/29-background-extension-safe-area-bars.swift` for media extension and safe-area bars.
