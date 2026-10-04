---
name: "visual-experience"
description: "Gorgeous/cinematic requirements every delivered app's UI must meet — anti-slop premium bar, exact brand tokens, motion, logo/image quality, WCAG 2.2 visual accessibility."
triggers:
  - "design"
  - "ui"
  - "visual"
  - "motion"
  - "theme"
priority: 2
pack: "design"
stage: stable
---

# Visual & Experience — every app's UI must be gorgeous

## The bar

- **Every surface: black + cyan + gorgeous + beautiful + animated + annotated + cited + HBO-level + cinematic + catchy.** Non-negotiable house style.
- Anti-AI-slop, premium, distinctive — investor-demo quality. Apple Test: two elements compete → remove one; crowded → add whitespace; final feel effortless, inevitable.
- Gorgeous-by-default: every iteration measurably more beautiful than the last. Never ship "functional but plain."

## Cinematic floor

- Hero: full-screen video or particle / gradient-mesh field — never a flat gradient placeholder.
- Scroll-driven section transitions + View Transitions on every public surface; `@starting-style` entrances; custom cursor / micro-interactions.
- Depth: layered surfaces, gradient meshes, glass + subtle grain.
- Bento asymmetry: 1-2 span-2 anchor cards in an auto-fill `minmax()` grid + an accent wash on the anchors — never a uniform card wall.

## Canvas hero layer (nebula/particle recipe)

- Zero-dep 2D canvas; cap `devicePixelRatio` at 2; scale particle count to viewport area — never a fixed density.
- `prefers-reduced-motion` → draw ONE rich static frame and stop (no rAF loop) — the gorgeous stays, the motion goes.
- Pause rAF on BOTH `document.hidden` AND element-offscreen (IntersectionObserver on the canvas) — either alone still burns battery.
- Reference impl: claude.megabyte.space hero — `heroNebula` fn in `public/index.html` (heymegabyte/claude.megabyte.space).

## Brand (exact, non-inferable)

- Dark-first. `#060610` bg (never `#000`) · `#00E5FF` cyan (primary CTA) · `#50AAE3` blue (secondary) · `#7C3AED`/`#8B5CF6` purple. Text `#f0f0f5` (never `#fff`).
- Fonts: Space Grotesk (headings) · Sora (body) · JetBrains Mono (mono) · Clash Display (hero only). Self-hosted WOFF2 — never Google Fonts CDN.
- Fluid `clamp()` type scale; `text-wrap: balance` (headings) / `pretty` (body); max 65ch; border-radius never 0, never pill.

## Motion

- Purposeful, brand-locked; scroll-driven + View Transitions; always honor `prefers-reduced-motion` with a full non-animated path.
- Scroll-driven = progressive enhancement: `animation-timeline: view()` / `scroll()` only behind `@supports (animation-timeline: view())`. Firefox: unsupported as of late 2026 — verify at caniuse; never animation-only state.
- JS fallback auto-disables when CSS support exists: `if (!CSS.supports('animation-timeline: view()')) observe(...)` — IntersectionObserver reveal only fills the gap; never double-drive one element.
- `@starting-style` first-paint entrances: transition-based, zero JS; pair `transition-behavior: allow-discrete` for display/dialog/popover entry+exit (Baseline mid-2024 — verify at caniuse).
- Kinetic gradient type: `background-clip: text` + `background-size: 200%+` + slow `background-position` pan — gated on `prefers-reduced-motion: no-preference`.

## Logo (non-negotiable)

- White/light-text logo only on dark/contrasting backing. Navbar wordmark: single line (never wraps), large + prominent (fluid), contrast halo over a transparent-nav hero. Mark rendered large (not a timid afterthought); a generated wordmark is a tight banner, not a padded square.

## Imagery

- Real, high-quality, relevant images — never gray placeholder boxes. Logos ship with alpha (no opaque box). Every image has meaningful alt text.

## Visual accessibility (WCAG 2.2 AA)

- Contrast ≥4.5:1 text / ≥3:1 large + UI — verify muted/accent tokens, not just defaults. Target size ≥24×24px. Focus ring 2px, ≥3:1, never obscured by sticky headers.
- 4-STATE distinction (NON-NEGOTIABLE): `default · hover · focus-visible · active` each visually distinct — never two identical.
- axe-core 0 violations at 6 breakpoints (375/390/768/1024/1280/1920). Theme toggle + persistence + system default.

## Immutable-asset cache-busting (mandate)

- Every `Cache-Control: immutable` / 1yr asset carries a content-version — hashed filename or `?v=` bumped on EVERY change — including any `_headers` Early-Hints preload of the same URL (CF 103 cache lags a deploy briefly).
- Reference incident (claude.megabyte.space, 2026-10-04): a stylesheet served `immutable, max-age=1yr` on an UNVERSIONED URL left returning visitors on stale CSS indefinitely.
