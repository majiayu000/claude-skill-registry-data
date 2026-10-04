---
license: Apache-2.0
name: ios-app-beauty
description: Makes iOS apps feel premium, polished, and unmistakably native — SF Symbols mastery, SwiftUI spring animations, haptic feedback choreography, blur/vibrancy materials, Dynamic Type, color system design, and the specific spacings and radii Apple uses. This is about TASTE, not syntax. Activate on 'iOS design polish', 'SwiftUI animation', 'SF Symbols', 'haptic feedback', 'premium iOS feel', 'Apple HIG', 'native iOS look', 'Liquid Glass', 'iOS visual design', 'app polish'.
allowed-tools: Read,Write,Edit,Glob,Grep,WebSearch,WebFetch
metadata:
  category: Design & UX
  tags:
    - ios
    - swiftui
    - design
    - sf-symbols
    - haptics
    - animation
    - apple-hig
    - polish
  pairs-with:
    - skill: native-app-designer
      reason: Architecture and platform patterns complement visual polish
    - skill: sound-engineer
      reason: Audio feedback pairs with haptics for multi-sensory experience
    - skill: mobile-ux-optimizer
      reason: Performance optimization ensures animations stay smooth
    - skill: vaporwave-glassomorphic-ui-designer
      reason: Glass and blur effects share material design vocabulary
category: Mobile Development
tags:
  - ios
  - design
  - beauty
  - polish
  - apple-hig
---

# iOS App Beauty

The difference between a functional iOS app and a beautiful one is not more features. It is the weight of a toolbar icon matching the weight of the nav title. It is a spring animation that overshoots by exactly 4% before settling. It is a haptic tap that arrives at the precise millisecond a toggle lands. This skill is about the thousand tiny decisions that make an iOS app feel like it belongs on the platform.

## When to Use This Skill

**Use for:**
- Polishing an existing iOS app to feel premium
- Designing a new app's visual language and motion system
- SF Symbol selection, weight matching, and rendering modes
- SwiftUI animation tuning (springs, timing, choreography)
- Haptic feedback design and when/where to use it
- Color system design for light/dark/tinted modes
- Blur, vibrancy, and material effects
- The "last 10%" polish that separates good from great

**Do NOT use for:**
- SwiftUI syntax tutorials or API reference
- Backend architecture or networking
- Cross-platform design (Flutter, React Native)
- Android Material Design (different philosophy entirely)

## The Apple Design Sensibility

Apple's design language has a set of unwritten rules that the best apps internalize:

### The Hierarchy of Polish

```
Level 1: It works               → Functional
Level 2: It looks right          → Correct (follows HIG)
Level 3: It feels right          → Native (motion, haptics, spacing)
Level 4: It feels inevitable     → Premium (Things 3, Halide, Bear)
```

Most apps stop at Level 2. This skill gets you to Level 4.

### What "Premium" Actually Means on iOS

Premium iOS apps share these qualities:
- **Restraint** — fewer elements, more whitespace, deliberate emptiness
- **Weight consistency** — icons, text, and controls feel like they belong together
- **Physicality** — elements have mass, springs have tension, gestures have momentum
- **Quietness** — the app doesn't shout; it whispers and you lean in
- **Surprise in the details** — a subtle parallax, an unexpected haptic, a delightful transition

**Reference apps to study:**
- **Things 3** — the gold standard of iOS task management; drag interactions, subtle shadows, spacing
- **Bear** — typography-first design, beautiful markdown rendering, tag system UX
- **Halide** — camera controls modeled on real hardware dials, gesture-driven, one-thumb operation
- **Flighty** — data visualization as art, live activity design, progressive information disclosure
- **Denim** — SwiftUI-native, mesh gradients, smooth scroll transitions (2025 Apple Design Award)
- **Linear** (macOS) — keyboard-first, animation choreography, information density done right
- **Arc** — tab management reimagined, spatial UI, bold use of color

## SF Symbols Mastery

### Weight Matching

SF Symbols come in 9 weights (ultralight through black). The weight of your icons MUST match the weight of adjacent text.

```swift
// WRONG: Default (regular) icon next to semibold text
Label("Settings", systemImage: "gear")
    .font(.headline) // headline is semibold

// RIGHT: Match the icon weight to the text weight
Label {
    Text("Settings").font(.headline)
} icon: {
    Image(systemName: "gear")
        .fontWeight(.semibold)
}
```

