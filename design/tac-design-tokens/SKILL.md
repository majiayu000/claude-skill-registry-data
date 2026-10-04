---
name: tac-design-tokens
description: >-
  Load when authoring premium UI surfaces (landing hero, marketing sections, mission-control panels, KPI cards, dashboard headers) in tac-express. Provides the full Violet Grid (v5.0) token reference — colors, typography scale, motion choreography, FUI utilities, gradients — and the patterns for composing premium-feel components without violating LAW 9/10/11.
---

# TAC Express — Design Tokens & Premium Composition (Violet Grid v5.0)

Use this skill when you need to **reach for the right token** instead of a raw value. It is the index to `globals.css` plus the playbook for premium feel: motion choreography, type rhythm, gradient text, and signal glow.

> **Single source of truth:** `packages/ui/src/styles/globals.css`. If a token isn't listed here, check there.

---

## Color Tokens

### Surfaces (LAW 1 — never raw colors)

| Class | Light | Dark | Use |
|---|---|---|---|
| `bg-background` | `oklch(0.9940 0 0)` | `oklch(0.2223 0.0060 271.14)` | Page canvas |
| `bg-card` | `oklch(1 0 0)` | `oklch(0.2568 0.0076 274.65)` | Primary panel |
| `bg-popover` | `oklch(1 0 0)` | `oklch(0.2568 0.0076 274.65)` | Floating surface |
| `bg-surface` | `oklch(0.9700 0.005 264.53)` | `oklch(0.2837 0.0137 274.65)` | Mid-layer |
| `bg-overlay` | `oklch(1 0 0)` | `oklch(0.2568 0.0076 274.65)` | Modal/sheet backdrop content |
| `bg-muted` | `oklch(0.9400 0.010 264.53)` | `oklch(0.3003 0.0094 271.14)` | De-emphasized |
| `bg-code-bg` | `oklch(0.9556 0.0074 264.53)` | `oklch(0.2223 0.0060 271.14)` | Code blocks |

### Text

| Class | Use |
|---|---|
| `text-foreground` | Primary text |
| `text-muted-foreground` | Secondary / dimmed |
| `text-primary` | Violet brand color (links, key data) |
| `text-primary-foreground` | On-violet fills (buttons, badges) |
| `text-accent-{success,warning,danger,info}` | Status text |

### Borders & Rings

| Class | Use |
|---|---|
| `border-border` | All structural framing (1px) |
| `border-primary` | Hover/active accent (1px) |
| `outline-ring` | Focus outline — sharp, no fuzz |

### Brand & Status

| Token | Light | Dark | Role |
|---|---|---|---|
| `--primary` | `oklch(0.5393 0.2713 286.7462)` | `oklch(0.6132 0.2294 291.7437)` | Violet — CTAs, focus, primary signal |
| `--accent-success` | `oklch(0.60 0.18 150)` | same | Delivered / paid / healthy |
| `--accent-warning` | `oklch(0.72 0.18 80)` | same | In-transit / due-soon |
| `--accent-danger` | `oklch(0.5885 0.2090 24)` | `oklch(0.6368 0.2078 25)` | Delayed / error |
| `--accent-info` | violet (= primary) | violet (= primary) | Info signal |

### Charts — TAC Orbital telemetry tokens

The Orbital chart system (docs/CHARTS-ORBITAL.md) uses its own token namespace.
Use these inside any `@workspace/ui/components/charts/*` primitive — never the
old `--chart-1..5` ramp (kept for backward compat only).

| Token | Use |
|---|---|
| `--chart-primary` | Single saturated hue per chart |
| `--chart-primary-muted` | Optional secondary series — never standalone |
| `--chart-axis` / `--chart-grid` / `--chart-track` | Structural greys |
| `--chart-ramp-1..5` | Single-hue intensity ramp (heatmap / density only) |
| `--chart-ontime` / `--chart-late` / `--chart-breached` | **SLA STATE ONLY** — never decorative |

**Hard rules:** at most two hues per chart; `ontime/late/breached` reserved
for SLA components; no donuts (use `SegmentBar`); no smooth curves (use
`stepAfter`); percentage gauges use `ProgressMeter`, not donut rings.

Tailwind utilities: `bg-chart-primary`, `text-chart-axis`, `border-chart-grid`,
`fill-chart-ramp-3`, `stroke-chart-late`, etc.

### Chart-internal typography utilities

| Class | Purpose |
|---|---|
| `tac-caption` | Mono 11px ALL-CAPS — chart frame headers |
| `tac-tag` | Mono 10px ALL-CAPS — sub-labels, legend entries |
| `tac-axis` | Mono 11px tabular — axis ticks |
| `tac-readout` | tnum + lnum — KPI numeric values |

Use these only inside chart primitives — they complement, do not replace,
the `t-display / t-h1..h4 / t-data / t-overline / t-mono` premium type scale.

---

## Typography

### Font Families (LAW 4 — declared only in `apps/*/app/layout.tsx`)

