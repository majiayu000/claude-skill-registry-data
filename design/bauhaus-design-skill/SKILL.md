---
name: bauhaus-design
description: "Create frontends, posters, dashboards, and web UIs rooted in Bauhaus and Swiss International Typographic Style (Internationale Typografische Stil) design principles. Use this skill when the user mentions Bauhaus, Swiss design, International Typographic Style, grid systems, Josef Müller-Brockmann, Max Bill, Jan Tschichold, Herbert Bayer, László Moholy-Nagy, constructivism, De Stijl-influenced UI, or asks for designs that emphasize mathematical grids, typographic hierarchy, geometric abstraction, asymmetric layouts, or modernist clarity. Also trigger when the user wants a 'clean modernist' look, 'grid-based' design, 'Swiss poster' style, minimalist-but-structured layouts, or references Neue Grafik, Akzidenz-Grotesk, Helvetica-era aesthetics, or rational/systematic design approaches. For iOS/SwiftUI projects, see IOS_ADAPTATION.md for platform-specific implementation patterns including design tokens, Grid/LazyVGrid layouts, SF Pro typography, Canvas geometry, and SwiftUI anti-patterns."
---

# Bauhaus & Swiss International Typographic Style

This skill produces frontends, posters, dashboards, and web interfaces following the design principles of Bauhaus (1919–1933) and the Swiss International Typographic Style (1950s–).

Read this file fully before writing any code.

## Core Philosophy

"Form follows function" is the surface reading. The deeper principle: **every visual element must justify its existence through communication, not decoration.** If it doesn't clarify, it's noise.

The Swiss/Bauhaus tradition treats the designer as an engineer of visual information — not an artist expressing themselves, but a systems thinker organizing content for maximum clarity and impact.

## The Five Pillars

### 1. The Grid Is the Architecture

The grid is not optional — it is the structural skeleton of the entire composition.

- Use a **mathematical grid** as the foundation. Common: 12-column, but 3-, 4-, 6-column grids are equally valid depending on content density.
- All elements — text blocks, images, shapes, whitespace — must **snap to grid intersections or grid lines**.
- **Margins and gutters are sacred.** Consistent outer margins (typically generous) and column gutters create rhythm.
- The grid should be **felt, not seen.** The viewer perceives order without consciously noticing the underlying structure.
- Müller-Brockmann's approach: divide the page into modules (rectangular units), then assign content to groups of modules. This creates proportional relationships across the layout.

**Implementation:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--gutter);
  padding: var(--margin);
}
```
Define `--gutter` and `--margin` as CSS variables and use them everywhere. Never ad-hoc spacing.

### 2. Typography Is Content, Not Decoration

Typography in this tradition is **the primary visual element.** It carries meaning through size, weight, and position — not through ornamental fonts.

**Typeface selection:**
- Sans-serif only. Period.
- Preferred families (load from Google Fonts):
  - **Primary:** `Inter` (closest widely-available digital equivalent of Akzidenz-Grotesk/Helvetica precision)
  - **Display alternative:** `Space Grotesk`, `DM Sans`, `Outfit`
  - **Monospace accent:** `JetBrains Mono`, `IBM Plex Mono`
- ONE typeface family per project is ideal. Two maximum. Never three.
- If the user explicitly requests a Helvetica feel, use `Inter` at tight letter-spacing (`-0.01em` to `-0.02em`).

**Typographic hierarchy through scale:**
- Use a **mathematical type scale.** Recommended: 1.333 (perfect fourth) or 1.5 (perfect fifth).
- Define all sizes as CSS variables from a base:
```css
:root {
  --text-base: 16px;
  --text-sm: calc(var(--text-base) / 1.333);
  --text-lg: calc(var(--text-base) * 1.333);
  --text-xl: calc(var(--text-base) * 1.333 * 1.333);
  --text-2xl: calc(var(--text-base) * 1.333 * 1.333 * 1.333);
  --text-3xl: calc(var(--text-base) * 1.333 * 1.333 * 1.333 * 1.333);
}
```
- **Weight contrast, not font-family contrast**, creates hierarchy: Light (300) for body, Regular (400) for labels, Bold (700) or Black (900) for headlines.
- **Uppercase + wide letter-spacing** for labels and section markers: `text-transform: uppercase; letter-spacing: 0.1em;`

**Alignment:**
- **Flush left, ragged right** is the default. This is non-negotiable in classic Swiss typography.
- Centered text is acceptable only for single-line headings in poster compositions.
- Justified text: only with proper hyphenation (`hyphens: auto;`), otherwise avoid.

### 3. Color as Information, Not Mood

Bauhaus and Swiss design use color **functionally** — to distinguish, to signal hierarchy, to direct attention.

**The palette structure:**
```css
:root {
  /* Ground */
  --bg: #FFFFFF;           /* or near-white: #F5F5F0 */
  --bg-dark: #1A1A1A;      /* for dark variant */
  
  /* Text */
  --text-primary: #1A1A1A;
  --text-secondary: #6B6B6B;
  
  /* Accent — ONE strong color */
  --accent: #E63946;       /* Bauhaus red */
  /* OR */
  --accent: #2660A4;       /* Swiss blue */
  /* OR */
  --accent: #F4A100;       /* Bauhaus yellow */
  
  /* Structure */
  --rule: #D4D4D4;         /* grid lines, dividers */
}
```

**Rules:**
- **Maximum 3 colors** in total (background + text + one accent). Bauhaus primaries (red, blue, yellow) may appear together only in explicit Bauhaus-homage compositions.
- The accent color is used **sparingly** — for emphasis, call-to-action, or a single visual anchor. It should occupy no more than 10–15% of the visual field.
- Black and white are structural, not decorative. A fully black-and-white design with one red element is more Bauhaus than a rainbow.
- **No gradients.** Flat, solid color fields only. Gradients belong to a different tradition.

### 4. Geometric Abstraction as Visual Language

Where illustration or imagery is needed, use **geometric forms** — circles, squares, triangles, lines — not photographs or illustrations (unless photographs are treated as grid-bound rectangles).

**Principles:**
- Circles, rectangles, and diagonal lines are the vocabulary.
- Forms should relate to the grid — a circle's diameter might equal a column width, a diagonal might connect two grid intersections.
- Use SVG for all geometric elements. Never raster images for shapes.
- **Diagonal lines and arcs** create dynamism within the rigid grid — this tension between order and movement is central to Müller-Brockmann's poster work.

**Implementation pattern for decorative geometry:**
```html
<svg class="accent-geometry" viewBox="0 0 400 400">
  <circle cx="200" cy="200" r="150" fill="none" stroke="var(--accent)" stroke-width="2"/>
  <line x1="0" y1="400" x2="400" y2="0" stroke="var(--accent)" stroke-width="1"/>
