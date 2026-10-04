---
name: "experience-and-design-system"
description: "Anti-AI-slop design system for distinctive, premium interfaces. Bold typography, dark-first #060610, fluid clamp() type, cascade layers + native nesting + container queries, OKLCH color, @starting-style, View Transitions API, DTCG tokens."
metadata:
  version: "2.2.0"
  updated: "2026-10-04"
  effort: "high"
  model: "opus"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
submodules:
  - build-breaking-rules.md
  - cinematic-doctrine.md
  - design-tokens.md
priority: 3
pack: "design"
stage: stable
triggers:
  - "design"
  - "ui"
  - "components"
  - "theme"
paths:
  - "org:website_build"
---

# 10 — Experience and Design System

Build anti-AI-slop premium interfaces: dark-first OKLCH color, fluid `clamp()` type, DTCG tokens, View Transitions on every public-facing surface.

**Apple Test** — after every design: two elements compete → remove one; crowded → add whitespace; busy type → reduce sizes, increase weight contrast; final feel: effortless, inevitable.

## CSS Patterns

- Overlay `rgba(0,0,0,0.81)` · Text shadow `1px 1px 1px rgba(255,255,255,0.333)` · Box shadow `2px 2px 2px rgba(0,0,0,0.69)`
- Border-radius 5px interactive, 10px containers (never 0, never pill)
- Hero padding 40px · Max text 720px · Line-height 1.4
- Letter-spacing: 0.4px labels, 0.5px nav, 1px titles, 1.4px CTAs
- CTA uppercase always · Button 700 always · Reference: Linear, Notion, Stripe

## Typography

- Body: Sora 400/500 · Headings: Space Grotesk 600/700 · Mono: JetBrains Mono 400/500 · Display: Clash Display 700 (hero only)
- Variable fonts: WOFF2, subset, self-host (never Google Fonts CDN), `font-display:swap`
- Body min 16px (prefer 18) · Line-height 1.6 body, 1.1-1.2 headings · Letter-spacing -0.02em >2rem · Max 65ch
- Never skip levels. Scale: Minor Third 1.2 general, Perfect Fourth 1.333 marketing
- `text-wrap:balance` headings, `text-wrap:pretty` paragraphs
- Kinetic gradient type (hero/display only): `background: var(--gradient-primary); background-size: 220% 220%; background-clip: text` (+ `-webkit-` pair), `color: transparent`, slow `background-position` pan 8-12s ease infinite alternate
- Gate the pan behind `@media (prefers-reduced-motion: no-preference)` — reduced-motion gets the static gradient fill; keep a solid `color` fallback where clip is unsupported

```css
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1rem + 1.25vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.1rem + 2vw, 2rem);
  --text-3xl: clamp(2rem, 1.5rem + 2.5vw, 3rem);
  --text-4xl: clamp(2.5rem, 1.5rem + 5vw, 4.5rem);
  --text-hero: clamp(3rem, 2rem + 5vw, 6rem);
}
```

## Color (Dark Default)

```css
:root {
  color-scheme: light dark;
  --bg-primary: #060610; --bg-secondary: #0a0a1a; --bg-tertiary: #121225;
  --bg-card: #0f0f1f; --bg-elevated: #1a1a35;
  --text-primary: #f0f0f5; --text-secondary: #a0a0b5; --text-muted: #606080;
  --accent-cyan: #00E5FF; --accent-blue: #50AAE3; --accent-purple: #8B5CF6;
  --gradient-primary: linear-gradient(135deg, #00E5FF, #50AAE3);
  --gradient-accent: linear-gradient(135deg, #50AAE3, #8B5CF6);
  --border-subtle: rgba(255,255,255,0.06); --border-hover: rgba(255,255,255,0.12);
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3); --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.5); --shadow-glow: 0 0 20px rgba(0,229,255,0.15);
}
```

