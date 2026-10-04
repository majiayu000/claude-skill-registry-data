---
name: tac-ui-authoring
description: "MANDATORY when writing or modifying any UI component in TAC Express. Enforces TAC Express v5.0 Violet Grid design system (Plus Jakarta Sans + IBM Plex Mono + Lora, 0rem radius, brutalist offset shadows, violet signal palette, no soft drop shadows, no glassmorphism), CVA pattern, packages/ui location, and Radix/shadcn primitives."
---

# TAC Express — UI Component Authoring

Every UI component in this project MUST follow the **TAC Express v5.0 — Violet Grid** design system and the strict component authoring pattern below.

> **Design identity:** Mission-control density + brutalist offset shadows + NASA FUI utilities. Dark-first, sharp 0rem corners, violet signal palette, solid surfaces. No glassmorphism. No soft drop shadows. No curves.

> **Before starting:** Check `packages/ui/src/components/` — does a similar component already exist? Extend it before creating a new one.

---

## Pre-Flight Checklist

```
[ ] Component doesn't already exist in packages/ui/src/components/
[ ] Design approved via tac-brainstorming skill
[ ] Failing test written (tac-tdd)
[ ] Violet Grid tokens identified in DESIGN_SYSTEM.md
[ ] Radix primitive identified (if applicable)
```

---

## Component File Structure

```
packages/ui/src/components/
  ComponentName/
    ComponentName.tsx         ← implementation
    ComponentName.test.tsx    ← co-located tests
    index.ts                  ← re-export
```

**OR** for simple single-file components:

```
packages/ui/src/components/
  ComponentName.tsx
  ComponentName.test.tsx
```

Add to `packages/ui/src/index.ts` exports after creation.

---

## Component Template

```tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { Slot } from "@radix-ui/react-slot"
import { cn } from "@workspace/ui/lib/utils"

const componentVariants = cva(
  // Base classes — semantic tokens only, no raw colors, no glass tokens
  [
    "relative inline-flex items-center",
    "transition-all duration-200 ease-out",
  ],
  {
    variants: {
      variant: {
        default: [
          "bg-card",
          "border border-border",
          "text-foreground",
        ],
        signal: [
          "bg-card",
          "border border-border",
          "border-t-2 border-t-primary",
          "text-foreground",
          "hover:border-primary/50",
        ],
        ghost: [
          "bg-transparent",
          "hover:bg-muted",
          "text-muted-foreground",
        ],
      },
      size: {
        sm: "text-sm px-3 py-1.5",
        md: "text-base px-4 py-2",
        lg: "text-lg px-6 py-3",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

interface ComponentProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof componentVariants> {
  asChild?: boolean
}

function ComponentName({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: ComponentProps) {
  const Comp = asChild ? Slot : "div"
  return (
    <Comp
      data-slot="component-name"
      className={cn(componentVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { ComponentName, componentVariants }
export type { ComponentProps }
```

---

## Violet Grid Design Tokens — Quick Reference

Use these semantic Tailwind classes (mapped from CSS variables in `globals.css`):

```
Backgrounds (dark-first — mission control):
  bg-background          page canvas
  bg-card                primary panel surface
  bg-popover             floating surface
  bg-surface             mid-layer surface
  bg-muted               de-emphasized surface
  bg-code-bg             code / mono blocks

Borders:
  border-border          all structural framing (1px)
  border-primary         primary violet accent

Text:
  text-foreground        primary text
  text-muted-foreground  secondary / dimmed text

Signal colors (status only — never decoration):
  bg-accent-success / text-accent-success     green  — delivered, paid, healthy
  bg-accent-warning / text-accent-warning     amber  — in transit, due-soon, attention
  bg-accent-danger  / text-accent-danger      red    — delayed / breached / error
  bg-accent-info    / text-accent-info        violet — data signal (= primary)

Shadows (BRUTALIST OFFSET ONLY — all soft shadows resolve to none):
  shadow-2xs / shadow-xs / shadow-sm / shadow / shadow-md / shadow-lg / shadow-xl / shadow-2xl
                                     1px..16px offset on var(--border) — sharp, no blur
  shadow-[var(--shadow-brutal-sm)]   alias → shadow-sm  (3px offset)
  shadow-[var(--shadow-brutal)]      alias → shadow-md  (6px offset)

Radius (ZERO — sharp corners always):
  var(--radius)        0rem  — single radius scale, all variants resolve to 0
  rounded-none         use this when expressiveness is needed

Fonts:
  font-sans    Plus Jakarta Sans — UI text, headings, labels
  font-mono    IBM Plex Mono     — AWBs, IDs, weights, currency, timestamps
  font-serif   Lora              — blockquotes, editorial / prose only

Type scale utilities (premium rendering — defined in globals.css):
  .t-display    3rem,    weight 800, tight tracking, balanced
  .t-h1 / h2 / h3 / h4    weight 700/600, kerned, balanced
  .t-body / t-body-sm      reading text
  .t-overline / t-caption  small uppercase + caption
  .t-data / t-data-sm      mono KPI values, tabular-nums
  .t-mono / t-mono-sm      mono inline data
  .t-gradient-primary / t-gradient-hero / t-gradient-success
                           clipped text gradients (dark mode hero only)
  .text-glow-primary       violet text-shadow bloom (dark mode hero only)

FUI utility classes:
  .tac-fui-panel         solid card, 1px border, brutalist offset
  .tac-mono-label        uppercase mono caps in primary color
  .tac-hazard-stripes    -45° primary/background gradient
  .tac-scanline          1px primary line scanning vertically (8s loop)
  .tac-blink             1s step terminal blink
  .tac-signal-glow       1px ring + 8px primary color-mix bloom
  .tac-fui-crosshair     centered + decoration
  .tac-fui-hover         instant border + 5%-mix bg on hover
  .tac-hero-bleed        full-bleed hero (compensates layout padding)
```

