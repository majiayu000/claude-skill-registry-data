---
name: ios26-liquid-glass
description: iOS 26 Liquid Glass API reference for SwiftUI and UIKit. Use this skill when working with glassEffect, GlassEffectContainer, glassEffectID, glassEffectUnion, or any Liquid Glass related code on iOS 26+.
---

# iOS 26 Liquid Glass Reference

Liquid Glass is Apple's design language introduced at WWDC 2025. Glass elements float above content with translucent, depth-aware surfaces that reflect and refract surrounding content.

## SwiftUI - glassEffect Modifier

```swift
func glassEffect<S: Shape>(
    _ glass: Glass = .regular,
    in shape: S = DefaultGlassEffectShape,
    isEnabled: Bool = true
) -> some View
```

Apply `.glassEffect()` **last** in your modifier chain for correct rendering.

### Glass Variants

| Variant | Description | Use Case |
|---------|-------------|----------|
| `.regular` | Default, balanced transparency | Most UI elements (buttons, controls, overlays) |
| `.clear` | High transparency, limited adaptivity | Media-rich backgrounds (needs dimming layer) |
| `.identity` | No effect applied | Conditional glass application |

### Glass Modifiers

```swift
// semantic color tinting - use only for meaning (success, warning, destructive)
.glassEffect(.regular.tint(.blue))

// iOS-only: enables scaling, bounce, shimmer on interaction
.glassEffect(.regular.interactive())

// combined
.glassEffect(.regular.tint(.blue).interactive())
```

### Shapes

```swift
// default shape (capsule)
.glassEffect()
.glassEffect(.regular, in: DefaultGlassEffectShape())

// built-in shapes
.glassEffect(.regular, in: .capsule)
.glassEffect(.regular, in: .circle)
.glassEffect(.regular, in: .ellipse)
.glassEffect(.regular, in: .rect(cornerRadius: 12))
.glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))

// adapts corner radius to parent container (for buttons in cards/sheets)
.glassEffect(.regular, in: .rect(cornerRadius: .containerConcentric))
```

## GlassEffectContainer

Groups multiple glass elements for seamless blending and morphing. **Glass cannot sample other glass**, so use this when elements are positioned closely.

```swift
GlassEffectContainer(spacing: 8) {  // spacing = merge threshold in points
    Button("One") { }
        .glassEffect()

    Button("Two") { }
        .glassEffect()
}
```

When elements are closer than `spacing`, they visually blend and morph together like water droplets.

### Rules
- Don't nest `GlassEffectContainer` inside another
- Don't place `Menu` inside `GlassEffectContainer` (breaks morphing in iOS 26.1)
- Don't use `.clipShape()` on glassEffect views

## glassEffectID - Morphing Transitions

Associates glass elements across states for fluid morphing animations. Requires `@Namespace` and `GlassEffectContainer`.

```swift
@Namespace var namespace
@State var expanded = false

GlassEffectContainer {
    if expanded {
        HStack {
            Button("Home") { }
                .glassEffect(.regular.interactive())
                .glassEffectID("home", in: namespace)

            Button("Settings") { }
                .glassEffect(.regular.interactive())
                .glassEffectID("settings", in: namespace)
        }
    } else {
        Button("Menu") { expanded = true }
            .glassEffect(.regular.interactive())
            .glassEffectID("menu", in: namespace)
    }
}
.animation(.easeInOut, value: expanded)
```

### Requirements for Morphing
1. Elements must be within the same `GlassEffectContainer`
2. Each view needs `glassEffectID` with shared namespace
3. Views must be conditionally shown/hidden
4. Animation must be applied to the state change
5. All morphing elements should use same Glass style and tint

## glassEffectUnion - Grouping Elements

Makes multiple elements appear as a **single glass shape** (like Apple Maps zoom controls).

```swift
@Namespace var ns

VStack(spacing: 0) {
    Button(action: { /* zoom in */ }) {
        Image(systemName: "plus")
    }
    .glassEffect(.regular.tint(.white.opacity(0.8)))
    .glassEffectUnion(id: "zoom", namespace: ns)

    Divider()

    Button(action: { /* zoom out */ }) {
        Image(systemName: "minus")
    }
    .glassEffect(.regular.tint(.white.opacity(0.8)))
    .glassEffectUnion(id: "zoom", namespace: ns)
}
```

