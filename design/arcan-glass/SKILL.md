---
name: arcan-glass
category: design
description: BroomVA trademark web styling system — Arcan Glass design language for Next.js + Tailwind v4 + shadcn/ui projects. Use when creating or styling BroomVA web interfaces, implementing glass/frosted UI effects, setting up brand-consistent dark-first themes, or integrating ArcanBG brand tokens (AI Blue #0066FF, Web3 Green #00CC66) into web applications. Provides a drop-in globals.css, glass component patterns, OKLCh color system, and shadcn/ui compatibility.
---

# Arcan Glass

**Arcan Glass** is BroomVA's trademark web design language — ArcanBG's brand DNA (AI Blue `#0066FF` + Web3 Green `#00CC66` + dark surfaces) fused with liquid glass web effects (backdrop-filter blur, layered highlights, adaptive tinting, morphing transitions). Dark-first, glass-elevated.

Light mode is **Day Glass**: a luminous 275° violet surface system, not a white inversion. It keeps hue continuity, uses low chroma to avoid glare, and preserves clear OKLCh lightness distance between surfaces, text, borders, and shadows.

## Quick Start

1. **Copy** `assets/globals.css` into your Next.js project as `app/globals.css`
2. **Import** in your layout: `import "./globals.css"`
3. **Use** glass classes: `<div class="glass-card">`, `<button class="glass-button glass-button-primary">`

That's it. All shadcn/ui components will automatically pick up the Arcan Glass theme.

## 7 Design Principles

1. **Dark-first, Day Glass second** — The default is dark mode. Light mode keeps the same 275° hue DNA with higher lightness, low chroma, and grounded shadows.
2. **Glass is earned** — Only key surfaces (nav, sidebar, modal, featured cards) get backdrop-filter. Limit to 3-5 per viewport.
3. **Brand through surface** — Surface hue 275° (blue-purple) connects all surfaces to AI Blue without competing.
4. **OKLCh primary** — Perceptually uniform lightness enables clean depth scales and natural color mixing.
5. **Additive on shadcn** — Glass effects layer on top of shadcn/ui, never replacing base accessibility.
6. **Motion with purpose** — Every animation communicates state (glow = active, lift = interactive, reveal = entering). Reduced motion is always respected.
7. **Token-prefixed** — All custom properties use `--ag-` prefix to avoid collisions with shadcn (`--`) and Tailwind (`--tw-`).

## Glass Effect System

Every glass component is built from 4 composable layers:

| Layer | Technique | Purpose |
|-------|-----------|---------|
| 1. Backdrop blur | `backdrop-filter: blur() saturate()` | Frosted glass foundation |
| 2. Highlight | `::before` with top-edge gradient | Light reflection / depth cue |
| 3. Shadow | Multi-level `box-shadow` | Elevation / grounding |
| 4. Adaptive tint | `color-mix(in oklab)` | Contextual color pickup |

Three intensity presets: `glass-subtle` (40% / 8px), `glass` (60% / 16px), `glass-heavy` (80% / 24px).

See `references/glass-components.md` for full component patterns.

## Color System

Brand colors in OKLCh with hex fallbacks:

| Token | Color | Usage |
|-------|-------|-------|
| `--ag-ai-blue` | `oklch(0.55 0.25 260)` / `#0066FF` | Primary, interactive, links |
| `--ag-web3-green` | `oklch(0.72 0.19 155)` / `#00CC66` | Accent, success, web3 |

5-step surface scale at hue 275°, 4-level text hierarchy, semantic colors, 3-level border scale.

Full palette: `references/color-system.md`

## Tailwind Integration

All tokens wired via `@theme inline`:

```html
<!-- Brand colors as utilities -->
<div class="bg-ai-blue text-white">Primary</div>
<span class="text-web3-green">Accent</span>

<!-- Glass utilities -->
<div class="glass p-6">Standard glass</div>
<nav class="glass-heavy sticky top-0">Heavy glass nav</nav>

<!-- Glow effects -->
<div class="glass-card glow-blue">Glowing card</div>
```

shadcn/ui components work unchanged — `bg-primary`, `bg-card`, `text-muted-foreground`, etc. all resolve to Arcan Glass tokens.

Full mapping: `references/tailwind-integration.md`

## Component Index

| Component | Class | Glass Level | Notes |
|-----------|-------|-------------|-------|
| Card | `.glass-card` | Medium | Highlight + hover lift |
| Nav | `.glass-nav` | Heavy | Sticky, bottom border |
| Button | `.glass-button` | Medium | + `.glass-button-primary`, `.glass-button-accent` |
| Input | `.glass-input` | Subtle | Focus ring with blue glow |
| Modal | `.glass-modal` | Heavy | + `.glass-modal-overlay`, reveal animation |
| Sidebar | `.glass-sidebar` | Heavy | Full height, right border |
| Badge | `.glass-badge` | Subtle | + `.glass-badge-blue`, `.glass-badge-green` |

Full patterns with raw CSS + Tailwind composition: `references/glass-components.md`

## Animation Index

| Animation | Tailwind | Duration | Usage |
|-----------|----------|----------|-------|
| Glow pulse | `animate-glow-pulse` | 2s loop | Active/loading states |
| Glass reveal | `animate-glass-reveal` | 0.5s once | Entry animations |
| Gradient flow | `animate-gradient-flow` | 8s loop | Hero backgrounds |

Plus hover lift, morph, focus ring, scroll reveal patterns.

Full patterns: `references/animation-patterns.md`

## shadcn/ui Compatibility

Arcan Glass defines all required shadcn/ui CSS variables. To add glass variants to shadcn components, extend with cva:

```tsx
// In your button.tsx variants
glass: "glass glass-highlight hover:-translate-y-px hover:shadow-lg",
"glass-primary": "glass-button glass-button-primary",
```

See `references/tailwind-integration.md` for full cva examples.

## Dark/Light Mode

Uses `next-themes` with class strategy (`.dark` / `.light`). All tokens auto-adapt via CSS custom properties — explicit `dark:` prefixes are rarely needed. Light mode should be authored as Day Glass: tinted surfaces around OKLCh `L=0.91-0.985`, primary text near `L=0.19`, and darker low-chroma borders with alpha instead of pale gray outlines.

```tsx
<ThemeProvider attribute="class" defaultTheme="dark">
  {children}
</ThemeProvider>
```

## Performance Notes

- **Limit `backdrop-filter`** to 3-5 elements per viewport — each creates a compositing layer
- **Use `glass-subtle`** for repeated items (list items, table rows)
- **Reserve `glass-heavy`** for landmark surfaces (nav, sidebar, modal)
- **Test on lower-end devices** — `backdrop-filter` perf varies by GPU
- **P3 gamut enhancement** is automatic via `@media (color-gamut: p3)` — wider chroma on capable displays
- **Reduced motion** is handled globally — all transforms and animations respect `prefers-reduced-motion`

## Resources

### references/
- `color-system.md` — Full OKLCh palette, hex fallbacks, surface scale, text hierarchy
- `design-tokens.md` — Shadows, blur, radius, spacing, typography, transitions
- `glass-components.md` — 4-layer glass system, component CSS patterns + Tailwind composition
- `animation-patterns.md` — Glow pulse, hover lift, morph, scroll reveal, gradient flow
- `tailwind-integration.md` — @theme inline wiring, @utility blocks, shadcn mapping, cva extensions

### assets/
- `globals.css` — Drop-in CSS file with all tokens, glass utilities, components, and animations
