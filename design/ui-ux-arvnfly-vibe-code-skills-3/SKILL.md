---
name: ui-ux
description: Comprehensive UI/UX design intelligence engine for web, mobile, and desktop interfaces. Covers design systems, visual hierarchy, 8pt spatial grids, semantic color palettes (60-30-10 rule), fluid typography scales, visual archetypes, responsive layouts, accessibility audits (WCAG 2.2 AA), and micro-interactions.
tools: Read, Write, Edit, Glob, Grep, Bash
model: inherit
---

# UI/UX Design Intelligence Engine

A self-contained, zero-dependency design intelligence skill for designing, building, and auditing user interfaces across web, mobile, and desktop applications.

---

## 1. Design System Foundations

### The 8-Point Spatial Grid
All layout dimensions, margins, paddings, component heights, and gaps must align to 8px intervals (using 4px only for tight micro-alignments):
- `space-1`: 4px (micro-spacing: icon-to-label, badge inner padding)
- `space-2`: 8px (compact padding, input gap, list item separation)
- `space-3`: 12px (form row gap, compact card padding)
- `space-4`: 16px (standard component padding, mobile gutter)
- `space-6`: 24px (card body padding, grid column gap)
- `space-8`: 32px (container padding, major section sub-gap)
- `space-12`: 48px (section vertical rhythm)
- `space-16`: 64px (hero padding, primary page divider)

### Border Radii System
- `radius-sm`: 4px to 6px (inputs, badges, tooltips, tags)
- `radius-md`: 8px to 10px (buttons, small cards, dropdown menus)
- `radius-lg`: 12px to 16px (cards, modal dialogs, bento panels)
- `radius-full`: 9999px (pills, avatars, status indicators)

---

## 2. Visual Style Archetypes

Select the visual archetype based on domain and product requirements:

| Style Archetype | Target Domains | Key Characteristics | Anti-Patterns |
| :--- | :--- | :--- | :--- |
| **Clean Modern SaaS** | B2B, DevTools, Dashboards, Productivity | Neutral slate/zinc canvas, hairline borders (`1px solid var(--border-subtle)`), single brand accent, high information density | Avoid gradient clutter, excessive drop shadows, low-contrast text |
| **Bento Grid** | Feature showcases, landing pages, modern portfolios | Modular rounded cards (`radius-lg`), varying column spans, subtle backdrop blur, asymmetric visual anchors | Avoid uneven inner padding across cards, chaotic visual weights |
| **Dark Mode High-Contrast** | Developer consoles, AI interfaces, telemetry | Deep dark surfaces (`#090A0F`, `#12131A`), crisp contrasting borders (`rgba(255,255,255,0.08)`), glowing semantic accents | Avoid pure `#000000` backgrounds, washed-out gray text under 4.5:1 contrast |
| **Neo-Brutalism** | Web3, Gen-Z apps, creative agencies | High-contrast thick solid borders (`2px - 3px #000`), hard offset drop shadows (`4px 4px 0 #000`), bold saturated color blocks | Avoid tiny illegible text, unreadable interactive states |
| **Corporate Trust** | Fintech, Healthcare, Enterprise, Legal | Deep navy, slate, and emerald palettes; structured grids; serif/sans hybrid typography; restrained animations | Avoid playful rounded bubbly components, neon colors |
| **Minimalist Editorial** | Publications, high-end commerce, documentation | Generous white space, refined typography scales, monochrome with single spot color, clean hairline dividers | Avoid decorative badges, busy animations, cluttered iconography |

---

## 3. Color System & Semantic Tokens

### The 60-30-10 Distribution Rule
- **60% Dominant Surface**: Background, canvas, card backdrops (`bg-canvas`, `bg-surface`).
- **30% Structural Neutral**: Typography, borders, dividers, subtle secondary fills (`text-primary`, `border-subtle`).
- **10% Intentional Accent**: Primary actions, active navigation indicator, focused state, key metrics (`bg-accent`, `text-accent`).

