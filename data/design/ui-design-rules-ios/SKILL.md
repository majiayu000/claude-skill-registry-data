---
name: ui-design-rules-ios
description: Expert knowledge for interpreting Figma design tokens and generating iOS-native SwiftUI code. Includes token mapping rules, design system patterns, and SwiftUI best practices for creating production-ready iOS applications.
version: 1.0.0
tags:
  - ios
  - swiftui
  - design-tokens
  - figma
  - ui-design
---

# UI Design Rules for iOS

This skill provides comprehensive guidance for converting Figma designs into production-ready SwiftUI code with proper design system architecture.

## Core Principles

### 1. Design Tokens Over Hardcoded Values
**Always extract reusable design tokens** for:
- Colors (semantic naming: primary, secondary, surface, content)
- Typography (size, weight, line height, letter spacing)
- Spacing (consistent scale: 4, 8, 16, 24, 32, 48, 64)
- Effects (shadows, blurs, borders)
- Corner radius (small, medium, large)

**Never hardcode** magic numbers or hex values directly in views.

### 2. Semantic Naming Convention
Use purpose-based names rather than appearance-based:

✅ **Good**: `Color.brandPrimary`, `Color.contentSecondary`, `Color.statusError`
❌ **Bad**: `Color.blue`, `Color.gray`, `Color.red`

✅ **Good**: `.titleLarge`, `.bodyMedium`, `.labelSmall`
❌ **Bad**: `.font24Bold`, `.font16Regular`, `.font12Medium`

### 3. Dark Mode by Default
- All colors MUST reference Asset Catalog entries
- Asset Catalog contains both light and dark variants
- Use semantic color names that work in both modes
- Test all UI in both appearances

### 4. Accessibility First
- Add `.accessibilityLabel()` to all interactive elements
- Support Dynamic Type with proper font scaling
- Ensure color contrast meets WCAG AA standards
- Use `.accessibilityElement(children:)` for complex components

## Figma to SwiftUI Mapping Rules

### Color Mapping

#### Figma Color Variables → SwiftUI Color Extensions
```swift
// Figma: Primary/500 (#0066FF)
// Asset Catalog: Brand/Primary (Light: #0066FF, Dark: #4D94FF)
extension Color {
    static let brandPrimary = Color("Brand/Primary")
}
```

#### Color Categories
1. **Brand Colors**: Primary, secondary, tertiary brand colors
2. **UI Colors**: Backgrounds, surfaces, dividers, borders
3. **Content Colors**: Primary, secondary, tertiary text/icons
4. **Status Colors**: Success, warning, error, info
5. **Interactive Colors**: Default, hover, pressed, disabled states

### Typography Mapping

#### Figma Text Styles → SwiftUI Font Extensions
```swift
// Figma: Title/Large (SF Pro Display, 22pt, Regular)
extension Font {
    static let titleLarge = Font.system(size: 22, weight: .regular, design: .default)
}
```

#### Typography Scale (iOS Material 3 Inspired)
| Category | Large | Medium | Small |
|----------|-------|--------|-------|
| Display  | 57pt  | 45pt   | 36pt  |
| Headline | 32pt  | 28pt   | 24pt  |
| Title    | 22pt  | 16pt   | 14pt  |
| Body     | 16pt  | 14pt   | 12pt  |
| Label    | 14pt  | 12pt   | 11pt  |

#### Font Weight Mapping
- Figma "Regular" → `.regular`
- Figma "Medium" → `.medium`
- Figma "Semibold" → `.semibold`
- Figma "Bold" → `.bold`

### Spacing Mapping

#### Figma Auto Layout Gap → SwiftUI Spacing
```swift
// Figma: Auto Layout with 16px gap
VStack(spacing: .spacingM) {
    // children
}

// Figma: 16px padding on all sides
.padding(.spacingM)
```

