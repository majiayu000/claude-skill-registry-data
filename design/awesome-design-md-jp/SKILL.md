---
name: awesome-design-md-jp
description: Generate accurate Japanese UI with proper CJK typography using DESIGN.md specifications for 186+ Japanese web services
triggers:
  - use Japanese design system
  - apply Japanese typography rules
  - create Japanese UI with proper fonts
  - implement CJK typographic standards
  - generate Japanese web interface
  - follow Japanese design guidelines
  - add Japanese font fallback chain
  - use DESIGN.md for Japanese site
---

# Awesome Design MD JP Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## What This Project Does

Awesome Design MD JP is a curated collection of `DESIGN.md` files for 186+ Japanese web services, enabling AI agents to generate accurate Japanese UI with proper CJK typography. It extends the Google Stitch DESIGN.md format with Japanese-specific typographic rules including font stacks, line-height, letter-spacing, OpenType features, and kinsoku shori (禁則処理).

Unlike Western DESIGN.md collections, this addresses fundamental differences in Japanese typography:
- Japanese font fallback chains (和文 → 欧文 → generic)
- Wider line-height (1.5-2.0 vs 1.4-1.5 for Latin)
- Letter-spacing for body text (0.04-0.1em)
- Kinsoku shori (禁則処理) for punctuation placement
- OpenType features (`palt`, `kern`) for proportional typesetting
- Mixed script composition rules (和文 + 欧文)

## Installation

Clone the repository:

```bash
git clone https://github.com/kzhrknt/awesome-design-md-jp.git
cd awesome-design-md-jp
```

No build step required — all DESIGN.md files are ready to use.

## Repository Structure

```
awesome-design-md-jp/
├── design-md/
│   ├── apple/
│   │   ├── DESIGN.md
│   │   ├── preview.html
│   │   └── preview-screenshot.png
│   ├── muji/
│   ├── mercari/
│   ├── studio/
│   └── [186+ other services]/
├── gallery.html          # Visual gallery of all designs
└── README.md
```

## Using DESIGN.md Files

### 1. Copy to Your Project

Copy the relevant DESIGN.md to your project root:

```bash
# Example: Using MUJI design system
cp design-md/muji/DESIGN.md ./DESIGN.md
```

### 2. Reference in AI Agent Context

Add to your AI agent's context (`.cursorrules`, `.clinerules`, etc.):

```markdown
Follow the design specifications in DESIGN.md for all UI implementation.
Pay special attention to Japanese typography rules in the Typography section.
```

### 3. Direct Integration

Import design tokens programmatically:

```javascript
// Example: Parsing DESIGN.md for design tokens
import fs from 'fs';
import path from 'path';

function parseDesignMd(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const tokens = {
    colors: {},
    typography: {},
    spacing: {}
  };
  
  // Extract color palette
  const colorMatch = content.match(/### Color Palette\n\n```css\n([\s\S]*?)```/);
  if (colorMatch) {
    const colorLines = colorMatch[1].split('\n');
    colorLines.forEach(line => {
      const match = line.match(/--([^:]+):\s*([^;]+);/);
      if (match) {
        tokens.colors[match[1]] = match[2].trim();
      }
    });
  }
  
  return tokens;
}

const tokens = parseDesignMd('./DESIGN.md');
console.log(tokens.colors);
// { primary: '#1976d2', background: '#ffffff', ... }
```

## Japanese Typography Patterns

### Font Stack Implementation

```css
/* Proper Japanese font fallback chain */
body {
  font-family: 
    "Hiragino Kaku Gothic ProN",  /* macOS Japanese */
    "Hiragino Sans",               /* macOS modern */
    "Yu Gothic Medium",            /* Windows 8.1+ */
    "Meiryo",                      /* Windows fallback */
    "Noto Sans JP",                /* Web font */
    sans-serif;                    /* Generic fallback */
}

/* For mixed Japanese + English content */
.body-text {
  font-family: 
    "Hiragino Kaku Gothic ProN", 
    "Helvetica Neue",              /* English portions */
    Arial, 
    "Noto Sans JP", 
    sans-serif;
}
```

### Line Height for Japanese

```css
/* Japanese text requires more vertical space */
.ja-body {
  line-height: 1.8;  /* vs 1.5 for English */
}

.ja-heading {
  line-height: 1.6;  /* vs 1.2 for English */
}

.ja-caption {
  line-height: 1.7;  /* vs 1.4 for English */
}
```

### Letter Spacing