</svg>
```
Position these elements relative to the grid, partially cropped at edges for visual tension.

### 5. Asymmetry Over Symmetry

Classical (pre-modernist) design centers everything. Bauhaus/Swiss design deliberately uses **asymmetric balance.**

- Place the primary content block off-center. A 7/5 or 8/4 column split is more dynamic than 6/6.
- Large headlines anchored to the left or top-left, with supporting content flowing from the grid.
- Whitespace is an active element — the empty columns are as designed as the filled ones.
- **Visual weight** should balance across the composition: a bold headline in the upper-left can be balanced by a geometric accent in the lower-right.

## Layout Patterns

### Poster / Hero
```
┌──────────────────────────────┐
│                              │
│  LARGE                       │
│  HEADLINE                    │
│  TEXT                        │
│                              │
│         ┌──────────┐         │
│         │ geometric│         │
│         │  element │         │
│         └──────────┘         │
│                              │
│  small body text             │
│  flush left                  │
│                              │
│  LABEL          DATE         │
└──────────────────────────────┘
```

### Dashboard / Data
```
┌────┬─────────────────────────┐
│NAV │  SECTION TITLE          │
│    │                         │
│    │  ┌─────┐ ┌─────┐       │
│    │  │card │ │card │       │
│    │  └─────┘ └─────┘       │
│    │  ┌─────┐ ┌─────┐       │
│    │  │card │ │card │       │
│    │  └─────┘ └─────┘       │
│    │                         │
│    │  ─────────────────      │
│    │  tabular data           │
└────┴─────────────────────────┘
```
- Cards have **no rounded corners** (or very minimal: 2px max). Sharp rectangles.
- Dividers are thin 1px lines in `--rule` color.
- No drop shadows. Elevation through whitespace and border, not shadow.

### Editorial / Content
```
┌──────────────────────────────┐
│  CATEGORY LABEL              │
│                              │
│  Large Headline              │
│  Spanning Multiple           │
│  Columns                     │
│                              │
│  ───────────────────         │
│                              │
│  Body text in a     │ Side   │
│  narrower column    │ notes  │
│  for readability    │ or     │
│  (45-75 chars/line) │ data   │
│                     │        │
└──────────────────────────────┘
```

## Motion & Interaction

Swiss modernism is static in print. In digital, apply motion **with restraint:**

- **Enter animations:** Translate-in from the grid direction (left-to-right, top-to-bottom). No bounce, no elastic. `ease-out` only.
- **Duration:** 200–400ms. Never exceed 600ms.
- **Hover states:** Subtle. Color shift on accent elements, underline reveal on links. No scale transforms.
- **Stagger:** When multiple elements enter, stagger by 50–80ms. This creates the reading rhythm.
- **No parallax, no 3D transforms, no blur transitions.** These are incompatible with the tradition.

```css
@keyframes enter {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.element {
  animation: enter 300ms ease-out both;
}
.element:nth-child(2) { animation-delay: 60ms; }
.element:nth-child(3) { animation-delay: 120ms; }
```

## Anti-Patterns (Never Do These)

- ❌ Rounded corners > 4px (use 0–2px)
- ❌ Drop shadows or box-shadow for elevation
- ❌ Gradients of any kind
- ❌ Decorative illustrations or icons with organic curves
- ❌ More than 2 typefaces
- ❌ Centered paragraph text
- ❌ Ornamental borders or decorative lines
- ❌ Pastel or muted color palettes (use high-contrast, decisive colors)
- ❌ Background images or textures (solid fields only)
- ❌ Emoji or playful UI elements
- ❌ Serif typefaces (the one exception: a deliberate Tschichold reference, which he himself did later — but this requires explicit user request)

## Responsive Behavior

The grid adapts but the principles don't:
- **Desktop (>1024px):** Full 12-column grid
- **Tablet (768–1024px):** Collapse to 8 or 6 columns. Maintain margins.
- **Mobile (<768px):** 4-column grid. Typography scale remains proportional. Generous vertical spacing replaces horizontal grid complexity.

Breakpoints should be defined as CSS custom properties or as variables in the component framework.

## Checklist Before Output

1. ☐ Is the grid defined and consistent?
2. ☐ Do all elements align to grid lines?
3. ☐ Is the type scale mathematical?
4. ☐ Is there only one (max two) typeface(s)?
5. ☐ Is the accent color used sparingly?
6. ☐ Are corners sharp (0–2px radius)?
7. ☐ Are there zero gradients and zero shadows?
8. ☐ Is text flush-left?
9. ☐ Is the layout asymmetric?
10. ☐ Does every element justify its existence?