| Text Style | Font Weight | SF Symbol Weight |
|------------|-------------|-----------------|
| `.largeTitle` | Regular | `.regular` |
| `.headline` | Semibold | `.semibold` |
| `.body` | Regular | `.regular` |
| `.caption` | Regular | `.regular` |
| `.title3` + `.bold()` | Bold | `.bold` |

### Rendering Modes

SF Symbols support four rendering modes. Choosing the right one is a design decision, not a technical one.

```swift
// Monochrome — single color, most common, cleanest
Image(systemName: "heart.fill")
    .symbolRenderingMode(.monochrome)

// Hierarchical — primary/secondary opacity, adds depth
Image(systemName: "square.and.arrow.up")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.blue)

// Palette — explicit colors per layer, bold statements
Image(systemName: "person.crop.circle.badge.plus")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.white, .blue)

// Multicolor — Apple's predefined colors, use for system icons
Image(systemName: "externaldrive.badge.icloud")
    .symbolRenderingMode(.multicolor)
```

**When to use which:**
- **Monochrome**: Toolbars, tab bars, list accessories — anywhere icons should recede
- **Hierarchical**: Navigation elements, empty states — when you want subtle depth
- **Palette**: Highlights, badges, selected states — when the icon IS the content
- **Multicolor**: System-like interfaces, settings — when matching Apple's own style

### Symbol Effects (iOS 17+)

Animated symbols are the single biggest upgrade in recent iOS design. They replace manual animations for common interactions.

```swift
// Bounce on tap — satisfying micro-interaction
Image(systemName: "heart.fill")
    .symbolEffect(.bounce, value: isFavorited)

// Pulse while loading — alive without being distracting
Image(systemName: "arrow.down.circle")
    .symbolEffect(.pulse, isActive: isDownloading)

// Variable color for progress — elegant loading indicator
Image(systemName: "wifi")
    .symbolEffect(.variableColor.iterative, isActive: isConnecting)

// Replace with transition — icon morphing
Image(systemName: isMuted ? "speaker.slash" : "speaker.wave.2")
    .contentTransition(.symbolEffect(.replace))

// Scale on appear — entrance animation
Image(systemName: "checkmark.circle.fill")
    .symbolEffect(.appear, isActive: showCheck)
```

### Symbol Sizing

Never hardcode icon sizes. Use `imageScale` to match the text environment.

```swift
// Let the symbol scale with Dynamic Type
Image(systemName: "star.fill")
    .imageScale(.medium) // .small, .medium, .large

// For custom sizing that still respects accessibility
Image(systemName: "star.fill")
    .font(.system(size: 24))
```

## SwiftUI Animation & Spring Physics

### The Spring System

Springs are the foundation of natural iOS motion. Every animation that moves an element should use a spring, not a linear or ease curve.

```swift
// Apple's built-in presets (use these first)
.animation(.spring, value: offset)                    // Default — good for most
.animation(.snappy, value: offset)                    // Quick settle — toggles, switches
.animation(.bouncy, value: offset)                    // Playful — celebrations, fun UI
.animation(.smooth, value: offset)                    // No bounce — serious/professional

// Custom spring — when presets aren't right
.animation(.spring(
    response: 0.35,        // Duration feel (seconds) — lower = faster
    dampingFraction: 0.7,  // 0 = infinite bounce, 1 = no bounce
    blendDuration: 0       // Transition between animations
), value: offset)
```

### Spring Tuning Reference

| Context | Response | Damping | Feel |
|---------|----------|---------|------|
| Toggle/switch | 0.25 | 0.8 | Snappy, decisive |
| Sheet presentation | 0.35 | 0.75 | Smooth, weighted |
| Card expand | 0.4 | 0.7 | Satisfying settle |
| Bounce celebration | 0.5 | 0.5 | Playful overshoot |
| Drag release | 0.3 | 0.65 | Elastic snap-back |
| Page transition | 0.45 | 0.85 | Cinematic, smooth |
| Pull-to-refresh | 0.35 | 0.6 | Springy, physical |
| Keyboard-driven nav | 0.2 | 0.9 | Instant, no play |

