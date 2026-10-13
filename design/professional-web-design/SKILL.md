---
name: professional-web-design
description: Industry-standard web design practices including responsive design, performance optimization, modern CSS techniques, and production-ready workflows. Use when building professional websites, web applications, or implementing advanced CSS/HTML patterns. Also triggers on responsive layout, mobile-first, Core Web Vitals, CSS Grid, Flexbox, container queries, typography system, font loading, image optimization, WCAG accessibility, semantic HTML, progressive enhancement, dark mode, design tokens in CSS, or pre-launch auditing. Even if someone says "make this responsive" or "optimize my site" — use this skill.
metadata:
  version: "1.0.0"
allowed-tools: "Bash, Read, Write, Glob"
---

<essential_principles>

### 1. Mobile-First, Always

Start at 320px and scale up via `min-width` media queries. Never build desktop-first and then try to squeeze it into mobile. Standard breakpoints: 768px (tablet), 1024px (desktop), 1440px (large).

### 2. Performance Is a Feature

Target Core Web Vitals: LCP under 2.5s, INP under 200ms, CLS under 0.1. Inline critical CSS, defer everything else, lazy-load images, use WebP with fallbacks, and set explicit width/height on all images.

### 3. Semantic HTML First, ARIA Second

Use the correct HTML element before reaching for ARIA attributes. A `<button>` is better than `<div role="button">`. A `<nav>` is better than `<div class="navigation">`. ARIA is a patch, not a foundation.

### 4. CSS Custom Properties as Design Tokens

All colors, spacing, typography, shadows, and radii live in `:root` as CSS custom properties. Components consume tokens, never raw values. Dark mode swaps token values, not component styles.

### 5. Progressive Enhancement

Build the base experience for all browsers, then layer on modern features behind `@supports`. Never require Grid, container queries, or modern CSS for basic usability.

</essential_principles>

<intake>

| User Says | Route To |
|-----------|----------|
| "Build a page" / "landing page" / "make this responsive" | `workflows/responsive-build.md` |
| "Pre-launch checklist" / "audit my site" / "performance check" | `workflows/pre-launch-audit.md` |
| "CSS Grid" / "Flexbox" / "container queries" / "modern CSS" | `references/css-techniques.md` |
| "Performance" / "Core Web Vitals" / "image optimization" / "font loading" | `references/performance.md` |
| "Accessibility" / "WCAG" / "ARIA" / "screen reader" / "focus management" | `references/accessibility.md` |
| "Typography" / "type scale" / "font system" / "line height" | `references/typography.md` |
| "Design tokens" / "CSS variables" / "dark mode" / "theme" | `references/design-tokens.md` |

**If the project type is unclear, ask:**
"What are you building — a landing page, web app, content site, or dashboard?"

</intake>

<routing>

| Workflow | Purpose | When to Read |
|----------|---------|--------------|
| `workflows/responsive-build.md` | Mobile-first build process: layout, breakpoints, images, testing | Building or fixing a responsive page |
| `workflows/pre-launch-audit.md` | Comprehensive checklist: performance, a11y, SEO, cross-browser | Before deploying to production |

| Reference | Purpose | When to Read |
|-----------|---------|--------------|
| `references/css-techniques.md` | Grid, Flexbox, container queries, animations, progressive enhancement | Implementing layouts or advanced CSS |
| `references/performance.md` | Core Web Vitals, image optimization, font loading, critical CSS | Optimizing load times |
| `references/accessibility.md` | Semantic HTML, ARIA patterns, focus management, skip links | Building accessible interfaces |
| `references/typography.md` | Type scales, font stacks, line height, readability rules | Setting up typography |
| `references/design-tokens.md` | CSS custom properties, theming, dark mode, spacing/color systems | Establishing design foundations |

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/lighthouse-audit.js` | Run Lighthouse performance audit, check Core Web Vitals against targets | Before launch or after performance changes |
| `scripts/a11y-audit.js` | Automated WCAG 2.2 accessibility audit using axe-core + Puppeteer | Before launch or after UI changes |
| `scripts/contrast-checker.py` | Check WCAG contrast ratio between any two colors | When choosing or validating color combinations |

| Asset | Purpose | When to Use |
|-------|---------|-------------|
| `assets/boilerplate.html` | Production-ready HTML starter with design tokens, skip link, critical CSS, meta tags, dark mode | Starting a new page from scratch |

**After reading the relevant workflow/reference, follow it exactly.**

</routing>

<quick_reference>

**Standard breakpoints:**
```
Mobile:  320px–767px   (base styles, no media query)
Tablet:  768px+        (@media min-width: 768px)
Desktop: 1024px+       (@media min-width: 1024px)
Large:   1440px+       (@media min-width: 1440px)
```

**Core Web Vitals targets:**
LCP under 2.5s, INP under 200ms, CLS under 0.1

**Quality gates (pre-launch):**
- Mobile-responsive (tested 320px–1920px)
- Lighthouse score 90+ (all categories)
- WCAG 2.2 AA compliant
- Cross-browser (Chrome, Firefox, Safari, Edge)
- Images optimized (WebP + fallback, lazy-loaded)
- Critical CSS inlined (under 14KB gzipped)
- JavaScript deferred/async
- No console errors

</quick_reference>

## CLAIMS

- [SOURCED] Core Web Vitals targets: LCP <2.5s, INP <200ms (FID deprecated March 2024), CLS <0.1 — web.dev/vitals
- [SOURCED] Critical CSS inlined in `<head>` should be under 14KB (one TCP round-trip) — web.dev/critical-css
- [GENERATED] `font-display: swap` prevents invisible text during font load but causes FOUT — `optional` is better for body text when fallback metrics match
- [GENERATED] Mobile-first (`min-width`) media queries produce smaller CSS than desktop-first (`max-width`) because base styles don't need overrides

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- HTTP/3 and connection-level performance are not covered — relevant for global audiences with high-latency connections
- Edge rendering (Cloudflare Workers, Vercel Edge) changes the performance model significantly — not addressed
- Container queries vs media queries tradeoffs are mentioned but not detailed