```css
/* Japanese body text needs slight letter-spacing */
.ja-body {
  letter-spacing: 0.05em;  /* 0.04-0.1em typical */
}

.ja-heading {
  letter-spacing: 0.08em;  /* Slightly more for headings */
}

/* No letter-spacing for Latin text */
.en-text {
  letter-spacing: 0;
}
```

### OpenType Features

```css
/* Enable proportional metrics for Japanese fonts */
.ja-text {
  font-feature-settings: 
    "palt" 1,    /* Proportional alternate metrics */
    "kern" 1;    /* Kerning */
}

/* For vertical text */
.vertical-text {
  writing-mode: vertical-rl;
  font-feature-settings: 
    "vpal" 1,    /* Vertical proportional alternates */
    "vkrn" 1;    /* Vertical kerning */
}
```

### Kinsoku Shori (禁則処理)

```css
/* Proper line-breaking rules for Japanese */
.ja-text {
  word-break: normal;
  overflow-wrap: break-word;
  line-break: strict;           /* Enforce strict kinsoku */
  /* or auto, normal, loose, anywhere, strict */
}

/* Prevent widows/orphans */
.ja-paragraph {
  orphans: 2;
  widows: 2;
}
```

## Common Implementation Patterns

### Pattern 1: Apply Complete DESIGN.md System

```css
/* Import design tokens from MUJI DESIGN.md */
:root {
  /* Colors from DESIGN.md */
  --primary: #000000;
  --background: #ffffff;
  --text: #333333;
  --border: #e0e0e0;
  
  /* Typography from DESIGN.md */
  --font-ja: "Hiragino Kaku Gothic ProN", "Yu Gothic Medium", "Noto Sans JP", sans-serif;
  --font-en: "Helvetica Neue", Arial, sans-serif;
  
  /* Spacing from DESIGN.md */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
}

body {
  font-family: var(--font-ja);
  line-height: 1.8;
  letter-spacing: 0.05em;
  color: var(--text);
  background: var(--background);
}

h1, h2, h3 {
  line-height: 1.6;
  letter-spacing: 0.08em;
}
```

### Pattern 2: Mix Japanese and English Typography

```html
<style>
.mixed-content {
  font-family: "Hiragino Kaku Gothic ProN", "Helvetica Neue", sans-serif;
}

/* Target Japanese characters */
.mixed-content:lang(ja) {
  line-height: 1.8;
  letter-spacing: 0.05em;
}

/* Target English characters */
.mixed-content:lang(en) {
  line-height: 1.5;
  letter-spacing: 0;
}
</style>

<div class="mixed-content">
  <p lang="ja">これは日本語のテキストです。</p>
  <p lang="en">This is English text.</p>
</div>
```

### Pattern 3: Responsive Japanese Typography

```css
/* Mobile-first Japanese typography */
.ja-heading {
  font-size: 1.5rem;
  line-height: 1.6;
  letter-spacing: 0.08em;
}

@media (min-width: 768px) {
  .ja-heading {
    font-size: 2rem;
    line-height: 1.5;
    letter-spacing: 0.1em;
  }
}

@media (min-width: 1024px) {
  .ja-heading {
    font-size: 2.5rem;
    line-height: 1.4;
  }
}
```

### Pattern 4: Component with DESIGN.md Tokens

```jsx
// React component using parsed DESIGN.md tokens
import React from 'react';
import designTokens from './design-tokens.json';

const JapaneseCard = ({ title, description }) => {
  const styles = {
    card: {
      backgroundColor: designTokens.colors.background,
      border: `1px solid ${designTokens.colors.border}`,
      borderRadius: designTokens.radii.md,
      padding: designTokens.spacing.lg,
    },
    title: {
      fontFamily: designTokens.typography.fontFamily.japanese,
      fontSize: designTokens.typography.fontSize.h3,
      lineHeight: designTokens.typography.lineHeight.heading,
      letterSpacing: designTokens.typography.letterSpacing.heading,
      color: designTokens.colors.text,
      marginBottom: designTokens.spacing.md,
    },
    description: {
      fontFamily: designTokens.typography.fontFamily.japanese,
      fontSize: designTokens.typography.fontSize.body,
      lineHeight: designTokens.typography.lineHeight.body,
      letterSpacing: designTokens.typography.letterSpacing.body,
      color: designTokens.colors.textSecondary,
    },
  };

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>{title}</h3>
      <p style={styles.description}>{description}</p>
    </div>
  );
};

export default JapaneseCard;
```