### Animation Choreography

The secret to premium animation is not one animation — it is multiple animations happening at slightly different times with slightly different springs.

```swift
// Staggered list appearance
ForEach(Array(items.enumerated()), id: \.element.id) { index, item in
    ItemRow(item: item)
        .opacity(appeared ? 1 : 0)
        .offset(y: appeared ? 0 : 20)
        .animation(
            .spring(response: 0.4, dampingFraction: 0.8)
            .delay(Double(index) * 0.05), // 50ms stagger
            value: appeared
        )
}

// Multi-property choreography — each property has its own timing
struct ExpandingCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            // Scale arrives first (fast spring)
            RoundedRectangle(cornerRadius: isExpanded ? 16 : 24)
                .animation(.spring(response: 0.3, dampingFraction: 0.7), value: isExpanded)

            // Content fades in slightly after
            if isExpanded {
                Text("Details here")
                    .transition(.opacity.combined(with: .move(edge: .bottom)))
                    .animation(.spring(response: 0.4, dampingFraction: 0.8), value: isExpanded)
            }
        }
    }
}
```

### Phase Animator (iOS 17+)

For multi-step animations that cycle through states:

```swift
PhaseAnimator([false, true]) { phase in
    Image(systemName: "bell.fill")
        .rotationEffect(.degrees(phase ? 15 : -15))
        .scaleEffect(phase ? 1.2 : 1.0)
} animation: { phase in
    .spring(response: 0.2, dampingFraction: 0.3)
}
```

## Haptic Feedback Design

### The Haptic Vocabulary

iOS has a specific haptic language. Using the wrong haptic is like using the wrong word — technically functional but feels wrong.

```swift
// IMPACT — physical collisions and weight
// Use when: elements land, snap into place, hit boundaries
UIImpactFeedbackGenerator(style: .light)    // Subtle snap (toggle)
UIImpactFeedbackGenerator(style: .medium)   // Solid tap (button press)
UIImpactFeedbackGenerator(style: .heavy)    // Thud (drag drop, significant action)
UIImpactFeedbackGenerator(style: .soft)     // Cushioned (elastic stretch)
UIImpactFeedbackGenerator(style: .rigid)    // Sharp click (precise selection)

// SELECTION — moving through discrete values
// Use when: scrubbing a picker, scrolling through options, cursor on grid
UISelectionFeedbackGenerator()              // Tick-tick-tick

// NOTIFICATION — semantic outcomes
// Use when: action completes with a result
UINotificationFeedbackGenerator().notificationOccurred(.success) // Completed
UINotificationFeedbackGenerator().notificationOccurred(.warning) // Caution
UINotificationFeedbackGenerator().notificationOccurred(.error)   // Failed
```

### SwiftUI Sensory Feedback (iOS 17+)

```swift
// Modern declarative haptics
Button("Save") { save() }
    .sensoryFeedback(.success, trigger: saveCompleted)

Toggle("Notifications", isOn: $notificationsOn)
    .sensoryFeedback(.selection, trigger: notificationsOn)

// Impact on drag threshold
    .sensoryFeedback(.impact(weight: .heavy), trigger: didCrossThreshold)
```

### Haptic Timing Rules

| Action | Haptic | Timing |
|--------|--------|--------|
| Button press | `.impact(.light)` | On touch down, not release |
| Toggle flip | `.selection` | At the flip point |
| Delete swipe | `.impact(.medium)` | When action commits |
| Pull-to-refresh release | `.impact(.light)` | When content snaps back |
| Long press menu | `.impact(.heavy)` | When menu appears |
| Picker scroll | `.selection` | Each value change |
| Success state | `.notification(.success)` | With the checkmark animation |
| Error state | `.notification(.error)` | With the shake animation |
| Drag snap to grid | `.impact(.rigid)` | At each grid line |

### Core Haptics for Custom Patterns

When built-in haptics aren't enough:

