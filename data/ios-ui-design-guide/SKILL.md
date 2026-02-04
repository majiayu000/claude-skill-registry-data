---
name: ios-ui-design-guide
description: Apply iOS/SwiftUI design principles following Apple Human Interface Guidelines when building any iOS UI component. Only execute this when the current project is an iOS project and involves UI-related work. Use this skill for SwiftUI views, UIKit components, or iOS app development. Ensures HIG compliance with Clarity, Deference, and Depth principles, system colors with Dark Mode support, 8pt grid spacing, SF Pro typography with Dynamic Type, and native iOS interaction patterns. Prevents common anti-patterns like fixed text sizes, Dark Mode neglect, and Safe Area violations.
---

# iOS UI Design Guide

## Overview

Build native iOS interfaces that look professional and follow Apple Human Interface Guidelines (HIG) by applying systematic design principles. This skill provides comprehensive guidelines for SwiftUI-first development with color system, spacing, typography, and component-specific patterns optimized for iOS.

## When to Use This Skill

Activate this skill when:
- Building iOS UI with SwiftUI or UIKit
- Creating iOS app screens, views, or components
- Working with iOS development (Swift, SwiftUI, Xcode)
- Receiving requests like:
  - "Create a login screen in SwiftUI"
  - "Design an iOS settings view"
  - "Build a profile card for iOS"
  - "Make this iOS UI follow HIG"
  - "Style this SwiftUI view"

**Do NOT activate** for:
- Web development
- Android development
- Backend/server code
- Non-visual iOS tasks

## Core Design Philosophy

Follow Apple Human Interface Guidelines (HIG) three principles + Flexible extensions:

### HIG Core Principles

1. **Clarity (명료성)** - Content and functionality clearly visible and understandable
2. **Deference (존중)** - UI helps content without competing with it
3. **Depth (깊이)** - Visual layers and motion convey hierarchy and meaning

### Flexible Extensions

4. **Simplicity** - Remove unnecessary elements, focus on core features
5. **Consistency** - Use system components, colors, and fonts
6. **Accessibility-First** - Dynamic Type, VoiceOver, WCAG AA compliance, Dark Mode

## Framework Priorities

- **Primary**: SwiftUI (declarative, modern, recommended)
- **Secondary**: UIKit (complex animations, legacy integration)

## How to Use This Skill

### Step 1: Load Relevant Reference

Before implementing any iOS UI component, load the appropriate reference file:

```
Read references/design-principles.md - HIG core principles + Flexible extensions
Read references/color-system.md - System colors, Dark Mode, semantic colors
Read references/spacing-system.md - 8pt grid, Safe Area handling
Read references/typography.md - SF Pro, Dynamic Type, text styles
Read references/component-patterns.md - SwiftUI component best practices
Read references/anti-patterns.md - Common iOS design mistakes
```

**Recommendation**: Start with `design-principles.md` for HIG philosophy, then load component-specific files as needed.

### Step 2: Apply Component-Specific Patterns

For each component type, reference the corresponding section in `component-patterns.md`:

- **Button**: `component-patterns.md` → Button section
- **List**: `component-patterns.md` → List section
- **Form**: `component-patterns.md` → Form section
- **Navigation**: `component-patterns.md` → Navigation section
- **Card**: `component-patterns.md` → Card section
- **Modal/Sheet**: `component-patterns.md` → Modal section
- **Search**: `component-patterns.md` → Search section
- **Image**: `component-patterns.md` → Image section

### Step 3: Validate Against Anti-Patterns

Before finalizing implementation, check `anti-patterns.md` to ensure the design avoids:

- ❌ Fixed text sizes (no Dynamic Type support)
- ❌ Dark Mode neglect (hardcoded colors like `.black`, `.white`)
- ❌ Safe Area violations (content hidden by notch/home indicator)
- ❌ Touch targets smaller than 44x44pt
- ❌ Ignoring system components
- ❌ Multiple Primary buttons

### Step 4: Ensure System Consistency

Apply the **8pt grid system** for all spacing:
- Use only: 4pt (rare), 8pt, 12pt, 16pt, 20pt, 24pt, 32pt, 40pt, 48pt, 64pt
- SwiftUI default `.padding()` = 16pt
- Reference `spacing-system.md` for component-specific spacing

Use **system colors** for automatic Dark Mode:
- Labels: `.primary`, `.secondary`, `Color(.tertiaryLabel)`
- Backgrounds: `Color(.systemBackground)`, `Color(.secondarySystemBackground)`
- ONE accent color via `.accentColor()` or project settings
- Reference `color-system.md` for detailed color usage