### Pattern 5: CSS-in-JS with Japanese Typography

```javascript
// Styled-components with Japanese typography
import styled from 'styled-components';

const JapaneseText = styled.p`
  font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic Medium", "Noto Sans JP", sans-serif;
  line-height: 1.8;
  letter-spacing: 0.05em;
  font-feature-settings: "palt" 1, "kern" 1;
  word-break: normal;
  overflow-wrap: break-word;
  line-break: strict;
`;

const JapaneseHeading = styled.h2`
  font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic Medium", "Noto Sans JP", sans-serif;
  font-size: 2rem;
  line-height: 1.6;
  letter-spacing: 0.08em;
  font-weight: 600;
  font-feature-settings: "palt" 1, "kern" 1;
`;

// Usage
const App = () => (
  <div>
    <JapaneseHeading>見出しテキスト</JapaneseHeading>
    <JapaneseText>
      本文のテキストです。適切な行間と字間が設定されています。
    </JapaneseText>
  </div>
);
```

## Browsing the Collection

### View Gallery

Open `gallery.html` in your browser or visit:
```
https://kzhrknt.github.io/awesome-design-md-jp/gallery.html
```

### Preview Individual Designs

Each design includes a `preview.html` file:

```bash
# Open MUJI preview
open design-md/muji/preview.html

# Open Apple preview
open design-md/apple/preview.html
```

## Available Design Systems (186+)

**Tech Companies**: Apple, LINE, Mercari, SmartHR, freee, note, Cybozu, Qiita, Zenn, pixiv, connpass, Sansan, PayPay, MOSH, STORES, Wantedly

**Media & Publishing**: WIRED, 日経電子版, BRUTUS, Casa BRUTUS, Pen Online, POPEYE, ほぼ日

**E-commerce & Retail**: MUJI, UNIQLO, Rakuten, Tabelog, Cookpad, 一休.com, Snow Peak, JINS, BEAMS

**Design & Creative**: STUDIO, nendo, Takram, teamLab, 21_21 DESIGN SIGHT, NDC, Droga5

**Automotive**: Toyota, Mazda, LEXUS

**Government**: デジタル庁 (Digital Agency)

**Traditional & Crafts**: とらや, 中川政七商店, 吉田カバン, SOU・SOU, カキモリ

**Luxury & Fashion**: ISSEY MIYAKE, AURALEE, ミナ ペルホネン, 45R

**Home & Lifestyle**: 星野リゾート, BALMUDA, ±0, KINTO, IDÉE, ACTUS, Karimoku New Standard

**Beauty & Cosmetics**: Shiseido, POLA, OSAJI

And 140+ more…

## Configuration

### Create design-tokens.json

```javascript
// scripts/extract-tokens.js
const fs = require('fs');
const path = require('path');

function extractTokens(designMdPath) {
  const content = fs.readFileSync(designMdPath, 'utf-8');
  const tokens = {
    colors: {},
    typography: {
      fontFamily: {},
      fontSize: {},
      lineHeight: {},
      letterSpacing: {}
    },
    spacing: {},
    radii: {}
  };

  // Extract CSS custom properties
  const cssBlocks = content.match(/```css\n([\s\S]*?)```/g) || [];
  cssBlocks.forEach(block => {
    const css = block.replace(/```css\n|```/g, '');
    const lines = css.split('\n');
    
    lines.forEach(line => {
      const match = line.match(/--([^:]+):\s*([^;]+);/);
      if (match) {
        const [, key, value] = match;
        
        if (key.startsWith('color-')) {
          tokens.colors[key.replace('color-', '')] = value.trim();
        } else if (key.startsWith('font-family-')) {
          tokens.typography.fontFamily[key.replace('font-family-', '')] = value.trim();
        } else if (key.startsWith('font-size-')) {
          tokens.typography.fontSize[key.replace('font-size-', '')] = value.trim();
        } else if (key.startsWith('line-height-')) {
          tokens.typography.lineHeight[key.replace('line-height-', '')] = value.trim();
        } else if (key.startsWith('letter-spacing-')) {
          tokens.typography.letterSpacing[key.replace('letter-spacing-', '')] = value.trim();
        } else if (key.startsWith('space-')) {
          tokens.spacing[key.replace('space-', '')] = value.trim();
        } else if (key.startsWith('radius-')) {
          tokens.radii[key.replace('radius-', '')] = value.trim();
        }
      }
    });
  });

  return tokens;
}

// Usage
const tokens = extractTokens('./design-md/muji/DESIGN.md');
fs.writeFileSync(
  './design-tokens.json',
  JSON.stringify(tokens, null, 2)
);
```