> **FORBIDDEN:** `backdrop-blur`, `backdrop-filter`, `rounded-full`, `rounded-md/lg/xl` with non-zero radius, soft `shadow-md/lg/xl` rendering as blur (they resolve to brutalist offset only), `bg-blue-500`, raw hex colors, glassmorphism, `Space Grotesk` / `JetBrains Mono` / `Inter` / `Geist` as font names (they were prior identities).

---

## Charts — TAC Orbital telemetry system

Any chart, KPI tile, sparkline, gauge, or distribution visualisation MUST use
the Orbital primitives at `@workspace/ui/components/charts`. Do not build
ad-hoc charts; do not import recharts directly outside this folder.

| Use case | Primitive |
|---|---|
| KPI tile (number + spark + delta) | `KpiTile` |
| Time series (shipments, revenue, volume) | `StepAreaChart` |
| Composition (status mix, service mix) | `SegmentBar` |
| Ranking (hubs, customers) | `RankBarChart` |
| Percentage progress (success rate, growth) | `ProgressMeter` |
| SLA state per day | `StackedColumnChart` |
| Origin × destination | `LaneHeatmap` |
| Universal chart shell | `ChartFrame` |
| Below-threshold data | `ChartEmptyState` (built into each primitive) |

Data shapes are defined in `@workspace/types/orbital`; produce them via
`@workspace/services/orbital.service` (or its `useOrbital*` hooks). UI never
derives chart shapes inline.

**FORBIDDEN charts:** donuts, pies, smooth curves (`type="monotone"`),
multi-hue categorical palettes. Use `SegmentBar`, `stepAfter`, and the
single-hue ramp instead. Full spec: `docs/CHARTS-ORBITAL.md`.

---

## Radix Primitive Mapping

When a Radix primitive exists, wrap it — don't build from scratch:

| UI Need | Radix Primitive | Import |
|---------|----------------|--------|
| Dialog/Modal | `@radix-ui/react-dialog` | via shadcn |
| Dropdown | `@radix-ui/react-dropdown-menu` | via shadcn |
| Select | `@radix-ui/react-select` | via shadcn |
| Popover | `@radix-ui/react-popover` | via shadcn |
| Tooltip | `@radix-ui/react-tooltip` | via shadcn |
| Tabs | `@radix-ui/react-tabs` | via shadcn |
| Checkbox | `@radix-ui/react-checkbox` | via shadcn |
| Switch | `@radix-ui/react-switch` | via shadcn |

Add via: `pnpm dlx shadcn@latest add [component]` from workspace root.

---

## Signal Panel Pattern (Primary Card Pattern)

```tsx
<div
  data-slot="signal-panel"
  className={cn(
    "bg-card",
    "border border-border",
    "border-t-2 border-t-primary",   // top accent = hierarchy marker
    "p-6",
    "shadow-sm",
    "transition-colors duration-200",
    "hover:border-primary/50",
    className
  )}
  {...props}
/>
```

> **Never use:** `backdrop-blur-*`, `bg-[var(--glass-bg)]`, glassmorphism of any kind.
> Sharp corners, solid surfaces, 1px directional shadows — that is Violet Grid.
```

---

## Icon Usage

```tsx
import { RiArrowRightLine } from "@workspace/ui/icons"
// or
import { RiArrowRightLine } from "@remixicon/react"

// Always include aria-hidden on decorative icons:
<RiArrowRightLine className="size-5 text-muted-foreground" aria-hidden="true" />

// With label context:
<button aria-label="Next page">
  <RiArrowRightLine className="size-5" aria-hidden="true" />
</button>
```

---

## Animation Patterns

```tsx
// Entrance (tw-animate-css):
className="animate-in fade-in-0 slide-in-from-bottom-4 duration-300"

// Exit (tw-animate-css):
className="animate-out fade-out-0 slide-out-to-bottom-2 duration-200"

// Hover translation (brutalist offset reveal):
className="transition-transform duration-fast ease-linear hover:-translate-x-0.5 hover:-translate-y-0.5"

// Signal glow on focus (1px ring + 8px bloom):
className="focus-visible:outline-none focus-visible:tac-signal-glow"

// Mission-control instant hover (preferred default):
className="tac-fui-hover"

// motion (motion/react) for component-level transitions when tw-animate-css is insufficient:
import { motion } from "motion/react"
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.15 }} />
```

---

## Validation Before Export

```
[ ] data-slot attribute set
[ ] Named export (not default)
[ ] CVA variants use semantic tokens only (NO glass tokens, NO legacy design-system tokens)
[ ] No raw hex colors in className
[ ] No Tailwind color classes (bg-blue-*, text-red-*)
[ ] No arbitrary [px] values
[ ] No var(--glass-*), no backdrop-blur, no rounded-full
[ ] No curve commands in SVG paths (LAW 13)
[ ] TypeScript props interface defined and exported
[ ] Accessibility attributes present (aria-*, role)
[ ] Exported from packages/ui/src/index.ts
[ ] Tests written alongside (tac-tdd)
```
