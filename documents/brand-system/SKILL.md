---
name: brand-system
description: >
  Create visual identity systems: color palettes, font pairings, style direction,
  and rendered preview PDFs. Use when the user needs a cohesive design system before
  building a deck, presentation, document, or any visual project. Works for consulting
  engagements, product pitches, personal brands, or any context requiring a unified
  visual language. Produces a markdown design brief, a JS config, and a preview PDF.
metadata:
  short-description: "Visual identity systems: palettes, fonts, style direction, preview PDFs"
---

# Brand System

Create a visual identity system: palette, typography, and style direction, documented in a markdown brief, extracted into a JS config, and rendered as a preview PDF.

## Artifacts

All output goes to the user's working directory. Ask for the path if not provided.

| File | What it is |
|---|---|
| `brand-brief.md` | The primary artifact. Research, rationale, and every design decision in one readable document. |
| `identity.js` | A machine-readable extraction of the brief. Importable by downstream build scripts. |
| `brand-preview.pdf` | A 3-slide rendered proof: palette, typography, and a combination demo. |

Intermediate HTML goes to `/tmp/brand-system/` and is cleaned up after rendering.

## Reference files

Load these on demand. Not all are needed for every engagement.

| File | When to load |
|---|---|
| [references/palette-guide.md](references/palette-guide.md) | When building the color palette: 8-role structure, derivation from anchor color, contrast testing |
| [references/typography-guide.md](references/typography-guide.md) | When selecting fonts: pairing lookup table, weight discipline, same-vs-different family guidance |
| [references/design-landscape.md](references/design-landscape.md) | When proposing a visual style: 6 active design directions with full specifications (2025-2026) |

---

## How to work

This is a conversational design process. The brief is built through dialogue: research, propose, refine.

### 1. Start from what you know

Read the user's request. Most of the direction is already implied: the subject, the context, the tone. Don't ask questions the request already answers.

If genuine ambiguity remains, ask the one or two questions that would most change your direction. Good questions resolve a fork in the road.

**Worth asking** (only if truly unclear):
- *"Should this feel institutional and restrained, or is there room for something more contemporary?"*
- *"Is there an existing brand I should align with, or are we starting fresh?"*

