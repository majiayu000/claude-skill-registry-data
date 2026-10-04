---
name: design-tokens
description: Extract code-ready design tokens from a DESIGN.md file. Converts design system documentation into CSS custom properties, Tailwind CSS config, styled-components theme objects, CSS-in-JS themes, or W3C Design Tokens JSON. Use when the user wants to turn a design system into usable code tokens, generate a Tailwind config from a brand's design, create CSS variables from a DESIGN.md, bootstrap a theme file for their framework, or extract a color palette, typography scale, or spacing system as code. Also trigger when the user wants to "use Stripe's colors in my project" or "set up a theme based on Linear".
---

# Extract Design Tokens

Convert a DESIGN.md file into code-ready design tokens in the user's preferred format. This bridges the gap between design documentation and actual code — instead of manually copying hex values and pixel sizes, this skill extracts a complete, structured token set.

## What gets extracted

From each DESIGN.md, extract these token categories:

| Category | Source Section | What's extracted |
|----------|---------------|-----------------|
| Colors | Section 2 | All hex values with semantic names and roles |
| Typography | Section 3 | Font families, size scale, weight scale, line-heights, letter-spacing |
| Spacing | Section 5 | Base unit and full spacing scale |
| Shadows | Section 6 | Shadow definitions at each elevation level |
| Radii | Section 5 | Border-radius scale |
| Breakpoints | Section 8 | Responsive breakpoint values |

## Available Designs

Read `design-md/_index.md` for the full catalog of 58 design systems.

## Workflow

### 1. Identify the design

If the user names a brand, match it against the catalog. Read `design-md/{directory}/DESIGN.md` to load the full design system.

If the user has a `DESIGN.md` in their project root, use that instead.

### 2. Determine the output format

Ask which format the user needs (or infer from their project):

**CSS Custom Properties** — For vanilla CSS or any framework
```css
:root {
  --color-primary: #533afd;
  --color-background: #ffffff;
  --font-display: 'sohne-var', sans-serif;
  --spacing-4: 1rem;
  --shadow-sm: 0px 1px 3px rgba(50,50,93,0.25);
}
```

**Tailwind CSS Config** — For Tailwind projects
```js
module.exports = {
  theme: {
    colors: {
      primary: '#533afd',
      background: '#ffffff',
    },
    fontFamily: {
      display: ['sohne-var', 'sans-serif'],
    },
    spacing: { /* ... */ },
    boxShadow: { /* ... */ },
  }
}
```

**Theme Object (JS/TS)** — For styled-components, Emotion, Stitches, or Chakra UI
```ts
export const theme = {
  colors: {
    primary: '#533afd',
    background: '#ffffff',
  },
  fonts: {
    display: "'sohne-var', sans-serif",
  },
  space: [0, 4, 8, 16, 24, 32, 48, 64],
  shadows: { /* ... */ },
}
```

**W3C Design Tokens JSON** — For cross-platform token exchange
```json
{
  "color": {
    "primary": { "$value": "#533afd", "$type": "color" },
    "background": { "$value": "#ffffff", "$type": "color" }
  }
}
```

**SCSS Variables** — For Sass projects
```scss
$color-primary: #533afd;
$color-background: #ffffff;
$font-display: 'sohne-var', sans-serif;
```

### 3. Extract tokens

Read the DESIGN.md and extract every design token into the chosen format.

**Colors** (from Section 2):
- Map every named color to a semantic token name
- Group by role: `primary`, `accent`, `surface`, `text`, `border`, `interactive`, `status`
- Include hover/active/focus variants from Section 4

**Typography** (from Section 3):
- Font families with full fallback stacks
- Font size scale mapped to named steps (xs, sm, base, lg, xl, 2xl, etc.)
- Font weight scale
- Line-height scale
- Letter-spacing values

**Spacing** (from Section 5):
- Full spacing scale from the base unit
- Container max-width
- Gutter sizes

**Shadows** (from Section 6):
- Each shadow level as a named token (sm, md, lg, xl)
- Include multi-layer shadow values exactly as documented

**Border Radius** (from Section 5):
- Radius scale (none, sm, md, lg, full/pill)

**Breakpoints** (from Section 8):
- Named breakpoints with pixel values

### 4. Naming conventions

Use consistent naming conventions per format:

| Format | Convention | Example |
|--------|-----------|---------|
| CSS Custom Properties | `--{category}-{name}` | `--color-primary`, `--shadow-lg` |
| Tailwind | Tailwind's standard keys | `colors.primary`, `boxShadow.lg` |
| Theme Object | camelCase nested objects | `theme.colors.primary` |
| Design Tokens JSON | Nested with `$value`/`$type` | `color.primary.$value` |
| SCSS | `${category}-{name}` | `$color-primary`, `$shadow-lg` |

### 5. Generate the output file

Write the token file to the appropriate location:
- CSS: `tokens.css` or `variables.css`
- Tailwind: `tailwind.config.js` or `tailwind.config.ts`
- Theme: `theme.ts` or `theme.js`
- Design Tokens: `tokens.json`
- SCSS: `_tokens.scss` or `_variables.scss`

Include a header comment noting which design system the tokens were extracted from.

### 6. Usage guidance

After generating tokens, briefly explain:
- How to import/use the tokens in their project
- Any font files or CDN links needed for the typography tokens
- Which tokens are most important to apply first for maximum visual impact (usually colors + font-family)

## Partial extraction

If the user only needs specific categories (e.g., "just give me Stripe's color palette as CSS vars"), extract only what's requested. Don't generate the full token set unless asked.

## Multiple designs

If the user wants tokens from multiple design systems (e.g., for a theme switcher), generate separate token sets with a shared structure so they can be swapped at runtime.
