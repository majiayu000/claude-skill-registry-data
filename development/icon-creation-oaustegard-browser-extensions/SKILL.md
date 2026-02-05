---
name: icon-creation
description: Generate browser extension icons at multiple sizes (16x16, 32x32, 48x48, 128x128) from SVG files. Use when creating new extension icons, converting SVG to PNG icons, or when user mentions extension icons, icon generation, or icon sizes.
---

# Icon Creation for Browser Extensions

This Skill helps generate browser extension icons at the required sizes from SVG source files.

## When to Use This Skill

Use this Skill when:
- Creating icons for a new browser extension
- Converting SVG designs to PNG icons at multiple sizes
- User mentions "extension icon", "icon generation", or "icon sizes"
- Need to generate 16x16, 32x32, 48x48, and 128x128 PNG icons

## Quick Start

### Option 1: Generate from text/emoji (fastest)

```bash
npm install canvas
node generate-icons.js "A"              # Single letter
node generate-icons.js "🎨"             # Emoji
node generate-icons.js "X" "#000" "#0f0" # Custom colors
```

### Option 2: Create custom SVG design

1. **Edit icon.svg** - Modify the text element or create custom graphics
2. **Generate PNGs**: See [README.md](README.md) for conversion methods (Inkscape, ImageMagick, online tools)

## Icon Size Requirements

Browser extensions require icons at these sizes:
- **16x16** - Browser toolbar (smallest)
- **32x32** - Browser toolbar (retina displays)
- **48x48** - Extension management page
- **128x128** - Chrome Web Store and extension installation

## Design Tips

- **Use the full 128x128 canvas** - Make primary elements large and bold
- **Test at 16x16** - Ensure icon is readable at smallest size
- **Simple, bold shapes** - Avoid thin lines that disappear when scaled down
- **High contrast** - Ensure icon stands out on light and dark backgrounds

## Generation Methods

### Method 1: Node.js Script (Recommended)
```bash
npm install canvas
node generate-icons.js
```

### Method 2: Other Tools
For Inkscape, ImageMagick, or online tools, see [README.md](README.md).

## Complete Documentation

- [USAGE.md](USAGE.md) - Full usage documentation and framework details
- [README.md](README.md) - Alternative generation methods

## Example Workflows

### Text/Emoji Icon
```bash
cd my-extension
npm install canvas
node path/to/generate-icons.js "📧"  # Email icon
```

### Custom SVG Icon
1. Copy and edit `icon.svg` from this skill directory
2. Modify the `<text>` element or add custom graphics
3. Convert using Inkscape/ImageMagick (see [README.md](README.md))

### Reference in manifest.json
```json
"icons": {
  "16": "icon16.png",
  "32": "icon32.png",
  "48": "icon48.png",
  "128": "icon128.png"
}
```

## Customization Examples

**Single letter icons:**
- `node generate-icons.js "A"`
- `node generate-icons.js "T"`
- `node generate-icons.js "𝔉"` (Unicode characters)

**Emoji icons:**
- `node generate-icons.js "🎨"` (art/design)
- `node generate-icons.js "📝"` (notes/writing)
- `node generate-icons.js "🔧"` (tools/settings)

**Custom colors:**
- `node generate-icons.js "X" "#1a1a1a" "#00ff00"` (dark bg, green text)
- `node generate-icons.js "!" "#ff0000" "#ffffff"` (red bg, white text)