#### Spacing Scale
```swift
extension CGFloat {
    static let spacingXXS: CGFloat = 2   // Figma: 2px
    static let spacingXS: CGFloat = 4    // Figma: 4px
    static let spacingS: CGFloat = 8     // Figma: 8px
    static let spacingM: CGFloat = 16    // Figma: 16px
    static let spacingL: CGFloat = 24    // Figma: 24px
    static let spacingXL: CGFloat = 32   // Figma: 32px
    static let spacingXXL: CGFloat = 48  // Figma: 48px
    static let spacingXXXL: CGFloat = 64 // Figma: 64px
}
```

### Layout Mapping

#### Auto Layout → SwiftUI Stacks

**Vertical Auto Layout:**
```swift
// Figma: Vertical Auto Layout, 16px gap, center aligned
VStack(alignment: .center, spacing: .spacingM) {
    // children
}
```

**Horizontal Auto Layout:**
```swift
// Figma: Horizontal Auto Layout, 8px gap, top aligned
HStack(alignment: .top, spacing: .spacingS) {
    // children
}
```

**Hug Contents:**
- Figma "Hug" → No `.frame()` modifier (let content determine size)

**Fill Container:**
- Figma "Fill" horizontal → `Spacer()` or `.frame(maxWidth: .infinity)`
- Figma "Fill" vertical → `.frame(maxHeight: .infinity)`

**Fixed Size:**
- Figma: Width 200px, Height 100px
- SwiftUI: `.frame(width: 200, height: 100)`

#### Constraints → Frame Modifiers
```swift
// Figma: Min Width 100px, Max Width 300px
.frame(minWidth: 100, maxWidth: 300)

// Figma: Aspect Ratio 16:9
.aspectRatio(16/9, contentMode: .fit)
```

### Effects Mapping

#### Shadows
```swift
// Figma: Drop Shadow (X: 0, Y: 2, Blur: 8, Color: #000000 at 8% opacity)
.shadow(color: Color.black.opacity(0.08), radius: 8, x: 0, y: 2)

// Create reusable shadow tokens
extension View {
    func shadowSmall() -> some View {
        shadow(color: Color.black.opacity(0.04), radius: 4, x: 0, y: 1)
    }

    func shadowMedium() -> some View {
        shadow(color: Color.black.opacity(0.08), radius: 8, x: 0, y: 2)
    }

    func shadowLarge() -> some View {
        shadow(color: Color.black.opacity(0.12), radius: 16, x: 0, y: 4)
    }
}
```

#### Corner Radius
```swift
// Figma: Corner Radius 12px
.cornerRadius(12)

// Or create tokens
extension CGFloat {
    static let radiusSmall: CGFloat = 4
    static let radiusMedium: CGFloat = 8
    static let radiusLarge: CGFloat = 12
    static let radiusXLarge: CGFloat = 16
    static let radiusRound: CGFloat = 999 // Fully rounded
}
```

#### Borders
```swift
// Figma: Stroke 1px, Color #E0E0E0
.overlay(
    RoundedRectangle(cornerRadius: 12)
        .stroke(Color.uiDivider, lineWidth: 1)
)
```

### Component Patterns

#### Buttons
```swift
// Figma: Primary Button Component
struct PrimaryButton: View {
    let title: String
    let action: () -> Void
    @State private var isPressed = false

    var body: some View {
        Button(action: action) {
            Text(title)
                .textStyle(.labelLarge)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding(.vertical, .spacingM)
                .background(isPressed ? Color.brandPrimary.opacity(0.8) : Color.brandPrimary)
                .cornerRadius(.radiusMedium)
        }
        .buttonStyle(PlainButtonStyle())
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
        .accessibilityLabel(title)
        .accessibilityAddTraits(.isButton)
    }
}
```

