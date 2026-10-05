---
name: figma-bridge
description: >
  Extract design information from Figma files. Pull design tokens, component
  structure, colors, typography, spacing, and export assets. Use when the user
  asks about their Figma designs, needs to extract design tokens, or wants to
  convert Figma designs to code. Triggers on: "figma", "design tokens",
  "get colors from figma", "component structure", "figma to code", "export from figma".
tags:
  - figma
  - design
  - ui
  - tokens
  - css
  - components
  - design-system
env:
  - name: FIGMA_TOKEN
    description: "Figma Personal Access Token (generate at figma.com → Settings → Personal Access Tokens)"
    required: true
---

# Figma Bridge

You extract design information from Figma and make it usable for development.

## Setup

This skill requires a Figma Personal Access Token provided via environment variable.

1. Go to figma.com → Settings → Personal Access Tokens → Generate
2. Set as environment variable: `export FIGMA_TOKEN="figd_..."`

## Credential Handling

- Token is read from the `FIGMA_TOKEN` environment variable at runtime
- This skill does NOT store tokens to disk
- This skill is read-only — it never modifies your Figma files
- If the token is missing, prompt the user to set the environment variable

## Figma API

All calls use the Figma REST API:
```bash
curl -s "https://api.figma.com/v1/[endpoint]" \
  -H "X-Figma-Token: [TOKEN]"
```

### Get file structure
```bash
curl -s "https://api.figma.com/v1/files/[FILE_KEY]" \
  -H "X-Figma-Token: [TOKEN]"
```

### Get specific node
```bash
curl -s "https://api.figma.com/v1/files/[FILE_KEY]/nodes?ids=[NODE_ID]" \
  -H "X-Figma-Token: [TOKEN]"
```

### Export assets
```bash
curl -s "https://api.figma.com/v1/images/[FILE_KEY]?ids=[NODE_IDS]&format=png&scale=2" \
  -H "X-Figma-Token: [TOKEN]"
```

## Commands

### "Get design tokens from [figma URL]"
Extract the file key from the URL, fetch styles, and output:
```css
:root {
  /* Colors */
  --color-primary: #ff6b2b;
  --color-secondary: #22d3ee;
  --color-background: #0b1120;
  --color-text: #e2e8f0;

  /* Typography */
  --font-heading: 'Inter', sans-serif;
  --font-body: 'IBM Plex Mono', monospace;
  --font-size-h1: 2.5rem;
  --font-size-body: 1rem;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 48px;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
}
```

### "Show components in [figma URL]"
List all components with their properties:
```
## Components

### Button
- Variants: primary, secondary, ghost
- Sizes: sm, md, lg
- States: default, hover, disabled
- Properties: label (text), icon (instance), loading (boolean)

### Card
- Variants: default, elevated
- Properties: title (text), description (text), image (instance)
```

### "Export assets from [figma URL]"
Export selected frames/components as PNG/SVG:
```
Exported 5 assets to ./figma-exports/:
  logo.svg (2.4 KB)
  hero-image.png (145 KB)
  icon-arrow.svg (0.8 KB)
  icon-check.svg (0.6 KB)
  avatar-placeholder.png (12 KB)
```

### "Figma to Tailwind from [URL]"
Convert Figma styles to tailwind.config.js:
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#ff6b2b',
        secondary: '#22d3ee',
        background: '#0b1120',
      },
      fontFamily: {
        heading: ['Inter', 'sans-serif'],
        mono: ['IBM Plex Mono', 'monospace'],
      },
    },
  },
};
```

## URL Parsing

Figma URLs follow this pattern:
`https://www.figma.com/design/[FILE_KEY]/[FILE_NAME]?node-id=[NODE_ID]`

Extract `FILE_KEY` and optionally `NODE_ID` from any Figma URL the user provides.

## Rules
- NEVER modify the Figma file — read-only operations only
- Token comes from environment variable FIGMA_TOKEN, never stored to disk
- If the token is invalid or expired, guide the user to generate a new one
- Present design tokens in both CSS custom properties AND JSON formats
- When exporting, default to 2x scale for retina
- Parse Figma's color format (RGBA 0-1) to hex: multiply by 255, convert
