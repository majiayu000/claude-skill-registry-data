---
name: design-tokens
description: This skill should be used when a user wants to scaffold or refactor a design token system — e.g. "set up design tokens", "create a design system foundation", "extract these hardcoded colors into tokens", "add a type scale", "theming setup", or "dark mode tokens". It produces a single source of truth for color, type, spacing, radius, shadow, motion, and z-index, emitted in the format the detected stack expects.
version: 0.1.0
---

# Design Tokens

Establish a coherent, themeable design token foundation — or migrate an existing
codebase of hardcoded values onto one — adapted to whatever stack the project
already uses. Tokens are the contract every other UX skill builds on: components
should reference token names, never raw values.

## When to use

Reach for this skill when the request resembles:

- "set up design tokens" / "create a design system foundation"
- "extract these hardcoded colors into tokens" / "replace these hex codes"
- "add a type scale" / "give me a modular scale"
- "theming setup" / "support multiple brands"
- "dark mode tokens" / "add a dark theme"

Two operating modes share most of the workflow:

- **Scaffold** — no token system exists; create one from the starter assets.
- **Migration** — values are hardcoded across the codebase; introduce tokens and
  replace usages incrementally.

## Step 1 — Detect the stack

Before generating anything, READ
`../ux-foundations/references/stack-detection.md`
and run the procedure. Do not duplicate it here. Hold the resulting decisions:

```
framework   = react | vue | svelte | angular | vanilla
styling     = tailwind | css-in-js | css-modules | sass | vanilla-css
tokenFormat = <per stack-detection §3>
language    = ts | js
```

Report the detection in one line, then proceed. Extend any existing token names
rather than inventing a parallel set.

## Step 2 — Define token categories

Design the full set up front so categories stay consistent. Use the starter
assets as the baseline and adjust values to the project's brand.

- **Color — use semantic layering.** Keep a small **primitive palette** (a
  neutral ramp plus a brand ramp). Never expose primitives to components. Map
  them to **semantic roles**: `--color-bg`, `--color-surface`, `--color-fg`,
  `--color-muted-fg`, `--color-primary`, `--color-primary-fg`, `--color-border`,
  and state colors (`--color-success`, `--color-warning`, `--color-danger`) each
  with a readable foreground variant. **Verify contrast** of every fg/bg pair
  (see `scripts/contrast-check.mjs`) before shipping — semantic roles are
  promises about legibility.
- **Type scale** — a modular scale (`--font-size-xs` … `--font-size-3xl`) in
  rem. Generate with `scripts/type-scale.mjs`.
- **Spacing scale** — a 4px-based ramp (`--space-1` … `--space-12`).
- **Radius** — `--radius-sm/md/lg/full`.
- **Shadow / elevation** — `--shadow-sm/md/lg`.
- **Motion** — durations (`--duration-fast/base/slow`) and easings
  (`--ease-standard`, `--ease-emphasized`).
- **Z-index** — a few named layers (dropdown, modal, etc.).
- **Breakpoints** — named min-widths for responsive logic.

## Step 3 — Emit in the stack's format

Translate the canonical tokens into what the project consumes. Keep
`assets/tokens.json` (DTCG) as the portable source of truth regardless of output.

- **Vanilla CSS / CSS Modules / Sass** — CSS custom properties on `:root`
  (start from `assets/tokens.css`). Components use `var(--token)`. Prefer custom
  properties over SCSS variables so themes can switch at runtime.
- **Tailwind v3** — extend `theme.extend` in `tailwind.config.*`, mapping tokens
  to scale keys (colors, fontSize, spacing, borderRadius, boxShadow). For
  runtime theming, point Tailwind colors at CSS custom properties.
- **Tailwind v4** — declare tokens in a `@theme { --color-…: … }` block in CSS.
- **CSS-in-JS** (styled-components / Emotion) — a typed `theme` object exported
  for `<ThemeProvider>`; emit a TypeScript type when `language = ts`.
- **Portable** — `assets/tokens.json` in DTCG format feeds Style Dictionary or
  similar pipelines when one exists.

## Step 4 — Theming (light / dark)

Support at least light and dark. Two complementary mechanisms:

- **Explicit** — override semantic roles under `[data-theme="dark"]` so a parent
  attribute (or a toggle) controls the theme. This is the default; it allows a
  manual switch.
- **System** — mirror the dark overrides inside a
  `@media (prefers-color-scheme: dark)` block so first paint respects the OS
  setting before any JS runs.

Only **semantic** roles change between themes — primitives and the type/spacing
scales stay fixed. `assets/tokens.css` ships both blocks as a model.

## Step 5 — Migration mode

When the codebase is full of literals, introduce tokens without a risky
big-bang rewrite:

1. **Inventory** — grep for hardcoded values:
   - hex colors: `#[0-9a-fA-F]{3,8}\b`
   - rgb/rgba/hsl: `rgba?\(` / `hsla?\(`
   - px font sizes: `font-size:\s*\d+px`
   - px spacing on margin/padding/gap.
2. **Map** — for each literal find the nearest semantic token (closest color by
   contrast/role, nearest step on the type or spacing scale). Note ambiguous
   ones for review instead of guessing.
3. **Replace incrementally** — swap literals for `var(--token)` (or the stack's
   equivalent) file-by-file, presenting diffs and verifying nothing shifts
   visually. Add missing tokens rather than forcing a bad fit.
4. **Guard** — once migrated, treat new raw values in components as a smell;
   `contrast-check.mjs` can gate CI on the color pairs.

## Principles

- **Single source of truth** — define each value once; everything derives from it.
- **Semantic over literal** — name by role (`--color-danger`), not by appearance
  (`--color-red-500`). Roles survive rebrands and theme switches.
- **No raw values in components** — components reference token names only.
- **Keep the primitive palette small** — a tight neutral ramp plus one brand
  ramp covers most needs; sprawl defeats the system.
- **Contrast is non-negotiable** — every fg/bg pairing must meet WCAG AA.

## Bundled files

Reference and reuse these:

- `assets/tokens.css` — starter CSS custom properties on `:root` with a
  `[data-theme="dark"]` override; the canonical CSS baseline.
- `assets/tokens.json` — the same tokens in W3C DTCG format; the portable source
  of truth for tooling.
- `scripts/type-scale.mjs` — generate a modular type scale.
  Usage: `node type-scale.mjs [basePx=16] [ratio=1.25] [stepsUp=6] [stepsDown=2]`.
  Prints a px/rem table plus paste-ready `--font-size-*` custom properties.
- `scripts/contrast-check.mjs` — verify token color pairs meet WCAG 2.x.
  Usage: `node contrast-check.mjs "#111:#fff" "#777:#fff"` or no args to check a
  built-in default set. Exits non-zero if any pair fails AA normal (CI-friendly).

## References

- Stack detection: `../ux-foundations/references/stack-detection.md`
