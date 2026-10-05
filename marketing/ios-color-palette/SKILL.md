---
name: ios-color-palette
description: >
  iOS color palette guidance. Triggers on: color palette, colors, color scheme,
  tinting, vibrancy, iOS colors, dark mode colors, accent color, semantic colors.
---

# iOS Color Palette — Semantic Colors + Liquid Glass

---

## 1. iOS 26 Semantic Colors

Use system semantic colors. They adapt automatically to Light/Dark Mode, accessibility settings, and glass surfaces.

### Backgrounds
| Token | Usage |
|---|---|
| `Color(.systemBackground)` | Primary background |
| `Color(.secondarySystemBackground)` | Grouped/card backgrounds |
| `Color(.tertiarySystemBackground)` | Nested groups |
| `Color(.systemGroupedBackground)` | Grouped table/list background |
| `Color(.secondarySystemGroupedBackground)` | Sections within grouped |
| `Color(.tertiarySystemGroupedBackground)` | Nested within grouped sections |

### Labels (Text)
| Token | Usage |
|---|---|
| `.foregroundStyle(.primary)` | Primary text — titles, body |
| `.foregroundStyle(.secondary)` | Supporting text — subtitles, metadata |
| `.foregroundStyle(.tertiary)` | Disabled or hint text |
| `.foregroundStyle(.quaternary)` | Barely visible — watermarks, separators |

### System Colors
`Color.red`, `.orange`, `.yellow`, `.green`, `.mint`, `.teal`, `.cyan`, `.blue`, `.indigo`, `.purple`, `.pink`, `.brown` — all adapt to Light/Dark automatically.

### Separators & Fills
| Token | Usage |
|---|---|
| `Color(.separator)` | Standard divider lines |
| `Color(.opaqueSeparator)` | Non-translucent dividers |
| `Color(.systemFill)` | Thin fill for small elements |
| `Color(.secondarySystemFill)` | Medium fill |
| `Color(.tertiarySystemFill)` | Thick fill |

---

## 2. Liquid Glass Color Behavior

Glass surfaces are translucent — the background bleeds through. This changes how color works:

- **`.tint()` on glass**: Adds a subtle color wash to the glass surface. Use your accent color here.
  ```swift
  .glassEffect(.regular.tint(.blue))
  ```
- **Vibrancy**: Text and symbols on glass automatically get vibrancy treatment. Use `.foregroundStyle(.primary)` — the system handles the rest.
- **Don't fight the glass**: Avoid opaque backgrounds behind glass elements. The translucency IS the design.
- **Test over different backgrounds**: Glass looks different over light content, dark content, and images. Verify readability across all.

---

## 3. Palette Construction Rules

### The One-Accent Rule
- Choose **one** accent color for your entire app
- Set it in asset catalog as `AccentColor` or via `.tint()` at the app level
- Use it for: primary buttons, active tab icons, links, toggles, selection highlights
- Everything else uses semantic system colors

### Color Constraints
- **No oversaturated neons** — keep saturation below 80% in HSB
- **No pure black** (`#000000`) — use `Color(.systemBackground)` which is near-black in Dark Mode
- **No pure white** (`#FFFFFF`) for backgrounds — use `Color(.systemBackground)`
- **No custom grays** — use `Color(.secondaryLabel)`, `Color(.systemFill)`, etc.
- **Tinted shadows** carry the background hue — use `.shadow(.drop(color: .accent.opacity(0.15), radius: 8))`

### Contrast Requirements
- Accent color must pass **WCAG AA** (4.5:1 ratio) against both light and dark system backgrounds
- Test with Accessibility Inspector in Xcode
- Body text on glass: use `.foregroundStyle(.primary)` — the system ensures contrast via vibrancy
- Small text (caption/footnote): needs even higher contrast — use `.foregroundStyle(.primary)`, never `.tertiary`

---

## 4. Light/Dark Mode

### Asset Catalog Setup
1. Create a Color Set in `Assets.xcassets`
2. Set Appearances to "Any, Dark"
3. Define both variants

### Code Pattern
```swift
// Asset catalog color (automatically adapts)
Color("BrandAccent")

// Programmatic adaptive color
extension Color {
    static let accent = Color("BrandAccent")
}

// Inline adaptive (rare — prefer asset catalog)
@Environment(\.colorScheme) var colorScheme
let tint = colorScheme == .dark ? Color.blue : Color.indigo
```

### Glass in Both Modes
- Light Mode: glass is bright, subtle tints show clearly
- Dark Mode: glass is darker, tints are more muted
- Always test `.glassEffect(.regular.tint(.yourAccent))` in both modes
- If tint looks too strong in one mode, consider using a semantic color that adapts

---

## 5. Quick Reference

### Color Modifier Patterns
```swift
// Text color
.foregroundStyle(.primary)
.foregroundStyle(.secondary)
.foregroundStyle(Color.accentColor)

// Hierarchical foreground (primary + secondary in one view)
.foregroundStyle(.blue, .blue.opacity(0.5))

// View tinting (buttons, controls)
.tint(.blue)

// App-wide accent
// Set AccentColor in asset catalog — no code needed

// Background
.background(Color(.secondarySystemBackground))
.background(.ultraThinMaterial)  // pre-iOS 26 glass alternative

// Shapes with fill
RoundedRectangle(cornerRadius: 12)
    .fill(Color(.secondarySystemGroupedBackground))
```

### Color Debugging
```swift
// Temporarily visualize color tokens
.border(Color.red) // layout debugging
.background(Color.yellow.opacity(0.3)) // hit area debugging
```