| Class | Family | Use |
|---|---|---|
| `font-sans` | Plus Jakarta Sans | UI text, headings, labels |
| `font-mono` | IBM Plex Mono | AWBs, IDs, weights, currency, timestamps |
| `font-serif` | Lora | Blockquotes, editorial / prose ONLY |

### Premium Type Scale (defined in `globals.css` `@layer utilities`)

Prefer these utilities over ad-hoc text-* classes on branded surfaces. They include kerning, ligatures, balanced text, and tabular nums.

| Class | Size | Use |
|---|---|---|
| `.t-display` | 3rem / 800 / `-0.045em` | Hero displays |
| `.t-h1` | 1.75rem / 700 / `-0.035em` | Page titles |
| `.t-h2` | 1.375rem / 700 / `-0.030em` | Section heads |
| `.t-h3` | 1.125rem / 600 / `-0.022em` | Sub-section heads |
| `.t-h4` | 0.9375rem / 600 / `-0.016em` | Panel heads |
| `.t-body` | 0.9375rem / 400 | Reading text |
| `.t-body-sm` | 0.8125rem / 400 | Dense reading text |
| `.t-caption` | 0.75rem / 400 / muted | Captions |
| `.t-overline` | 0.6875rem / 500 / `+0.1em` / uppercase | Eyebrow labels |
| `.t-data` | 2.5rem / 600 / mono / tabular-nums | KPI displays |
| `.t-data-sm` | 1.25rem / 500 / mono / tabular-nums | Inline KPIs |
| `.t-mono` | 0.8125rem / mono / tabular-nums | Inline mono data |
| `.t-mono-sm` | 0.6875rem / mono / tabular-nums | Dense mono cells |

### Extra small text scales

- `text-3xs` → `0.5625rem`
- `text-2xs` → `0.625rem`

For mission-control field-key labels, prefer `.tac-mono-label` (uppercase mono caps in primary violet).

---

## Geometry