### Semantic Color Token Architecture
Implement tokenized semantic colors rather than hardcoded hex values:

```css
:root {
  /* Surfaces */
  --bg-canvas: #FAFAFA;
  --bg-surface: #FFFFFF;
  --bg-surface-elevated: #FFFFFF;
  --bg-subtle: #F4F4F5;

  /* Borders */
  --border-subtle: #E4E4E7;
  --border-strong: #A1A1AA;

  /* Text & Content */
  --text-primary: #09090B;
  --text-secondary: #71717A;
  --text-muted: #A1A1AA;
  --text-inverse: #FFFFFF;

  /* Brand / Action */
  --color-primary: #2563EB;
  --color-primary-hover: #1D4ED8;
  --color-primary-subtle: #EFF6FF;

  /* Functional Status */
  --color-success: #16A34A;
  --color-success-bg: #F0FDF4;
  --color-warning: #D97706;
  --color-warning-bg: #FFFBEB;
  --color-danger: #DC2626;
  --color-danger-bg: #FEF2F2;
  --color-info: #0284C7;
  --color-info-bg: #F0F9FF;
}

[data-theme="dark"] {
  --bg-canvas: #09090B;
  --bg-surface: #18181B;
  --bg-surface-elevated: #27272A;
  --bg-subtle: #27272A;

  --border-subtle: #27272A;
  --border-strong: #52525B;

  --text-primary: #F4F4F5;
  --text-secondary: #A1A1AA;
  --text-muted: #71717A;
  --text-inverse: #09090B;

  --color-primary: #3B82F6;
  --color-primary-hover: #60A5FA;
  --color-primary-subtle: #1E293B;

  --color-success: #22C55E;
  --color-success-bg: #052E16;
  --color-warning: #F59E0B;
  --color-warning-bg: #451A03;
  --color-danger: #EF4444;
  --color-danger-bg: #450A0A;
  --color-info: #38BDF8;
  --color-info-bg: #082F49;
}
```

---

## 4. Typography Hierarchy & Pairings

### Typographic Scales (Major Third 1.250 or Perfect Fourth 1.333)
- **Hero Title**: `40px - 56px` (`font-bold`, `tracking-tight`, `line-height: 1.1`)
- **Heading 1 (H1)**: `32px - 40px` (`font-bold`, `tracking-tight`, `line-height: 1.2`)
- **Heading 2 (H2)**: `24px - 28px` (`font-semibold`, `tracking-tight`, `line-height: 1.25`)
- **Heading 3 (H3)**: `20px - 22px` (`font-semibold`, `line-height: 1.3`)
- **Subheading / Large Body**: `18px` (`font-medium`, `line-height: 1.5`)
- **Body Standard**: `16px` (`font-normal`, `line-height: 1.5 - 1.6`)
- **Body Compact / Form Labels**: `14px` (`font-medium`, `line-height: 1.4`)
- **Caption / Meta**: `12px` (`font-medium`, `tracking-wide`, `line-height: 1.4`)

### Curated Font Pairings
- **Modern Tech / SaaS**: `Inter` / `Geist Sans` + `Geist Mono` / `JetBrains Mono`
- **Clean Neutral**: `Plus Jakarta Sans` + `Inter`
- **Editorial & Elegance**: `Playfair Display` or `Newsreader` (Headings) + `Inter` (Body)
- **High-Trust Corporate**: `Public Sans` or `IBM Plex Sans` + `IBM Plex Mono`
- **High-Impact Bold**: `Space Grotesk` (Headings) + `Inter` (Body)

---

## 5. Layout Architecture & Responsive Breakpoints

### Mobile-First Breakpoint Matrix
- `xs`: `< 640px` (Single column, full-width cards, bottom sheets, 16px horizontal gutter)
- `sm`: `>= 640px` (2-column grids, compact modals)
- `md`: `>= 768px` (Tablet layouts, collapsible sidebars, multi-column forms)
- `lg`: `>= 1024px` (Desktop layouts, fixed sidebars, 3-column bento grids, 32px gutters)
- `xl`: `>= 1280px` (Wide desktop, maximum container width constraint: `max-w-7xl` or `1200px`)

