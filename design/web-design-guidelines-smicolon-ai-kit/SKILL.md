---
name: web-design-guidelines
description: Audits UI code against modern Web Interface Guidelines for typography, interactive affordances, responsive layouts, contrast, and accessibility compliance.
version: 1.0.0
---

# Web Interface Guidelines

Auditing rules for React, Next.js, and web frontend UI reviews.

## Core Review Checkpoints

### 1. Typography & Hierarchy
- Headings use semantic tags (`<h1>` to `<h6>`) in logical order without skipping levels.
- Line heights and letter spacing maintain readable proportions (`leading-relaxed` or `leading-normal` for body text).
- Avoid fixed pixel font sizes; use responsive Tailwind classes (`text-sm`, `text-base`, `text-lg`).

### 2. Interactive States & Affordances
- **Hover, Focus, and Active states**: Every interactive element (`<button>`, `<a>`, `<input>`) must have discernible hover, focus-visible, and active states.
- **Focus Rings**: Never use `outline-none` without providing an accessible `focus-visible:ring-2 focus-visible:ring-offset-2` replacement.
- **Loading & Disabled States**: Interactive buttons triggering async actions must indicate loading and be disabled to prevent duplicate submissions.

### 3. Touch Targets & Mobile Usability
- Minimum touch target size for mobile/tablet is **44x44px** (or `min-h-[44px] min-w-[44px]`).
- Adequate padding between adjacent interactive elements to prevent mis-taps.

### 4. Color & Contrast
- Text meets WCAG 2.1 AA minimum contrast ratio:
  - Normal text: **4.5:1**
  - Large text (18pt / 24px+ or 14pt bold): **3:1**
- Colors are not the sole indicator of state (always pair color changes with icons, underline, or text labels).

### 5. Layout & Responsive Behavior
- No horizontal scrollbars on viewport widths from 320px up to 4K.
- Use CSS grid or flexbox with wrapping (`flex-wrap`).
- Modals and popovers lock body scroll when open and dismiss on `Escape` key or backdrop click.