| Token | Value |
|---|---|
| `--radius` | `0rem` (LAW 13 — sharp always) |
| `--radius-sm/md/lg/xl` | all alias to `var(--radius)` |
| `--spacing` | `0.25rem` (Tailwind's base unit) |
| `--tracking-normal` | `-0.025em` (body letter-spacing) |

---

## Shadows (Brutalist Offset Only — LAW 9)

All `shadow-*` utilities resolve to sharp offset shadows on `var(--border)`:

| Class | Offset |
|---|---|
| `shadow-2xs` | 1px 1px |
| `shadow-xs` | 2px 2px |
| `shadow-sm` | 3px 3px |
| `shadow` | 4px 4px |
| `shadow-md` | 6px 6px |
| `shadow-lg` | 8px 8px |
| `shadow-xl` | 12px 12px |
| `shadow-2xl` | 16px 16px |

Aliases (kept for backward compat): `--shadow-brutal-sm` = `shadow-sm`; `--shadow-brutal` = `shadow-md`.

> Soft drop shadows do not exist in this system. If you reach for one, you're using the wrong token.

---

## Motion Choreography (Premium Cadence)

### Tokens

| Token | Value | Use |
|---|---|---|
| `--duration-fast` | 80ms | Hover, focus, instant feedback |
| `--duration-base` | 150ms | Modal / sheet open, tab switch |
| `--duration-slow` | 300ms | Page-level enter, drawer slide |
| `--duration-slower` | 500ms | Hero entrance, marquee start |
| `--ease-smooth` | `cubic-bezier(0.4, 0, 0.2, 1)` | Default ease-in-out |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Premium "bounce" — buttons, badges |
| `--ease-linear` | `linear` | Mission-control instant transitions, marquees |

### The Premium Recipe

```tsx
// Mission-control surfaces — instant, machine-like (default)
className="transition-all duration-fast ease-linear"

// Branded marketing surfaces — smooth, considered
className="transition-all duration-base ease-[var(--ease-smooth)]"

// Hover lift on a brutalist card — preserves the offset shadow read
className="transition-transform duration-fast ease-linear
           hover:-translate-x-0.5 hover:-translate-y-0.5"

// Premium press feedback — bouncy, confident
className="transition-transform duration-base ease-[var(--ease-spring)]
           active:scale-[0.98]"

// Entrance choreography — staggered with tw-animate-css
<div className="animate-in fade-in-0 duration-slow">
  <h1 className="animate-in slide-in-from-bottom-4 duration-slow">…</h1>
  <p  className="animate-in slide-in-from-bottom-3 duration-slower delay-100">…</p>
</div>
```

### `prefers-reduced-motion`

`globals.css` already handles the global override. For component-level safety:

```tsx
className="tac-scanline motion-reduce:hidden"
className="tac-blink motion-reduce:animate-none"
```

---

## FUI Utilities (the mission-control vocabulary)

Defined in `globals.css` `@layer utilities`. Compose, don't redefine.

| Class | Use |
|---|---|
| `.tac-fui-panel` | Solid card surface, 1px border, brutalist offset shadow |
| `.tac-fui-border` | 1px border on background |
| `.tac-fui-hover` | Instant border + 5%-mix bg on hover |
| `.tac-mono-label` | Uppercase mono caps in primary violet |
| `.tac-fui-crosshair` | Centered `+` decoration via `::before` |
| `.tac-signal-glow` | 1px ring + 8px primary color-mix bloom |
| `.tac-hazard-stripes` | -45° border/transparent repeating gradient |
| `.tac-scanline` | 1px primary line scanning vertically (8s loop) |
| `.tac-blink` | 1s step terminal blink |
| `.tac-surface` / `.tac-overlay` / `.tac-code-bg` | Surface convenience classes |
| `.tac-print-label` | Print-safe black-on-white wrapper |
| `.tac-hero-bleed` | Full-bleed hero (compensates layout padding at every breakpoint) |

---

## Text Gradients & Glow (Premium Hero Treatment)

Use sparingly — these are the visual "splash" reserved for marketing surfaces and dashboard hero KPIs.

```tsx
// Violet primary gradient — for headings and key labels
<h1 className="t-display t-gradient-primary">Mission Control</h1>

// Hero gradient — wider sweep, includes adjacent hue for richness
<h1 className="t-display t-gradient-hero">North-East Logistics</h1>

// Success gradient — for positive KPI values
<span className="t-data t-gradient-success">98.7%</span>

// Violet glow on dark mode hero
<h1 className="t-display dark:text-glow-primary">Velocity</h1>

// Text shadows for depth on busy backgrounds
<p className="text-shadow-sm">Subtle</p>
<p className="text-shadow-md">Medium</p>
<p className="text-shadow-lg">Heavy (use only behind imagery)</p>
```

---

## Premium Composition Patterns

### Signal Panel (the canonical card)

```tsx
<div
  data-slot="signal-panel"
  className={cn(
    "bg-card",
    "border border-border",
    "border-t-2 border-t-primary",   // top accent = hierarchy marker
    "p-6",
    "shadow-sm",                     // 3px brutalist offset
    "transition-colors duration-fast ease-linear",
    "hover:border-primary",
  )}
/>
```

### KPI Card

```tsx
<div className="tac-fui-panel p-6 flex flex-col gap-2">
  <span className="tac-mono-label">Active Manifests</span>
  <span className="t-data text-foreground">128</span>
  <span className="t-caption">+12 vs. last hour</span>
</div>
```

### Mission-Control Header

```tsx
<header className="border-b border-border bg-card">
  <div className="container flex items-center justify-between py-3">
    <div className="flex items-center gap-3">
      <span className="tac-mono-label">SECTOR</span>
      <span className="font-mono text-sm tabular-nums">DEL · BLR · BOM · MAA</span>
    </div>
    <span className="t-mono-sm text-muted-foreground tabular-nums">
      {now.toISOString()}
    </span>
  </div>
</header>
```

### Hero Display (landing page)

```tsx
<section className="tac-hero-bleed bg-background relative">
  <div className="absolute inset-0 tac-scanline pointer-events-none" />
  <div className="container py-24 lg:py-32">
    <span className="t-overline text-primary">North-East Corridor · Logistics</span>
    <h1 className="t-display t-gradient-hero mt-4">
      Move faster than the road.
    </h1>
    <p className="t-body mt-6 max-w-prose text-muted-foreground">
      Real-time tracking, predictive arrival, mission-grade ops.
    </p>
  </div>
</section>
```

---

## What NOT to do (premium-killers)

```
❌ Soft drop shadows                      → use brutalist offset
❌ Glassmorphism / backdrop-blur          → solid surfaces only
❌ Curved decorations / wavy SVGs         → straight lines, brackets, hazard stripes
❌ Three or more accent hues in one view  → one violet, one status hue, that's it
❌ Mid-saturation pastels                 → violet is saturated; status hues are saturated; surfaces are neutral
❌ Three+ font weights in one block       → 400 / 600 / 700 / 800 are all you need
❌ Inline styles                          → semantic tokens via Tailwind classes only
❌ `Inter`, `Geist`, `Space Grotesk`,
   `JetBrains Mono`, `Fira Mono` strings  → those are dead identities; only Plus Jakarta Sans / IBM Plex Mono / Lora
```

---

## Pre-flight Before Shipping a Premium Surface

```
[ ] Uses .t-display / .t-h1..h4 / .t-data / .t-overline (not raw text-* classes)
[ ] Uses violet primary, never indigo (260°)
[ ] Brutalist offset shadows, never blur
[ ] Zero radius — sharp corners read as "engineered, premium"
[ ] Motion choreography uses --ease-smooth or --ease-spring (not stock ease-out)
[ ] FUI utility used where it earns its place (.tac-mono-label on every field key)
[ ] Dark mode: text-glow-primary or t-gradient-hero on the hero only (don't sprinkle)
[ ] prefers-reduced-motion guard on .tac-scanline / .tac-blink
[ ] All copy in font-sans; all numbers in font-mono with tabular-nums
```
