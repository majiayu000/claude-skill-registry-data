---
name: design-system
description: Use when establishing visual foundations for a new product, when defining design tokens, when building or auditing a component library, before any UI work begins on a fresh codebase, or when the existing UI has drifted into hex codes and magic numbers.
---

# Design System

## Overview

Define the visual + interaction foundation *before* features get built. Output is `.forge/design-system.md` — the semantic token layer (color, typography, spacing, radius, motion), the breakpoint and dark-mode rules, the primitive component inventory with all states, the gallery, the composition rules, and the documented anti-patterns. Consumed by every UI-shipping skill (`incremental-implementation`, `interaction-patterns`, `accessibility`, `demo-narrative`).

## When to Use

- A new product or marketing surface is being designed and nothing exists yet
- The codebase has 20+ components with inconsistent spacing, radii, or color usage
- A redesign is starting and the team wants a foundation before screens get built
- Dark mode is being added and the existing palette has raw hex everywhere
- Two designers or two engineers are about to ship competing button styles

## When NOT to Use

- A single one-off internal admin page with no future
- A backend-only service with no UI surface
- A tiny bug fix to one component — that's `incremental-implementation`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll standardize later" | Later means 50 components with 50 different spacing values. Standardization costs nothing on day one, costs a refactor on day 200. |
| "Just use Tailwind defaults" | Defaults without a semantic mapping create implicit coupling to the framework. When the framework changes, every component breaks. |
| "Dark mode can wait" | Retrofitting dark mode costs 5x building it in. Every color picked without dark-mode awareness becomes a contrast bug. |
| "Loading states aren't important" | A component without a loading state is a component that lies about its readiness. The user sees a button that looks ready and isn't. |
| "Designer will fix it later" | The component shipped to production *is* the design. Later means never. |
| "It looks fine in Figma" | Figma is not the runtime. Real fonts render differently, real data overflows, real users have light/dark/HC modes. |

## Red Flags

- A hex code (`#3B82F6`) anywhere in a component file
- A spacing value not from the scale (`padding: 13px`)
- A component without a `disabled` or `loading` state
- Inconsistent `border-radius` across two buttons in the same product
- A color used to convey meaning with contrast below WCAG AA
- A component that "works" in light mode and breaks in dark
- A skeleton screen on one page and a spinner on the next
- A button that has hover but no focus-visible outline

## Core Process

### Step 1: Define the brand foundation

Pin down before tokens:
- Brand voice (formal / friendly / technical / playful) — informs typography choice and motion timing
- One accent color (the brand color)
- One neutral scale (warm / cool / true gray)
- Density target (compact / comfortable / spacious)

### Step 2: Write the semantic token layer

Two levels:

```
Reference tokens          →   Semantic tokens
gray-50, gray-100, ...    →   surface, surface-muted, border, text, text-muted
blue-500, blue-600, ...   →   accent, accent-hover, accent-active
red-500                   →   danger, danger-bg
```

Components use **only** semantic tokens. Never reference tokens directly. Dark mode is a remapping of semantic → reference tokens, not a rewrite.

Document every semantic token with: light hex, dark hex, WCAG contrast against its default partner, intended use.

### Step 3: Define the scales

- **Typography:** 6-7 sizes (caption / body / body-lg / heading-sm / heading / heading-lg / display). Line height per size. Font family + weight roles (regular / medium / semibold).
- **Spacing:** 4px or 8px grid. 6-8 stops (`0, 2, 4, 8, 12, 16, 24, 32, 48, 64`). No values outside this scale.
- **Radius:** 3-4 values (`none, sm, md, lg, full`). One canonical radius per component type.
- **Motion:** 3 durations (`fast 150ms / normal 250ms / slow 400ms`). 2 easings (`standard, emphasized`). Respect `prefers-reduced-motion`. For detailed motion conventions, generate and reference [references/motion-system.md](../../references/motion-system.md) alongside the design-system artifact.
- **Breakpoints:** mobile-first. 3-4 stops (`sm 640 / md 768 / lg 1024 / xl 1280`). Document which is the "design target."

### Step 4: Define primitive components with all 6 states

Every interactive primitive has **default / hover / active / focus-visible / disabled / loading / error** documented. Build the inventory:

| Primitive | States required |
|---|---|
| Button (primary, secondary, ghost, danger) | all 6 |
| Input (text, number, password, search) | all 6 + filled, with-error |
| Select / combobox | all 6 + open, with-search |
| Checkbox / radio / switch | all 6 + checked, indeterminate |
| Toast / banner | info, success, warning, error, with-action |
| Skeleton | matches every component that fetches |

Skeleton screens, not spinners, for content-shaped loading.

### Step 5: Write the gallery

A single Storybook (or equivalent) page per primitive showing every state, every size, every variant in light + dark. The gallery *is* the design system documentation — code and Figma diverge; the gallery doesn't.

### Step 6: Composition rules + anti-patterns

In `.forge/design-system.md`:
- How primitives compose into patterns (toolbar, form row, list item, empty state, error state).
- The anti-patterns: don't nest cards 3-deep, don't use red for anything but danger, don't put a spinner inside a button without disabling the button, don't mix toast and modal for the same severity.

## Verification

- [ ] `.forge/design-system.md` written
- [ ] No raw hex in any component (grep for `#[0-9a-fA-F]{6}`)
- [ ] All spacing values come from the scale (grep for `px:` and `padding:` values not in the scale)
- [ ] Every interactive primitive has all 6 states documented in the gallery
- [ ] Dark mode has parity — every screen renders cleanly in both modes
- [ ] Every text/background pairing meets WCAG AA (4.5:1 for body, 3:1 for large text)
- [ ] Every async action has a skeleton or loading state — no bare spinners on content
- [ ] `prefers-reduced-motion` respected — no animation longer than 100ms when set
- [ ] Focus-visible outline on every interactive element (no `outline: none` without a replacement)