### Requirements
All elements in a union must have:
- Same union id
- Same glass effect variant
- Same tint (color and opacity)

## UIKit Support

### UIGlassEffect

```swift
if #available(iOS 26.0, *) {
    let glassEffect = UIGlassEffect()
    let effectView = UIVisualEffectView(effect: glassEffect)
    effectView.frame = CGRect(x: 20, y: 100, width: 200, height: 50)
    view.addSubview(effectView)

    // add content to contentView
    let label = UILabel()
    label.text = "Glass Effect"
    effectView.contentView.addSubview(label)
}
```

### UIGlassContainerEffect - Merging Glass Views

```swift
if #available(iOS 26.0, *) {
    let containerEffect = UIGlassContainerEffect()
    containerEffect.spacing = 12  // merge distance threshold

    let containerView = UIVisualEffectView(effect: containerEffect)

    let glass1 = UIVisualEffectView(effect: UIGlassEffect())
    let glass2 = UIVisualEffectView(effect: UIGlassEffect())

    containerView.contentView.addSubview(glass1)
    containerView.contentView.addSubview(glass2)
}
```

### Corner Configuration

```swift
if #available(iOS 26.0, *) {
    let effectView = UIVisualEffectView(effect: UIGlassEffect())
    effectView.cornerConfiguration = UIViewCornerConfiguration(
        corners: .allCorners,
        cornerRadius: 16
    )
}
```

### UIHostingController Integration

When embedding SwiftUI glass in UIKit:
- Place in `navigationItem.titleView` (not `leftBarButtonItem`/`rightBarButtonItem`)
- Set `sizingOptions = [.intrinsicContentSize]`

## Backward Compatibility

The `Glass` type only exists on iOS 26+. Create wrappers with `#available`:

```swift
extension View {
    @ViewBuilder
    func applyGlassEffect() -> some View {
        if #available(iOS 26.0, *) {
            self.glassEffect()
        } else {
            self  // no-op on older iOS
        }
    }

    // with parameters - requires @available at call site
    @available(iOS 26.0, *)
    @ViewBuilder
    func applyGlassEffect(
        _ glass: Glass,
        in shape: some Shape = DefaultGlassEffectShape()
    ) -> some View {
        self.glassEffect(glass, in: shape)
    }
}
```

### Fallback for older iOS

```swift
if #available(iOS 26.0, *) {
    content.glassEffect()
} else {
    content.background(.ultraThinMaterial, in: .capsule)
}
```

## Design Guidelines

### When to Use
- Navigation elements (tab bars, toolbars, nav bars)
- Floating action buttons
- Control panels and overlays
- Search bars and input fields
- Modal/sheet presentations
- Interactive elements that sit "above" content

### When NOT to Use
- Core content (list rows, table cells)
- Card backgrounds with primary information
- Media-rich content areas
- Text-heavy sections
- Decorative elements with no function

### Best Practices
- Use `.interactive()` for buttons/controls on iOS
- Use `.tint()` only for semantic meaning
- Test in light mode, dark mode, and with "Reduce Transparency"
- Maintain 4.5:1 contrast ratio (WCAG AA)
- Use `.containerConcentric` corner radius for elements in containers
- Monitor performance in scrollable lists on older iPhones

## Known Issues

| Issue | Workaround |
|-------|------------|
| `Menu` in `GlassEffectContainer` breaks morphing (iOS 26.1) | Don't nest Menu in container |
| Morphing circle ↔ rectangle has glitches | Avoid drastically different shape transitions |
| `glassEffectID` inconsistent | Consider `.matchedGeometryEffect` as alternative |
| UIHostingController in bar items causes side effects | Use `titleView` instead |

## Button Styles

```swift
// translucent glass button
Button("Glass") { }
    .buttonStyle(.glass)

// opaque prominent glass button
Button("Prominent") { }
    .buttonStyle(.glassProminent)
```

## Tab Bar Behavior

```swift
// tab bar minimizes when scrolling down
.tabBarMinimizeBehavior(.onScrollDown)
```

## Resources

- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [GlassEffectContainer](https://developer.apple.com/documentation/swiftui/glasseffectcontainer)
- [WWDC 2025 Session 323: Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/)
- [WWDC 2025 Session 284: Build a UIKit app with the new design](https://developer.apple.com/videos/play/wwdc2025/284/)
- [WWDC 2025 Session 219: Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/)