#### Cards
```swift
// Figma: Content Card Component
struct ContentCard: View {
    let title: String
    let description: String
    let imageURL: URL?

    var body: some View {
        VStack(alignment: .leading, spacing: .spacingM) {
            // Image
            if let imageURL {
                AsyncImage(url: imageURL) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Color.uiSurface
                }
                .frame(height: 200)
                .clipped()
            }

            // Content
            VStack(alignment: .leading, spacing: .spacingS) {
                Text(title)
                    .textStyle(.titleMedium)
                    .lineLimit(2)

                Text(description)
                    .textStyle(.bodySmall)
                    .foregroundColor(.contentSecondary)
                    .lineLimit(3)
            }
            .padding(.horizontal, .spacingM)
            .padding(.bottom, .spacingM)
        }
        .background(Color.uiSurface)
        .cornerRadius(.radiusLarge)
        .shadowMedium()
        .accessibilityElement(children: .combine)
    }
}
```

#### Text Fields
```swift
// Figma: Input Field Component
struct CustomTextField: View {
    let placeholder: String
    @Binding var text: String
    let isSecure: Bool

    var body: some View {
        Group {
            if isSecure {
                SecureField(placeholder, text: $text)
            } else {
                TextField(placeholder, text: $text)
            }
        }
        .textStyle(.bodyMedium)
        .padding(.spacingM)
        .background(Color.uiSurface)
        .overlay(
            RoundedRectangle(cornerRadius: .radiusMedium)
                .stroke(Color.uiDivider, lineWidth: 1)
        )
        .accessibilityLabel(placeholder)
    }
}
```

## Design System Architecture

### File Structure
```
YourApp/
├── DesignSystem/
│   ├── Tokens/
│   │   ├── ColorTokens.swift
│   │   ├── TypographyTokens.swift
│   │   ├── SpacingTokens.swift
│   │   ├── ShadowTokens.swift
│   │   └── RadiusTokens.swift
│   ├── Components/
│   │   ├── Buttons/
│   │   │   ├── PrimaryButton.swift
│   │   │   ├── SecondaryButton.swift
│   │   │   └── TextButton.swift
│   │   ├── Cards/
│   │   │   ├── ContentCard.swift
│   │   │   └── ProfileCard.swift
│   │   └── Inputs/
│   │       ├── CustomTextField.swift
│   │       └── CustomTextEditor.swift
│   └── Modifiers/
│       ├── TextStyleModifier.swift
│       ├── ShadowModifiers.swift
│       └── CardStyleModifier.swift
├── Features/
│   ├── Authentication/
│   │   ├── Views/
│   │   │   ├── LoginView.swift
│   │   │   └── SignUpView.swift
│   │   └── ViewModels/
│   │       └── AuthenticationViewModel.swift
│   └── Home/
│       ├── Views/
│       │   ├── HomeView.swift
│       │   └── Components/
│       │       ├── HomeHeader.swift
│       │       └── HomeCard.swift
│       └── ViewModels/
│           └── HomeViewModel.swift
└── Resources/
    └── Assets.xcassets/
        ├── Brand/
        │   ├── Primary.colorset
        │   └── Secondary.colorset
        ├── UI/
        │   ├── Background.colorset
        │   ├── Surface.colorset
        │   └── Divider.colorset
        └── Content/
            ├── Primary.colorset
            ├── Secondary.colorset
            └── Tertiary.colorset
```

### Implementation Order
1. **Foundation First**: Create all token files (colors, typography, spacing)
2. **Asset Catalog**: Set up all color assets with dark mode variants
3. **Base Components**: Build reusable primitives (buttons, cards, inputs)
4. **Feature Views**: Compose features using design system components
5. **Refinement**: Add custom modifiers and polish interactions

## Edge Cases & Solutions

### Issue: Figma Uses Absolute Positioning
**Problem**: Figma design has elements positioned with X/Y coordinates
**Solution**: Convert to flexible layout using stacks and spacers
```swift
// Instead of absolute positioning
.position(x: 100, y: 200) // ❌ Not responsive

// Use flexible layout
HStack {
    Spacer()
    content
        .padding(.leading, .spacingL)
}
```

### Issue: Complex Vector Graphics
**Problem**: Figma has custom vector illustrations
**Solution Options**:
1. Export as SVG and use as Image asset
2. Replace with SF Symbol if semantically similar
3. Use Shape API for simple vectors