- Never `#000` (use `#060610`) · Never `#fff` (use `#f0f0f5`)
- Cyan: primary CTAs · Blue: secondary · Gradients on buttons only · 6% borders · Subtle glow on primary interactive
- Elevation via lightness not shadows: base → surface 1 → surface 2 → surface 3
- `color-scheme:light dark` · `data-theme="dark|light"` user override · `localStorage` persistence · `prefers-color-scheme` system default · Always provide toggle
- OKLCH is the authoring space — perceptually uniform ramps, hue-true shifts · relative color `oklch(from var(--brand) l c calc(h + 30))` for derived accents
- Derive shades via `color-mix(in oklch, …)`, never hand-picked hex neighbors: hover `color-mix(in oklch, var(--accent-cyan) 85%, white)` · pressed `…80%, black` · wash `…12%, transparent`
- `light-dark()` for theme-aware one-liners · dark-ONLY surfaces (cockpit, editor) set `color-scheme: dark` — native controls/scrollbars/autofill render dark, no white flash
- Contrast 4.5:1 normal, 3:1 large/UI (WCAG 2.2 AA) · Target size min 24×24 px (2.5.8) · Focus 2px thick, 3:1 contrast (2.4.13)

## CSS Architecture (2026)

```css
@layer reset, base, tokens, components, utilities, overrides;
```

- Native nesting (Baseline 2023, `&` syntax) · size container queries `container-type: inline-size` + `@container (min-width: 28rem)` (Baseline 2023) — component-owned breakpoints
- Style queries `@container style(--variant: featured)` — Chrome 111+ / Safari 18+, Firefox pending (verify at caniuse); enhancement-only, base styles ship first
- `:has()` parent selection (Baseline 2023) replaces state JS — `form:has(:invalid) [type=submit]`, `.grid:has(.card:hover) .card:not(:hover)` sibling-dim
- Declare layer order ONCE at bundle top — later layers win (utilities beat components); un-layered styles beat ALL layers, so layer everything
- `@scope` bounded styling · Scroll-state queries `@container scroll-state(stuck: top)` (Baseline 2026)
- Anchor positioning (`anchor-name` / `position-anchor` / `position-area`) replaces Floating UI — Chrome/Edge 133+ first, cross-engine newer (verify at caniuse) · @oddbird polyfill v0.7+ for the tail
- Popover API `popover` + `popovertarget` (Baseline 2024) — top-layer, light-dismiss, focus-managed, zero JS; pair with anchor positioning for menus/tooltips
- CSS `if()` · Typed `attr()` · `sibling-index()` / `sibling-count()` stagger: `transition-delay: calc((sibling-index() - 1) * 40ms)`
- `appearance:base-select` native `<select>` (Chrome 135+) · `@supports` for progressive enhancement
- **Baseline 2026**: `@scope` · Anchor positioning · Scroll-state queries · `@starting-style` · `interpolate-size: allow-keywords` · `field-sizing: content` · `text-wrap: pretty` · `@property`

## W3C DTCG Design Tokens (2025.10 Stable)

- JSON `.tokens` / `.tokens.json`, MIME `application/design-tokens+json`
- Token: `$value` (required), `$type`, `$description`, `$deprecated`, `$extensions`
- Types: color | dimension | duration | fontFamily | fontWeight | cubicBezier | number + composites (shadow, border, gradient, typography, transition)
- Aliasing: `"$value": "{base.color}"` · `$ref` JSON Pointer · Group `$type` inheritance · `$root` for base + variants · `$extends` for deep merge
- Full Display P3, OKLCH, CSS Color Module 4; naming: no `$` prefix, no `{}` / `.` in names
- Tools: Tokens Studio, Style Dictionary, Penpot, Figma

## AI-Ready Design Documentation

- `DESIGN.md`: plain-text markdown; sections: Visual Theme, Color Palette, Typography, Spacing + Layout, Components, Elevation
- Atomic docs: context-rich units per component with states, variants, props, constraints, a11y, rationale
- MCP servers (Figma Dev Mode MCP) for programmatic access

## Layout

