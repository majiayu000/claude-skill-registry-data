---
name: eco-tokens
description: Canonical ECO Design System token names and values (color, spacing, typography, shadow, border) for this repo. Use whenever writing or editing CSS/inline styles in any .html file, to look up the correct var(--...) name and value instead of guessing or hardcoding hex/px.
---

# eco-tokens

Single source of truth for design token names in swedol-ui-prototype. Pairs with `tokens.json` in this folder.

## Where the tokens actually come from

The real tokens live in the `alligo-design-tokens` npm package (source: `github.com/Alligo-AB/alligo-design-tokens`, private repo). Every page in this repo already loads them at runtime via CDN — see the `<head>` of `template.html` and `mypages/mypages-template.html`:

```html
<link rel="stylesheet" href="https://unpkg.com/alligo-design-tokens@latest/dist/css/fonts.css">
<link rel="stylesheet" href="https://unpkg.com/alligo-design-tokens@latest/dist/css/index.css">
```

That means every `--color-*`, `--dimension-*`, `--shadow-*`, `--border-*` custom property is already available in the browser on every page — nothing needs to be imported or built for a token to work. `tokens.json` in this skill folder is **not** loaded by the browser; it's a lookup file for Claude to reference while writing code, so generated CSS uses the right token name on the first try instead of hardcoding a hex value that happens to match.

This repo does not use Tailwind (no `tailwindcss` build, no CDN script, no `tailwind.config.js` anywhere in the repo — confirmed by search). Every page is hand-written CSS in `<style>` blocks referencing these CSS custom properties directly, plus `@media (min-width: ...)` blocks for the breakpoints in CLAUDE.md. Do not introduce Tailwind utility classes here — it would be inconsistent with the rest of the codebase and wouldn't have a build step to generate the utilities anyway.

## Rule: always reference tokens, never hardcode

When writing or editing any CSS in this repo:

1. Look up the semantic name in `tokens.json` (e.g. `color.text-primary`, `shadow.elevation-b-80`, `spacing.space-24`).
2. Emit `var(--the-token-var)` in the CSS, not the literal hex/px value.
3. If a value doesn't exist in `tokens.json` under any category, check CLAUDE.md first (it documents a few composite/derived values, like button hover gradients, that aren't 1:1 tokens) — only fall back to a literal value if genuinely nothing else fits, and flag it in your response so a human can confirm.

Example — correct:
```css
.card {
  background: var(--color-surface-raised-primary);
  border: 1px solid var(--color-border-primary);
  box-shadow: var(--shadow-elevation-b-20);
  padding: var(--dimension-spacing-space-24, 24px);
}
```

Example — avoid:
```css
.card {
  background: #ffffff;
  border: 1px solid #e5e5e5;
  padding: 24px;
}
```
(Works visually, but silently drifts from the design system the moment Supernova changes a value — the whole point of the token package is that it doesn't.)

## Categories in tokens.json

- **color** — 98 semantic tokens (`text-*`, `border-*`, `surface-*`, `background-*`, `accent-*`, `icon-*`). Primitives (`--color-primitive-*`) are intentionally excluded — always use the semantic name, never the raw grey/blue/etc. scale, so intent stays legible in the CSS.
- **spacing** — `space-0` through `space-120`, matching CLAUDE.md's Spacing Scale table exactly (this is the *fixed* pixel scale, not the per-breakpoint `space-sm`/`space-lg` layout tokens documented separately in CLAUDE.md, which vary by breakpoint and aren't in the package as discrete tokens).
- **typography** — 20 entries (`display-sm/md/lg`, `headline-sm/md/lg/xl`, `title-sm/md/lg`, `label-sm/md/lg`, `alt-label-sm/md/lg`, `body-sm/md/lg/xl`). Each has a `mobile` block (base styles) and a `desktopOverride` block (only the properties that actually change at 769px+) — mirrors CLAUDE.md's mobile-first breakpoint approach and matches the naming convention already shipping in the Magento project's `typography-plugin.js`. When writing a component's type styles, start from `mobile`, then add the properties in `desktopOverride` inside a `@media (min-width: 769px)` block — don't repeat properties that don't change.
- **shadow** — the `elevation-*` tokens (`elevation-b-20` through `elevation-b-100`, `elevation-t-*`, `elevation-drawer-*`, plus the component-specific ones). Use `var(--shadow-elevation-b-XX)` directly as a `box-shadow` value — it's already a full multi-layer shadow string.
- **border** — the 3 border-width shorthand tokens (`brd-1`, `brd-2`, `brd-4`), each a full `width solid color` string.
- **radius** — currently only `full` (pill/circle radius, `62.438rem`). Everything else in this design system uses `border-radius: 0` (sharp corners) per CLAUDE.md — there is no small/medium radius token because the system intentionally doesn't use one.

## Generation / verification

`tokens.json` is generated from the `dist/` folder supplied to `generate-tokens.py`; do not hand-edit token values. Typography is sourced from the current Supernova export structure: `css/base/typography.css` supplies the semantic type-scale names and descriptions, while `css/base/dimension.css` and `css/mobiletypography/dimension.css` supply desktop/base and mobile dimensions respectively. The generator preserves the ECO mobile-first output contract: a complete `mobile` block plus only changed values in `desktopOverride` at 769px. Typography modifier tokens are intentionally excluded from the canonical 20 type-scale entries.