Maintain **Dynamic Type support** (REQUIRED):
- Text styles: `.largeTitle`, `.title`, `.title2`, `.title3`, `.headline`, `.body`, `.callout`, `.subheadline`, `.footnote`, `.caption`, `.caption2`
- NEVER use fixed `.font(.system(size: 24))` without `relativeTo`
- Reference `typography.md` for complete type scale

## Resources

### references/

Documentation loaded into context as needed to inform design decisions:

- **design-principles.md** - HIG principles (Clarity, Deference, Depth) + Flexible extensions (Simplicity, Consistency, Accessibility)
- **color-system.md** - System colors, Dark Mode support, semantic colors, adaptive colors, custom colors with Asset Catalog
- **spacing-system.md** - 8pt grid scale, Safe Area handling, SwiftUI padding modifiers, component spacing
- **typography.md** - SF Pro font, Dynamic Type (REQUIRED), text styles, font weights, accessibility
- **component-patterns.md** - SwiftUI patterns for Button, List, Form, Navigation, Card, Modal, Search, Image, Progress, Badge
- **anti-patterns.md** - Common iOS mistakes: fixed text, Dark Mode neglect, Safe Area violations, touch targets, system component neglect

## Quick Decision Tree

```
iOS UI Component Request
│
├─ What component? → Load component-patterns.md section
│
├─ What spacing? → Use 8pt grid (spacing-system.md)
│
├─ What colors? → System colors + Dark Mode (color-system.md)
│
├─ What typography? → Dynamic Type text styles (typography.md)
│
├─ SwiftUI or UIKit? → SwiftUI first (unless specific UIKit need)
│
└─ Validation → Check anti-patterns.md
```

## Examples

**Good Request Flow**:
```
User: "Create a login form in SwiftUI"
→ Read references/component-patterns.md (Form section)
→ Read references/spacing-system.md (Form spacing)
→ Apply: TextField with .body font (Dynamic Type), 8pt spacing, system colors
→ Validate against anti-patterns.md
→ Implement with Form { Section { TextField, SecureField, Button } }
```

**Component Implementation Checklist**:
- ✅ Spacing uses 8pt multiples
- ✅ Dynamic Type support (.title, .body, etc.)
- ✅ System colors (auto Dark Mode)
- ✅ Safe Area respected
- ✅ Touch targets minimum 44x44pt
- ✅ SwiftUI system components used
- ✅ Single Primary button
- ✅ Accessibility (VoiceOver labels)

## SwiftUI Code Examples

### ✅ Good: HIG-Compliant Button

```swift
Button("확인") {
    saveData()
}
.buttonStyle(.borderedProminent)
.controlSize(.large)
```

### ✅ Good: Adaptive Colors

```swift
VStack {
    Text("제목")
        .font(.headline)
        .foregroundColor(.primary)  // Auto Dark Mode

    Text("설명")
        .font(.body)
        .foregroundColor(.secondary)
}
.padding()
.background(Color(.systemBackground))
```

### ❌ Bad: Fixed Sizes, No Dark Mode

```swift
Text("제목")
    .font(.system(size: 24))  // ❌ No Dynamic Type
    .foregroundColor(.black)  // ❌ No Dark Mode

VStack { }
    .ignoresSafeArea()  // ❌ Content hidden by notch
```

## Platform-Specific Considerations

### Safe Area (CRITICAL)
- Always respect Safe Area for content
- Use `.ignoresSafeArea()` only for backgrounds
- Test on iPhone with notch/Dynamic Island

### Dark Mode (REQUIRED)
- Test in both Light and Dark modes
- Use system colors (never `.black`, `.white` directly)
- Define custom colors in Asset Catalog with Light/Dark variants

### Dynamic Type (REQUIRED)
- Test with largest accessibility text size
- Use system text styles (`.body`, `.headline`, etc.)
- Avoid fixed `.lineLimit()` that breaks with large text

### Preview Multiple Configurations

```swift
struct MyView_Previews: PreviewProvider {
    static var previews: some View {
        Group {
            MyView()
                .preferredColorScheme(.light)
                .previewDisplayName("Light Mode")

            MyView()
                .preferredColorScheme(.dark)
                .previewDisplayName("Dark Mode")

            MyView()
                .environment(\.sizeCategory, .accessibilityExtraExtraLarge)
                .previewDisplayName("Large Text")
        }
    }
}
```

## Reference Documentation

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui/)
- [SF Symbols](https://developer.apple.com/sf-symbols/)