```swift
// Option 2: SF Symbol replacement
Image(systemName: "checkmark.circle.fill")
    .foregroundColor(.brandPrimary)
    .font(.system(size: 24))
```

### Issue: Missing Design Tokens
**Problem**: Figma file has no variables/styles defined
**Solution**: Analyze raw values and create semantic groupings

```swift
// Observed values: #0066FF, #0052CC, #004099
// Create semantic system:
extension Color {
    static let brandPrimary = Color(hex: "0066FF")      // Default state
    static let brandPrimaryHover = Color(hex: "0052CC") // Hover state
    static let brandPrimaryPressed = Color(hex: "004099") // Pressed state
}
```

### Issue: Component Variants in Figma
**Problem**: Figma component has multiple variants (Primary, Secondary, Small, Large)
**Solution**: Use enum-based configuration

```swift
enum ButtonStyle {
    case primary, secondary, tertiary
}

enum ButtonSize {
    case small, medium, large

    var padding: CGFloat {
        switch self {
        case .small: return .spacingS
        case .medium: return .spacingM
        case .large: return .spacingL
        }
    }
}

struct ConfigurableButton: View {
    let title: String
    let style: ButtonStyle
    let size: ButtonSize
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .padding(.vertical, size.padding)
                .frame(maxWidth: .infinity)
                .background(backgroundColor)
                .foregroundColor(textColor)
        }
    }

    private var backgroundColor: Color {
        switch style {
        case .primary: return .brandPrimary
        case .secondary: return .brandSecondary
        case .tertiary: return .clear
        }
    }

    private var textColor: Color {
        switch style {
        case .primary, .secondary: return .white
        case .tertiary: return .brandPrimary
        }
    }
}
```

## Quality Checklist

Before completing a conversion, verify:

- [ ] **Colors**: All from Asset Catalog, no hex values in code
- [ ] **Typography**: Uses font extensions, no inline `.font(.system(...))` calls
- [ ] **Spacing**: Uses spacing tokens, no magic numbers
- [ ] **Dark Mode**: All colors support dark appearance automatically
- [ ] **Accessibility**: All interactive elements have accessibility labels
- [ ] **Dynamic Type**: Text scales properly with system settings
- [ ] **Previews**: Multiple preview states provided
- [ ] **Documentation**: Complex logic has inline comments
- [ ] **Naming**: Semantic names (not appearance-based)
- [ ] **Organization**: Files in correct feature/component directories
- [ ] **Reusability**: Common patterns extracted to shared components
- [ ] **Performance**: No expensive operations in view body

## Common Mistakes to Avoid

❌ **Hardcoding Colors**
```swift
Text("Hello")
    .foregroundColor(Color(red: 0, green: 0.4, blue: 1.0)) // BAD
```
✅ **Use Token**
```swift
Text("Hello")
    .foregroundColor(.brandPrimary) // GOOD
```

❌ **Magic Numbers**
```swift
.padding(17) // BAD - arbitrary value
```
✅ **Semantic Spacing**
```swift
.padding(.spacingM) // GOOD - from spacing scale
```

❌ **Appearance-Based Naming**
```swift
static let blue = Color("Blue") // BAD
```
✅ **Semantic Naming**
```swift
static let brandPrimary = Color("Brand/Primary") // GOOD
```

❌ **Missing Accessibility**
```swift
Button(action: {}) {
    Image(systemName: "heart")
} // BAD - no label
```
✅ **Proper Accessibility**
```swift
Button(action: {}) {
    Image(systemName: "heart")
}
.accessibilityLabel("Favorite") // GOOD
```

## Resources & References

- **Apple Human Interface Guidelines**: https://developer.apple.com/design/human-interface-guidelines/
- **SwiftUI Documentation**: https://developer.apple.com/documentation/swiftui
- **Figma API**: https://www.figma.com/developers/api
- **Material Design 3**: https://m3.material.io/ (for typography scale inspiration)
- **WCAG Accessibility**: https://www.w3.org/WAI/WCAG21/quickref/

## Version History

**v1.0.0** - Initial release with comprehensive Figma to SwiftUI mapping rules