- Container 1140px (wide 1400, narrow 720), padding `clamp(1rem,3vw,3rem)`
- Sections `clamp(4rem,8vw,8rem)`, border between; grid `auto-fit minmax(280px,1fr)`, 1fr at 768px
- Patterns: Hero (full-viewport, centered) · Features (3-col icon+heading+desc) · Alternating (zigzag) · Pricing (3-tier highlighted) · FAQ (accordion) · CTA (full-width dark) · Footer (4-col stack)
- SaaS: Single-CTA 13.5%; Hero / Proof / Features / Demo / Testimonials / Pricing / FAQ / CTA; bento grid for feature showcases
- Bento: `repeat(auto-fill, minmax(240px, 1fr))` + `grid-auto-flow: dense`; 1-2 anchor cards `grid-column: span 2` (hero metric also `grid-row: span 2`) — never uniform tiles
- Bento anchors carry an accent wash `linear-gradient(135deg, rgba(0,229,255,.08), transparent 60%)` + border-hover; collapse spans via container query ≤480px, not viewport
- Asymmetry with order: ONE dominant cell per visual row, constant gap `clamp(0.75rem, 2cqi, 1.5rem)`, internal baselines aligned

## Components

- **Cards** — bg-card, border-subtle, 12px radius, hover: border-hover + shadow-glow
- **Buttons** — Primary gradient #060610 text, 600 weight, 8px radius, hover 0.9, active scale(0.98), focus 3px cyan. Secondary: transparent, border, hover cyan
- **Nav** — sticky, `rgba(6,6,16,0.85)`, `blur(16px)`
- **Forms** — bg-secondary, border-subtle, 8px, focus cyan + glow
- **Glass** — `backdrop-filter: blur(16px) saturate(140%)` + `rgba(10,10,26,0.6)` bg + 1px top `--border-subtle`; `@supports` solid fallback; ≤3 blurred surfaces per view (GPU)
- **Grain** — tiled SVG `feTurbulence` data-URI at 3-5% opacity, `mix-blend-mode: overlay`, `pointer-events:none` — kills gradient banding; never a runtime filter over scrolling areas
- **Spartan UI** — copied-in components (not a black-box dep), OnPush everywhere, lazy-load heavy views (tables, editors, charts), Tailwind + design-token theming. Per `rules/angular.md`.

## Interaction (every interactive element)

`cursor:pointer`, hover state, focus-visible (3px cyan, 2px offset), active (scale 0.98), transition (0.2s color, 0.1s transform). WCAG 2.2 — min 24×24px targets, focus not obscured by sticky headers, dragging alternatives required, accessible auth.

- Rings on `:focus-visible` only (keyboard), never bare `:focus` — and via `outline` + `outline-offset`, which survive `overflow:hidden` + `border-radius` where box-shadow clips
- Focus-Not-Obscured (2.4.11 AA): `html { scroll-padding-top: calc(var(--nav-h) + 1rem) }` (+ `scroll-padding-bottom` for sticky footers) so tab/anchor targets never land under sticky chrome

### 4-state distinction (NON-NEGOTIABLE)

Every link/button/card MUST visually differ across `:default | :hover | :focus-visible | :active` — NEVER let two states look identical.

- Default → neutral · Hover → underline-sweep + color shift + `translateY(-1px)` · Focus-visible → 3px cyan ring 2px offset (distinct from hover) · Active → `scale(0.98)` + immediate color confirm

Audit gate: Playwright cycles each interactive element through 4 states → screenshots → diff ≥3px pixel-difference between adjacent states or fail.

### Underline-sweep (text links default)

```css
.underline-hover{position:relative}
.underline-hover::after{content:"";position:absolute;z-index:1;left:51%;right:51%;bottom:0;background:var(--brand-accent);height:1px;transition:left .3s ease-out,right .3s ease-out}
.underline-hover:hover::after,.underline-hover:focus-visible::after{left:0;right:0}
```

`var(--brand-accent)` / theme equivalent — never hard-coded #hex.

## See submodules: design-tokens.md, build-breaking-rules.md, cinematic-doctrine.md.
