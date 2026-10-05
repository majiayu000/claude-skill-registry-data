---
name: ios-typography
description: >
  iOS typography guidance. Triggers on: typography, fonts, type scale, text styling,
  iOS fonts, open source fonts, custom fonts, Dynamic Type, font pairing.
---

# iOS Typography — Type Scale, Custom Fonts & Readability

---

## 1. Open-Source Font Recommendations

All fonts listed are free for commercial use.

### Sans-Serif Display (Headlines, Large Titles)
| Font | Character | Source |
|---|---|---|
| Satoshi | Geometric, modern, confident | Fontshare |
| Cabinet Grotesk | Distinctive, editorial feel | Fontshare |
| Outfit | Clean, geometric, versatile | Google Fonts |
| General Sans | Neutral, contemporary | Fontshare |
| Switzer | Swiss-inspired, professional | Fontshare |

### Sans-Serif Body (Body Text, UI)
| Font | Character | Source |
|---|---|---|
| Plus Jakarta Sans | Warm, rounded, highly readable | Google Fonts |
| DM Sans | Clean, low-contrast geometric | Google Fonts |
| Nunito Sans | Friendly, balanced | Google Fonts |
| Source Sans 3 | Adobe's workhorse sans | Google Fonts |
| Inter | Designed for screens, excellent at small sizes | Google Fonts |

### Monospace (Code, Data, Tabular)
| Font | Character | Source |
|---|---|---|
| JetBrains Mono | Developer-friendly, ligatures | JetBrains |
| Fira Code | Ligatures, wide language support | Google Fonts |
| IBM Plex Mono | Corporate-clean monospace | Google Fonts |

### Serif (Editorial Apps Only)
| Font | Character | Source |
|---|---|---|
| Fraunces | Variable, quirky soft-serif | Google Fonts |
| Lora | Elegant, well-balanced text serif | Google Fonts |
| Source Serif 4 | Adobe's companion to Source Sans | Google Fonts |

**Font sources**: [Google Fonts](https://fonts.google.com), [Fontshare](https://www.fontshare.com) (Indian Type Foundry — high quality, free)

---

## 2. iOS Type Scale

Map custom fonts to iOS text styles for automatic Dynamic Type scaling:

| Text Style | Default Size | Weight | Typical Usage |
|---|---|---|---|
| `.largeTitle` | 34pt | Regular | Screen titles (NavigationStack large title) |
| `.title` | 28pt | Regular | Section headers |
| `.title2` | 22pt | Regular | Subsection headers |
| `.title3` | 20pt | Regular | Card titles |
| `.headline` | 17pt | Semibold | Emphasized body text |
| `.body` | 17pt | Regular | Primary content |
| `.callout` | 16pt | Regular | Secondary content |
| `.subheadline` | 15pt | Regular | Metadata, captions above content |
| `.footnote` | 13pt | Regular | Timestamps, auxiliary info |
| `.caption` | 12pt | Regular | Labels, badges |
| `.caption2` | 11pt | Regular | Fine print, legal |

### Using Custom Fonts with Dynamic Type
```swift
// CORRECT — scales with Dynamic Type
.font(.custom("Satoshi-Bold", size: 28, relativeTo: .title))

// WRONG — fixed size, ignores Dynamic Type
.font(.custom("Satoshi-Bold", fixedSize: 28))
```

Always use `relativeTo:` to bind custom fonts to a text style. This ensures your font scales when the user changes their preferred text size.

---

## 3. Typography Rules

### Hierarchy
- Use **one display font** (for titles/headers) and **one body font** (for everything else). Two fonts max.
- If using a custom display font, SF Pro (system font) works well as the body font — no registration needed.
- Create hierarchy through **weight and color**, not just size:
  ```swift
  Text("Title")
      .font(.custom("Satoshi-Bold", size: 20, relativeTo: .title3))
  Text("Subtitle")
      .font(.subheadline)
      .foregroundStyle(.secondary)
  ```

### Line Length
- Constrain body text to roughly **65 characters** per line for readability
- Use `.frame(maxWidth: 600)` on text-heavy content for iPad
- `lineLimit(_:)` for truncation, `.lineSpacing()` for vertical rhythm

### Weight Spectrum
- Use at minimum 3 weights to create clear hierarchy: Bold/Semibold for titles, Regular for body, Regular + `.secondary` color for metadata
- Avoid using Light/Thin weights for body text — they're hard to read on small screens

### Spacing
```swift
// Adjust line spacing for readability
Text(longParagraph)
    .font(.body)
    .lineSpacing(4)

// Letter spacing for uppercase labels
Text("SECTION")
    .font(.caption)
    .kerning(1.2)
    .foregroundStyle(.secondary)
```

---

## 4. Readability on Glass

Liquid Glass surfaces are translucent — text must remain readable against variable backgrounds.

- **Increase font weight** on glass surfaces. Where you'd normally use Regular, use Medium or Semibold.
- **Use `.foregroundStyle(.primary)`** — the system applies vibrancy to maintain contrast.
- **Avoid `.foregroundStyle(.tertiary)` or `.quaternary` on glass** — too faint against translucent backgrounds.
- **Don't manually set opacity on text over glass** — let the vibrancy system handle it.

```swift
// Text on glass surface
VStack {
    Text("Card Title")
        .font(.headline)           // Already semibold
    Text("Supporting text")
        .font(.subheadline)
        .foregroundStyle(.secondary) // System handles vibrancy
}
.padding()
.glassEffect(in: .rect(cornerRadius: 12))
```

---

## 5. Custom Font Registration

### Step 1: Add Font Files
Add `.ttf` or `.otf` files to your Xcode project. Ensure they're included in the app target (check Target Membership).

### Step 2: Register in Info.plist
```xml
<key>UIAppFonts</key>
<array>
    <string>Satoshi-Regular.otf</string>
    <string>Satoshi-Medium.otf</string>
    <string>Satoshi-Bold.otf</string>
</array>
```

Or in Xcode: Target → Info → "Fonts provided by application" → add each filename.

### Step 3: Verify Font Name
The font name in code may differ from the filename. Print available fonts to find the exact name:
```swift
// Debug helper — remove before shipping
for family in UIFont.familyNames.sorted() {
    for name in UIFont.fontNames(forFamilyName: family) {
        print(name)
    }
}
```

### Step 4: Create a Type Scale Extension
```swift
extension Font {
    static func display(_ style: Font.TextStyle = .title) -> Font {
        .custom("Satoshi-Bold", size: UIFont.preferredFont(
            forTextStyle: style.uiKit).pointSize, relativeTo: style)
    }

    static func bodyText(_ style: Font.TextStyle = .body) -> Font {
        .custom("PlusJakartaSans-Regular", size: UIFont.preferredFont(
            forTextStyle: style.uiKit).pointSize, relativeTo: style)
    }
}

// Usage
Text("Welcome").font(.display(.largeTitle))
Text("Content").font(.bodyText())
```

This centralizes your type scale and ensures every use respects Dynamic Type.
