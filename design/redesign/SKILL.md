---
name: redesign
description: Redesign or restyle existing UI to match a specific brand's design system. Use when the user has existing code, components, or an app and wants to transform the visual language to match Apple, Stripe, Linear, Notion, Vercel, or any of 58 curated design systems. Also trigger when the user says "retheme", "restyle", "make this look like [brand]", "apply [brand] design", wants to migrate an app's visual identity, change the look and feel, or apply a new skin to existing UI. This includes partial redesigns like "make just the header look like Linear" or "use Stripe's color palette".
---

# Redesign Existing UI

Transform existing UI code to match a target brand's design system. Unlike building from scratch, redesign requires analyzing what exists, creating a mapping between current and target tokens, and transforming systematically while preserving functionality.

## Why redesign is different from building new

Building new UI is additive — you start from nothing. Redesign is transformative — you must understand what exists, identify every visual decision in the current code, and replace each one with the target system's equivalent. The risk is breaking functionality or missing tokens, so the approach must be methodical.

## Available Designs

Read `design-md/_index.md` for the full catalog of 58 available design systems.

## Workflow

### 1. Analyze the existing UI

Before loading any target design, understand the current code:

**Inventory the current design tokens:**
- Colors: background, text, borders, accents, interactive states
- Typography: font families, size scale, weights, line-heights
- Spacing: padding, margins, gaps — identify the base unit
- Shadows: elevation levels, shadow colors
- Border-radius: scale being used
- Component patterns: button styles, card styles, input styles

**Identify the tech stack:**
- What framework (React, Vue, Svelte, plain HTML)?
- What styling approach (Tailwind, CSS modules, styled-components, inline, CSS vars)?
- Are there existing theme files, CSS custom properties, or design tokens?

**Map the structure:**
- Which files contain styling?
- Are styles co-located with components or in separate stylesheets?
- Is there a theme provider or global CSS?

### 2. Identify the target design

Match the user's request against the catalog in `design-md/_index.md`. Load the target `design-md/{directory}/DESIGN.md`.

### 3. Create the token mapping

This is the most important step. Build an explicit mapping between current tokens and target tokens:

**Color mapping:**
```
Current background (#f8f9fa) → Target background (from Section 2)
Current primary text (#212529) → Target heading color (from Section 2)
Current body text (#495057) → Target body text (from Section 2)
Current accent (#0d6efd) → Target primary accent (from Section 2)
Current hover state (#0b5ed7) → Target hover state (from Section 4)
```

**Typography mapping:**
```
Current font-family → Target font families (from Section 3)
Current heading sizes → Target heading hierarchy (from Section 3)
Current body size → Target body size (from Section 3)
Current weights → Target weights (from Section 3)
Current line-heights → Target line-heights (from Section 3)
```

**Spacing mapping:**
```
Current base unit → Target base unit (from Section 5)
Current spacing scale → Target spacing scale (from Section 5)
```

**Shadow mapping:**
```
Current shadow levels → Target shadow system (from Section 6)
```

**Radius mapping:**
```
Current border-radius scale → Target border-radius scale (from Section 5)
```

### 4. Transform systematically

Apply the mapping in this order. Each layer builds on the previous one, so the order matters:

**Step 1 — Colors**: Replace all color values. This is the highest-impact change.
- Background surfaces
- Text colors (heading, body, secondary, muted)
- Border colors
- Accent/brand colors
- Interactive states (hover, active, focus, disabled)
- Shadow colors (often brand-tinted — don't miss this)

**Step 2 — Typography**: Replace font families, update size hierarchy.
- Swap font-family declarations
- Adjust sizes to match the target hierarchy table
- Update weights (some brands are heavy, some are light)
- Adjust line-heights and letter-spacing (huge impact on feel)
- Add font import/link if needed

**Step 3 — Spacing**: Adjust spacing to match the target system.
- Remap padding and margins to the target scale
- Adjust gaps in flex/grid layouts
- Update container max-widths and gutters

**Step 4 — Components**: Restyle interactive elements.
- Buttons: shape, padding, radius, states
- Cards: border treatment, shadow, radius, padding
- Inputs: border style, focus ring, padding
- Navigation: layout pattern, active states

**Step 5 — Depth**: Replace shadow system.
- Apply target shadow values at each elevation level
- Update any gradient backgrounds
- Adjust overlay/backdrop styles

**Step 6 — Responsive**: Adjust breakpoints if they differ significantly.
- Usually the least disruptive — most responsive patterns are similar
- Focus on touch targets and mobile-specific spacing

### 5. Check guardrails

Read Section 7 (Do's and Don'ts) of the target DESIGN.md and verify:
- Nothing in the "Don't" list is present in the output
- Key items in the "Do" list are followed
- The overall atmosphere from Section 1 is achieved

### 6. Present the changes

Show the user a clear summary:

**Token mapping table:**
| Token | Before | After |
|-------|--------|-------|
| Background | `#f8f9fa` | `{target value}` |
| Primary text | `#212529` | `{target value}` |
| ... | ... | ... |

**Files modified** with a brief note on what changed in each.

**Before/after comparison** — describe the visual difference the changes create.

**Font imports** or other dependencies that need to be added.

## Partial redesigns

If the user wants to restyle only part of the UI (e.g., "make the header look like Linear"):
- Still load the full DESIGN.md for reference
- Only transform tokens within the specified scope
- Ensure visual coherence at the boundary between redesigned and original sections
- Warn the user if the partial redesign creates visual inconsistency

## Preserving functionality

Never change:
- Component logic, event handlers, or state management
- Data flow, API calls, or business logic
- Accessibility attributes (aria-*, role, tabIndex)
- Semantic HTML structure (unless the target design requires a different layout pattern)
- Test selectors or IDs used by automated tests

Only change visual presentation — colors, fonts, spacing, shadows, borders, and layout CSS.
