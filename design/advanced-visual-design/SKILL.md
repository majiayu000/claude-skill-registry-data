---
name: advanced-visual-design
description: Advanced visual design techniques including typography systems, color theory, grid-based layouts, visual hierarchy, and composition principles. Use when creating high-quality visual designs, establishing design foundations, or implementing sophisticated design systems. Also triggers on type scale, font pairing, color palette, HSL color, 8-point grid, 12-column layout, visual hierarchy, whitespace, composition, rule of thirds, golden ratio, dark mode design, optical adjustments, or easing curves. Even if someone says "make this look professional" or "set up my design foundations" — use this skill.
metadata:
  version: "1.0.0"
allowed-tools: "Bash, Read, Write"
---

<essential_principles>

### 1. Mathematical Foundations

Typography scales use ratios (Major Third 1.250, Perfect Fourth 1.333). Spacing uses the 8-point grid. Layouts use 12-column grids. Color palettes use HSL with consistent lightness steps. Design decisions are systematic, not arbitrary.

### 2. Visual Hierarchy Through Contrast

Size, weight, color, spacing, and position — in that order of impact. Every element on the page should have a clear hierarchy level. If everything is bold, nothing is bold.

### 3. Whitespace Is Structure

Macro whitespace (48–96px between sections) creates rhythm. Micro whitespace (16–32px between elements) creates grouping. Whitespace is not empty — it's the structural system that makes content readable.

### 4. Color Serves Function

Every color has a semantic role: surfaces, text levels, actions, feedback states. Dark mode swaps semantic values, not individual component colors. Accessibility contrast ratios are non-negotiable.

</essential_principles>

<intake>

| User Says | Route To |
|-----------|----------|
| "Typography" / "type scale" / "font pairing" / "font stack" | `references/typography.md` |
| "Color palette" / "HSL" / "color harmony" / "dark mode colors" | `references/color-systems.md` |
| "Grid" / "layout" / "spacing" / "visual hierarchy" / "composition" / "whitespace" | `references/layout-composition.md` |
| "Optical adjustments" / "animation easing" / "micro-interactions" | `references/layout-composition.md` → Advanced Techniques |

</intake>

<quality_gates>

Before finalizing any visual design:

- [ ] Type scale mathematically consistent (ratio applied correctly)
- [ ] Line length 45–75 characters (`max-width: 65ch`)
- [ ] Color contrast: 4.5:1 normal text, 3:1 large text/UI components
- [ ] 8-point grid applied (all spacing in multiples of 8px)
- [ ] Visual hierarchy clear (3–4 distinct levels using size, weight, color, spacing)
- [ ] Whitespace sufficient (48px+ between sections, 16px+ between elements)
- [ ] Alignment consistent (left/center/right used intentionally)
- [ ] Dark mode implemented (semantic tokens swapped, not pure white on pure black)
- [ ] Optical adjustments applied (overshoot on circles, visual centering of icons)
- [ ] Animations respect `prefers-reduced-motion`

</quality_gates>

<reference_index>

| Reference | Purpose | When to Read |
|-----------|---------|--------------|
| `references/typography.md` | Type scales (3 ratio options), line heights, font pairing, font stacks | Setting up or auditing typography |
| `references/color-systems.md` | HSL palette building, semantic tokens, color harmony, dark mode strategy | Choosing or building color systems |
| `references/layout-composition.md` | 8pt grid, 12-column layout, hierarchy principles, composition rules, optical adjustments, animation | Building layouts or refining visual polish |

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/palette-generator.py` | Generate a 9-step HSL color palette from a base hue (CSS + JSON output) | Creating a new color system |
| `scripts/type-scale.py` | Calculate a typographic scale from any ratio (table, CSS, or JSON output) | Setting up or comparing type scales |
| `scripts/contrast-checker.py` | Check WCAG 2.2 AA contrast ratio between any two colors (hex, HSL, RGB) | Validating color accessibility |

| Asset | Purpose | When to Use |
|-------|---------|-------------|
| `assets/color-palettes.json` | 5 pre-built accessible color palettes (ocean, forest, sunset, royal, neutral) with semantic token template | Starting a new color system without building from scratch |

</reference_index>

<quick_reference>

**Quick examples:**

Generate a blue palette:
```bash
python scripts/palette-generator.py 240 --name blue --format css
```

Calculate a Major Third type scale:
```bash
python scripts/type-scale.py --ratio 1.250 --format css
```

Check contrast between two colors:
```bash
python scripts/contrast-checker.py "#3b82f6" "#ffffff"
```

**Common ratios:** 1.250 (Major Third, balanced), 1.333 (Perfect Fourth, more contrast), 1.618 (Golden Ratio, dramatic)

**8-point spacing:** 8, 16, 24, 32, 40, 48, 64, 80, 96, 128px

**Environment note:** When integrating design tokens into a build pipeline, configure token source paths via environment variables rather than hardcoding: `DESIGN_TOKENS_PATH`, `THEME_OUTPUT_DIR`.

</quick_reference>

## CLAIMS

- [GENERATED] Major Third ratio (1.250) produces legible UI type scales; Perfect Fourth (1.333) suits editorial/marketing contexts with more dramatic hierarchy
- [GENERATED] Hue-matched shadows (surface hue at reduced opacity) are a professional signal — `rgba(0,0,0,X)` on colored surfaces creates a visual disconnect that reads as unsophisticated
- [GENERATED] The 8-point grid maintains alignment across screen densities because 8px divides evenly into all common device pixel ratios (1x, 1.5x, 2x, 3x)

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- Display P3 and wide-gamut color for modern displays is not covered — relevant for Apple device targets
- Variable fonts (weight/width/optical-size axes) dramatically change typographic possibility but add complexity not addressed here
- Dark mode optical adjustments (slightly lower text weight, reduced saturation) are referenced but not fully detailed
