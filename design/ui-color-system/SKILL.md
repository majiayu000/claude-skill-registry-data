---
name: ui-color-system
description: >-
  Generate accessible color palettes (semantic + scale) with WCAG contrast checking for light/dark/high-contrast modes. AUTO-TRIGGERS when user asks for "color palette", "brand colors", "accessible colors", "dark mode colors", "color tokens", "WCAG", "contrast", "Theme-Farben", "Akzentfarbe", "Brand-Farben als Code", or wants WCAG-compliant UI colors.
version: 1.0.0
author: |
  Yuno (Hermes Agent) — based on KIMI K2 UI-Factory-Pattern 2026-06-30
license: MIT
metadata:
  hermes:
    tags: ['ui', 'color', 'palette', 'accessibility', 'wcag', 'contrast', 'brand', 'theming', 'dark-mode']
    related_skills: ['ui-design-system', 'ui-component-library', 'ui-dashboard', 'ui-factory', 'web-design-guidelines']
    part_of: ui-factory
    triggers: ['color palette', 'brand colors', 'WCAG', 'contrast', 'dark mode colors', 'color tokens', 'theme colors', 'Akzentfarbe', 'Brand-Farben', 'which colors', 'Farbschema', 'accessible colors']
lane: worker-vision
reasoning_effort: xhigh
agent: Designer
routing_hint: |
  **Agent-Scope:** UI/UX, visual, art-styles, design-systems, motion. Off-scope: code building, data modeling, long-form copy — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
## 🚨 AUTO-TRIGGER

Dieser Skill triggert **automatisch** wenn the user's Input UI-Farb-Themen enthält. Auch ohne expliziten Aufruf — wenn die Trigger-Phrasen matchen, wird dieser Skill geladen und seine Workflows genutzt.

**Trigger-Keywords (deutsch + englisch):** Farbe, Farben, Palette, Brand, Akzent, Theme, WCAG, Contrast, Dark Mode, Light Mode, Color, accessible, accessible colors

Wenn the user nach **mehreren UI-Aspekten** fragt (z.B. "komplettes UI mit Farben + Components + Dashboard"), wird stattdessen `ui-factory` getriggert (orchestriert color-system + design-system + component-library + dashboard als Chain).

# ui-color-system

> **Atom:** Generates accessible color palettes with WCAG contrast checks. Foundation for `ui-design-system` and every UI component.

## When to use

- User asks for "color palette", "brand colors", "accessible colors"
- Need light + dark + cozy + cyberpunk + high-contrast variants
- Want to verify WCAG AA/AAA compliance
- Migrating arbitrary hex codes to a semantic scale

## Inputs

```yaml
brief:
  brand_primary: "#7C3AED"  # hex code or skip to auto-generate
  mood: "trustworthy"  # trustworthy | playful | serious | cozy | futuristic | minimal
  modes: ["light", "dark", "high-contrast", "cozy", "cyberpunk"]  # which to generate
  accessibility_target: "AA"  # AA | AAA
  semantic_colors:
    - "primary"
    - "secondary"  # optional, auto-derived from primary if absent
    - "neutral"    # gray scale
    - "success"    # green
    - "warning"    # amber
    - "error"      # red
    - "info"       # blue
```

## Output

- **`colors.json`** — Structured palette with contrast checks
- **`colors.css`** — CSS variables ready to import
- **`contrast-report.md`** — Markdown report of all contrast pairs

## Workflow

### Step 1: Brand-Color-Analyse (1 min)

If `brand_primary` provided:
- Convert hex → HSL
- Extract hue (0-360)
- Calculate saturation/lightness for scale generation
- Validate it's not too close to black/white (needs room for scale)

If not provided, auto-generate based on `mood`:
- **trustworthy:** blue family (hue 200-220)
- **playful:** purple/pink family (hue 280-320)
- **serious:** navy/charcoal (hue 210-230, low sat)
- **cozy:** orange/amber family (hue 20-40)
- **futuristic:** cyan/teal (hue 170-190)
- **minimal:** neutral grayscale (any hue, low sat)

### Step 2: Scale-Generation (2 min)

