---
name: component-library
description: Use when building a component catalog, when standardizing component props and states across a product, when two engineers are about to build competing versions of the same component, or before a major UI build sprint.
---

# Component Library

## Overview

Catalog every component the product needs *before* the build sprint — props, states, responsive behavior, accessibility, composition rules, and microcopy. Output is `.forge/component-library.md`. Inherits tokens from `design-system`, behaviors from `interaction-patterns`, and voice + icons from `brand-and-identity`. Consumed by `page-composition`, `data-visualization`, and every UI build task.

## When to Use

- A major UI build sprint is starting and no component catalog exists
- Two engineers are about to build a `Button` / `Card` / `Modal` independently
- The codebase has 3 different `Button` components with different APIs
- A new domain-specific component (`ScoreCard`, `RepCard`, `CallTimeline`) is being designed
- A redesign is replacing shadcn defaults with domain-shaped components

## When NOT to Use

- A single one-off component for one screen — `incremental-implementation`
- Backend-only services
- The product genuinely doesn't have a UI yet — establish `design-system` and `interaction-patterns` first

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll extract components as we go" | Extraction after the fact means 3 versions of `Button` with different APIs. Catalog first, build once. |
| "This is premature abstraction" | A component catalog is not abstraction. It's a vocabulary. You define words before writing sentences. |
| "Just use shadcn and move on" | shadcn gives generic components. `ScoreCard`, `RepCard`, `CallTimeline` are domain-specific — those need defining. |
| "Props can evolve" | Props that evolve without a catalog diverge. One engineer adds `size`, another adds `isLarge`. The catalog prevents this. |
| "We don't need a loading state for that component" | Every async component lies about readiness without a loading state. |

## Red Flags

- Two components doing the same job under different names (`Button` and `ActionButton`, `Card` and `Panel`)
- A component with 15+ props — it's two components fused
- A component without a `loading` or `empty` state
- Hardcoded strings inside a component instead of prop-driven microcopy
- No accessibility attributes (`role`, `aria-*`) on interactive components
- A component accepting `className` as a token-override escape hatch

## Core Process

### Step 1: Read upstream artifacts

Read `.forge/design-system.md` (tokens, spacing, motion, breakpoints), `.forge/interaction-patterns.md` (behaviors per shape), `.forge/brand-identity.md` (voice + icon system). The catalog inherits from these. If any are missing, run them first — building the catalog without them encodes accidents as decisions.

### Step 2: Inventory — what the product actually needs

List every component the product needs. Group by category. **Only include what's used.** Generic libraries rot fast.

| Category | Components |
|---|---|
| Layout | Container, Grid, Stack, Divider |
| Navigation | Navbar, Sidebar, Tabs, Breadcrumb, BottomNav |
| Feedback | Toast, Alert, Badge, Progress, Skeleton |
| Input | TextField, Select, Checkbox, Radio, Toggle, DatePicker, Search |
| Display | Card, Table, List, Avatar, Chip, Tooltip, EmptyState |
| Overlay | Modal / BottomSheet, Drawer, Popover, DropdownMenu |
| Data | Chart, Metric, ScoreCard, Timeline, Heatmap |

Domain-specific components (e.g., `ScoreCard`, `RepCard`, `CallTimeline`) are **first-class catalog entries**, not afterthoughts.

### Step 3: Define each component

For every component, document:

- **Props** — name, type, default, required. Be specific: `variant: 'primary' | 'secondary' | 'ghost'`, never `style: object`.
- **All 6 states** — `default / hover / active or pressed / disabled / loading / error`. Loading is skeleton or spinner per `interaction-patterns`.
- **Responsive behavior** — what changes at each breakpoint from `design-system` (size, layout, density, hidden affordances).
- **Accessibility** — `role`, ARIA attributes, keyboard interaction, focus behavior, screen-reader narration where non-obvious.
- **Composition rules** — what nests inside what. *"`Card` contains `CardHeader` + `CardBody` + `CardFooter`. `CardHeader` contains title + optional action."*
- **Microcopy** — default labels per `brand-identity` voice. Empty state text. Error text. Placeholder text. Microcopy is prop-driven, never hardcoded.

### Step 4: Naming and file conventions

- **Naming:** PascalCase. Multi-product repos use a product prefix (`MgrScoreCard`, `RepScoreCard`) only when behavior differs; identical components stay shared.
- **File structure:** one component per file; co-located styles (`.tsx` + `.module.css` or equivalent); co-located tests (`Component.test.tsx`); co-located stories (`Component.stories.tsx`) if Storybook is used.
- **Export rule:** named exports only; no default exports (default exports break grep and rename).

### Step 5: Anti-patterns to document

State the forbidden patterns explicitly in the catalog:

- `<div onClick={...}>` — use a `Button` with the `ghost` variant
- A `Card` doing its own data fetching — data flows in via props, not internals
- Components accepting `className` for token overrides — leaks the design system
- A `loading` prop AND a separate `isLoading` prop — pick one name product-wide
- A `Modal` that takes a `children` *and* a `content` prop — choose composition or content, not both

### Step 6: Write `.forge/component-library.md`

Section order: upstream-read confirmation, inventory by category, per-component specs, naming + file conventions, anti-patterns. Prepend a `forge:meta` header (`generated_by: component-library`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/design-system.md, .forge/interaction-patterns.md, .forge/brand-identity.md]` — paths only, never hashes, `generated_from: {.forge/design-system.md: <hash>, .forge/interaction-patterns.md: <hash>, .forge/brand-identity.md: <hash>}` — each upstream's content_hash AT generation time, `content_hash: <sha256 first 8 of THIS file's body>`).

## Verification

- [ ] All three upstream artifacts read (or noted absent and the gap accepted)
- [ ] Every component has all 6 states defined (`default / hover / active / disabled / loading / error`)
- [ ] Every prop has a type — no `any`, no `object` without a typed schema
- [ ] Every component has responsive behavior documented per breakpoint
- [ ] Every interactive component has accessibility attributes (`role`, ARIA, keyboard, focus)
- [ ] No two components overlap in purpose (`Button` ≠ `ActionButton`)
- [ ] Domain-specific components (`ScoreCard`, `RepCard`, `CallTimeline`, etc.) are included, not deferred
- [ ] Microcopy is prop-driven — no hardcoded strings inside components
- [ ] Anti-patterns section is non-empty and specific
- [ ] `.forge/component-library.md` written with `forge:meta` header
