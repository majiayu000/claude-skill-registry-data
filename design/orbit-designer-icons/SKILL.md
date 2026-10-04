---
name: orbit-designer-icons
description: Audit icon usage across a WordPress plugin's admin UI — icon library consistency (one set, not three), accessible-icon patterns (label + role), inline SVG vs icon-font tradeoffs, dashicons vs custom SVGs, icon-only buttons accessibility. Use when the user says "icon audit", "icon system", "dashicons", "SVG icons".
---

# 🪐 orbit-designer-icons — Icon system audit

Plugins routinely ship 3 icon libraries (Dashicons + Font Awesome + custom SVG) for no good reason. This audit catches the duplication and proposes a single source.

---

## Quick start

```bash
claude "/orbit-designer-icons Audit ~/plugins/my-plugin's icon usage."
```

---

## What it checks

### 1. Library inventory
Greps every PHP / JS / CSS file for:
- `dashicons-*` classes
- `fa-*` / `fas` / `far` / `fab` (Font Awesome)
- Inline SVG `<svg>` elements
- Custom icon-font CSS (e.g. `eicon-*` from Elementor)
- IconJar / Heroicons / Phosphor / Tabler embeds

```
[Icons] my-plugin

Libraries detected:
  - Dashicons:    47 references (WP-bundled, free)
  - Font Awesome: 23 references (3rd-party, requires license for Pro icons)
  - Custom SVG:   18 inline (mixed sizes, inconsistent stroke widths)
  - Icomoon:       4 references (1 forgotten leftover from 2022)

⚠ 4 different icon systems in one plugin. Recommend consolidating.
```

### 2. Inline SVG > icon font (modern best practice)
**Whitepaper intent:** Icon fonts have accessibility issues (screen readers read the unicode char), CSP issues (require `font-src`), and load-order issues (FOUT/FOIT). Inline SVGs are crisp, accessible, and tree-shakeable.

```html
<!-- ❌ Icon font -->
<i class="fa fa-trash"></i>

<!-- ✅ Inline SVG -->
<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
  <path d="..." />
</svg>
```

### 3. Icon-only button accessibility
```html
<!-- ❌ Screen reader hears "button" with no context -->
<button><i class="fa fa-trash"></i></button>

<!-- ✅ Accessible name -->
<button aria-label="Delete">
  <svg aria-hidden="true">...</svg>
</button>
```

### 4. Decorative vs meaningful icons
```html
<!-- Decorative — hide from AT -->
<svg aria-hidden="true">...</svg>

<!-- Meaningful — give it a label -->
<svg role="img" aria-label="Success">...</svg>
```

### 5. Consistent sizing system
All icons should use a discrete size scale: 12 / 16 / 20 / 24 / 32 / 48px. Plugins with 17 different icon sizes look chaotic.

### 6. Stroke width consistency (for outline icons)
Heroicons use 1.5px. Lucide uses 2px. Phosphor offers 1/1.5/2/2.5/3. Pick one and stick with it.

---

## Output

```markdown
# Icon Audit — my-plugin

## Inventory
- Dashicons: 47 (mostly admin nav)
- Font Awesome: 23 (mostly settings page) — forgot to remove from when we used FA
- Inline SVG: 18 (recent additions)
- Icomoon: 4 — DEAD CODE, remove

## Recommendations
1. Consolidate to inline SVG everywhere
2. Drop Font Awesome (saves ~78 KB asset weight)
3. Remove Icomoon references in admin/legacy.css
4. Standardise stroke width to 1.5px (matches WP admin)
5. Use 16px icons in lists, 20px in buttons, 24px in headings

## Accessibility issues
- 7 icon-only buttons missing aria-label
- 12 decorative icons missing aria-hidden="true"
```

---

## Pair with

- `/orbit-designer-tokens` — overall visual system
- `/orbit-bundle-analysis` — measure asset weight from icon libs
- `/orbit-accessibility` — icon-only button a11y

---

## Sources & Evergreen References

### Canonical docs
- [Heroicons](https://heroicons.com/) — open-source SVG, 1.5px stroke
- [Lucide](https://lucide.dev/) — fork of Feather, 2px stroke
- [Phosphor Icons](https://phosphoricons.com/) — multi-weight system
- [Dashicons](https://developer.wordpress.org/resource/dashicons/) — WP-bundled
- [Inclusive Components — Icons](https://inclusive-components.design/notifications/) — a11y patterns
- [SVGO](https://github.com/svg/svgo) — SVG optimisation

### Rule lineage
- Icon fonts → inline SVG — industry shift since ~2018, conventional wisdom now

### Last reviewed
- 2026-04-29