```swift
import CoreHaptics

func playSuccessPattern() {
    guard CHHapticEngine.capabilitiesForHardware().supportsHaptics else { return }

    let engine = try? CHHapticEngine()
    try? engine?.start()

    // Two-tap celebration pattern
    let tap1 = CHHapticEvent(
        eventType: .hapticTransient,
        parameters: [
            CHHapticEventParameter(parameterID: .hapticIntensity, value: 0.6),
            CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.4)
        ],
        relativeTime: 0
    )
    let tap2 = CHHapticEvent(
        eventType: .hapticTransient,
        parameters: [
            CHHapticEventParameter(parameterID: .hapticIntensity, value: 1.0),
            CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.8)
        ],
        relativeTime: 0.1 // 100ms after first tap
    )

    let pattern = try? CHHapticPattern(events: [tap1, tap2], parameters: [])
    let player = try? engine?.makePlayer(with: pattern!)
    try? player?.start(atTime: 0)
}
```

## Color System Design

### Asset Catalog Structure

```
Colors.xcassets/
├── Brand/
│   ├── Primary          → Light: #1A1A2E  Dark: #E8E8F0
│   ├── Secondary        → Light: #4A90D9  Dark: #6BB5FF
│   └── Accent           → Light: #FF6B35  Dark: #FF8F5E
├── Semantic/
│   ├── Background       → Light: #FFFFFF  Dark: #000000
│   ├── Surface          → Light: #F5F5F7  Dark: #1C1C1E
│   ├── SurfaceElevated  → Light: #FFFFFF  Dark: #2C2C2E
│   ├── TextPrimary      → Light: #1D1D1F  Dark: #F5F5F7
│   ├── TextSecondary    → Light: #86868B  Dark: #98989D
│   └── Separator        → Light: #D2D2D7  Dark: #38383A
└── State/
    ├── Success          → Light: #34C759  Dark: #30D158
    ├── Warning          → Light: #FF9F0A  Dark: #FFD60A
    └── Destructive      → Light: #FF3B30  Dark: #FF453A
```

### Apple's Color Philosophy