### Critical Layout Rules
1. **Zero Horizontal Scroll**: Never allow unconstrained fixed widths (`width: 600px`). Always combine with `max-width: 100%`.
2. **Fluid Typography & Containers**: Prefer `clamp()` or Tailwind responsive utility prefixes over static media queries.
3. **Cumulative Layout Shift (CLS < 0.1)**: Always reserve explicit aspect ratios or skeleton heights for images, charts, and asynchronous data cards.

---

## 6. Interaction, State & Motion Standards

### Interactive Touch & Pointer Targets
- Minimum touch target: **44px × 44px** (on mobile / touch surfaces).
- Minimum button gap: **8px**.
- Icon-only buttons must provide explicit `aria-label` and visual tooltips.

### Context-Aware Animation Timing
- **Micro-interactions** (checkbox, toggle, button hover): `150ms cubic-bezier(0.4, 0, 0.2, 1)`.
- **Component Entrances** (dropdowns, tooltips, popovers): `200ms cubic-bezier(0, 0, 0.2, 1)`.
- **Surface Transitions** (dialogs, sheet drawers, modals): `300ms cubic-bezier(0, 0, 0.2, 1)`.
- **Accessibility Motion**: Must wrap non-essential motion in `@media (prefers-reduced-motion: reduce)`.

---

## 7. Data Visualization & Charts

Select chart types according to data relationships:

| Data Goal | Recommended Chart | Design Requirement |
| :--- | :--- | :--- |
| **Trend over Time** | Smooth Area / Line Chart | High-contrast line (`2px`), subtle gradient fill (`opacity: 0.15`), tooltips with crosshairs |
| **Discrete Comparison** | Horizontal / Vertical Bar Chart | Rounded bar caps (`radius-sm`), clean numerical axis, no distracting gridlines |
| **Part-to-Whole** | Donut Chart (Max 5 segments) | Center KPI summary, distinct categorical palette, direct segment labels |
| **Multi-Metric Overview** | Bento Metric Card with Sparkline | Standalone hero number, delta badge (+/-%), 7-day sparkline |

---

## 8. Multi-Agent Integration Protocol

### Integration with Sub-Agent Council
When `subagent-council` reviews a prompt or project diff:
- **Design Review Lens**: Evaluates visual balance, spacing consistency, contrast ratio compliance (WCAG AA 4.5:1), and responsive ergonomics.
- Rejects raw hardcoded hex values, unstyled native inputs, and layout overflowing.

### Integration with Sub-Agent Helper
Dispatch `subagent-helper` in `ui-ux` mode to:
1. Scan CSS/Tailwind classes for inconsistent spacing, font sizes, or color values.
2. Generate responsive component code or design tokens without altering application business logic.
3. Audit accessibility tree attributes (`aria-expanded`, `aria-controls`, `role`, `tabindex`).

---

## 9. Pre-Flight UI/UX Verification Checklist

Before closing any UI-related task, verify:
- [ ] **Contrast Ratio**: Normal text meets at least 4.5:1 against its background (3:1 for large text >= 24px).
- [ ] **Interactive Targets**: Buttons, inputs, and links have at least 44×44px interactive bounds on touch viewports.
- [ ] **Focus Rings**: Keyboard navigation preserves visible, non-obscured focus indicators (`outline` or `ring`).
- [ ] **Empty & Loading States**: Skeletons or spinners prevent layout shifts (CLS < 0.1).
- [ ] **Dark Mode Parity**: All surfaces, borders, and text tokens resolve legibly in dark mode without inverted low-contrast patches.
- [ ] **Mobile Responsiveness**: Checked at 360px, 768px, and 1280px widths with zero horizontal scrollbar.
- [ ] **Input Error Feedback**: Form validation provides both color indicators and descriptive text labels (not color alone).