**Decide yourself** (don't ask the user):
- What colors to use: research the brand and propose
- What font to use: match the context and recommend
- How many palette roles: the structure is defined, follow it

### 2. Research

Before choosing colors or fonts, look at what exists.

**Known brand** → search for their actual colors, typeface, and visual direction. Extract the primary brand color, the typeface family, and the tone.

**New project** → search for what works in the space: peer palettes, industry conventions, tone-appropriate examples.

### 3. Build the palette

Load [references/palette-guide.md](references/palette-guide.md) for the full role structure and derivation rules.

The palette grows from an anchor color:
- User provides one → build around it
- Known brand → extract from research
- Fresh → choose based on tone and context

Eight roles. One accent + three signals. Every color traces to a reason.

### 4. Choose typography

Load [references/typography-guide.md](references/typography-guide.md) for the pairing lookup table and rules.

Find the Google Font that echoes the subject's typographic character. One family for both heading and body is the default. A second family must earn its place.

### 5. Propose a style direction

Load [references/design-landscape.md](references/design-landscape.md) for the full catalog of six active design directions.

The style defines shape language, surface treatment, and compositional rules. It is recorded in the brief and the config, but it is **un-opinionated in application**: the style direction is a vocabulary that downstream skills interpret for their own medium. This skill defines *what the visual language is*, not *how every slide or page should look*.

Recommend the best fit based on context and offer 1-2 alternatives. Filter by context. Don't present all six.

**Anti-patterns regardless of style:**
- Rounded cards with shadows → SaaS product UI
- Cards nested inside cards → visual noise
- Gradient fills on content → marketing, not professional
- Inconsistent radius within a single composition

### 6. Draft the brief, then refine

Write `brand-brief.md` with everything so far. Present it and ask the user 2-3 targeted questions: the decisions most likely to benefit from their input.

Identify what to surface based on what you're least certain about. If the accent color was a clear derivation from the brand, don't ask about it. If you had to choose between two equally good fonts, surface that choice.

**Structure of the brief:**

```markdown
# Brand Brief: [Project Name]

## Context
[Who, what, for whom]

## Research
[What was found: colors, typeface, tone, sources]

## Color Palette
| Role | Hex | Rationale |
|---|---|---|
| ... | ... | ... |

## Typography
| Role | Font | Weights | Rationale |
|---|---|---|---|
| ... | ... | ... | ... |

## Visual Style
[Which direction, why, what it means in practice]

## Identity (if applicable)
[Project or firm name, tagline, positioning, only when the project calls for it]
```

Iterate until the user approves. Typically 1-3 rounds. Each round should narrow.

**Do not generate `identity.js` or render the preview until the brief is finalized.** The preview confirms decisions already made. It is not a design exploration tool.

### 7. Generate the config

Extract the approved brief into `identity.js`. Every value comes from the brief.

```javascript
module.exports = {
  // 'institutional' | 'modern' | 'dark' | 'bento' | 'editorial' | 'data-forward'
  style: 'modern',

  palette: {
    name: 'project-name',
    surfaceDark: '#...',  accent: '#...',  accentLight: '#...',
    surfaceMuted: '#...',  surface: '#...',
    text: '#...',  textMuted: '#...',  textFine: '#...',  textOnDark: '#FFFFFF',
    chartPrimary: '#...',  chartSecondary: '#...',
    positive: '#...',  warning: '#...',  negative: '#...',
  },

  fonts: {
    heading: { family: '...', weights: [600, 700], stack: "'...', system-ui, sans-serif" },
    body:    { family: '...', weights: [400, 600], stack: "'...', system-ui, sans-serif" },
    mono:    null,
  },

  // Optional: include when the project has a brand identity
  firm: null, // or { name: '...', tagline: '...', logoSVG: null }

  toCSS() { /* generates [data-palette="..."] { --accent: ...; --radius: ...; ... } */ },
  // Style tokens are included in the CSS output alongside palette colors.
  // Downstream skills use var(--radius), var(--card-border), etc.
};
```

### 8. Render the preview

Write a short Node script to the user's working directory. The script requires the engine from this skill's base directory (provided in context) and the identity config from the working directory:

```javascript
const { createPreview } = require('<this-skill>/engine');
const brand = require('./identity');
createPreview(brand, { output: './brand-preview.pdf' });
```

`<this-skill>` = this skill's base directory path. Node resolves `playwright` from the skill's own `node_modules/`. No install needed in the user's project.

Three slides: palette swatches, typography specimens + combo demo, cover on dark surface. Present to the user. If anything is off, update the brief first, then regenerate.

---

## Architecture

```
brand-system/
  SKILL.md                            ← always loaded (this file)
  references/
    palette-guide.md                  ← load when building palette
    typography-guide.md               ← load when choosing fonts
    design-landscape.md               ← load when proposing style
  engine/
    index.js                          ← createPreview(brand) → PDF
    render.js                         ← Playwright HTML → PDF
  package.json                        ← playwright only
  node_modules/                       ← self-contained
```

Self-contained: `package.json` + `node_modules/` are inside the skill folder. All `require()` calls resolve locally. No workspace-level install needed. Run `npm install` inside this skill folder if `node_modules/` is missing.

The `identity.js` this skill produces is an **input to downstream skills**, not an instruction. Downstream skills interpret the style direction for their own medium. This skill defines the vocabulary, not the implementation. Deck-building skills each define an identity intake step in their own SKILL.md that consumes this file directly (palette CSS for web-based renderers via `toCSS()`, theme-object registration for native PPTX).
