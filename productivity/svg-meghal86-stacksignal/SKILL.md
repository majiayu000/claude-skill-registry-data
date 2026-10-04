---
name: SVG
version: 1.1.0
changelog: "Restructured with auxiliary files for focused reference"
description: Create and optimize SVG graphics with proper viewBox, accessibility, and CSS styling.
metadata: {"clawdbot":{"emoji":"📐","requires":{},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File | Key Trap |
|-------|------|----------|
| viewBox & Scaling | `viewbox.md` | Missing viewBox = no scaling |
| Screen Readers | `accessibility.md` | role="img" + title as first child |
| SVGO Config | `optimization.md` | Default removes viewBox/title |
| Inline vs img | `embedding.md` | `<img>` cannot be styled with CSS |
| currentColor | `styling.md` | Hardcoded fills block theming |

## Critical Defaults

```svg
<!-- Minimum viable SVG -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="..."/>
</svg>
```

## Common Mistakes Checklist

- [ ] viewBox present (not just width/height)
- [ ] Coordinates within viewBox bounds
- [ ] No hardcoded `fill="#000"` if theming needed
- [ ] `role="img"` + `<title>` for informative SVGs
- [ ] `aria-hidden="true"` for decorative SVGs
- [ ] Unique IDs across all inline SVGs on page
- [ ] xmlns included for external `.svg` files

## Memory Storage

User preferences persist in `~/svg/memory.md`. Create on first use.

```markdown
## User Preferences
<!-- SVG workflow defaults. Format: "setting: value" -->
<!-- Examples: default_viewbox: 0 0 24 24, prefer_inline: true -->

## Accessibility Mode
<!-- informative | decorative -->

## Optimization
<!-- Tool and settings. Format: "tool: setting" -->
<!-- Examples: svgo: preset-default, remove_metadata: true -->

## Icon Defaults
<!-- Fill and sizing preferences -->
<!-- Examples: fill: currentColor, default_size: 24x24 -->
```

*Empty sections = use skill defaults. Learns user preferences over time.*