- **Never use pure black (#000000) for text in light mode.** Apple uses #1D1D1F — it is softer.
- **Never use pure white (#FFFFFF) for backgrounds in dark mode.** Apple uses #000000 for OLED true black (saves battery) and #1C1C1E for elevated surfaces.
- **Semantic colors over hardcoded values.** Use `.primary`, `.secondary`, `.label`, `.systemBackground` before creating custom colors.
- **Vibrancy > opacity for overlays.** Use `.ultraThinMaterial` instead of `Color.black.opacity(0.5)`.

```swift
// Apple's material system — automatically adapts to light/dark
.background(.ultraThinMaterial)    // Barely there — navigation bars
.background(.thinMaterial)         // Subtle — sidebars
.background(.regularMaterial)      // Standard — sheets, popovers
.background(.thickMaterial)        // Heavy — overlays on busy content
.background(.ultraThickMaterial)   // Opaque — near-solid backgrounds
```

## Spacing, Padding, and Corner Radii

### Apple's Spacing Scale

Apple uses an 8-point grid. Every spacing value should be a multiple of 4, with 8 as the standard unit.

```swift
// The spacing scale
let spacingXS:    CGFloat = 4    // Tight: between icon and label
let spacingS:     CGFloat = 8    // Compact: between related elements
let spacingM:     CGFloat = 12   // Standard: list row internal padding
let spacingL:     CGFloat = 16   // Comfortable: section padding, card insets
let spacingXL:    CGFloat = 20   // Roomy: between sections
let spacingXXL:   CGFloat = 24   // Generous: screen-edge margins (iPhone)
let spacingXXXL:  CGFloat = 32   // Spacious: hero section spacing
```

### Corner Radius Reference

```swift
// Apple's actual corner radii (measured from system apps)
let radiusSmall:     CGFloat = 6    // Small chips, tags
let radiusStandard:  CGFloat = 10   // Buttons, text fields
let radiusMedium:    CGFloat = 12   // Cards, list rows
let radiusLarge:     CGFloat = 16   // Sheets, larger cards
let radiusXLarge:    CGFloat = 20   // Modals, group containers
let radiusScreen:    CGFloat = 38.5 // iPhone 15 Pro screen radius (for continuous corners)

// CRITICAL: Use continuous corner style, not circular
.clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
// NOT: .cornerRadius(16) — this uses circular corners which look off on iOS
```

### The Continuous Corner Rule

Apple uses **continuous (superellipse) corners** everywhere, not circular corners. This is the single most common mistake in third-party iOS apps.

```swift
// WRONG — circular corners (looks like Android)
.clipShape(RoundedRectangle(cornerRadius: 12))

// RIGHT — continuous corners (looks like Apple)
.clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
```

## Dynamic Type and Accessibility as Beauty

Great iOS apps look BETTER with large text, not worse. This is a design skill, not just an accessibility checkbox.

```swift
// Scale with Dynamic Type — text and spacing
@ScaledMetric var iconSize: CGFloat = 24
@ScaledMetric var cardPadding: CGFloat = 16

// Test at ALL sizes: Settings > Accessibility > Larger Text
// Your layout should be beautiful at AX5 (the largest), not just default
```

**Rules:**
- Never hardcode font sizes. Use text styles (`.body`, `.headline`, `.caption`).
- Test at the 5 largest accessibility sizes. If your layout breaks, fix the layout, not the text.
- Images and icons should scale with `@ScaledMetric`.
- Minimum tap target: 44x44 points (Apple HIG). Aim for 48x48.

## Liquid Glass (iOS 26 / 2025)

Apple's newest visual language emphasizes translucency and depth:

```swift
// Liquid Glass material — the new standard
.background(.liquidGlass)

// Key characteristics:
// - Translucent with refraction-like effects
// - Content behind affects appearance (not flat tint)
// - Rounded, fluid shapes (continuous corners everywhere)
// - Depth-aware: modals float above, toolbars recede

// Adapting to Liquid Glass:
// - Reduce opacity of decorative elements
// - Let content shine through navigation
// - Use system materials instead of custom blurs
// - Test with varied background content (photos, text, solid colors)
```

## Anti-Patterns

### Circular Corners on iOS
**What it looks like:** Standard CSS-style border-radius
**Why it's wrong:** Every Apple element uses continuous (superellipse) corners. Circular corners look foreign.
**Fix:** Always use `RoundedRectangle(cornerRadius: r, style: .continuous)`

### Mismatched Icon Weights
**What it looks like:** Thin SF Symbols next to bold text, or vice versa
**Why it's wrong:** Creates visual tension; elements don't feel like they belong together
**Fix:** Match SF Symbol `.fontWeight()` to the text style weight

### Linear Animations
**What it looks like:** Elements that move at constant speed, stop abruptly
**Why it's wrong:** Nothing in the physical world moves linearly. It feels robotic.
**Fix:** Use `.spring` or `.snappy` for movement, `.easeOut` only for opacity

### Haptic Spam
**What it looks like:** Haptic feedback on every scroll, every tap, every state change
**Why it's wrong:** Overwhelms the sense; user becomes numb to meaningful haptics
**Fix:** Haptics only at decision points, state changes, and physical metaphors

### Dark Mode as an Afterthought
**What it looks like:** White text on #1A1A1A with the same assets as light mode
**Why it's wrong:** Dark mode needs elevated surfaces, adjusted contrast ratios, and muted colors
**Fix:** Design dark mode FIRST, then adapt to light. Use Asset Catalog with appearance variants.

### Over-Decorating Empty States
**What it looks like:** Massive illustrations, long paragraphs explaining what the empty state means
**Why it's wrong:** Empty states should invite action, not explain failure
**Fix:** One icon, one line, one button: "No messages yet. Start a conversation."

## Quality Checklist

Before considering any iOS screen "finished":

- [ ] SF Symbol weights match adjacent text weights
- [ ] All corners use `.continuous` style
- [ ] Every moving element uses spring animation (no linear, no ease-in-out)
- [ ] Haptic feedback at key interaction moments (not every tap)
- [ ] Works beautifully at AX5 Dynamic Type size
- [ ] Dark mode designed intentionally, not inverted
- [ ] Minimum 44x44pt tap targets
- [ ] Spacing follows 8-point grid (4pt minimum increment)
- [ ] Materials used for overlays (not `Color.black.opacity(0.5)`)
- [ ] Content visible through any translucent element
- [ ] Navigation feels native (system back, swipe gestures work)
- [ ] No custom loading spinners (use system `ProgressView`)
- [ ] Empty states have clear call to action
- [ ] Screenshot looks like it belongs on the App Store
