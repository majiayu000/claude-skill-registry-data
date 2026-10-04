---
name: ui-design-system
description: >-
  Generate a complete design system (tokens, colors, typography, spacing scale) as JSON/CSS variables from a brief. Trigger phrases: creative/ui, design, system. Converted from Hermes-Skill (Yuno's mastery library).
version: 1.0.0
changelog:
  - 1.0.0 (2026-07-03): Initial conversion from MiniMax Hub
author: Toqsick + Yuno (Hub→Hermes conversion)
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    source: minimax-hub
    hub_skill_id: creative-ui-design-system
    category: ui-design-system
    domain: multimedia
    converted_at: 2026-07-03T23:19:32.978737
  tags:
    - hub
    - conversion
    - workflow
triggers:
  - creative/ui
  - design
  - system
agent: Designer
routing_hint: |
  **Agent-Scope:** UI/UX, visual, art-styles, design-systems, motion. Off-scope: code building, data modeling, long-form copy — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
> **Hub Origin:** Convexed from MiniMax Hub skill `creative/ui-design-system` (version 1.0.0). Original Hub-SKILL.md is preserved at `scripts-originals/SKILL.md.hub`, original meta.yaml at `scripts-originals/meta.yaml.hub`. All Hub-specific paths (e.g. `~/.hub-global/skills/creative-ui-design-system/`) translated to Hermes-equivalent references in `references/`.
## 🚨 AUTO-TRIGGER

Dieser Skill triggert **automatisch** wenn the user's Input nach Design-System/Tokens fragt. Auch ohne expliziten Aufruf — wenn die Trigger-Phrasen matchen, wird dieser Skill geladen.

**Trigger-Keywords (deutsch + englisch):** design system, design tokens, tokens, CSS variables, theme, brand identity, Komponenten-Standards, Brand-Identität, theme aufbauen, Token-Set, Spacing-Skala, Typography-Skala

Wenn the user nach **mehreren UI-Aspekten** fragt (z.B. "komplettes UI mit Tokens + Components + Dashboard"), wird stattdessen `ui-factory` getriggert (orchestriert die ganze Chain).

# ui-design-system

> **Atom:** Generates a complete, accessible design-system as JSON tokens + CSS variables from a brief. The foundation every other UI skill builds on.

## When to use

- User asks for a "design system", "design tokens", "brand identity" als Code
- Starting a new project and want consistency from day one
- Migrating from arbitrary values to a token-based approach
- Need CSS variables for a theme (light/dark/high-contrast)

## Inputs

```yaml
brief: |
  - Product type (SaaS, e-commerce, dashboard, blog, etc.)
  - Mood/feel (clean, playful, serious, cozy, futuristic)
  - Mode (light, dark, both)
  - Brand colors (if any hex codes provided)
  - Typography preference (sans, serif, mono, mixed)
  - Accessibility target (WCAG AA, AAA)
```

## Output

**3 deliverables:**

1. **`tokens.json`** — Structured design tokens (Style Dictionary format)
2. **`tokens.css`** — CSS variables ready to drop into any project (`@import url('tokens.css')`)
3. **`tokens.d.ts`** — TypeScript types for IDE autocompletion

## Workflow

### Step 1: Brief-Analyse (1-2 min)

Parse the brief. Extract:
- **Product type** → influence spacing density (compact vs cozy)
- **Mood** → influence corner radius (sharp vs rounded), shadows (subtle vs bold)
- **Mode** → generate light OR dark OR both palettes
- **Brand colors** → use as-is or generate complementary palette

### Step 2: Token-Generation (3-5 min)

Generate token categories:

| Category | Tokens | Reasoning |
|----------|--------|-----------|
| **Color** | `primary`, `secondary`, `accent`, `neutral.50-900`, `success/warning/error/info` | Semantic + scale |
| **Typography** | `font.family.sans/serif/mono`, `font.size.xs-6xl`, `font.weight.regular-bold`, `lineHeight.tight/relaxed` | Fluid type with clamp() |
| **Spacing** | `space.0-32` (4px base scale) | 4px or 8px grid |
| **Radius** | `radius.none/sm/md/lg/xl/full` | 0, 2, 6, 12, 24, 9999 |
| **Shadow** | `shadow.xs/sm/md/lg/xl/2xl` | Elevation scale |
| **Motion** | `duration.fast/normal/slow`, `easing.default/in/out` | 150/300/500ms, ease-in-out |
| **Z-Index** | `z.dropdown/modal/toast/popover` | Layering |
| **Breakpoints** | `breakpoint.sm/md/lg/xl/2xl` | 640/768/1024/1280/1536 |

### Step 3: Accessibility-Check (2-3 min)

Run contrast checks on all color combinations:
- **Text on background:** ≥ 4.5:1 (AA) or ≥ 7:1 (AAA)
- **UI components:** ≥ 3:1 (AA non-text)
- **Large text (18pt+):** ≥ 3:1

Report violations with suggested fixes:
```
❌ primary-500 on neutral-50: 2.8:1 (FAIL AA)
✅ Fix: use primary-700 on neutral-50: 6.2:1 (PASS AAA)
```

### Step 4: Output Generation (1 min)

Generate all 3 deliverables in code-blocks.

### Step 5: Usage-Doc

Short README section showing how to import in different stacks:
- **Vanilla HTML:** `<link rel="stylesheet" href="tokens.css">`
- **React/Vue:** `import './tokens.css'` + `tokens.json` via Style Dictionary
- **Tailwind:** `tailwind.config.js` reads from `tokens.json`

## Example

**Input:**
```yaml
brief: |
  Modern SaaS dashboard for developers.
  Dark mode default.
  Clean, minimal, slightly playful.
  Brand color: #7C3AED (purple).
  Sans-serif typography.
  WCAG AA minimum.
```

**Output:** (abbreviated — full version in `examples/saas-dashboard-dark.md`)
```json
// tokens.json
{
  "color": {
    "primary": {
      "50": "#F5F3FF",
      "500": "#7C3AED",
      "900": "#4C1D95"
    },
    "neutral": {
      "50": "#FAFAFA",
      "900": "#0A0A0A"
    },
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#3B82F6"
  },
  "font": {
    "family": {
      "sans": "Inter, system-ui, sans-serif",
      "mono": "JetBrains Mono, monospace"
    },
    "size": {
      "xs": "clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem"
    }
  },
  "space": {
    "0": "0",
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "0.75rem",
    "4": "1rem",
    "6": "1.5rem",
    "8": "2rem",
    "12": "3rem",
    "16": "4rem",
    "24": "6rem"
  },
  "radius": {
    "sm": "0.25rem",
    "md": "0.5rem",
    "lg": "0.75rem",
    "xl": "1rem",
    "full": "9999px"
  }
}
```

```css
/* tokens.css */
:root {
  --color-primary-500: #7C3AED;
  --color-primary-700: #6D28D9;
  --color-neutral-50: #FAFAFA;
  --color-neutral-900: #0A0A0A;
  --font-sans: Inter, system-ui, sans-serif;
  --font-size-base: 1rem;
  --space-4: 1rem;
  --radius-md: 0.5rem;
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --duration-normal: 300ms;
}
```

## Validation Checklist

- [ ] All token categories present (color, font, space, radius, shadow, motion, z-index, breakpoints)
- [ ] At least 3 contrast combinations checked for AA
- [ ] All hex values are 7-character (`#XXXXXX`)
- [ ] Spacing follows 4px or 8px grid (no arbitrary values like `13px`)
- [ ] Font sizes use `clamp()` for fluid typography
- [ ] CSS variables use kebab-case (`--font-size-base`)
- [ ] JSON uses camelCase or kebab-case consistently

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `px` for spacing instead of `rem` | Convert: `16px → 1rem` (root font-size dependent) |
| Hardcoding colors in components | Reference `--color-primary-500` always |
| Random hex codes without contrast check | Use ui-color-system first to validate |
| Skipping dark mode tokens | Generate `light` and `dark` variants, swap with `[data-theme="dark"]` |

## Companion Skills

- **`claude-design`** — Die design-philosophische "Surface-First"-Doctrine. Lies das ZUERST wenn du nicht sicher bist welcher Surface-Type es ist (Monitor / Operate / Compare / Configure / Decide-Learn / Explore / Command-Inspect). ui-design-system liefert die Tokens, claude-design liefert die Composition-Regel.
- **ui-color-system** — Generate accessible color palette BEFORE running ui-design-system
- **ui-component-library** — Use design tokens to scaffold components
- **ui-dashboard** — Compose components into a dashboard layout (Monitor-Surface)
- **web-design-guidelines** — Vercel's UI review checklist for additional polish

## Part of UI-Factory

This skill is one of the **atoms** in the UI-Factory pattern:
- **Atoms (Skills):** ui-design-system, ui-color-system, ui-component-library, ui-dashboard
- **Molecules (Agents):** ui-builder, ui-designer (compose multiple atoms with SOUL.md)
- **Organisms (Loops):** Cron/Webhook automation (nightly a11y-scan, drift detection, PR-review)

Based on the KIMI K2 UI-Factory-Pattern (2026-06-30).

---

_Converted from Hermes-Skill by Yuno. Original SKILL.md preserved in references/original-hermes.md._
