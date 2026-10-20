---
name: oblivion-component
description: "World Pulse: Any time you create or modify a UI component. The Oblivion aesthetic is the project's visual identity — apply it unconditionally to every visible element."
---

# Oblivion Component

**When to use:** Any time you create or modify a UI component. The Oblivion aesthetic is the project's visual identity — apply it unconditionally to every visible element.

---

## Color Tokens (from `src/renderer/index.css`)

Always use CSS custom properties, never hardcoded hex values:

| Token | Value | Use |
|---|---|---|
| `--ob-bg-primary` | `#0a0a0f` | Page/body background |
| `--ob-bg-panel` | `#101820` | Panel fills |
| `--ob-bg-elevated` | `#141c26` | Elevated card surfaces |
| `--ob-text-primary` | `#c8e6f0` | Primary readable text |
| `--ob-text-dim` | `rgba(200,230,240,0.5)` | Labels, secondary text |
| `--ob-accent-cyan` | `#00d4ff` | Active UI, highlights, borders |
| `--ob-accent-cyan-dim` | `rgba(0,212,255,0.6)` | Muted cyan accents |
| `--ob-accent-amber` | `#ff8c42` | Featured/selected state |
| `--ob-accent-amber-dim` | `rgba(255,140,66,0.6)` | Muted amber |
| `--ob-success` | `#4ae68a` | Healthy / connected |
| `--ob-danger` | `#ff3d3d` | Error / critical |
| `--ob-warning` | `#ffb020` | Warning / degraded |
| `--ob-border-subtle` | `rgba(200,230,240,0.12)` | Default panel border |
| `--ob-border-active` | `rgba(0,212,255,0.4)` | Focused/hovered border |
| `--ob-glow-cyan` | `rgba(0,212,255,0.3)` | Glow shadow |
| `--ob-glow-amber` | `rgba(255,140,66,0.3)` | Amber glow |

Tailwind class equivalents defined in `tailwind.config.js` use the same names (`bg-ob-bg-primary`, `text-ob-accent-cyan`, etc.).

---

## Panel System

Every panel must use `.ob-panel` + optional `.ob-panel-inner` for the four-corner tick pattern:

```tsx
<div className="ob-panel ob-panel-active p-4">
  <div className="ob-panel-inner">
    {/* content */}
  </div>
</div>
```

**Corner tick geometry:**
- 12×12 px L-shaped borders at each corner via `::before` / `::after` pseudo-elements
- Default color: `--ob-accent-cyan`
- On hover: `filter: drop-shadow(0 0 2px var(--ob-accent-cyan))`
- Active state (`.ob-panel-active`): `box-shadow: 0 0 20px var(--ob-glow-cyan)` + inset glow

Never fake corner ticks with icons or SVGs — the CSS pseudo-element approach is canonical.

---

## Typography

- **Font:** `JetBrains Mono` (loaded from Google Fonts in `index.css`). Fallbacks: SF Mono, Fira Code, Consolas, monospace.
- **All text** uses this font — it is set globally on `body`.
- **Headings:** class `ob-heading` — uppercase, `letter-spacing: 0.2em`, weight 300.
- **Labels:** class `ob-label` — uppercase, `letter-spacing: 0.05em`, `font-size: 0.7rem`, `--ob-text-dim` color.
- **Data values:** class `ob-value` — tabular numerics, `--ob-text-primary`.
- **Highlighted values:** class `ob-value-highlight` — cyan color + `text-shadow: 0 0 10px var(--ob-glow-cyan)`.

Never use proportional serif or sans-serif fonts. Never use `font-weight > 500` for body text.

---

## Motion & Timing

Use CSS variables for animation durations — never hardcode:

| Variable | Value | Use |
|---|---|---|
| `--ob-timing-glitch` | `60ms` | Snap/glitch effects |
| `--ob-timing-snap` | `120ms` | Quick state transitions |
| `--ob-timing-fade` | `300ms` | Standard fade, border transitions |
| `--ob-timing-pulse` | `3s` | Breathing glow, dot grid pulse |
| `--ob-timing-sweep` | `6s` | Full-viewport scanline sweep |
| `--ob-easing-mechanical` | `cubic-bezier(0.25,0.1,0.25,1)` | Mechanical/robotic feel |
| `--ob-easing-snap` | `cubic-bezier(0.4,0,0.2,1)` | Material-style snap |

---

## Scan Line Effect

Panels that emit data use `.ob-scanline`:

```tsx
<div className="ob-scanline ob-panel p-4">
  {/* A 2px cyan line sweeps top→bottom over 6 s (var(--ob-timing-sweep)) */}
</div>
```

The `::after` pseudo-element creates the sweep automatically. Do not replicate with JS.

---

## Glow Effects

- **Breathing glow:** class `ob-glow` — `animation: breathingGlow 3s ease-in-out infinite`
- **Dot grid background:** class `ob-dot-grid` — radial gradient dots every 40px
- **Animated dot grid:** class `ob-dot-grid-animated` — pulses at `--ob-timing-pulse`
- **In Three.js:** glow rendered as `meshBasicMaterial` with `opacity: 0.15` on a back-facing sphere scaled 1.06× (see `Globe.tsx:23-34`)

---

## HUD Layout

The Dashboard (`src/renderer/components/Dashboard/Dashboard.tsx`) uses a full-viewport globe (z-0) with `fixed`-position HUD panels layered on top at z-20+:

- Globe canvas: `fixed inset-0 z-0`
- All HUD panels: `fixed` with specific `top/left/right/bottom` values, `z-20`
- Ticker: `fixed bottom-0 left-0 right-0 z-20`
- Modals: `z-50` or higher

Never use absolute positioning for HUD panels — always `fixed` so they stay viewport-relative regardless of scroll.

---

## Severity → Color Mapping (Three.js markers and UI badges)

```ts
severity >= 7  → --ob-danger   (#FF3D3D)  // critical
severity >= 4  → --ob-accent-amber (#FF8C42) // elevated
severity < 4   → --ob-accent-cyan (#00D4FF)  // nominal
featured event → --ob-accent-amber          // selection
```

---

## Anti-Patterns

- **Do not** use Tailwind colors directly (`blue-500`, `gray-900`) — use the `ob-*` token classes.
- **Do not** add rounded corners (`rounded-*`) to panels — Oblivion aesthetic is rectilinear.
- **Do not** use `shadow-*` Tailwind utilities — use explicit `box-shadow` with `var(--ob-glow-*)` tokens.
- **Do not** use `font-sans` or `font-serif` anywhere.
- **Do not** omit the corner ticks on any panel that shows data.
- **Do not** use color literals in TypeScript/JSX — use the `OB_COLORS` object (defined in `Globe.tsx:13-20`) or the CSS variables.