Generate 10-step scale per color (Tailwind-inspired):

```yaml
primary:
  50:  # Lightest, near-white tint
  100: # Very light
  200: # Light
  300: # Light-medium
  400: # Medium-light
  500: # BASE — primary brand color (input)
  600: # Medium-dark
  700: # Dark
  800: # Very dark
  900: # Darkest, near-black shade
  950: # Almost black (for high-contrast mode)
```

**Algorithm for each step:**
```
For step n from 50 to 900:
  lightness = base_lightness + (n - 500) / 100 * adjustment_factor
  saturation = base_saturation * scale_factor(n)  # less saturated at extremes
  return hsl(base_hue, saturation, lightness)
```

### Step 3: Semantic-Assignment (1 min)

Map colors to semantic roles:
- `primary.500` → brand color (CTAs, links, focus)
- `primary.700` → hover state
- `primary.50` → light backgrounds (badges, highlights)
- `neutral.50-900` → gray scale (text, borders, backgrounds)
- `success.500` → positive actions (green)
- `warning.500` → caution states (amber)
- `error.500` → destructive actions (red)
- `info.500` → informational (blue)

### Step 4: Contrast-Checking (2-3 min)

Test all critical combinations using WCAG 2.2 formulas:

```typescript
function contrastRatio(fg: string, bg: string): number {
  const l1 = relativeLuminance(fg);
  const l2 = relativeLuminance(bg);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}

function relativeLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  const [r, g, b] = [rgb.r, rgb.g, rgb.b].map(v => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
```

**Required contrast pairs to test (min. 10, ideal 17+):**

| Pair | AA | AAA | Use |
|------|-----|------|-----|
| `primary.700` on `neutral.50` | 4.5 | 7.0 | Body text on background |
| `primary.700` on `cozy.cream` | 4.5 | 7.0 | Text on cozy mode cream BG |
| `primary.900` on `neutral.50` | 4.5 | 7.0 | Heading on background |
| `primary.500` on `neutral.900` | 4.5 | 7.0 | Inverse (dark mode) |
| `neutral.900` on `neutral.50` | 4.5 | 7.0 | Default text |
| `neutral.50` on `neutral.900` | 4.5 | 7.0 | Inverse default text |
| `success.700` on `success.50` | 4.5 | 7.0 | Success text |
| `warning.700` on `warning.50` | 4.5 | 7.0 | Warning text |
| `error.700` on `error.50` | 4.5 | 7.0 | Error text |
| `info.700` on `info.50` | 4.5 | 7.0 | Info text |
| `white` on `primary.500` | 4.5 | 7.0 | Button text on brand |
| `white` on `primary.700` | 4.5 | 7.0 | Button text on hover |
| `white` on `neutral.800` | 4.5 | 7.0 | Button text on dark bg |
| `primary.500` on `white` | 3.0 | — | UI icon on background |
| `error.500` on `white` | 3.0 | — | Error icon on background |
| `accent.700` on `cyber.bg` | 4.5 | 7.0 | Neon accent on cyberpunk bg |
| `neutral.50` on `cyber.bg` | 4.5 | 7.0 | Text on cyberpunk bg |
| `white` on `black` | 7.0 | 7.0 | A11y mode text (AAA guaranteed) |

### Step 5: Dark-Mode-Generation (2 min)

For dark mode, invert the lightness curve:
- `neutral.50` (light bg in light mode) → `neutral.900` (dark bg in dark mode)
- `neutral.900` (dark text in light mode) → `neutral.50` (light text in dark mode)
- Primary stays similar hue but slightly desaturated (reduces eye strain)

**Dark mode adjustments:**
- Reduce contrast slightly (8:1 → 7:1, easier on eyes)
- Reduce saturation by 10-15% (less vibrant in dark)
- Use `neutral.800/900` as base bg, not pure black (OLED-friendly)

### Step 6: High-Contrast-Mode (1 min)

For accessibility (WCAG AAA + Windows High Contrast):
- Pure black `#000000` background
- Pure white `#FFFFFF` text
- Saturated primary colors (no subtle desaturation)
- Minimum 7:1 contrast for all text
- No gradients (solid colors only)
- Visible focus indicators (3px solid, not just outline)

