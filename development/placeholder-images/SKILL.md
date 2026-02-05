---
name: placeholder-images
description: Generate SVG placeholder images for prototypes. Use when adding placeholder images for layouts, mockups, or development. Supports simple, labeled, and brand-aware types.
allowed-tools: Read, Write, Edit, Bash
---

# Placeholder Images Skill

Generate SVG placeholder images for HTML prototypes and layouts.

## Placeholder Types

| Type | Description | Use Case |
|------|-------------|----------|
| **simple** | Grey box with diagonal X | Basic layout placeholder |
| **labeled** | Grey box with text label | Describe image purpose |
| **brand** | Uses design token colors | Polished prototypes |

## Size Presets

| Preset | Dimensions | Common Use |
|--------|------------|------------|
| `avatar-sm` | 48x48 | User list avatars |
| `avatar-lg` | 128x128 | Profile avatars |
| `thumbnail` | 150x150 | Grid thumbnails |
| `product` | 400x400 | Product cards |
| `card` | 400x225 | Blog/article cards (16:9) |
| `hero` | 1200x400 | Hero banners |
| `og` | 1200x630 | Open Graph images |

Custom sizes: Use `WxH` format (e.g., `800x600`).

---

## Simple Placeholder

Grey background with diagonal X lines:

```html
<img src="/.assets/images/placeholder/simple-400x400.svg"
     alt="Placeholder image"
     width="400"
     height="400"/>
```

**SVG Pattern:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"
     role="img" aria-label="Placeholder image">
  <title>Placeholder image</title>
  <rect width="400" height="400" fill="#f3f4f6"/>
  <line x1="0" y1="0" x2="400" y2="400" stroke="#d1d5db" stroke-width="1"/>
  <line x1="400" y1="0" x2="0" y2="400" stroke="#d1d5db" stroke-width="1"/>
</svg>
```

---

## Labeled Placeholder

Grey background with descriptive text:

```html
<img src="/.assets/images/placeholder/hero-1200x400.svg"
     alt="Hero banner placeholder"
     width="1200"
     height="400"/>
```

**SVG Pattern:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400"
     role="img" aria-label="Hero Image placeholder">
  <title>Hero Image placeholder</title>
  <rect width="1200" height="400" fill="#f3f4f6"/>
  <line x1="0" y1="0" x2="1200" y2="400" stroke="#d1d5db" stroke-width="1"/>
  <line x1="1200" y1="0" x2="0" y2="400" stroke="#d1d5db" stroke-width="1"/>
  <text x="600" y="200" text-anchor="middle" dominant-baseline="middle"
        font-family="system-ui, -apple-system, sans-serif"
        font-size="24" fill="#6b7280">
    Hero Image
  </text>
</svg>
```

---

## Brand Placeholder

Uses design tokens for brand-consistent placeholders. The script automatically looks for CSS files in common locations and extracts color tokens.

**Token Mapping:**

| Placeholder Color | Tokens Searched |
|-------------------|-----------------|
| Background | `--background-alt`, `--background-main`, `--surface-color` |
| Stroke | `--border-color`, `--border-light` |
| Text | `--text-muted`, `--text-color` |
| Accent | `--primary-color`, `--primary`, `--accent-color` |
| Accent Text | `--text-inverted`, `--primary-text` |

**Auto-detection paths:**
- `src/styles/main.css`
- `src/styles/_tokens.css`
- `.assets/styles/main.css`
- `.claude/styles/main.css`

```bash
# Auto-detect CSS file
node .claude/scripts/generate-placeholder.js --type brand --label "Product" --preset product

# Specify CSS file explicitly
node .claude/scripts/generate-placeholder.js --type brand --label "Hero" --size 1200x400 --tokens src/styles/main.css
```

**Example output:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"
     role="img" aria-label="Product Shot placeholder">
  <title>Product Shot placeholder</title>
  <rect width="400" height="400" fill="#f8fafc"/>
  <line x1="0" y1="0" x2="400" y2="400" stroke="#e2e8f0" stroke-width="1"/>
  <line x1="400" y1="0" x2="0" y2="400" stroke="#e2e8f0" stroke-width="1"/>
  <rect x="125" y="175" width="150" height="50" rx="4" fill="#2563eb"/>
  <text x="200" y="205" text-anchor="middle" dominant-baseline="middle"
        font-family="system-ui, -apple-system, sans-serif"
        font-size="14" fill="#ffffff">
    Product Shot
  </text>
</svg>
```

---

## Common Image Types

Use these labels for semantic clarity:

| Label | Typical Size | Description |
|-------|--------------|-------------|
| Hero Image | 1200x400 | Page header banner |
| Product Shot | 400x400 | E-commerce product |
| Team Photo | 300x300 | Staff headshot |
| Thumbnail | 150x150 | Grid/list preview |
| Logo | 200x50 | Brand logo |
| Icon | 48x48 | UI icon |
| Banner | 728x90 | Ad banner |
| Card Image | 400x225 | Blog/article card |
| Gallery | 800x600 | Photo gallery |
| Avatar | 64x64 | User profile |

---

## File Organization

```
.assets/images/placeholder/
├── simple-400x400.svg
├── simple-800x600.svg
├── hero-1200x400.svg
├── product-400x400.svg
├── avatar-128x128.svg
└── card-400x225.svg
```

---

## Generate with Script

```bash
# Simple placeholder
node .claude/scripts/generate-placeholder.js --type simple --size 400x400

# Labeled placeholder
node .claude/scripts/generate-placeholder.js --type labeled --label "Hero Image" --size 1200x400

# Brand placeholder (auto-detects CSS tokens)
node .claude/scripts/generate-placeholder.js --type brand --label "Product" --preset product

# Brand placeholder with specific CSS file
node .claude/scripts/generate-placeholder.js --type brand --label "Hero" --size 1200x400 \
  --tokens src/styles/main.css

# Output to file
node .claude/scripts/generate-placeholder.js --type labeled --label "Product" --size 400x400 \
  --output .assets/images/placeholder/product-400x400.svg

# Generate preset
node .claude/scripts/generate-placeholder.js --preset product
node .claude/scripts/generate-placeholder.js --preset hero --label "Welcome Banner"
```

---

## Inline Data URI

For quick prototyping, use inline data URIs:

```html
<img src="data:image/svg+xml,..." alt="Placeholder"/>
```

Generate with:

```bash
node .claude/scripts/generate-placeholder.js --type simple --size 200x200 --inline
```

---

## Accessibility

All placeholders MUST include:

1. `role="img"` on the SVG element
2. `aria-label` describing the placeholder
3. `<title>` element as first child of SVG
4. Meaningful `alt` text on the `<img>` element

---

## Checklist

When adding placeholder images:

- [ ] Use appropriate preset or custom size
- [ ] Add descriptive label for labeled/brand types
- [ ] Include meaningful alt text
- [ ] Place in `.assets/images/placeholder/` directory
- [ ] Use consistent naming: `{type}-{width}x{height}.svg`

## Related Skills

- **images** - Umbrella coordinator for image handling with automation
- **responsive-images** - Modern responsive image techniques using picture element
- **fake-content** - Generate realistic fake content for HTML prototypes
- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **performance** - Write performance-friendly HTML pages