### Tailwind CSS Integration

```javascript
// tailwind.config.js
const designTokens = require('./design-tokens.json');

module.exports = {
  theme: {
    extend: {
      colors: designTokens.colors,
      fontFamily: {
        ja: designTokens.typography.fontFamily.japanese?.split(',').map(f => f.trim()) || [],
        en: designTokens.typography.fontFamily.english?.split(',').map(f => f.trim()) || [],
      },
      fontSize: designTokens.typography.fontSize,
      lineHeight: designTokens.typography.lineHeight,
      letterSpacing: designTokens.typography.letterSpacing,
      spacing: designTokens.spacing,
      borderRadius: designTokens.radii,
    },
  },
  plugins: [],
};
```

## Troubleshooting

### Font Not Loading Properly

**Problem**: Japanese fonts not displaying correctly.

**Solution**: Ensure font fallback chain is complete and in correct order:

```css
/* Wrong - missing fallbacks */
font-family: "Noto Sans JP", sans-serif;

/* Correct - full fallback chain */
font-family: 
  "Hiragino Kaku Gothic ProN",
  "Hiragino Sans",
  "Yu Gothic Medium",
  "Meiryo",
  "Noto Sans JP",
  sans-serif;
```

### Line Breaking Issues

**Problem**: Punctuation appearing at beginning of lines.

**Solution**: Enable proper kinsoku shori:

```css
.ja-text {
  word-break: normal;      /* Not 'break-all' */
  overflow-wrap: break-word;
  line-break: strict;      /* Enforce kinsoku */
}
```

### Mixed Script Spacing

**Problem**: English words too close to Japanese text.

**Solution**: Add word-spacing for mixed content:

```css
.mixed-content {
  word-spacing: 0.25em;  /* Space between words */
  letter-spacing: 0.05em; /* Space between Japanese chars */
}
```

### Web Font Loading

**Problem**: Flash of unstyled text (FOUT) with Japanese web fonts.

**Solution**: Use font-display and preload:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
```

```css
@font-face {
  font-family: 'Noto Sans JP';
  font-display: swap;  /* or 'fallback', 'optional' */
  src: url('...') format('woff2');
}
```

### OpenType Features Not Working

**Problem**: `font-feature-settings` not applying.

**Solution**: Ensure font supports the feature and use correct syntax:

```css
/* Check if font supports 'palt' */
.ja-text {
  font-feature-settings: "palt" 1, "kern" 1;
  /* Not "palt" on or "palt" true */
}

/* Alternative: use font-variant */
.ja-text {
  font-variant-ligatures: common-ligatures;
  font-kerning: normal;
}
```

### Vertical Text Issues

**Problem**: Vertical text not rendering correctly.

**Solution**: Use proper writing-mode and text-orientation:

```css
.vertical-text {
  writing-mode: vertical-rl;  /* or vertical-lr */
  text-orientation: upright;  /* Keep characters upright */
  font-feature-settings: "vpal" 1, "vkrn" 1;
}

/* For mixed vertical/horizontal */
.vertical-mixed {
  writing-mode: vertical-rl;
  text-orientation: mixed;  /* Rotate Latin text */
}
```

## Best Practices

1. **Always include complete font fallback chains** — don't rely on single web fonts
2. **Use appropriate line-height** — 1.8+ for Japanese body text vs 1.5 for English
3. **Apply letter-spacing** — 0.04-0.1em for Japanese body text
4. **Enable OpenType features** — `palt` and `kern` for better spacing
5. **Enforce kinsoku shori** — use `line-break: strict` for proper punctuation handling
6. **Test on multiple platforms** — macOS, Windows, iOS, Android have different default fonts
7. **Consider web font loading** — use `font-display: swap` to avoid FOUT
8. **Separate Japanese and English styles** — use `:lang()` or separate classes

## Resources

- [Google Stitch DESIGN.md Documentation](https://stitch.withgoogle.com/docs/design-md/overview/)
- [W3C Japanese Layout Task Force](https://www.w3.org/TR/jlreq/)
- [CSS Writing Modes Level 3](https://www.w3.org/TR/css-writing-modes-3/)
- [OpenType Feature Tags](https://docs.microsoft.com/en-us/typography/opentype/spec/featuretags)
