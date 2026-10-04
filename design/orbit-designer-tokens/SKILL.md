---
name: orbit-designer-tokens
description: Audit design tokens — color palette, typography scale, spacing system, border-radius scale, shadow tokens — for a WordPress plugin's admin UI and frontend output. Catches hardcoded magic numbers, inconsistent type ramps, and palette drift. Use when the user says "design tokens", "color palette audit", "typography scale", "spacing system", or before any visual refresh.
---

# 🪐 orbit-designer-tokens — Design tokens audit

A plugin without a token system has 47 shades of grey in its CSS. This skill catalogues what's used and proposes a consistent system.

---

## Quick start

```bash
claude "/orbit-designer-tokens Audit ~/plugins/my-plugin's CSS for design token consistency."
```

---

## What it checks

### 1. Color palette extraction
Greps every CSS file for color values (hex, rgb, rgba, hsl, named). Counts unique values + usage frequency.

```
[Colors] my-plugin

Found 73 unique color values across 14 CSS files.
Top 10 by usage:
  #2271b1 — 47 uses (WP admin primary blue)
  #ffffff — 38 uses
  #1d2327 — 24 uses (WP admin text)
  #f0f0f1 — 19 uses (WP admin bg)
  #d63638 — 11 uses (WP admin error red)
  ...

Outliers (used 1-2 times):
  #2196f3 — 1 use (Material Design blue — drift from WP palette)
  #ff5722 — 2 uses (Material Design orange)

Suggestion: consolidate to 8-12 named tokens.
```

### 2. Typography scale audit
**Whitepaper intent:** Type scales should follow a ratio (1.125, 1.25, 1.333, 1.5). Plugins with random sizes (13, 14.5, 17, 22, 31px) feel chaotic.

```
[Typography] my-plugin

font-size values found: 17 unique
  12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 28, 32, 36, 42, 48, 60, 72px

⚠ This is 17 sizes — most design systems use 8 (xs/sm/base/md/lg/xl/2xl/3xl).
   Consolidate via CSS custom properties or theme.json.
```

### 3. Spacing system
Check for consistent spacing scale (4px base = 4/8/12/16/24/32/48/64).

### 4. Border-radius
Should typically be 3-5 values: none / sm / md / lg / full. Plugins with 12 different radii are inconsistent.

### 5. Shadow tokens
Same — 3-5 shadows max (xs / sm / md / lg).

### 6. Reference WP admin tokens
Use WP admin's CSS custom properties where possible:
```css
/* ✓ Use WP admin tokens */
.my-plugin-primary { color: var(--wp-admin-theme-color); }

/* ❌ Hardcoded hex */
.my-plugin-primary { color: #2271b1; }
```

WP admin theme colors are user-customisable (Profile → Admin Color Scheme). Hardcoding breaks customisation.

---

## Output

```markdown
# Design Tokens — my-plugin

## Colors
- 73 unique values → recommend consolidating to 12
- ⚠ 5 Material Design colours drifted in from a copy-paste

## Typography
- 17 font-sizes → recommend 8 (use CSS scale)
- ✓ font-family consistent (system-ui stack)

## Spacing
- 22 unique padding/margin values → recommend 4px scale (4/8/12/16/24/32/48/64)

## Border-radius
- 9 unique values → recommend 4 (none / 3 / 6 / 12)

## Shadows
- 7 unique → recommend 4 (none / sm / md / lg)

## WP admin token adoption
- 23/47 places use var(--wp-admin-theme-color) ✓
- ⚠ 24 places hardcode #2271b1 — use the variable instead
```

---

## Pair with

- `/orbit-designer-empty-error` — empty + error state designs
- `/orbit-designer-rtl` — RTL layout checks
- `/orbit-pm-ux-audit` — guided UX score
- `/orbit-visual-regression` — pixel-diff after token changes

---

## Sources & Evergreen References

### Canonical docs
- [WP Admin CSS Variables](https://developer.wordpress.org/news/2023/02/build-with-color-modes-in-wordpress/) — admin theme tokens
- [Design Tokens Community Group (W3C)](https://www.w3.org/community/design-tokens/) — spec
- [theme.json palette](https://developer.wordpress.org/themes/global-settings-and-styles/settings/color/) — frontend
- [Material Design 3 — Tokens](https://m3.material.io/foundations/design-tokens/overview) — example system
- [Tailwind palette](https://tailwindcss.com/docs/customizing-colors) — common reference

### Rule lineage
- WP admin CSS variables — added WP 5.7
- theme.json palette — WP 5.8
- W3C Design Tokens spec — draft, evolving

### Last reviewed
- 2026-04-29 — re-review on WP minor (admin theming evolves)
