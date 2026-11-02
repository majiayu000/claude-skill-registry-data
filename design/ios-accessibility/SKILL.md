---
name: ios-accessibility
description: "Implements, reviews, or improves accessibility in iOS/macOS apps with SwiftUI and UIKit. Use when adding VoiceOver, Voice Control, Switch Control, or Full Keyboard Access support; when working with accessibility labels, hints, values, traits, or accessibilityInputLabels; when grouping or reordering accessibility elements; when managing focus with @AccessibilityFocusState or .focusable(); when supporting Dynamic Type with @ScaledMetric; when building custom rotors or accessibility actions; when writing automated accessibility tests with XCTest; when auditing a11y compliance; or when adapting UI for assistive technologies and system accessibility preferences."
---

# iOS Accessibility — SwiftUI and UIKit

Every user-facing view must be usable with VoiceOver, Switch Control, Voice Control, Full Keyboard Access, and other assistive technologies. This skill covers the patterns and APIs required to build accessible iOS apps.

## Contents

- [Core Principles](#core-principles)
- [How VoiceOver Reads Elements](#how-voiceover-reads-elements)
- [SwiftUI Accessibility Modifiers](#swiftui-accessibility-modifiers)
- [Focus Management](#focus-management)
- [Dynamic Type](#dynamic-type)
- [Custom Rotors](#custom-rotors)
- [System Accessibility Preferences](#system-accessibility-preferences)
- [Decorative Content](#decorative-content)
- [Voice Control](#voice-control)
- [Switch Control](#switch-control)
- [Full Keyboard Access](#full-keyboard-access)
- [Assistive Access (iOS 18+)](#assistive-access-ios-18)
- [UIKit Accessibility Patterns](#uikit-accessibility-patterns)
- [AppKit Accessibility Patterns](#appkit-accessibility-patterns)
- [Accessibility Custom Content](#accessibility-custom-content)
- [Testing Accessibility](#testing-accessibility)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

---

## Core Principles

1. Every interactive element MUST have an accessible label. If no visible text exists, add `.accessibilityLabel`.
2. Every custom control MUST have correct traits via `.accessibilityAddTraits` (never direct assignment).
3. Decorative images MUST be hidden from assistive technologies.
4. Sheet and dialog dismissals MUST return VoiceOver focus to the trigger element.
5. All tap targets MUST be at least 44x44 points.
6. Dynamic Type MUST be supported everywhere (system fonts, `@ScaledMetric`, adaptive layouts).
7. No information conveyed by color alone -- always provide text or icon alternatives.
8. System accessibility preferences MUST be respected: Reduce Motion, Reduce Transparency, Bold Text, Increase Contrast.

## How VoiceOver Reads Elements

VoiceOver reads element properties in a fixed, non-configurable order:

**Label -> Value -> Trait -> Hint**

Design your labels, values, and hints with this reading order in mind.

## SwiftUI Accessibility Modifiers

See [references/a11y-patterns.md](references/a11y-patterns.md) for detailed SwiftUI modifier examples (labels, hints, traits, grouping, custom controls, adjustable actions, and custom actions).

## Focus Management

Focus management is where most apps fail. When a sheet, alert, or popover is dismissed, VoiceOver focus MUST return to the element that triggered it.

This section is about accessibility focus for assistive technologies. For keyboard focus, directional focus, `focusSection()`, scene-focused values, and `UIFocusGuide`, use the `focus-engine` skill.

### @AccessibilityFocusState (iOS 15+)

`@AccessibilityFocusState` is a property wrapper that reads and writes the current accessibility focus. It works with `Bool` for single-target focus or an optional `Hashable` enum for multi-target focus.

```swift
struct ContentView: View {
    @State private var showSheet = false
    @AccessibilityFocusState private var focusOnTrigger: Bool

    var body: some View {
        Button("Open Settings") { showSheet = true }
            .accessibilityFocused($focusOnTrigger)
            .sheet(isPresented: $showSheet) {
                SettingsSheet()
                    .onDisappear {
                        // Slight delay allows the transition to complete before moving focus
                        Task { @MainActor in
                            try? await Task.sleep(for: .milliseconds(100))
                            focusOnTrigger = true
                        }
                    }
            }
    }
}
```

### Multi-Target Focus with Enum

```swift
enum A11yFocus: Hashable {
    case nameField
    case emailField
    case submitButton
}

struct FormView: View {
    @AccessibilityFocusState private var focus: A11yFocus?

    var body: some View {
        Form {
            TextField("Name", text: $name)
                .accessibilityFocused($focus, equals: .nameField)
            TextField("Email", text: $email)
                .accessibilityFocused($focus, equals: .emailField)
            Button("Submit") { validate() }
                .accessibilityFocused($focus, equals: .submitButton)
        }
    }

    func validate() {
        if name.isEmpty {
            focus = .nameField // Move VoiceOver to the invalid field
        }
    }
}
```

### Custom Modals

Custom overlay views need the `.isModal` trait to trap VoiceOver focus and an escape action for dismissal:

```swift
CustomDialog()
    .accessibilityAddTraits(.isModal)
    .accessibilityAction(.escape) { dismiss() }
```

### Accessibility Notifications (UIKit)

When you need to announce changes or move focus imperatively in UIKit contexts:

```swift
// Announce a status change (e.g., "Item deleted", "Upload complete")
UIAccessibility.post(notification: .announcement, argument: "Upload complete")

// Partial screen update -- move focus to a specific element
UIAccessibility.post(notification: .layoutChanged, argument: targetView)

// Full screen transition -- move focus to the new screen
UIAccessibility.post(notification: .screenChanged, argument: newScreenView)
```

## Dynamic Type

See [references/a11y-patterns.md](references/a11y-patterns.md) for Dynamic Type and adaptive layout examples, including @ScaledMetric and minimum tap target patterns.

## Custom Rotors

Rotors let VoiceOver users quickly navigate to specific content types. Add custom rotors for content-heavy screens. See [references/a11y-patterns.md](references/a11y-patterns.md) for complete rotor examples.

## System Accessibility Preferences

Always respect these environment values:

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion
@Environment(\.accessibilityReduceTransparency) var reduceTransparency
@Environment(\.colorSchemeContrast) var contrast         // .standard or .increased
@Environment(\.legibilityWeight) var legibilityWeight    // .regular or .bold
```

### Reduce Motion

Replace movement-based animations with crossfades or no animation:

```swift
withAnimation(reduceMotion ? nil : .spring()) {
    showContent.toggle()
}
content.transition(reduceMotion ? .opacity : .slide)
```

### Reduce Transparency, Increase Contrast, Bold Text

```swift
// Solid backgrounds when transparency is reduced
.background(reduceTransparency ? Color(.systemBackground) : Color(.systemBackground).opacity(0.85))

// Stronger colors when contrast is increased
.foregroundStyle(contrast == .increased ? .primary : .secondary)

// Bold weight when system bold text is enabled
.fontWeight(legibilityWeight == .bold ? .bold : .regular)
```

## Decorative Content

```swift
// Decorative images: hidden from VoiceOver
Image(decorative: "background-pattern")
Image("visual-divider").accessibilityHidden(true)

// Icon next to text: Label handles this automatically
Label("Settings", systemImage: "gear")

// Icon-only buttons: MUST have an accessibility label
Button(action: { }) {
    Image(systemName: "gear")
}
.accessibilityLabel("Settings")
```

## Voice Control

Voice Control relies on accessibility labels to generate spoken tap targets. If a label is missing or unspeakable, Voice Control cannot target the element.

- Every interactive element MUST have a speakable accessibility label (no emoji-only, no symbol-only).
- Labels must be unique within the visible screen — duplicate labels force users to disambiguate with overlay numbers.
- When the primary label is long or awkward to speak, provide shorter alternatives with `accessibilityInputLabels` (iOS 14+). Voice Control and Full Keyboard Access use these. List alternatives in descending order of importance.
- Test with Voice Control enabled: say "Show Names" and "Show Numbers" to verify all interactive elements are targetable.

See [references/a11y-patterns.md](references/a11y-patterns.md) for `accessibilityInputLabels` examples and speakable label guidelines.

## Switch Control

Switch Control scans accessibility elements sequentially in reading order. Proper grouping and custom actions are critical for usability.

- Group related content with `.accessibilityElement(children: .combine)` to reduce scan stops.
- Every scan target should be meaningful and actionable. Decorative elements hidden from VoiceOver are also hidden from Switch Control.
- Switch Control users cannot perform swipe-to-delete, long-press, or multi-finger gestures. Expose these interactions as `.accessibilityAction(named:)` custom actions instead — Switch Control presents them as a menu.
- Custom controls with non-standard hit areas should ensure `accessibilityFrame` accurately reflects the tappable region (for point scanning mode).

See [references/a11y-patterns.md](references/a11y-patterns.md) for custom action and grouping examples.

## Full Keyboard Access

Full Keyboard Access (iOS/iPadOS 13.4+) provides Tab/Shift-Tab navigation, arrow keys, Space/Enter activation, and Escape for dismissal. Standard SwiftUI controls are focusable by default.

- Tab order follows the accessibility element order.
- Use `.focusable()` (iOS 17+) to make custom views participate in the focus system. The `focusable(_:interactions:)` variant controls whether the view supports `.activate`, `.edit`, or both.
- Use `@FocusState` to track and programmatically move keyboard focus.
- Add `.keyboardShortcut()` to frequently used actions. Do not override system-defined shortcuts (Cmd+C, Cmd+V, Cmd+Tab, etc.).
- The system draws a focus ring automatically. Use `@FocusState` + `.focused($isFocused)` if a custom view needs to adjust its appearance when focused.

See [references/a11y-patterns.md](references/a11y-patterns.md) for `.focusable()`, `FocusInteractions`, keyboard shortcut, and multi-field focus examples.

## Assistive Access (iOS 18+)

Assistive Access provides a simplified interface for users with cognitive disabilities. Apps should support this mode:

```swift
// Check if Assistive Access is active (iOS 18+)
@Environment(\.accessibilityAssistiveAccessEnabled) var isAssistiveAccessEnabled

var body: some View {
    if isAssistiveAccessEnabled {
        SimplifiedContentView()
    } else {
        FullContentView()
    }
}
```

Key guidelines:
- Reduce visual complexity: fewer controls, larger tap targets, simpler navigation
- Use clear, literal language for labels and instructions
- Minimize the number of choices presented at once
- Test with Assistive Access enabled in Settings > Accessibility > Assistive Access

## UIKit Accessibility Patterns

When working with UIKit views:

- Set `isAccessibilityElement = true` on meaningful custom views.
- Set `accessibilityLabel` on all interactive elements without visible text.
- Use `.insert()` and `.remove()` for trait modification (not direct assignment).
- Set `accessibilityViewIsModal = true` on custom overlay views to trap focus.
- Post `.announcement` for transient status messages.
- Post `.layoutChanged` with a target view for partial screen updates.
- Post `.screenChanged` for full screen transitions.

```swift
// UIKit trait modification
customButton.accessibilityTraits.insert(.button)
customButton.accessibilityTraits.remove(.staticText)

// Modal overlay
overlayView.accessibilityViewIsModal = true
```

## AppKit Accessibility Patterns

AppKit accessibility uses `NSAccessibilityProtocol` and related role-specific protocols to describe accessible elements. Standard AppKit controls already provide much of this behavior; customize labels, values, roles, and actions only when the defaults are insufficient.

- Prefer standard AppKit controls first — they already expose accessibility metadata and notifications.
- For custom `NSView` subclasses, adopt the appropriate role-specific accessibility behavior and return the correct role, label, value, and actions.
- Use `NSAccessibilityElement` for accessible items that are not backed by their own `NSView`.
- Post `NSAccessibility` notifications when state changes need to be announced to assistive apps.

```swift
final class FavoriteToggleView: NSView {
    var isFavorite = false {
        didSet {
            NSAccessibility.post(element: self, notification: .valueChanged)
        }
    }

    override func isAccessibilityElement() -> Bool { true }
    override func accessibilityRole() -> NSAccessibility.Role? { .button }
    override func accessibilityLabel() -> String? { "Favorite" }
    override func accessibilityValue() -> Any? { isFavorite ? "On" : "Off" }

    override func accessibilityPerformPress() -> Bool {
        isFavorite.toggle()
        return true
    }
}
```

See [references/a11y-patterns.md](references/a11y-patterns.md) for AppKit examples including `NSAccessibilityElement` and announcement notifications.

## Accessibility Custom Content

See [references/a11y-patterns.md](references/a11y-patterns.md) for UIKit and AppKit accessibility patterns and custom content examples.

```swift
ProductRow(product: product)
    .accessibilityCustomContent("Price", product.formattedPrice)
    .accessibilityCustomContent("Rating", "\(product.rating) out of 5")
    .accessibilityCustomContent(
        "Availability",
        product.inStock ? "In stock" : "Out of stock",
        importance: .high  // .high reads automatically with the element
    )
```

## Testing Accessibility

### Manual Testing

- **Accessibility Inspector** (Xcode > Open Developer Tool): Audit views for missing labels, traits, and contrast issues. Run audits against the Simulator or connected device.
- **VoiceOver testing**: Enable in Settings > Accessibility > VoiceOver. Navigate every screen with swipe gestures.
- **Voice Control testing**: Enable in Settings > Accessibility > Voice Control. Say "Show Names" and "Show Numbers" to verify all elements are targetable.
- **Full Keyboard Access testing**: Enable in Settings > Accessibility > Keyboards > Full Keyboard Access. Tab through every screen and verify all interactive elements receive focus.
- **Switch Control testing**: Enable in Settings > Accessibility > Switch Control. Verify scan order is logical and custom actions appear for gesture-based interactions.
- **Dynamic Type**: Test with all text sizes in Settings > Accessibility > Display & Text Size > Larger Text.

### Automated Testing with XCTest

Use `XCUIElement` accessibility attributes to write UI tests that verify accessibility properties:

```swift
func testProductRowAccessibility() throws {
    let app = XCUIApplication()
    app.launch()

    let productCell = app.cells["product-organic-apples"]
    XCTAssertTrue(productCell.exists)
    XCTAssertTrue(productCell.isEnabled)

    // Verify the label is set and meaningful
    XCTAssertFalse(productCell.label.isEmpty)

    // Verify a specific element has the expected label
    let favoriteButton = productCell.buttons["Favorite"]
    XCTAssertTrue(favoriteButton.exists)
    XCTAssertTrue(favoriteButton.isEnabled)
}
```

Key `XCUIElementAttributes` properties for accessibility verification: `label`, `identifier`, `value`, `isEnabled`, `hasFocus`, `isSelected`, `placeholderValue`, `title`.

Test dismissal focus restoration:

```swift
func testSheetDismissReturnsFocus() throws {
    let app = XCUIApplication()
    app.launch()

    let triggerButton = app.buttons["Open Settings"]
    triggerButton.tap()

    // Dismiss the sheet
    let doneButton = app.buttons["Done"]
    doneButton.tap()

    // Verify focus returns to trigger (in accessibility-focused testing)
    XCTAssertTrue(triggerButton.hasFocus)
}
```

## Common Mistakes

1. **Direct trait assignment**: UIKit trait mutation or incorrect SwiftUI trait APIs can overwrite existing behavior. In SwiftUI, use `.accessibilityAddTraits(.isButton)`.
2. **Missing focus restoration**: Dismissing sheets without returning VoiceOver focus to the trigger element.
3. **Ungrouped list rows**: Multiple text elements per row create excessive swipe stops. Use `.accessibilityElement(children: .combine)`.
4. **Redundant trait in labels**: `.accessibilityLabel("Settings button")` reads as "Settings button, button." Omit the type.
5. **Missing labels on icon-only buttons**: Every `Image`-only button MUST have `.accessibilityLabel`.
6. **Ignoring Reduce Motion**: Always check `accessibilityReduceMotion` before movement animations.
7. **Fixed font sizes**: `.font(.system(size: 16))` ignores Dynamic Type. Use `.font(.body)` or similar text styles.
8. **Small tap targets**: Icons without `frame(minWidth: 44, minHeight: 44)` and `.contentShape()`.
9. **Color as sole indicator**: Red/green for error/success without text or icon alternatives.
10. **Missing `.isModal` on overlays**: Custom modals without `.accessibilityAddTraits(.isModal)` let VoiceOver escape.

## Review Checklist

For every user-facing view, verify:

- [ ] Every interactive element has an accessible label
- [ ] Custom controls use correct traits via `.accessibilityAddTraits`
- [ ] Decorative images are hidden (`Image(decorative:)` or `.accessibilityHidden(true)`)
- [ ] List rows group content with `.accessibilityElement(children: .combine)`
- [ ] Sheets and dialogs return focus to the trigger on dismiss
- [ ] Custom overlays have `.isModal` trait and escape action
- [ ] All tap targets are at least 44x44 points
- [ ] Dynamic Type supported (`@ScaledMetric`, system fonts, adaptive layouts)
- [ ] Reduce Motion respected (no movement animations when enabled)
- [ ] Reduce Transparency respected (solid backgrounds when enabled)
- [ ] Increase Contrast respected (stronger foreground colors)
- [ ] No information conveyed by color alone
- [ ] Custom actions provided for swipe-to-reveal and context menu features
- [ ] Icon-only buttons have labels
- [ ] Heading traits set on section headers
- [ ] Custom accessibility types and notification payloads are `Sendable` when passed across concurrency boundaries
- [ ] Labels are speakable and unique for Voice Control (no emoji-only or duplicate labels on screen)
- [ ] `accessibilityInputLabels` provided for elements with long or awkward primary labels
- [ ] Gesture-based interactions (swipe-to-delete, long-press) have accessibility custom action equivalents for Switch Control
- [ ] Custom views use `.focusable()` when they should participate in Full Keyboard Access navigation
- [ ] System keyboard shortcuts are not overridden

## References

- [references/a11y-patterns.md](references/a11y-patterns.md) — SwiftUI and UIKit modifier examples, grouping, custom actions, rotors, Dynamic Type
- [references/nutrition-labels.md](references/nutrition-labels.md) — App Store Accessibility Nutrition Labels: all 9 categories with pass/fail criteria
- [references/media-accessibility.md](references/media-accessibility.md) — Captions, audio descriptions, AVMediaCharacteristic, SDH

