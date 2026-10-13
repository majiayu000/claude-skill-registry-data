---
name: applying-web-design-standards
description: "Applies web design standards covering typography systems, color theory, grid layouts, design tokens, component library architecture, responsive CSS, and performance optimization. Activates on: type scale, font pairing, color palette, HSL color, 8-point grid, design tokens, component API, Storybook, Style Dictionary, atomic design, responsive layout, mobile-first, Core Web Vitals, CSS Grid, Flexbox, container queries, pre-launch audit. Does NOT activate for Kyle-specific branded builds — use executing-branded-frontends or managing-design-briefs instead."
metadata:
  version: "1.0.0"
allowed-tools: "Read, Write, Bash, Glob"
---

# Applying Web Design Standards

Consolidated reference for typography, color, grid, design tokens, component
architecture, responsive CSS, and performance. Merged from three prior skills:
`advanced-visual-design`, `design-system-builder`, `professional-web-design`.

---

## Domain Routing

| Request type | Reference file |
|---|---|
| Typography scale, font pairing, loading | `references/typography-system.md` |
| Web-specific type concerns | `references/web-typography.md` |
| Color systems, HSL, contrast, palettes | `references/color-and-grid.md` |
| Layout, composition, spatial principles | `references/layout-composition.md` |
| Design token architecture, Style Dictionary | `references/design-tokens.md` |
| Responsive tokens, dark mode tokens | `references/responsive-tokens.md` |
| Component patterns, compound components | `references/component-library.md` |
| Design system governance, versioning | `references/design-system-governance.md` |
| Tech stack selection (Storybook, CVA, etc.) | `references/tech-stack-comparison.md` |
| Core Web Vitals, image opt, critical CSS | `references/performance-standards.md` |
| CSS Grid, Flexbox, container queries | `references/css-techniques.md` |
| WCAG 2.2, ARIA, keyboard nav | `references/accessibility.md` |

---

## Workflow Routing

| Task | Workflow file |
|---|---|
| Starting a new design system from scratch | `workflows/new-design-system.md` |
| Adding a new component to an existing system | `workflows/add-component.md` |
| Documenting a design system | `workflows/document-system.md` |
| Pre-launch quality audit | `workflows/pre-launch-audit.md` |
| Building a responsive layout | `workflows/responsive-build.md` |

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/contrast-checker.py` | WCAG contrast ratio validation |
| `scripts/palette-generator.py` | HSL palette generation with lightness steps |
| `scripts/type-scale.py` | Modular type scale calculator |
| `scripts/build-tokens.js` | Style Dictionary token compilation |
| `scripts/generate-component.js` | Component scaffolding with CVA variants |
| `scripts/a11y-audit.js` | Automated accessibility checks |
| `scripts/lighthouse-audit.js` | Core Web Vitals measurement |

**Visual regression (pre-launch / multi-screen builds):**
```bash
npm install -D @vizzly-testing/cli
npx vizzly tdd "npx playwright test"   # local TDD — no account needed
npx vizzly run "npx playwright test"   # CI run with cloud baseline sync
```
Free tier: 1 private project, local TDD unlimited. See `vizzly.dev/pricing`.

---

## Core Principles (Quick Reference)

**Typography:** Scales use ratios (Major Third 1.250, Perfect Fourth 1.333).
See `references/typography-system.md` for full scale table, pairing rules, and loading patterns.

**Color:** HSL with consistent lightness steps for palette construction. **OKLCH preferred for gradients and perceptual consistency** — OKLCH lightness is uniform across hues, preventing muddy gradient midpoints that HSL produces. Minimum contrast 4.5:1 normal text, 3:1 large text.
See `references/color-and-grid.md`.

**OKLCH quick reference:**
- Format: `oklch(L% C H)` — L=lightness 0–100, C=chroma 0–0.4, H=hue 0–360
- Browser support: Chrome 111+, Firefox 113+, Safari 15.4+ — include hex fallback for older targets
- When to use: gradient generation, new token creation, perceptual contrast checks
- When to keep hex: locked brand profiles (FlashFusion v3, Loxihart) — profiles are the execution SOT

**Grid:** 8-point spatial system. 12-column layout. Every spacing value is a multiple of 8.
Exceptions require written justification. See `references/layout-composition.md`.

**Design Tokens:** Primitive → Semantic → Component three-tier architecture.
Never use primitive tokens directly in components — always via semantic alias.
See `references/design-tokens.md`.

**Responsive:** Mobile-first at 320px, scale up via `min-width`. Standard breakpoints:
768px (tablet), 1024px (desktop), 1440px (large). See `workflows/responsive-build.md`.

**Performance:** LCP <2.5s, INP <200ms, CLS <0.1. Inline critical CSS, defer rest,
lazy-load images, set explicit dimensions. See `references/performance-standards.md`.

---

## Anti-Patterns

See `patterns/anti-patterns.md` for full catalog. Critical failures:
- Hardcoded hex values instead of token references
- Desktop-first responsive (always mobile-first)
- ARIA added as an afterthought instead of semantic HTML first
- Pixels for spacing instead of the 8-point grid
- Everything bold (destroys hierarchy — size and weight are contrast tools)