### Step 6b: Cyberpunk-Mode (1 min, optional)

For dark + neon aesthetic (inspired by 2026-07-06 Yuno-Operator-Build):
- Deep purple/night BG: `#0D0020` (neutral.950-like with purple shift)
- Neon Magenta accents: `#FF1493` (DeepPink) for CTAs and highlights
- Sparkle-Particle overlays: 4× radial-gradients at 0.04 opacity (0.12 in cyberpunk)
- Bright Cyan `#00E5FF` for secondary accents (hacker-green alternative)
- Text on cyberpunk bg: **immer dunkle Töne verwenden, nicht White** — White auf Magenta-500 = 3.64:1 FAIL. Stattdessen `Night-700` (`#1A0033`) oder `Night-800` (`#0D0020`)
- Buttons: Magenta-700 (`#B30066`) on Night-800, Text = Night-700 (`#1A0033`, 5.48:1 ✓)
- Card-BG: `#1A0033` (eine Stufe heller als page BG)

**Cyberpunk adjustments vs Dark mode:**
- Higher saturation (doesn't need to reduce eye strain — it's intentionally intense)
- Gradient buttons allowed (but ensure text still passes AA on darkest gradient point)
- Subtle glow effects via `box-shadow` with neon color
- Use `@media (prefers-reduced-motion)` to disable glow animations

### Step 7: Output-Generation (1 min)

**`colors.json`:**
```json
{
  "primary": {
    "50": "#F5F3FF",
    "100": "#EDE9FE",
    "200": "#DDD6FE",
    "300": "#C4B5FD",
    "400": "#A78BFA",
    "500": "#7C3AED",
    "600": "#6D28D9",
    "700": "#5B21B6",
    "800": "#4C1D95",
    "900": "#3B0F7A",
    "950": "#2E1065"
  },
  "neutral": {
    "50": "#FAFAFA",
    "100": "#F4F4F5",
    "200": "#E4E4E7",
    "300": "#D4D4D8",
    "400": "#A1A1AA",
    "500": "#71717A",
    "600": "#52525B",
    "700": "#3F3F46",
    "800": "#27272A",
    "900": "#18181B",
    "950": "#0A0A0A"
  },
  "success": {
    "50": "#ECFDF5",
    "500": "#10B981",
    "700": "#047857",
    "900": "#064E3B"
  },
  "warning": {
    "50": "#FFFBEB",
    "500": "#F59E0B",
    "700": "#B45309",
    "900": "#78350F"
  },
  "error": {
    "50": "#FEF2F2",
    "500": "#EF4444",
    "700": "#B91C1C",
    "900": "#7F1D1D"
  },
  "info": {
    "50": "#EFF6FF",
    "500": "#3B82F6",
    "700": "#1D4ED8",
    "900": "#1E3A8A"
  },
  "modes": {
    "light": {
      "bg": "neutral.50",
      "fg": "neutral.900",
      "border": "neutral.200",
      "muted": "neutral.500"
    },
    "dark": {
      "bg": "neutral.900",
      "fg": "neutral.50",
      "border": "neutral.700",
      "muted": "neutral.400"
    },
    "high-contrast": {
      "bg": "neutral.950",
      "fg": "neutral.50",
      "border": "primary.300",
      "muted": "neutral.200"
    }
  }
}
```

**`colors.css`:**
```css
:root {
  --color-primary-50: #F5F3FF;
  --color-primary-500: #7C3AED;
  --color-primary-700: #5B21B6;
  /* ... */
  --color-bg: var(--color-neutral-50);
  --color-fg: var(--color-neutral-900);
  --color-success: var(--color-success-500);
  --color-error: var(--color-error-500);
}

[data-theme="dark"] {
  --color-bg: var(--color-neutral-900);
  --color-fg: var(--color-neutral-50);
}

[data-theme="high-contrast"] {
  --color-bg: var(--color-neutral-950);
  --color-fg: var(--color-neutral-50);
  --color-primary-500: var(--color-primary-300); /* brighter for contrast */
}
```

