---
name: ios-design
description: Create distinctive, production-grade iOS interfaces with SwiftUI. Use this skill when the user asks to build iOS screens, components, or views. Generates polished, native-feeling code that goes beyond generic templates while respecting Apple's Human Interface Guidelines.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade iOS interfaces using SwiftUI. Implement real working code with exceptional attention to aesthetic details and creative choices that feel authentically Apple while maintaining unique character.

The user provides iOS UI requirements: a screen, component, view, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a clear aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it? What's the core user action?
- **Tone**: Pick a direction that fits: elegant/refined, playful/vibrant, professional/serious, warm/friendly, bold/striking, calm/meditative, energetic/dynamic, luxurious/premium, approachable/casual, focused/minimal
- **Context**: Where does this screen live in the app flow? What comes before/after?
- **Differentiation**: What makes this interface memorable? What's the signature detail?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. The best iOS apps have a consistent personality that users can feel.

Then implement working SwiftUI code that is:
- Production-grade and functional
- Visually refined and memorable
- Cohesive with Apple's design language while having unique character
- Meticulously polished in every detail

## iOS Design Principles

### Typography
- **SF Pro** is the system default - use it intentionally with proper weights and optical sizes
- Use **Dynamic Type** (`Font.body`, `Font.headline`, etc.) for accessibility
- Create hierarchy through weight contrast (Ultralight to Black) rather than just size
- Consider **SF Pro Rounded** for friendlier interfaces
- Custom fonts: Choose distinctive display fonts for headers, keep body text readable
- Respect text scaling - your layouts must adapt to accessibility sizes

### Color & Theme
- **Semantic colors** first: `Color.primary`, `Color.secondary`, `Color.accentColor`
- Define a signature accent color that becomes the app's identity
- Use **Asset Catalogs** with light/dark variants for all custom colors
- Gradients: Linear and angular gradients add depth - use sparingly but boldly
- Vibrancy and materials: `.ultraThinMaterial`, `.regularMaterial` for layered depth
- Avoid flat, lifeless backgrounds - add subtle texture or gradient

### Dark Mode
- **Mandatory**: Every view must look intentional in both light and dark modes
- Dark mode is not just "inverted colors" - it's a separate design exercise
- Use `Color(.systemBackground)` hierarchy: primary, secondary, tertiary
- Ensure sufficient contrast - test with Accessibility Inspector
- Consider OLED-friendly true blacks where appropriate

### Motion & Animation
SwiftUI's animation system is powerful - use it thoughtfully:
- **withAnimation** for state changes with `.spring()`, `.easeInOut`, `.interpolatingSpring()`
- **matchedGeometryEffect** for hero transitions between views
- **phaseAnimator** and **keyframeAnimator** (iOS 17+) for complex sequences
- Micro-interactions: button presses (`.scaleEffect`), toggle feedback, loading states
- Page transitions: `.transition(.asymmetric(...))` for entering/exiting
- Scroll effects: `.scrollTransition`, parallax, sticky headers
- **Haptics**: `UIImpactFeedbackGenerator` for tactile feedback on key actions

**Timing matters**: Quick (0.2s) for feedback, medium (0.35s) for transitions, slow (0.5s+) for dramatic reveals.

### Spatial Composition
- **Safe Areas**: Respect them, but know when to edge-bleed for impact
- **Padding**: Use consistent spacing (8pt grid). `padding()` defaults are often too tight
- Embrace **negative space** - cramped UIs feel cheap
- **Cards and surfaces**: Rounded corners (12-20pt), subtle shadows, layered depth
- **Full-bleed images**: Let photos breathe edge-to-edge
- Consider **asymmetry** for visual interest while maintaining functional clarity

### SF Symbols
Apple's icon system is extensive and expressive:
- Use **hierarchical** and **multicolor** rendering modes
- Apply **variable color** for animated states (e.g., Wi-Fi strength)
- Symbol effects: `.bounce`, `.pulse`, `.variableColor`, `.replace`
- Custom symbols: Create when needed, but prefer built-in for consistency
- Size symbols relative to text with `Font.system(size:).weight()`

### Native Components Done Right
Elevate standard components beyond defaults:
- **Lists**: Custom row designs, swipe actions, section headers with personality
- **Navigation**: Large titles, custom back buttons, toolbar items
- **Sheets**: Detents (`.presentationDetents`), custom backgrounds
- **Buttons**: Beyond `.bordered` - custom shapes, gradients, press states
- **Text Fields**: Floating labels, inline validation, character counts
- **Tab Bars**: Custom icons, badges, selection indicators

### Gestures & Interactions
- **DragGesture** for swipe-to-dismiss, card stacks, sliders
- **LongPressGesture** with preview/context menus
- **MagnificationGesture** for zoom interactions
- Combine gestures with `.simultaneously` and `.sequenced`
- Always provide visual feedback during gesture

## Anti-Patterns to Avoid

NEVER create generic iOS interfaces with:
- Unstyled default components without customization
- Flat, solid color backgrounds with no depth
- Missing dark mode support
- Ignoring Dynamic Type and accessibility
- Web-like layouts that don't feel native
- Overuse of SF Symbols without consideration
- Animations that feel slow or janky
- Cramped layouts without breathing room
- Inconsistent corner radii and spacing

## Implementation Approach

1. **Structure first**: Define the view hierarchy and data flow
2. **Layout foundation**: Establish spacing, safe areas, scroll behavior
3. **Visual layer**: Colors, typography, shapes, materials
4. **Animation layer**: State transitions, micro-interactions
5. **Polish pass**: Shadows, haptics, edge cases, accessibility

Remember: The best iOS apps feel inevitable - as if they could only exist on Apple's platform. Embrace SwiftUI's declarative nature, leverage platform capabilities, and create interfaces that users will love to interact with.

## Code Quality

- Use `@ViewBuilder` for complex conditional views
- Extract reusable components into separate files
- Prefer composition over inheritance
- Use `PreviewProvider` with multiple configurations (dark mode, large text, etc.)
- Consider `@Environment` for propagating design tokens
- Keep views focused - if it's doing too much, split it
