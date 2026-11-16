---
name: design-tokens-system
description: Enterprise design token architecture. Defines spacing, scaling, elevation, and grid systems following Adobe Spectrum, Salesforce Lightning, Amazon Style Dictionary, and 6 other production token systems. Use when building or auditing a token layer for any UI project.
origin: yana-ai — synthesized from adobe/spectrum-tokens, salesforce/design-system-tokens, amzn/style-dictionary, workday/canvas-tokens, elastic/eui, microsoft/fluentui-design-tokens, pinterest/gestalt, backpack/backpack-tokens, dekorator/design-tokens, audi/appearance
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 1.3.35
---

# /design-tokens-system

## When to Use

- Starting a new design system or component library
- Auditing existing token structure for inconsistency
- Cross-platform token compilation (web → iOS → Android)
- "Spacing is inconsistent", "shadows feel random", "hard to maintain scale"

## Do NOT use for

- One-off UI tweaks that don't require a system
- Projects with < 5 components (use inline values)

---

## Token Architecture (Style Dictionary pattern — Amazon)

```
tokens/
  base/          ← primitive values (raw numbers, hex codes)
    color.json
    spacing.json
    typography.json
    shadow.json
  semantic/      ← purpose-mapped aliases
    color.json   ← color.background.primary → base.blue.500
    spacing.json ← spacing.component.gap → base.spacing.4
  component/     ← component-scoped overrides
    button.json
    card.json
```

**Rule:** Never reference base tokens directly in component code.
Always use semantic tokens. Semantic tokens reference base tokens.

---

## Spacing Scale (Salesforce Lightning + Backpack mobile)

```json
{
  "spacing": {
    "1":  "4px",
    "2":  "8px",
    "3":  "12px",
    "4":  "16px",
    "5":  "20px",
    "6":  "24px",
    "8":  "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px",
    "24": "96px"
  }
}
```

Mobile (Backpack): use 4px base unit. Desktop: 8px base unit.
Never invent spacing values outside this scale.

---

## Elevation / Shadow Scale (Workday Canvas + Elastic EUI)

```json
{
  "elevation": {
    "0": "none",
    "1": "0 1px 2px rgba(0,0,0,0.08)",
    "2": "0 2px 4px rgba(0,0,0,0.10)",
    "3": "0 4px 8px rgba(0,0,0,0.12)",
    "4": "0 8px 16px rgba(0,0,0,0.14)",
    "5": "0 16px 32px rgba(0,0,0,0.16)"
  }
}
```

Cards = elevation.2. Modals = elevation.4. Tooltips = elevation.3.
Never use arbitrary box-shadow values.

---

## Scaling / Density (Adobe Spectrum)

Adobe Spectrum defines 3 scale densities:
- `medium` — desktop default (base 14px)
- `large` — touch-optimized (base 17px)
- `extra-large` — accessibility (base 20px)

All spacing and typography tokens scale proportionally when density changes.
Implement via CSS custom properties + data-scale attribute on root.

---

## Grid System (Pinterest Gestalt — Masonry + Microsoft Fluent — Responsive)

```css
/* Fluid grid — 4-column mobile, 8-column tablet, 12-column desktop */
.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-cols, 12), 1fr);
  gap: var(--spacing-4);
  padding: 0 var(--spacing-6);
}

@media (max-width: 768px)  { --grid-cols: 4; }
@media (max-width: 1024px) { --grid-cols: 8; }
```

---

## Token Compilation (amzn/style-dictionary)

```bash
# Build tokens to all platforms
npx style-dictionary build --config style-dictionary.config.json

# Output: dist/tokens/css/variables.css
#         dist/tokens/ios/StyleDictionaryColor.swift
#         dist/tokens/android/colors.xml
```

---

## Anti-Pattern Checklist

```
❌ Hardcoded hex values in component styles (#3B82F6 → use color.primary.500)
❌ Arbitrary spacing not from scale (margin: 13px → round to nearest token)
❌ Shadow values not from elevation scale
❌ Component-scoped tokens not documented in component/token file
❌ Base tokens referenced directly in components
```