**`contrast-report.md`:**
```markdown
# Contrast Report

Generated 2026-06-30 by Yuno ui-color-system skill.

## Light Mode

| Pair | Ratio | AA | AAA | Status |
|------|-------|-----|------|--------|
| primary.700 on neutral.50 | 7.2:1 | ✓ | ✓ | PASS |
| neutral.900 on neutral.50 | 16.4:1 | ✓ | ✓ | PASS |
| success.700 on success.50 | 5.8:1 | ✓ | ✗ | PASS AA |
| error.700 on error.50 | 6.4:1 | ✓ | ✗ | PASS AA |
| white on primary.500 | 4.6:1 | ✓ | ✗ | PASS AA |

## Dark Mode

| Pair | Ratio | AA | AAA | Status |
|------|-------|-----|------|--------|
| primary.300 on neutral.900 | 8.1:1 | ✓ | ✓ | PASS |
| neutral.50 on neutral.900 | 15.8:1 | ✓ | ✓ | PASS |

## High-Contrast Mode

All pairs ≥ 7.0:1 (WCAG AAA).

## Violations

None — all critical combinations pass AA.

## Recommendations

- Use `primary.700` (not `primary.500`) for body text on light backgrounds
- Use `primary.300` (not `primary.500`) for accents on dark backgrounds
- For accessibility mode, swap to high-contrast palette via `[data-theme="high-contrast"]`
```

## Validation Checklist

- [ ] At least 10-step scale per color (50-950)
- [ ] All semantic roles assigned (primary, neutral, success, warning, error, info)
- [ ] Light + dark + high-contrast modes generated (cozy + cyberpunk optional)
- [ ] All critical contrast pairs checked (≥10 pairs, ideal 17+)
- [ ] AA minimum for all text (4.5:1)
- [ ] AAA for primary text (7:1) where possible
- [ ] Color-blind simulation passed (deuteranopia, protanopia, tritanopia)
- [ ] High-contrast mode follows WCAG AAA + Windows HC spec
- [ ] No pure black `#000000` in regular dark mode (use neutral.950)
- [ ] **Cyberpunk mode: Night-BG statt Neutral (0D0020), neon-tauglich**
- [ ] **A11y mode als separates Theme (data-theme="a11y") — nicht nur prefers-contrast**
- [ ] **Helle Brand-Colors (Pink, Coral, Cyan, Lime, Gelb): primary-800/900 als Button-BG testen, nicht nur 700**

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hardcoding colors in components | Reference CSS variables always |
| Same color for light + dark mode | Generate separate palettes with inverted lightness |
| No contrast checking | Run ui-color-system contrast-check before shipping |
| Using red/green only for status | Add icon + text (color-blind friendly) |
| Pure black `#000000` in dark mode | Use `#0A0A0A` (neutral.950) — OLED-friendly, less harsh |
| Bright saturated colors in dark mode | Desaturate by 10-15% — reduces eye strain |
| Missing focus-visible contrast | Test focus ring against bg, ≥3:1 |

## Color-Blind-Simulation

Test palette with simulators:
- **Deuteranopia** (red-green, 6% of males)
- **Protanopia** (red-green, 1% of males)
- **Tritanopia** (blue-yellow, <1%)

Tools: [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/), Sim Daltonism, Chrome DevTools Rendering > "Emulate vision deficiencies"

If primary brand color is indistinguishable from success/error for color-blind users, **add icon + text labels** (not just color).

## Companion Skills

- **`claude-design`** — Color-Doctrine ist dort detaillierter ("Color"-Sektion). ui-color-system ist die MECHANIK (Token-Generation + WCAG-Check), claude-design ist die PHILOSOPHIE (wie Color Kontext trägt).
- **ui-design-system** — REQUIRED next step (uses these colors as tokens)
- **ui-component-library** — Components reference these variables
- **ui-dashboard** — Composes components with consistent theming
- **web-design-guidelines** — Vercel's UI review checklist

## Part of UI-Factory

This is the **first atom** in the UI-Factory pattern. Run before `ui-design-system`. Output colors feed into tokens, which feed into components, which compose into dashboards.

Based on the KIMI K2 UI-Factory-Pattern (2026-06-30).